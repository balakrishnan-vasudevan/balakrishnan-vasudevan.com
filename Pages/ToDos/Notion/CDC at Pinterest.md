

Tags: cdc
Category: Articles
Company: Pintrest
Status: Not started
URL: https://medium.com/pinterest-engineering/change-data-capture-at-pinterest-7e4c357ac527

What is Change Data Capture?

CDC is a set of software design patterns used to identify and track changes in a database. These changes can include inserts, updates, and deletes. CDC allows applications to respond to these changes in real-time, making it an essential component for data integration, replication, and synchronization.

## Why is CDC Important?

1. **Real-Time Data Processing**: CDC enables real-time data processing by capturing changes as they happen. This is crucial for applications that require up-to-date information, such as fraud detection systems or recommendation engines.

2. **Data Integration**: By capturing changes, CDC facilitates seamless data integration between different systems. This is particularly useful in environments where multiple applications need to access and process the same data.

3. **Reduced Load on Source Systems**: Instead of performing full data loads, CDC captures only the changes, reducing the load on source systems and improving performance.

4. **Audit and Compliance**: CDC provides a reliable way to track changes for audit and compliance purposes, ensuring that all modifications are logged and traceable.

# Our Journey of Implementing Generic CDC at Pinterest

## Challenges of Prior Generic CDC

In the past, various teams have implemented isolated CDC solutions to meet specific use cases. While effective for their intended purposes, these solutions have led to user dissatisfaction due to inconsistencies, unclear ownership, and reliability issues.

## Introducing Generic CDC

