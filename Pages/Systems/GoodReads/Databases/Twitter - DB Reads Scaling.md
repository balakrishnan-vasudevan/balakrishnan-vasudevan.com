# How we scaled Reads On the Twitter Users Database

Tags: databases, scale, sql
Category: Articles
Company: Twitter
Status: Reading
URL: https://blog.x.com/engineering/en_us/topics/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database

### **Introduction**

Twitter operates one of the world’s largest User Reservation Systems, referred to as URS. The User Reservation System was initially built using [Gizzard](https://blog.twitter.com/engineering/en_us/a/2010/introducing-gizzard-a-framework-for-creating-distributed-datastores), an old [MySQL](https://www.mysql.com/) framework, which was quite popular and performant during the time it was built, with bespoke features like quorum reads, which were unique to URS. With time, progress in technology and increase in scale, it was a challenge to adhere to the strict SLOs on QPS (Queries Per Second), latency, success rates and cross data center consistency while supporting main features of the application. With the increased scale, reducing maintenance costs was yet another challenge. This motivated us to explore other ways to address the problem. [MySQL](https://www.mysql.com/) being widely used at Twitter for other applications, seemed to be the obvious choice because of its simplicity and performance.

These MySQL servers at Twitter are mostly on-premise, commodity hardware, customized and optimized for our specific use-cases. While we could add several replicas for supporting redundancy, it was not a feasible solution to spin up several replica servers to scale the reads to millions of queries per second. So we used [Vitess](https://vitess.io/), which is an open source database solution for scaling MySql. While Vitess is mostly used for sharding and scaling writes, we also leveraged the [Vtgate](https://vitess.io/docs/13.0/concepts/vtgate/) component to scale the reads.

### **What is Vtgate and how did we scale it**

Vtgate is a Vitess component. It is a stateless proxy used to route traffic to the correct [Vttablet](https://vitess.io/docs/16.0/reference/programs/vttablet/) and return consolidated results to the application. Each MySQL instance is paired with a Vttablet process, which provides features like connection pooling, query rewriting, and query deduplication.

The Vtgates can run on the same machine as MySQL instances but we moved them out of the MySQL servers mainly for 2 reasons:

- It would use resources which could be freed up for MySql
- We wanted to scale them up to hundreds to achieve the read scalability

Twitter uses [Apache Mesos](https://blog.twitter.com/engineering/en_us/a/2012/incubating-apache-mesos) which provides a scalable platform for running containerized applications. Since the Vtgates are stateless proxies, we spinned up the Vtgates on Aurora Mesos and tuned the number of Mesos instances, resources like CPU, number of OS threads and GOGC values to achieve the high rate of millions of queries per second. The number of connections on each Vtgate were tested to scale upto a couple of thousand connections. This met all our stringent requirements for the read scalability of the database.

![https://cdn.cms-twdigitalassets.com/content/dam/blog-twitter/engineering/en_us/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database/how-we-scaled-reads-on-the-twitter-users-database.png.img.fullhd.medium.png](https://cdn.cms-twdigitalassets.com/content/dam/blog-twitter/engineering/en_us/infrastructure/2023/how-we-scaled-reads-on-the-twitter-users-database/how-we-scaled-reads-on-the-twitter-users-database.png.img.fullhd.medium.png)

Figure 1 - High level architecture

### **Why we chose Vitess**

We chose Vitess because it is open source! Also, it integrates well with MySql. It also comes with a topology service to store all configuration data. At Twitter we have highly available [Zookeeper](https://zookeeper.apache.org/) clusters which we used for the topology service. It can be easily integrated with Orchestrator (VTORC in later releases), the MySQL replication topology manager which removes a lot of cluster maintenance overhead and provides everything we need for a highly available MySQL cluster. Plus, if required, we can shard the clusters to scale the writes as well.

### **Security**

Encryption-in-Transit is a strict requirement at Twitter. Vitess allows encryption between the application and Vtgate, and between all its components. To avoid downtime during enabling TLS, we pushed an optional TLS feature to Open source Vitess which was used while enabling TLS. We found that Vitess was using cert only for client verification, so we updated the open source Vitess to use chain and ensured Vitess used full chain for client verification.

### **Conclusion**

The URS cluster is a tier 1 application running in production for several months now with an extremely high availability for both writes and reads. While we use several vanilla MySQl clusters to serve many critical applications, we found Vitess to be good for scaling and will recommend this to the industry.