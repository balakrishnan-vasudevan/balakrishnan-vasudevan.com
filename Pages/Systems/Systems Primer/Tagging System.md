Ref: https://medium.com/@codebuster/designing-a-scalable-tagging-system-171bef077a14

![[Pasted image 20250501133058.png]]

# Requirements

Atlassian offers a variety of products, each containing distinct types of content. Tagging related content across these products is crucial for improving discoverability, enabling seamless navigation, and fostering collaboration among users. For instance, consider the following examples:

- **Jira**: Issues
- **Confluence**: Web Pages
- **Bitbucket**: Pull Requests
- **Trello**: Boards

1. How would you implement a tagging system to link related pages across all Atlassian products?
2. How would you scale the system to handle 100 million tag requests per day? Consider addressing critical aspects such as infrastructure scalability, efficient caching mechanisms, load balancing, database optimizations, and ensuring fault tolerance to maintain consistent performance under high demand.

## _Functional Requirements:_

- Add tag to a content
- Remove a tag from a content
- Search a tag
- Retrieve tags for a content
- Get contents list of tag
- View Popular tags

## _Non Functional Requirements:_

- Scalability 100M requests per day
- Low latency
- Fault tolerant
- High availability
- Consistency
- Durability
- Analytics/Reporting (Optional)

## **Back of the Envelope Estimation:**

Performing a back-of-the-envelope estimation is essential for understanding the system’s scalability requirements and identifying potential bottlenecks. This calculation provides an early approximation of the load the system will need to handle, guiding critical design decisions around infrastructure, storage, and performance optimization.

100M requests per day = 1157 QPS (With Peak 2–3x => 2.5–3k QPS)  
Reads Write ratio = 70:30  
30M writes per day ~= 350 QPS  
70M Reads per day ~= 800 QPS

## Storage Requirements:

For a tag we need ( id, name, content_id, product_type )

id - Integer = 4 bytes  
name - String = 2 bytes per character ~= 50bytes  
content_id - Integer = 4 bytes  
product_type - String = 20–30 bytes  
Approx ~= 100bytes per tag  
  
Per day write = 30M * 100bytes ~= 3GB per day ~= 1TB per year

## **Database Schema:**

The chosen schema design aims to ensure scalability and performance for handling large-scale tagging operations. Each tag entry is compact, requiring minimal storage, which supports efficient read and write operations. By separating tags into `Tag` and `Content_tag` tables, the schema normalizes data, reducing redundancy and improving query performance. Additionally, indexing on `tag_id` and `content_id` enables faster lookups, which is crucial for maintaining low latency in high-traffic scenarios. This design also facilitates future scalability, as new product types or tag attributes can be incorporated with minimal disruption.

**_Tag => {_**id, name, description, timestamp}

**_Content_tag => {_**id, tag_id, content_id, product_type(jira, confluence, trello) }

## **API Design:**

The APIs are designed to be RESTful, adhering to standard practices for simplicity and interoperability. Below are some examples:

- **_Add Tag to a content_  
    **POST — /api/v1/content/<content_id>/tags  
    {name:”example”, product_type:”jira”, content_id:”jira-123"}
- **_Remove tag from a content_  
    **DELETE — /api/v1/content/<content_id>/tags/tag
- **_Get Tags for a content_**  
    GET — /api/v1/content/<content_id>/tags
- **_Search Tags  
    _**GET — /api/v1/tags/tag  
    Response: {page:1, total:3, size:500, items: [{product_type:”jira”, content_id:”jira-123"}]}

Error handling includes clear HTTP status codes, such as 400 for invalid input or 404 for not found, and meaningful error messages. For example, if a requested tag does not exist, the response could return:

{  
  "error": "Tag not found",  
  "status_code": 404  
}

Edge cases, like attempting to add duplicate tags or deleting non-existent tags, are handled gracefully to maintain system consistency.

# **Components**

1. **API Gateway:** Handles authorization, authentication, and rate limiting.
2. **Load Balancer:** Distributes traffic across services and replicas to ensure even load distribution.
3. **Cache:** Stores frequently accessed tags and popular searches to reduce the load on the database and improve read latency, especially for high-demand tags.
4. **ElasticSearch:** Provides full-text search capabilities, ideal for fast retrieval and indexing of tags. Supports complex searches across tags and is well-suited for aggregating data (e.g., identifying the most popular tags).
5. **Add Tag Service:** Adds a new tag and maps it to the corresponding content, then writes the data to the primary database.
6. **Search Tag Service:** Searches for tags and retrieves a list of all related content, reading from read replicas.
7. **Analytics DB:** A time-series database to store metrics related to tags, such as usage statistics and popular tags.
8. **Apache Flink:** Analyzes tag popularity over specific time ranges (e.g., last 24 hours, past week) to identify trending tags. Flink can process real-time data streams and compute aggregations, such as counting tag occurrences within the defined time windows, enabling dynamic updates to the list of popular tags.

> **Why Postgres?**
> 
> PostgreSQL, when architected with a primary-replica setup, partitioning, and caching layers, can effectively handle high loads.

## **Scaling PostgreSQL to Handle Millions of Records**

**Primary-Replica Setup:**

- All insert, update, and delete operations are directed to the primary database, while all read operations are served from replicas.
- PostgreSQL can handle 10,000 to 20,000 transactions per second (TPS) on high-end hardware.
- With read replicas, overall read capacity can scale significantly, potentially reaching 100,000+ requests per second (RPS).
- **Simple Reads:** 10ms latency with proper indexing and caching.
- **Complex Reads:** Up to 100ms latency, depending on query complexity and data volume.

**Replication**

- PostgreSQL supports built-in streaming replication, allowing replicas to stay updated in near real-time.
- **Asynchronous Replication:** Offers higher performance and lower latency but introduces eventual consistency.
- **Synchronous Replication:** Ensures data consistency at the cost of higher latency.

**Load Balancing Reads:** Use pgbouncer or a load balancer to distribute read requests across replicas.

**Connection Pooling:** Efficiently manages database connections to optimize performance.

To handle large volumes of tagging data, partitioning tables by date or product type can optimize query performance and manage storage efficiently.

In our use case, PostgreSQL can handle the traffic without any issues. Since the data volume is not massive, the latency is unlikely to be affected.

However, there are some constraints with PostgreSQL, and we should consider exploring a NoSQL database like Cassandra for more scalable solutions.

## **Cache**

- Cache is used to reduce the load on the database and improve response times for frequently accessed data, particularly in read-heavy scenarios like popular tag lookups.
- Frequently accessed tags and popular search results can be directly fetched from the cache.

**Cache Invalidation and Stale Data Handling:** If a tag association is added to the database, any cached search results may be stale.

- To handle this, the database should be updated, and the cache invalidated. This ensures the next request fetches the updated data from the database and refreshes the cache.
- Additionally, a Time-to-Live (TTL) should be implemented to periodically refresh cached data.

# Conclusion:

This architecture leverages PostgreSQL, ElasticSearch, caching, and Apache Flink to efficiently manage tags, ensuring scalability, low latency, and real-time analytics, while maintaining reliability and cost-efficiency.