To address these challenges, we have decided to build a Generic CDC solution based on Red Hat [Debezium](https://debezium.io/)(™). This solution aims to:

- Ensure reliable, low-latency, scalable systems with guarantees of at least once processing.
- Support highly distributed database setup.
- Implement robust load balancing and minimize the impact on upstream databases.
- Provide configurability and advanced monitoring integration for users.

## Architecture

[https://miro.medium.com/v2/resize:fit:700/0*xfo4O4EQslssUM0r](https://miro.medium.com/v2/resize:fit:700/0*xfo4O4EQslssUM0r)

Our database architecture at Pinterest is characterized by high distribution, with each distributed unit known as a shard. Some large databases can have approximately 10,000 shards. While the open source Debezium connector, such as the MySQL connector, works seamlessly for a single shard, the challenge lies in making it compatible with our distributed databases.

Initially, we considered modifying the Debezium implementation to support distributed databases. However, this approach raised concerns about the potential difficulty of upgrading to newer Debezium versions in the future due to customized logic. We also encountered similar issues with other open-source software at Pinterest, such as Apache Maxwell.

To address this challenge, we opted for an alternative approach involving the separation of the control plane and data plane.

**The control plane manages various aspects of the system:**

1. It runs on a single host inside an AWS® Auto Scaling Group with a minimum and maximum host count of 1. This configuration ensures that if the host goes down due to an EC2® event or any other reason, it will be automatically reprovisioned.
2. The control plane runs its main logic on a scheduled basis, typically set to one minute in our case.
3. The main logic involves the following steps:Reads the connector configuration and Apache ZooKeeper(™), which contain information about the database topology. This combined information represents the ideal state of the system, including the number of connectors that should be running and the updated configuration for each connector.Calls the data plane Apache Kafka® Connect API to obtain information about the current state of the system, such as the status of currently running connectors and their configurations.Compares the ideal state and the current state and takes actions to bring the current state closer to the ideal state. For example, it creates new connectors for new shards, updates the configuration of existing connectors when necessary, and attempts to fix failed connectors.
4. Finally, the control plane emits enriched metrics to enable effective monitoring of the system.

**The data plane:**

1. To ensure even distribution across three Availability Zones (AZs), we operate Kafka Connect in distributed mode on a separate cluster (ASG) with more machines.
2. All hosts in this cluster join the same group and run Kafka Connect in distributed mode.
3. Each host may run multiple Debezium connectors, with each connector responsible for a specific database shard.
4. The primary function of a connector is to capture database changes and send them to Kafka.

**Kafka:**

1. Kafka stores metadata about connectors in several internal topics that are not exposed to end users.
2. The actual CDC data is stored in preconfigured topics within Kafka, which can be consumed by users.
3. Internally, Kafka Connect utilizes a select group of Kafka brokers to facilitate a distributed computing framework. This includes tasks like leader election and coordination.

In addition, we’d like to share some technical challenges we encountered and the solutions we implemented.

## Challenges & Solutions

- **Scalability Issues:** Some of the datasets have high query per second (QPS) rates and throughput (millions of QPS, TBs of data per day) led to out-of-memory (OOM) errors in CDC tasks caused by processing backlogs.**Solution:** Implementing bootstrapping allowed tasks to start from the latest offset, and rate limiting helped manage OOM risks in running tasks.
- **Rebalancing Timeout:** As we ramped up the number of connectors (approximately 3K) in a single cluster, we observed an unexpected behavior in the Kafka Connect framework. Instead of maintaining a balanced distribution, where each host ideally runs an equal number of connectors, the framework continually shifted connectors between hosts. This resulted in instances where all connectors were assigned to a single host, leading to high latency during deployments and failovers. Additionally, the risk of duplicate tasks increased due to this imbalanced distribution.**Solution**: The primary source of the issue is the default heartbeat timeout value, which is too brief. As a result, the framework does not wait long enough before reassigning tasks to other workers, leading to continuous rebalancing. To address this problem, increasing the rebalance.timeout.ms configuration to 10 minutes effectively resolves it.
- **Failover Recovery:** Deploys in KV Store clusters could take 2+ hours, causing 2+ hour leader failovers. Tasks failed with outdated leaders, prompting the control plane to delete and recreate them, triggering constant rebalancing over 2+ hours.**Solution**: Allow CDC workers to handle shard discovery and failover, which reduced failover recovery latency to sub-minute and minimized rebalances.
- **Duplicate Tasks:** Running over 500 connector tasks led to duplicate instances, as seen in the bug [KAFKA-9841](https://issues.apache.org/jira/browse/KAFKA-9841), causing duplicate data, uneven task loads on hosts, constant rebalances, and maximum CPU usage. Duplicate tasks are duplicate instances of each CDC task, where multiple hosts each run an instance of the same task. When hosts reach their 99% CPU, it causes more rebalancing as the hosts try to reduce their load.**Solution**: Upgrading to Kafka 2.8.2 ver. 3.6 with the Kafka bug fixes and increasing rebalance timeout to 10 minutes.**Graphs:** The graphs show normal behavior that turns into duplicate tasks at 12:00. Each task was running on 2–3 hosts at the same time. The total number of running tasks for 3,000 tasks fluctuated between 1,000 to 6,000, and the CPU usage increased significantly to 99%.

[https://miro.medium.com/v2/resize:fit:700/0*QVSVYL7v88gF2d3w](https://miro.medium.com/v2/resize:fit:700/0*QVSVYL7v88gF2d3w)

[https://miro.medium.com/v2/resize:fit:700/0*piwtuh3ViAhFd63i](https://miro.medium.com/v2/resize:fit:700/0*piwtuh3ViAhFd63i)

[https://miro.medium.com/v2/resize:fit:700/0*-zIR5MIgfnOgt9Oo](https://miro.medium.com/v2/resize:fit:700/0*-zIR5MIgfnOgt9Oo)

After fixes, we see each task runs on a singular host. The total number of running tasks is 3,000. CPU is stable and healthy at 45%.

[https://miro.medium.com/v2/resize:fit:700/0*Zlgy8popd1H1JVB9](https://miro.medium.com/v2/resize:fit:700/0*Zlgy8popd1H1JVB9)

[https://miro.medium.com/v2/resize:fit:700/0*NKzxkl0elGaGwsaf](https://miro.medium.com/v2/resize:fit:700/0*NKzxkl0elGaGwsaf)

[https://miro.medium.com/v2/resize:fit:700/0*iOYIl-Co4gMjiL8_](https://miro.medium.com/v2/resize:fit:700/0*iOYIl-Co4gMjiL8_)

# Next Steps

In the upcoming period, we remain dedicated to enhancing the platform’s scalability and unlocking new use cases:

1. **Scalability Enhancement:**
- Improving the platform’s capacity to efficiently manage large-scale datasets is one of the areas for future exploration.
- Our goal is to achieve data throughput of hundreds of TBs per day and support millions of queries per second (QPS).

**2. Disaster Recovery with CDC:**

- We plan to implement robust disaster recovery measures by replicating data across different regions using Change Data Capture (CDC) technology.

**3. Near Real-Time Database Ingestion:**

- We are developing a near real-time database ingestion system, utilizing CDC, to ensure timely data accessibility and efficient decision-making.

# Acknowledgments

The success of Pinterest Generic CDC would not have been possible without the significant contributions and support of:

- Shardul Jewalikar, Ambud Sharma, Jeff Xiang, Vahid Hashemian, and the Logging Platform team.
- Lianghong Xu, Alberto Ordonez Pereira, and the Storage Foundation Team.
- Rajath Prasad, Jia Zhan, Shuhui Liu, and the KV Systems Team.
- Se Won Jang, Qingxian Lai, Anton Arboleda, and the ML Data Team.

Special gratitude must be extended to Ang Zhang and Chunyan Wang for their continuous guidance, feedback, and support throughout the project.

# Disclaimer

Apache®️, Apache Kafka®️, and Kafka®️ are trademarks of the Apache Software Foundation ([https://www.apache.org/](https://www.apache.org/)).

Amazon®️, AWS®️, S3®️, and EC2®️ are trademarks of Amazon.com, Inc. or its affiliates.

Debezium®️ is a trademark of Red Hat, Inc.

MySQL®️ is a trademark of Oracle Corporation.

RocksDB®️ is a trademark of Meta Platforms, Inc. or its affiliates.

TiDB®️ is a trademarks of Beijing PingCAP Xingchen Technology and Development Co.