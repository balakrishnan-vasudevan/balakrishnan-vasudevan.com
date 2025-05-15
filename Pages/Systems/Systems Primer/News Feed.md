**Functional requirements:**

1. Newsfeed is based on the posts from people, pages and groups that a user follows. For simplicity lets assume only a user can post.
2. User may follow friends, groups or pages.
3. Feed may contains photos, videos or just text.
4. The feed should automatically update the active user’s feed as and when new posts arrive.

**Non-functional requirements:**

1. Maximum latency is 2s for any user’s newsfeed.
2. When a user posts anything, it should not take no more than 5s to appear on his followers feed.

Lets assume each user has 300 friends and follows 200 pages

Total DAUs = 500M, fetches feed 5 times a day, QPS = 2.5B requests/day ~ 30k requests/second

Storage estimation: Assume we keep 500 posts for each user’s feed and keep all these in memory for faster access, if each post is 1KB then each user needs 500KB storage. To store for 500M DAUs, we need 500M x 500KB = 250 TB of memory

Server estimation: Assume one server can hold up to 100GB then we need 2500 servers.

# **DB Schema**

To store user/entity details, lets use relational database like PostgreSQL or MySQL, since they offer ACID (Atomicity, Consistency, Isolation, Durability) transactions and support for complex queries. Relational databases offer strong consistency guarantees, which are important for maintaining user data integrity. They also provide features for enforcing data constraints, such as unique constraints for usernames or email addresses.

Schema representation: Entity(page/group): _EntityID_, EntityName, EmailI, Type(page/group), CreationDate

To store post/feed details, a NoSQL database like MongoDB or Cassandra may be preferable. They are designed to handle large volumes of semi or unstructured data which is common in social media posts. They also offer flexible schema designs, allowing for easy modification and adaptation to changing data requirements. Additionally, their distributed architecture supports high throughput and horizontal scaling to accommodate growing datasets. I would go with Cassandra for the below reasons,

Scalability: Cassandra is known for its ability to scale horizontally, making it suitable for handling large volumes of posts and users. It can easily accommodate the requirement of updating the active user’s feed as new posts arrive.

Performance: Cassandra offers low-latency reads and writes, which aligns with the requirement of maximum latency of 2s for any user’s newsfeed. Users should be able to quickly access their newsfeeds without experiencing significant delays.

Real-time Updates: Cassandra’s ability to handle high write throughput makes it suitable for ensuring that new posts appear on followers’ feeds within 5s of being posted. Its decentralized architecture and tunable consistency levels allow for efficient propagation of updates across the cluster.

Flexible Data Model: Cassandra’s wide-column data model can accommodate different types of content in posts, including photos, videos, and text. It provides flexibility in storing and querying diverse data types, allowing for rich and dynamic newsfeeds.

High Availability: Cassandra is designed for high availability and fault tolerance, ensuring that the newsfeed service remains operational even in the event of node failures or network partitions. This reliability is crucial for meeting the non-functional requirement of maintaining consistent access to newsfeeds.

When storing media such as photos or videos in a feed system, a common approach is to store the media files in a separate storage system service like Amazon S3, Google Cloud Storage, or Azure Blob Storage to store media files such as photos and videos. When a user creates a post that includes media, store the reference (e.g., URL or file path) to the media file in the post record.

Storing relationships between users, such as friendships or follows, can be efficiently handled by a graph database like Neo4j. Graph databases excel at representing and querying relationships between entities, making them ideal for modeling social network connections. They offer efficient traversal of relationships and support advanced graph algorithms for recommendation systems, such as collaborative filtering or personalized recommendations based on user interactions.

![[Pasted image 20250429203856.png]]

We have two major services, Feed publishing and Feed retrieval

Feed publishing:

1. A user post some content “I am feeling great”
2. Load balancer distributes the traffic to API server
3. API server checks for user authenticity and rate limiting service
4. Post service posts the data in the cache and DB
5. Fanout service pushes the content to friends news feed, newsFeed cache will have this data for faster retrieval
6. Notification service will send push notifications to all the user friends about the new post

Feed retrieval:

1. User sends a request to fetch latest news feed
2. Load balancer distributes the traffic to API server
3. API server checks for user authenticity and rate limiting service and routes the request to newsFeed service
4. Newsfeed service fetch the newsfeed from the cache
5. Newsfeed cache stores the stores the news feed IDs needed to serve the request

# **6. Design deep dive**

Fanout service: Fanout is a process of making a post available to all the user friends. Below are the steps involved in this:

1. Fetch the friend IDs from graph database(suitable because of relationship and recommendations)
2. Get the friends info from the user cache. There may be many settings or filters like selective sharing or muting are applied here
3. Send the friends ID list and new FeedItem ID to the message queue
4. Fanout workers fetch this info from the queue and stores it in a cache as a < FeedItemID, userID> mapping table. We just need to store the Ids since entire post would consume a lot of memory.

There are two ways to achieve this, push/fanout on write model or pull/fanout on read model. In push model, the feed is pre-computed during write time. When a new post is made, it is delivered to all the users cache immediately. The main advantage is post retrieval is fast since it is already computed, giving the user real time experience. the down side is if a user has many friends, fetching all of their details and updating each one of their cache will be slow and time consuming. Which causes **hotkey problem**. Also for user who are inactive, this computing will be unnecessary. In pull model/ on-demand, the feed is generated during read time or when a user loads the home page. This approach is efficient for inactive users. There is no hotkey problem, but fetching the feed will be slow.

==One can employ hybrid model, for celebrities who has more friends, we can have pull model and for users with less friends, we can have push model.==

Newsfeed service:

1. User sends a request to retrieve her news feed.
2. The LB redistributes the traffic
3. Web server call news feed service to fetch news feed
4. News feed service gets a list of postIDs from the newsfeed cache
5. A newsfeed is more than just feed ID, hence it retrieves other related details from user DB and post DB
6. The fully hydrated news feed is returned as JSON format back to the user

# **7. Optimizations**

1. Use CDNs to store the media data for fast retrieval.
2. Introduce parallelism: Build a loosely coupled systems by introducing message queues between components.
3. Cost optimization: CDN comes with a high cost, hence coming up with your own CDNs will be cost efficient.

# **8. Fault Tolerance**

1. Replicating data across multiple nodes and multiple data centers to ensures redundancy and fault tolerance.
2. Use consistant hashing for mitigate hotkey problem.
3. Introduce load balancing so that traffic can be evenly routed without causing bottleneck to servers causing them to fail.
4. Introduce redundancy and failover by configuring automated failover mechanisms to detect failures and switch to standby components seamlessly.
5. Graceful degradation can also help during failures by rendering limited data from cache until the server comes up instead of completely halting service.
6. Implement circuit breakers to detect and handle failures in external dependencies, such as downstream services or APIs. Circuit breakers monitor the health of external services and temporarily halt requests if they detect failures. This prevents cascading failures and allows the system to recover gracefully.
7. Implement robust monitoring and alerting systems to detect anomalies, performance issues, and failures in real-time.
8. Implement automated recovery mechanisms to restore service and recover from failures quickly. Use automated scripts or orchestration tools to restart failed components, reconfigure load balancers, and perform failover procedures automatically.

# **9. Performance**

1. Cache data as much as possible.
2. Asynchronous Processing: Use message queuing systems like RabbitMQ or Apache Kafka to decouple components and enable asynchronous processing. Use pub/sub mechanisms to notify subscribers of new events or changes in data.
3. Optimized API Design: Implement pagination, filtering, and sorting mechanisms to limit the amount of data returned in each API response and improve query performance.

# 10. Scalability

We use horizontal scaling to scale servers.

# **11. CAP theorem**

In most practical distributed systems, especially those dealing with real-time data and user interactions, partition tolerance (P) is considered a non-negotiable attribute. This is because network partitions can and do occur in distributed environments, and it’s essential for the system to remain operational even during network partitions to maintain overall system reliability. Given the requirements like max latency of 2s and 5s of update, it is wise to prioritizing availability over consistency and ensures that the newsfeed system remains responsive and accessible to users, even in the face of network partitions or temporary failures. Eventual consistency will suit our needs.