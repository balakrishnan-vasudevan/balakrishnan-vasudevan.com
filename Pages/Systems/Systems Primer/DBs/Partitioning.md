Source: https://levelup.gitconnected.com/system-design-concepts-partitioning-for-scalability-and-resilience-a953e53be72d


Partitioning is the process of splitting a system or dataset into smaller, independent, and manageable subsets (called partitions). Each partition operates independently, often in parallel, to optimize system **scalability, performance, and reliability**.

1. **Scalability**

- **Horizontal scaling:** Adding more nodes/servers to handle growing workloads.
- Each partition handles a fraction of the overall load, making the system resilient to traffic surges.

**2. Isolation :** Failures in one partition do not impact others.

- **Example**: If a shard storing data for **North America** goes down, users from **Europe** and **Asia** remain unaffected.

**3. Data Sharding (Partitioning in Databases) :** Divides data logically or geographically:

- **Horizontal Partitioning:** Rows are divided across tables or nodes.
- **Vertical Partitioning:** Columns are separated by functionality (e.g., user metadata vs. purchase history).

Optimizes query performance and minimizes contention on resources.



1. **Global Load Balancer 🎛️**: Routes traffic based on region or request type. Handles failover and retries.
2. **Region-Based Shards 🌎🌍🌏**: Separate independent shards for fault isolation and scalability. Each shard contains:

- A database cluster (replicated for redundancy).
- Local application servers to process requests.
- A cache layer to speed up frequent reads.

**3. Local Load Balancers**: Manage traffic within each shard.

**4. High Availability**: Each shard operates independently; failure in one doesn’t impact others.


## Types
**Horizontal Partitioning (Sharding) :** Data rows are split across multiple tables or databases.

**Benefits:**

- Simplifies scaling by adding more shards as user base grows.
- Localizes queries, reducing latency.
- Isolates failures to specific shards.

**Use Case Scenario**: Social Media User Data

- A platform with millions of users, where data is sharded by geographical region for scalability and latency reduction.

![[Pasted image 20250420140259.png]]

**Horizontal Partitioning by Region**

**North America Shard (Shard 1):**
![[Pasted image 20250420140312.png]]

**Europe Shard (Shard 2):**
![[Pasted image 20250420140323.png]]

**Benefits:**

- Queries for a specific region are directed to that shard, reducing latency.
- Regional failures (e.g., Asia server crash) affect only a subset of users.
![[Pasted image 20250420140336.png]]


**Key Takeaways from the Diagram:**

- **_Horizontal Partitioning_** _allows data to be distributed across multiple servers, preventing any one server from becoming a bottleneck._
- _Each_ **_shard_** _contains a subset of the data, and they all follow the same_ **_structure_** _(e.g., user data with fields like_ `_username_`_,_ `_email_`_, etc.)._
- _A_ **_Sharded Database_** _routes requests to the appropriate shard, based on a predefined_ **_sharding strategy_** _(in this case, based on user ranges)._


## Vertical Partitioning

Data columns are split across different storage systems.

**Benefits:**

- Keeps frequently accessed data (e.g., user profiles) in faster storage.
- Optimizes data management by separating unrelated data.

**Use Case Scenario**: E-Commerce User Data

- Separating **user profiles** and **order details** into different storage systems.

**Combined Table (Unpartitioned)**

![[Pasted image 20250420140403.png]]

**Vertical Partitioning**

**User Profiles Table:**

![[Pasted image 20250420140414.png]]

**Order Details Table:**
![[Pasted image 20250420140423.png]]

**Benefits:**

- Keeps frequently accessed data (e.g., user profiles) in faster storage.
- Optimizes data management by separating unrelated data.

![[Pasted image 20250420140435.png]]

**Key Points from above Diagram:**

- **_Vertical Partitioning_** _splits data based on columns rather than rows. For example, the_ **_User ID_** _and_ **_User Name_** _are stored together in one partition, while the_ **_Email_** _and_ **_Phone_** _are stored in another partition._
- _The_ **_Vertical Partitioned Database_** _routes requests to the appropriate_ **_partition_** _based on the columns needed by the query._
- **_Sharding Strategy_**_: The vertical partitioning strategy involves splitting the columns across different servers, providing better optimization based on queries that need access to specific columns._


## Functional Partitioning

System services or functions are divided into independent modules.

**Benefits:**

- Each service is developed, deployed, and scaled independently.
- Fault isolation: A bug in one service does not crash the system.

**Use Case Scenario**: Microservices in an E-Commerce Application

- Services are divided into independent modules based on functionality.

**Functional Components**

1. **User Service (Authentication, Profiles) :** Handles login, user data storage.
2. **Inventory Service (Products, Stock Levels) :** Manages product catalog and stock information.
3. **Order Service (Purchases, Payments) :** Handles order creation, payment processing.

