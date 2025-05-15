#databases , #sharding

https://iorilan.medium.com/a-5-years-tech-lead-said-they-shard-a-database-to-scale-but-then-he-failed-to-answer-this-question-8be39115dcb0

It is a technique used to scale a database by horizontally [partitioning](https://designgurus.org/path-player?courseid=grokking-the-system-design-interview&unit=grokking-the-system-design-interview_1627054339994_4Unit) the data across multiple servers, or shards. The goal of [sharding](https://medium.com/codex/grokking-system-design-what-is-database-sharding-97830014baab) is to distribute the data and workload across multiple servers, so that each server can handle a smaller portion of the overall data and workload. This can help improve the performance and scalability of the database, as each server can process queries and updates more efficiently when it is working with a smaller amount of data.

![[Pasted image 20250324152522.png]]


### [Memcached and Redis – Algorithmic Sharding](https://www.yugabyte.com/blog/four-data-sharding-strategies-we-analyzed-in-building-a-distributed-sql-database/#memcached-and-redis-algorithmic-sharding)

Distributed caches have had to distribute data across multiple nodes for a while. A commonly used technique is algorithmic sharding, where each key consistently maps to the same node. This is achieved by computing a numeric hash value out of the key and computing a modulo of that hash using the total number of nodes to compute which node owns the key.

![[Pasted image 20250324152537.png]]
_Part of the image from source: [How Sharding Works](https://medium.com/@jeeyoungk/how-sharding-works-b4dec46b3f6)_

**Pros**  
In algorithmic sharding, the client can determine a given partition’s database without any help.

**Cons**  
When a new node is added or removed, the ownership of almost all keys would be affected, resulting in a massive redistribution of all the data across nodes of the cluster. While this is not a correctness issue in a distributed cache (because cache misses will repopulate the data), it can have a huge performance impact since the entire cache will have to be warmed again.



### [DynamoDB and Cassandra – Consistent Hash Sharding](https://www.yugabyte.com/blog/four-data-sharding-strategies-we-analyzed-in-building-a-distributed-sql-database/#dynamodb-and-cassandra-consistent-hash-sharding)

[[pages/Systems/Systems Primer/Add Ons/Consistent Hashing]]

With consistent hash sharding, data is evenly and randomly distributed across shards using a partitioning algorithm. Each row of the table is placed into a shard determined by computing a consistent hash on the partition column values of that row. This is shown in the figure below.

![[Pasted image 20250324152549.png]]

**Pros**  
This sharding strategy is ideal for massively scalable workloads because it distributes data evenly across all the nodes in the cluster, while retaining ease of adding nodes into the cluster. Recall from earlier that algorithmic hash sharding is very effective also at distributing data across nodes, but the distribution strategy depends on the number of nodes. With consistent hash sharding, there are many more shards than the number of nodes and there is an explicit mapping table maintained tracking the assignment of shards to nodes. When adding new nodes, a subset of shards from existing nodes can be efficiently moved into the new nodes without requiring a massive data reassignment.

**Cons**  
Performing range queries could be inefficient. Examples of range queries are finding rows greater than a lower bound or less than an upper bound (as opposed to point lookups).


### [Google Spanner and HBase – Range Sharding](https://www.yugabyte.com/blog/four-data-sharding-strategies-we-analyzed-in-building-a-distributed-sql-database/#google-spanner-and-hbase-range-sharding)

Apache HBase is a massively scalable, distributed NoSQL database modelled after Google BigTable. This is another database that many members in the Yugabyte team are familiar with given they built and ran HBase at scale inside Facebook many years ago. It was the database that backed multiple internet-scale services such as Facebook Messenger (the user to user messaging platform) and the Operational Data Store (which powered metrics and alerts across all Facebook infrastructure). HBase, as well as Google Spanner, have support for range sharding.

Range sharding involves splitting the rows of a table into contiguous ranges that respect the sort order of the table based on the primary key column values. The tables that are range sharded usually start out with a single shard. As data is inserted into the table, it is dynamically split into multiple shards because it is not always possible to know the distribution of keys in the table ahead of time. The basic idea behind range sharding is shown in the figure below.

![[Pasted image 20250324152621.png]]

**Pros**  
This type of sharding allows efficiently querying a range of rows by the primary key values. Examples of such a query is to look up all keys that lie between a lower bound and an upper bound.

**Cons**  
Range sharding leads to a number of issues in practice at scale, some of which are similar to that of linear hash sharding.

[[Shuffle Sharding]]

When it comes to scaling databases, one of the most effective tools at our disposal is **sharding**. If you’re wondering what that means, or why splitting up data can make things faster, you’re in the right place! This guide will cover the essentials of sharding, when it’s needed, and how it can take your database to the next level.

# What is Sharding, Anyway?

Imagine you’re running a library with only one shelf, and every book you own is squeezed onto it. Over time, it gets crowded, making it harder to find what you need quickly. So, you decide to add more shelves, organizing books by genre, author, or some other method. This way, people can go directly to the right shelf rather than sifting through everything. That’s essentially what **database sharding** is — spreading data across multiple “shelves” (or nodes) to make it more manageable.

In database terms, **sharding** is the practice of dividing a large dataset into smaller, more manageable chunks, called **shards**, each stored on a different server. Instead of one large database handling all requests, each shard handles a subset of data, making the system faster and more efficient.

# Why Sharding Matters: Scaling and Performance

As applications grow, the databases supporting them often become overwhelmed. Every time a database grows in size and the number of users increases, it can slow down:

- **Read operations** start to take longer because the database has more data to sift through.
- **Write operations** slow down since there’s more data to manage and store.
- **Availability** can be affected, as a single large database represents a single point of failure.

Sharding addresses these issues by breaking data into smaller pieces that can be stored across multiple servers. With sharding, each server holds just a part of the data, so read and write operations don’t have to interact with the entire dataset — just the relevant shard. This improves speed, reduces the load on each server, and enhances availability.

# How Sharding Works: Key Concepts

To understand sharding, let’s break down some key concepts:

1. **Shards**  
    Shards are the “pieces” that make up a sharded database. Each shard is a complete database in itself, responsible for a specific subset of data. Together, all the shards function as a single logical database for the application.
2. **Shard Key**  
    A shard key is the piece of information used to determine which shard a piece of data belongs to. Think of it like the criteria you use to split up books in a library — by genre, author, or some other rule.
3. **Horizontal Partitioning**  
    Sharding is a type of horizontal partitioning, which means that rows of a table are split across different nodes (unlike vertical partitioning, where columns are split). Horizontal partitioning allows each shard to handle its own subset of rows, improving performance for larger tables.
4. **Routing**  
    When a query is made to a sharded database, the system needs a way to figure out which shard to query. Routing is the process of directing each query to the correct shard based on the shard key.

# Types of Sharding Strategies

Not all sharding strategies are the same, and choosing the right one depends on how your data is structured and how your application uses it. Here are the most common approaches:

## 1. Range-Based Sharding

In **range-based sharding**, data is divided based on a defined range of values. For example, if you’re storing customer data, you might split users based on their IDs:

- Users with IDs 1–100,000 go to Shard 1
- Users with IDs 100,001–200,000 go to Shard 2

Range-based sharding is simple to implement and understand, but it can lead to “hot spots,” where one shard is handling much more data than others. This is common in scenarios where certain values are accessed more frequently than others.

## 2. Hash-Based Sharding

In **hash-based sharding**, a hash function is applied to the shard key to assign data to shards. For example, if your shard key is a user ID, a hash function can generate a unique number from the ID, which determines the shard. Hashing evenly distributes data across shards, minimizing hot spots. However, this method can be more challenging to rebalance if you add or remove shards.

## 3. Geographic Sharding

With **geographic sharding**, data is split based on the user’s location. For example, data from users in North America might be stored in one shard, while data from Europe is stored in another. Geographic sharding is ideal for applications with global users since it keeps data closer to the users, reducing latency. However, it requires careful planning to handle cross-region data consistency.

# When to Shard (and When Not To)

Sharding can be powerful, but it’s not always the right choice. Here’s when it makes sense to implement sharding:

1. **Your Database is Growing Rapidly**: When data volume increases beyond what a single server can handle, sharding allows you to distribute the load across multiple servers.
2. **High Read/Write Demand**: Applications with frequent read and write requests benefit from sharding since each shard handles only a subset of data.
3. **Global User Base**: For apps with users around the world, sharding by geography can help reduce latency and improve performance.

## When Not To Shard

If your application is small, sharding can introduce unnecessary complexity. Smaller datasets can often be managed with vertical scaling or simple replication instead. Sharding works best for applications with specific scaling needs or high availability requirements.

# How to Implement Sharding in Your Database

If you decide to go forward with sharding, here’s a quick roadmap for getting started:

1. **Choose Your Shard Key Wisely**  
    The shard key determines how data is distributed, so it’s essential to pick one that evenly spreads the data. A poor shard key can lead to an uneven distribution, where some shards are overloaded while others are underutilized.
2. **Define Sharding Strategy**  
    Decide on a sharding strategy (range, hash, or geographic) that aligns with your application’s access patterns and growth expectations. If your data is fairly balanced, hash-based sharding is often a good choice.
3. **Set Up Shards**  
    Configure individual servers or clusters as shards. Each shard should operate independently, but be accessible as part of the overall system.
4. **Implement Routing Logic**  
    Ensure your application’s queries can route to the correct shard. This may involve custom application logic or a sharding middleware that handles routing automatically.
5. **Test and Monitor**  
    Monitor each shard’s load and performance. Sharded systems can become unbalanced over time, so keeping an eye on performance helps you spot and address issues early.

# Real-Life Use Cases for Sharding

Sharding is widely used in high-demand applications. Here are a few examples where sharding shines:

- **Social Media Platforms**: With millions of users and high interaction, sharding helps social media apps distribute data like posts, profiles, and interactions across multiple servers.
- **E-commerce Websites**: Online stores often shard databases by product categories or customer regions to handle a high volume of transactions and product data efficiently.
- **Financial Services**: Banks and payment platforms shard customer data across regions to comply with data regulations, reduce latency, and maintain availability.

# Pros and Cons of Sharding

Like any approach, sharding has its advantages and challenges. Here’s a quick rundown:

**Pros**:

- **Improved Performance**: Shards handle smaller datasets, reducing query times.
- **Scalability**: Adding new shards allows your database to scale horizontally.
- **Fault Isolation**: If one shard fails, others can continue operating.

**Cons**:

- **Complexity**: Managing multiple shards adds complexity, particularly around routing and data consistency.
- **Maintenance Overhead**: Rebalancing and adding new shards require careful planning.
- **Potential for Hot Spots**: Poor shard key choices can lead to unbalanced shards, where some handle more load than others.

# In Summary: Is Sharding Right for You?

Sharding is a valuable tool for scaling large databases, especially when your application needs to handle massive data loads or cater to a global audience. By splitting data across multiple nodes, sharding enables faster reads and writes, improves fault tolerance, and provides a foundation for scalable growth.

While it’s not for every application, sharding offers a structured way to scale databases without overwhelming a single server. As you experiment with sharding, remember that choosing the right strategy and shard key is crucial — and with the right setup, you can keep your database running smoothly as your application scales.