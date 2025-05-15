
Distributed messaging systems enable the exchange of messages between multiple, potentially geographically-dispersed applications, services, or components in a reliable, scalable, and fault-tolerant manner. They facilitate communication by decoupling the sender and receiver components, allowing them to evolve and operate independently. Distributed messaging systems are particularly useful in large-scale or complex systems, such as those found in microservices architectures or distributed computing environments. Examples of such systems are Apache Kafka and RabbitMQ.

- Message queues can be used for asynchronous communication between services and for processing batched workloads.
- As applications become decoupled, they often need mechanisms to share state, mutate data and handle events in different areas of the system.

1. RabbitMQ
Advantages
- Supports a wide range of messaging patterns and easily scales horizontally by adding more nodes to the cluster.
- RabbitMQ has many official and unofficial client libraries and developer tools [linked on its website](https://www.rabbitmq.com/devtools.html).
- Provides durability for its message by storing backups on disk through other nodes in the cluster.

 Disadvantages
- Can be slow at processing larger datasets, typically handling tens of thousands of events per second.
- Some integration services, such as intra-cluster compression and warm standby replication, are only available as part of their paid commercial offering.
- RabbitMQ is somewhat complex and will require technical expertise to set up and maintain over time.
2. SQS - Amazon Simple Queue
3. Apache ActiveMQ
4. Kafka - not technically a message queue, it has the functionality of a message queue using a topic partition. [[Notes/Pages/Systems/Systems Design/Framework/Kafka]]
 Advantages
- Easily scales horizontally and span multiple data center and cloud environments.
- Kafka is reliable, with high availability and fault tolerance through replication and partitioning.
- Kafka now has libraries for most languages, including Java, C++, Python, Go, .NET, Rub and NodeJS.
Disadvantages
- Kafka has a steep learning curve due to its technical complexity, likely requiring in-house or external experts.
- Kafka doesn’t have an official interface for management and monitoring, and third-party tools may be required.
6. GCP Pub/Sub  
 Advantages
- High scalability and availability that requires no setup and is managed for you automatically by Google.
- The maximum message payload size is 10MB, considerably higher than most other solutions.
- Supports push and pull delivery types.
- The easy-to-use interface on the Google Cloud console for managing and debugging topics and subscriptions.
Disadvantages
- It can be difficult to calculate how much you will be billed for Pub/Sub, as they charge for throughput, storage and egress as described on their length and complex pricing page.
- Low latency for message delivery is not guaranteed as Google prioritizes scalability over speed for Pub/Sub.
7. Azure Bus


![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d8831d-0447-41f5-a2b6-c4d04440ed7c_720x414.webp)





- [[Notes/Pages/Systems Primer/Kafka]]
-