**Data Partitioned by Function**

**User Service Table:**
![[Pasted image 20250420140521.png]]

**Inventory Service Table:**
![[Pasted image 20250420140530.png]]

**System Flow:**

1. **User Authentication:** User logs in through the **User Service**.
2. **Product Search:** Query is directed to the **Inventory Service**.
3. **Order Placement:** Request is handled by the **Order Service**.

## Benefits:

- **Independent scaling of services:** High traffic on product search doesn’t overload user authentication.
- **Fault isolation:** If the **Order Service** crashes, login and product browsing are unaffected.


![[Pasted image 20250420140553.png]]


**_Practical Examples with Data Tables and Partitions: Video Streaming Platform_**

We will explore **horizontal partitioning** and **vertical partitioning** using a video streaming platform’s **user data**, **video metadata**, and **playback analytics**.

**1. Horizontal Partitioning (Sharding by Region)**

**Scenario :** A global video streaming platform serves millions of users. To reduce latency and improve scalability, users are partitioned based on their geographical location (e.g., US-West, Europe, Asia).

**Unpartitioned Table (Before Sharding)**

![[Pasted image 20250420140622.png]]

**Partitioned Data by Region**

**US-West Shard:**
![[Pasted image 20250420140632.png]]

**Europe Shard:**
![[Pasted image 20250420140642.png]]

**2. Vertical Partitioning (Dataset Segmentation)**

**Scenario :** The platform stores **video metadata** and **playback analytics** separately for optimization. Metadata is used frequently for browsing, while analytics are accessed periodically for insights.

**Unpartitioned Table (Before Segmentation)**

![[Pasted image 20250420140701.png]]

**Partitioned Data by Dataset**

**Video Metadata Table:**
![[Pasted image 20250420140710.png]]

**Playback Analytics Table:**
![[Pasted image 20250420140722.png]]

**Benefits and Use Cases**

**i. Horizontal Partitioning**

- **Latency Reduction:** US-West users access their local shard, avoiding delays caused by accessing a global table.
- **Failure Isolation:** A failure in the Europe shard doesn’t impact US-West or Asia regions.
- **Scaling:** More shards can be added as user base grows (e.g., separate shards for Central America or Australia).

**ii. Vertical Partitioning**

- **Optimized Storage:** Video metadata (frequently accessed) is stored in a high-performance database. Playback analytics (used less often) can be stored in cheaper archival storage.
- **Independent Scaling:** Metadata tables scale independently from analytics tables, ensuring efficient resource use.

**Challenges of Partitioning**

1. **Key Design Decisions:** Choosing the right partition key is critical. A poor key can lead to **data hotspots** or **skewed partitions**.

- **Example**: Using “region” as a key can overload a single partition if most users are from one area.

**2. Cross-Partition Queries:** Queries spanning multiple partitions can degrade performance.

- **Example**: Calculating the **global average user activity** requires data from all shards.

**3. Consistency Challenges:** Distributed partitions often use **eventual consistency** to maintain availability.

- Trade-off: Real-time consistency might be hard to guarantee.

**4. Operational Complexity:** Partitioning requires careful management of replication, rebalancing, and monitoring.

- Example: Adding new shards may involve migrating data from existing partitions.

**Use Cases of Partitioning**

**1. Social Media Applications (Horizontal Partitioning)**

- **Example:** Facebook stores user posts in partitions based on user IDs.
- **Benefit:** Even with billions of users, individual queries are served efficiently.

**2. E-Commerce (Functional Partitioning) : Example:** Amazon divides services into microservices: Inventory management, Payment processing, User account handling.

- **Benefit:** Each service is scaled and optimized independently.

**3. Financial Systems (Vertical Partitioning) : Example:** A bank separates: Account balances (highly accessed), Transaction history (archived but infrequently accessed).

**Benefit:** Improves performance for day-to-day banking operations.

**When to Use Partitioning?**

- **High Traffic:** Systems with millions of concurrent users.
- **Geographic Distribution:** Applications needing low-latency access for users worldwide.
- **Scalability Needs:** Systems that anticipate rapid growth.
- **Failure Isolation:** Critical systems where downtime must be minimized.

**Best Practices for Partitioning**

1. **Choose a Good Partition Key:** Ensure even distribution of data to avoid hot partitions.
2. **Replication for Fault Tolerance:** Replicate data across partitions to prevent data loss.
3. **Implement Monitoring:** Use tools to monitor the load, health, and performance of each partition.
4. **Plan for Rebalancing:** Design systems to redistribute partitions as traffic or data grows.
5. **Minimize Cross-Partition Dependencies:** Structure data and operations to avoid queries that span multiple partitions.

