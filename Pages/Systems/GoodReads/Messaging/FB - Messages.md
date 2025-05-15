

Tags: messaging-system
Category: Articles
Company: Facebook
Status: Not started
URL: https://engineering.fb.com/2010/11/15/core-infra/the-underlying-technology-of-messages/

![https://engineering.fb.com/wp-content/uploads/2011/05/f.png](https://engineering.fb.com/wp-content/uploads/2011/05/f.png)

![https://engineering.fb.com/wp-content/uploads/2010/11/Fnf_DADgnJfX1HYBALXe0TZuPQkAAAE.jpg](https://engineering.fb.com/wp-content/uploads/2010/11/Fnf_DADgnJfX1HYBALXe0TZuPQkAAAE.jpg)

We’re [launching a new version of Messages](http://blog.facebook.com/blog.php?post=452288242130) today that combines chat, SMS, email, and Messages into a real-time conversation. The product team spent the last year building out a robust, scalable infrastructure. As we launch the product, we wanted to share some details about the technology.

The current Messages infrastructure handles over 350 million users sending over 15 billion person-to-person messages per month. Our chat service supports over 300 million users who send over 120 billion messages per month. By monitoring usage, two general data patterns emerged:

1. A short set of temporal data that tends to be volatile
2. An ever-growing set of data that rarely gets accessed

When we started investigating a replacement for the existing Messages infrastructure, we wanted to take an objective approach to storage for these two usage patterns. In 2008 we open-sourced [Cassandra](http://cassandra.apache.org/), an eventual-consistency key-value store that was already in production serving traffic for Inbox Search. Our Operations and Databases teams have extensive knowledge in managing and running MySQL, so switching off of either technology was a serious concern. We either had to move away from our investment in Cassandra or train our Operations teams to support a new, large system.

We spent a few weeks setting up a test framework to evaluate clusters of MySQL, Apache Cassandra, [Apache HBase](http://hbase.apache.org/), and a couple of other systems. We ultimately chose HBase. MySQL proved to not handle the long tail of data well; as indexes and data sets grew large, performance suffered. We found Cassandra’s eventual consistency model to be a difficult pattern to reconcile for our new Messages infrastructure.

HBase comes with very good scalability and performance for this workload and a simpler consistency model than Cassandra. While we’ve done a lot of work on HBase itself over the past year, when we started we also found it to be the most feature rich in terms of our requirements (auto load balancing and failover, compression support, multiple shards per server, etc.). HDFS, the underlying filesystem used by HBase, provides several nice features such as replication, end-to-end checksums, and automatic rebalancing. Additionally, our technical teams already had a lot of development and operational expertise in HDFS from data processing with Hadoop. Since we started working on HBase, we’ve been focused on committing our changes back to HBase itself and working closely with the community. The open source release of HBase is what we’re running today.

Since Messages accepts data from many sources such as email and SMS, we decided to write an application server from scratch instead of using our generic Web infrastructure to handle all decision making for a user’s messages. It interfaces with a large number of other services: we store attachments in [Haystack](http://www.facebook.com/note.php?note_id=76191543919), wrote a user discovery service on top of [Apache ZooKeeper](http://hadoop.apache.org/zookeeper/), and talk to other infrastructure services for email account verification, friend relationships, privacy decisions, and delivery decisions (for example, should a message be sent over chat or SMS). We spent a lot of time making sure each of these services are reliable, robust, and performant enough to handle a real-time messaging system.

The new Messages will launch over 20 new infrastructure services to ensure you have a great product experience. We hope you enjoy using it.

*Kannan is a software engineer at Facebook.*