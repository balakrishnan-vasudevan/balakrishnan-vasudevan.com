# Building a Global Caching System at Netflix: A Deep Dive to Global Replication

Tags: caching, memache
Category: Articles
Company: Netflix
Status: Complete
URL: https://www.infoq.com/articles/netflix-global-cache/

EVCache stands for Ephemeral Volatile Cache. It is a distributed key-value store based on [Memcached](https://memcached.org/), designed to deliver linear scalability and robust resilience. Despite its name, EVCache benefits from SSD backing, ensuring reliable and persistent storage.

Although Memcached doesn't use SSDs for persistence by default, its [extstore](https://github.com/memcached/memcached/wiki/Extstore) extension allows offloading less frequently accessed data to SSDs, freeing up RAM for frequently accessed data. Netflix leverages this in EVCache, combining the speed of RAM with the capacity of SSDs to optimize performance and storage efficiency. @

Netflix's EVCache is deployed across four regions, comprising 200 Memcached clusters tailored to support various use cases. Each cluster is responsible for serving an app or a group of apps. This extensive infrastructure includes 22,000 server instances, enabling the system to handle 30 million replication events globally and 400 million overall operations per second. In terms of data, EVCache manages around 2 trillion items, totaling 14.3 petabytes, showcasing its immense capacity and scalability.

## Why Replicate Cache Data?

Rapid data availability is crucial for maintaining a seamless and responsive user experience. By keeping cache data readily accessible, the system avoids time-consuming and resource-intensive database queries. This immediate access keeps users engaged and satisfied. In the event of a region failover, having cache data available in the failover region ensures uninterrupted service with minimal latency, preventing any noticeable disruption for users. This level of performance and reliability is essential for meeting user expectations and maintaining high engagement.

Building personalized recommendations requires significant computational resources, particularly for Netflix, where machine learning algorithms are key. Recomputing data for cache misses can be extremely CPU-intensive and costly. Each cache miss demands substantial computational power to retrieve and recompute data, including running complex machine learning models. By replicating cache data across regions, Netflix minimizes these expensive recomputation processes, reducing operational costs and ensuring a smoother user experience. This allows quick data access and efficient delivery of personalized recommendations, making the system more cost-effective and responsive.

## Design of the Global Replication Service

![[Pasted image 20250401122410.png]]

**Data replication between two regions**

The above diagram illustrates how EVCache replicates data across regions. This process is comprised of the following steps:

1. **Send Mutation**: The application uses the EVCache client to send various mutation calls, such as set, add, delete, and touch, to the local EVCache servers.
2. **Send Metadata**: EVCache sends an asynchronous event containing metadata to [Kafka](https://kafka.apache.org/). This metadata includes critical information such as the key, TTL (time-to-live), and creation timestamp. However, it notably excludes the value to prevent overloading Kafka with potentially large data payloads.
3. **Poll Messages**: The replication reader service continuously reads messages from Kafka. This service is responsible for processing and preparing the metadata events for the next stage.
4. **Local Read**: Upon reading the metadata from Kafka, the replication reader service issues a read call to the local region's EVCache server to fetch the latest data for the key. This step ensures that the most up-to-date value is retrieved without placing undue load on Kafka. Additionally, the reader can filter out unwanted messages, such as those with very short TTLs (e.g., 5 seconds), to optimize the replication process based on business needs.
5. **Cross-Region Traffic**: The replication reader service then makes a cross-region call to the replication writer service in the destination region. This call includes all relevant information, such as metadata and the fetched value, ensuring the data is replicated accurately.
6. **Destination Write**: The replication writer service receives the cross-region call and writes the key-value pair to the EVCache server in the destination region. This step ensures that the data is consistently replicated across regions.
7. **Read Data**: When data is read in the failover region, it is readily available due to the replication process. This ensures minimal latency and provides a seamless user experience.

### Error Handling in the Replication System


![[Pasted image 20250401122453.png]]

**Error handling in Netflix's replication system**

In a distributed system, failures can occur at any step of the replication process. To ensure data reliability and maintain the integrity of the replication process, Netflix employs Amazon [Simple Queue Service](https://aws.amazon.com/sqs/) (SQS) for robust error handling due to its reliable message queuing capabilities.

When a failure occurs during any step of the replication process, the failed mutation is captured and sent to an SQS queue, ensuring that no failed mutation is lost and can be retried later. The replication service monitors the SQS queue for failed mutations and reprocesses them through the replication workflow upon detection. This retry mechanism ensures that all mutations are eventually processed, maintaining data reliability across regions and minimizing the risk of data loss.

## Closer Look into the Replication Reader and Writer Service

![[Pasted image 20250401122433.png]]

**Multiple reader service instances replicate data to different regions**

The diagram above illustrates Netflix's replication service. The Reader Service in US-EAST-1 pulls data from Kafka topics and partitions, processes it, and sends it to the Writer Service in other regions, which writes the data to EVCache servers, ensuring regional availability.

### Replication Reader Service

The reader service pulls messages from Kafka, applies necessary transformations, and fetches the most recent values from the local EVCache service. To streamline management, Netflix uses a single Kafka cluster for the replication service, which supports over 200 EVCache clusters. Each EVCache cluster is represented as a topic in Kafka, with topics partitioned based on the volume of events they handle.

Different consumer groups are designated to read from this Kafka cluster within the reader service. Each consumer group corresponds to a set of nodes, with each node responsible for reading multiple partitions. This structure allows for parallel processing and effective load distribution, ensuring high throughput and efficient data handling. Each consumer group targets a different region, ensuring data is replicated across multiple regions.

The reader service is hosted on [EC2](https://aws.amazon.com/ec2/) instances, providing scalability and resilience. Each reader service is a compute cluster, a group of interconnected computers (nodes) that work together to perform complex computations and data processing tasks. By organizing readers as consumer groups, Netflix can scale the system horizontally to meet demand.

After the reader service fetches and transforms the necessary data, it initiates a cross-region call to the writer service in the target region. The transformation involves converting the fetched data, which includes the key, metadata, and value, into a JSON format suitable for transmission via REST. This call includes all pertinent information, ensuring the data is replicated accurately.

### Replication Writer Service

The writer service's primary function is to receive REST calls from the reader service and write the data to the destination EVCache service. The writer service is also hosted on EC2 instances, providing scalability and resilience. Upon receiving the data, the writer service processes it and writes the key-value pair to the EVCache server in the destination region. This ensures data availability across regions. The writer service is designed to handle large volumes of data efficiently, maintaining the integrity of the replication process and ensuring that the system remains robust and reliable.

## Why Did We Choose Client-Initiated Replication Over Server-Initiated Replication?

For EVCache, we opted for client-initiated replication primarily because the EVCache client is topology-aware. This topology awareness allows the client to efficiently manage and route data within the distributed caching environment. Specifically, the EVCache client is aware of:

- **Node Locations**: The client knows the physical or logical locations of the memcached nodes. This includes information about which nodes are in which data centers or regions.
- **Node Availability**: The client is aware of which memcached nodes are currently available and operational. This helps in avoiding nodes that are down or experiencing issues.
- **Data Distribution**: The client understands how data is distributed across the memcached nodes. This includes knowledge of which nodes hold replicas of specific data items.
- **Network Latency**: The client can make decisions based on network latency, choosing memcached nodes that provide the fastest response times for read and write operations.

### Advantages of Client-Initiated Replication

**Topology Awareness**: As explained, the EVCache client's topology awareness enables it to make intelligent decisions about data routing and replication. This ensures efficient data distribution and minimizes latency.

**Reduced Server Load**: By initiating replication at the client level, we reduce the computational burden on the servers. This allows the servers to focus on their core responsibilities, such as serving read and write requests, without the added overhead of managing replication tasks.

**Scalability**: Client-initiated replication allows for more straightforward horizontal scaling. As the number of clients increases, the replication workload is distributed across these clients, preventing any single point of bottleneck and ensuring that the system can handle increased load.

**Flexibility**: With client-initiated replication, it is easier to implement and manage various replication strategies and optimizations at the client level. This includes filtering out unwanted messages, applying business-specific rules, and dynamically adjusting replication behavior based on current conditions.

### Disadvantages of Client-Initiated Replication

**Complexity in Client Management**: Managing replication logic at the client level can introduce complexity. Ensuring that all clients are up-to-date with the latest replication logic and handling potential inconsistencies across clients can be challenging.

**Increased Network Traffic**: Client-initiated replication can increase network traffic, as each client is responsible for sending replication data across regions. This can result in higher bandwidth usage and potential network congestion compared to a centralized server-initiated approach, where replication traffic can be more efficiently managed and optimized at the server level.

**Message Duplication**: With each client responsible for initiating replication, there is a possibility of duplicated efforts, especially if multiple clients are handling similar data. This can lead to inefficiencies and increased resource consumption.

**Error Handling**: Implementing robust error handling and retry mechanisms at the client level can be more complex than a centralized server-initiated approach. Ensuring data reliability in the face of network failures or client crashes adds another layer of complexity.

## Efficiency Improvements

Netflix continuously seeks to optimize its infrastructure for both performance and cost efficiency. Two significant improvements in the EVCache replication process have been implementing batch compression and removing network load balancers.

### Batch Compression

To reduce network bandwidth usage, we implemented batch compression for the data transferred from the reader to the writer. This process involves batching multiple messages and applying [Zstandard](https://facebook.github.io/zstd/) compression to the batch. By compressing the data before transmission, we achieved a 35% reduction in network bandwidth usage. This significant optimization not only lowers costs but also enhances the overall efficiency of the replication process. Batch compression ensures that the data transfer between reader and writer clusters is more efficient, reducing overhead and improving throughput.

![[Pasted image 20250401122512.png]]

**Comparison of Compressed vs Uncompressed Payload Sizes**

This graph illustrates the overall payload size reduction across various use cases and clusters. Due to the diverse traffic patterns of each cluster, we observed a cumulative savings of approximately 35% in network throughput.

### Removing Network Load Balancers

Initially, we used [Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html) (NLBs) to manage communication between the reader and writer services. However, this setup incurred additional network transfer costs. To address this, we switched from using NLBs to leveraging [Eureka DNS](https://github.com/bfg/eureka-dns-server) for service discovery. Using Eureka DNS, we can fetch the IP addresses of the writer nodes and handle the routing ourselves. This change reduced network transfer costs by 50% while maintaining predictable latencies and efficient load distribution.


![[Pasted image 20250401122540.png]]

**Communication topology comparison with and without an NLB**

The switch to client-side load balancing streamlined our infrastructure, significantly cutting costs without compromising performance. By removing the dependency on NLBs, we achieved greater control over the traffic routing process, leading to more efficient resource utilization.


![[Pasted image 20250401122606.png]]

**Process bytes in the NLB before and after migration**

The above graph illustrates the amount of traffic routed via NLBs. Since we migrated off of NLBs and started leveraging client-side load balancing, we could significantly save on network transfer costs.

The daily NLB usage hovered around 45 GB/s across all the regions, and after the change, the usage decreased to less than 100 MB/s. We still keep NLBs around in our architecture as a fallback option.

## Conclusion

Building a robust, scalable, and efficient global caching system is critical for Netflix to provide a seamless user experience. By leveraging EVCache and a well-designed replication service, Netflix ensures high availability, low latency, and cost efficiency.The topology-aware EVCache client, combined with client-initiated replication, allows for efficient data management and routing, reducing server load and enhancing scalability.

Through careful design choices, such as using a single Kafka cluster for streamlined management and implementing a flexible replication reader service, Netflix has optimized its caching infrastructure to handle massive volumes of data across multiple regions. This ensures that data is always readily available, even in failover scenarios, maintaining a seamless and responsive user experience.

As we continue on our journey of continuous improvement and innovation, we look forward to further enhancing our systems to meet the evolving needs of our global user base. By consistently refining our approaches and embracing new technologies, Netflix aims to provide an even more resilient, responsive, and cost-effective experience for users worldwide.



Questions

Protocol for topology awareness - zookeeper

Need for dns if you have service discvery