[[Key-based vs Range-based Partitioning]]


# Why Do We Need Data Partitioning?

Without partitioning, databases and distributed systems suffer from:  
✅ **Slow queries** — As the dataset grows, searching through millions (or billions) of records takes longer.  
✅ **High resource consumption** — CPUs and RAM get overloaded when dealing with large datasets.  
✅ **Limited scalability** — As traffic increases, a single server struggles to handle all requests efficiently.

Partitioning solves these issues by:  
🚀 **Improving Query Performance** — Queries scan smaller datasets, making search operations faster.  
🔄 **Enhancing Scalability** — Data is distributed across multiple storage nodes or databases.  
🔐 **Increasing Fault Tolerance** — Even if one partition fails, the system remains operational.

# Types of Data Partitioning (With Real-World Examples)

# 1️⃣ Range-Based Partitioning

📌 **Problem:** A bank needs to store transaction data for the last 10 years. Older data is rarely accessed, while recent data is frequently queried.

🔹 **Solution:** Use **Range Partitioning**, where transactions are stored based on **date ranges**:

- 2024 transactions → Partition 1
- 2023 transactions → Partition 2
- 2010–2022 transactions → Archived Storage

🔥 **Real-World Example:**

- Credit card companies partition transactions by **year/month** to speed up retrieval.
- **Log management systems (e.g., Splunk, ElasticSearch)** use date-based partitions to store logs efficiently.

# 2️⃣ Hash-Based Partitioning

📌 **Problem:** A social media platform (like Instagram) has millions of users, and each user’s profile data needs to be stored and accessed quickly.

🔹 **Solution:** Use **Hash Partitioning**, where data is distributed based on a **hash function** of the primary key (e.g., user ID). This evenly distributes data across multiple partitions.

🔥 **Real-World Example:**

- **Twitter partitions user tweets** using hash-based partitioning, ensuring data is evenly spread across servers.
- **Distributed databases like Amazon DynamoDB** use hashing to balance load across storage nodes.

# 3️⃣ List-Based Partitioning

📌 **Problem:** A **global e-commerce platform** needs to store order history based on regions (USA, Europe, Asia).

🔹 **Solution:** Use **List Partitioning**, where data is categorized into **specific lists**:

- Orders from the **USA** → Partition 1
- Orders from **Europe** → Partition 2
- Orders from **Asia** → Partition 3

🔥 **Real-World Example:**

- **Amazon partitions order data** based on regions to optimize delivery times.
- **Netflix partitions customer streaming history** based on country-specific regulations.

# 4️⃣ Composite Partitioning (Hybrid Approach)

📌 **Problem:** A ride-hailing app (like Uber) needs to store **trip history** efficiently while considering both **date of the trip** and **city location**.

🔹 **Solution:** **Combine Range & Hash Partitioning**

- First, partition data **by date** (range partitioning).
- Then, further partition by **city ID** (hash partitioning).

🔥 **Real-World Example:**

- **Uber partitions ride history** using a hybrid approach, ensuring queries for past rides in specific locations are lightning fast.
- **YouTube partitions videos** based on both **upload date** and **category** for efficient content delivery.

# Partitioning in System Design Interviews (FAANG-Level Insight 🚀)

Partitioning is a **common topic in system design interviews**, especially for **backend engineering roles at FAANG (Facebook, Apple, Amazon, Netflix, Google) and top tech firms**.

Here’s how to discuss partitioning in an interview:

❓ **Interviewer:** “How would you design a system that stores and retrieves travel pricing data for Expedia?”  
✅ **Your Answer (Partitioning Strategy):**

1. **Use Range Partitioning** — Store pricing data by **travel date** (recent searches are accessed more frequently).
2. **Use Hash Partitioning** — Distribute price data across multiple nodes based on **hotel ID or destination city**.
3. **Use Composite Partitioning** — Combine **range (date)** and **hash (hotel ID)** to optimize lookups.

This approach ensures:  
✔ **Fast query performance** (no need to scan the entire dataset).  
✔ **Scalability** (data is evenly distributed across multiple servers).  
✔ **Fault tolerance** (if one partition fails, others remain accessible).

# Challenges & Trade-offs of Data Partitioning

While partitioning improves performance, it comes with trade-offs:

⚠ **Complex Query Logic:** Some queries may require **scanning multiple partitions**, making retrieval slower.  
⚠ **Uneven Load Distribution:** Poor partitioning strategies (e.g., range partitions with imbalanced data) may cause **hotspots** on some servers.  
⚠ **Repartitioning Complexity:** As data grows, **repartitioning becomes expensive** (e.g., moving data from one partition to another).

**Solution?** Careful **partition key selection** and **auto-scaling mechanisms** to rebalance partitions dynamically.