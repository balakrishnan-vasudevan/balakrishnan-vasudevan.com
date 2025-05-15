**Amazon DynamoDB** is a **NoSQL cloud database service** that delivers consistent performance at any scale, making it an essential tool for applications with demanding operational requirements. Let’s explore the key properties and architecture that make **DynamoDB** a powerhouse in modern cloud-based solutions.

## Core Properties 💪

DynamoDB's fundamental properties make it a powerhouse for enterprise applications:

- Consistent performance across all scales
- High availability and durability
- Fully managed serverless experience

To put its **performance** into **perspective**, during the **2021 Amazon Prime Day** (a 66-hour shopping event), **DynamoDB** showcased its incredible capabilities by:

- Handling trillions of API calls
- Peaking at **89.2 million requests per second**
- Maintaining **single-digit** millisecond response times
- Ensuring high **availability** throughout the event

## The Six Pillars of DynamoDB's Success 🏛️

### 1. Fully Managed Cloud Service

DynamoDB's API allows applications to create tables and manage data without concerning themselves with storage locations or management details.

### 2. Multi-tenant Architecture

The service efficiently manages resources across multiple customers.

### 3. Optimal Resource Utilization

By storing data from different customers on the same machine, DynamoDB achieves cost efficiency without compromising performance.

### 4. Unlimited Scale

Tables can grow without predefined limits, offering true scalability for your applications.

### 5. Predictable Performance

Consistent low-latency responses make application behaviour reliable and predictable.

### 6. High Availability

Data replication across multiple Availability Zones ensures robust durability and availability.

## Data Storage and Management 📦

A table in DynamoDB is a collection of items and each item is a collection of attributes. Each item is uniquely identified by a primary key.

### Primary Key Structure

Each item in a DynamoDB table is uniquely identified by a primary key, which consists of:

- **Partition key**(mandatory) used for identifying the partition
- **Sort key**(optional)

The system passes the primary key to an internal hash function to determine data location:

**Primary Key ➡️ Hash Function ➡️ Storage Location**

## Advanced Features

### Secondary Indexes:

Even supports secondary indexes to enhance its querying capability. A table can have one or more secondary indexes.

### ACID Transactions

Despite being a NoSQL database, DynamoDB supports **ACID** transactions, which means  that the application can update multiple items while ensuring atomicity, consistency, isolation, and durability (ACID) across items without compromising the scalability, availability, and performance characteristics of DynamoDB tables.

### Partitioning

- Tables are divided into multiple partitions for optimal throughput and storage. Each partition of the table hosts a disjoint and contiguous part of the table’s key-range.
- Each partition has multiple replicas distributed across different Availability Zones for high availability and durability.
- The replica for a partition form a replication group. The replication group uses an algorithm known as Multi-Paxos for leader election(more on this algorithm in a future article).

## Storage Node Architecture and Replication 🏗️

Lets first look at the structure of a storage replica, then we will discuss the use of the leader we chose using that algorithm:

![[Pasted image 20250316112947.png]]
As we can see a storage replicas(nodes) consists of write-ahead log(WAL) and B-tree. Here B-tree stores the key value data, while the WAL as the name suggests it's write ahead which means the data which comes from application writes or updates are stored as log in these to be later persisted to the store i.e. our B-tree.

Also we have log replicas as well. As we can see it only consists of WAL. More on this in upcoming paragraphs.

### Replication and Leadership Mechanism

The replication mechanism in DynamoDB follows a sophisticated process:

1. **Leader's Role**

- Only the leader replica can serve write and strongly consistent read requests
- Any replica from the replication group can serve eventually consistent reads

2. **Write Process**

**When the leader receives a write request:**

- leader of the replication group for the key being written generates a WAL records and sends it to the other replicas from the group.
- Once the write is acknowledged by a quorom of replicas i.e. they have persisted this WAL to their local WAL(hopefully the function of WAL is clear now)
- Confirms success at the application level once quorum persists the WAL

3. **Failure Handling**

**_What if the leader fails_**_:_ who do you think will serve the request? So if the leader of the group is failure detected by any of its peers, the peer can propose a new round of election to elect itself as the new leader.

4. **Replica Recovery**

**_What if one of the replica fails_**_:_ Do you remember i showed you a log-replica structure, so if any of the replica fails these log replicas are the one's that hold the WAL for this replica till the time our replica is repaired back or becomes available.

## Core Services Deep Dive 🔧

![[Pasted image 20250316113017.png]]

While DynamoDB consists of numerous microservices, let's explore the essential ones in detail:

### 1. Metadata Service

The backbone of DynamoDB's routing system, containing:

- Routing information about tables
- Index details
- Replication group information for keys
- Table-specific metadata

### 2. Request Routing Service

Acts as the traffic controller for DynamoDB:

- Handles authentication and authorization of requests
- Routes requests to appropriate servers based on metadata lookup
- Directs resource creation, updates, and data definition requests to autoadmin service

### 3. Storage Service

The data management powerhouse:

- Responsible for storing customer data across storage nodes
- Manages multiple replicas of different partitions
- Ensures data distribution and availability

### 4. Autoadmin Service

Functions as DynamoDB's central nervous system:

- Monitors fleet health continuously
- Tracks partition health
- Manages table scaling operations
- Executes all control plane requests
- Replaces unhealthy replicas (slow, unresponsive, or on failing hardware)
- Performs health checks of core components
- Manages hardware replacement for failing components

### Additional Service 🎯

DynamoDB has a set of other services which offers various other capabilities:

- **Point-in-time restore**
- **On-demand backups**
- **Update streams**
- **Global admission control**
- **Global tables**
- **Global secondary indices**
- **Transactions**

