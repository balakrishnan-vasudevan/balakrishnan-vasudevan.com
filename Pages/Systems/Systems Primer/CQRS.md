---
source: https://newsletter.scalablethread.com/p/what-is-command-query-responsibility
---

### Understanding How Separating Reads and Writes Can Improve Performance

A data model defines how data is organized and represented in a database. In traditional CRUD application architectures a single data model is used for both reading and writing data. As applications scale, this approach leads to performance bottlenecks and complexity. Read operations optimized for retrieval may clash with write operations optimized for [data integrity](https://newsletter.scalablethread.com/p/how-transaction-isolation-provides). Increased load can degrade responsiveness for both types of operations. Complex domain models further complicate the issue, making optimizing for both read and write scenarios challenging.

## What is the CQRS Pattern?

The Command Query Responsibility Segregation (CQRS) pattern is a design approach that separates a data store's read and write operations into distinct models. The core principle is to use separate interfaces for querying data (reads) and commanding data (writes). The command model handles create, update, and delete operations, focusing on data integrity and business logic. The query model handles data retrieval and is optimized for fast reads. This separation allows for

1. **Optimized Performance**: Read and write operations can be tuned separately, improving overall performance.
2. **Independent Scaling**: Read and write databases can be scaled independently based on their specific load requirements.

## **CQRS on Single Database Systems**

In a single database system, the command model may utilize a normalized database schema optimized for writes, and the query model may use denormalized data, or materialized views for performance enhancements. Data synchronization between the command and query models can be done synchronously or asynchronously.

![[Pasted image 20250314162642.png]]

Fig. CQRS on Single Database Systems

Consider a micro-blogging application with a single "Posts" table.

#### **Traditional Model:**

- When a user creates a post, the system writes to the "Posts" table.
- When a user views a post, the system reads from the same "Posts" table.
- If the site becomes very popular, both read and write operations compete for resources, potentially slowing down the system.

#### **CQRS Model:**

- **Write Model:** The "Posts" table remains optimized for writes. It ensures data consistency when creating or updating posts.
- **Read Model:** A separate "PublishedPostsView" can be created. This view can use the "Posts" table to pre-calculate summaries or format the content for display. When a user views a post, the system reads from this optimized view. This view might not contain all the details of the original post, but only the data needed for display.
- Another read model might be created for search functionality, containing indexed terms extracted from the post content.
- When a new post is created, the write model updates the "Posts" table and then asynchronously updates the "PublishedPostsView" and the search index.

Both operations utilize the same underlying database. However, their access patterns and data structures are logically separated, improving system responsiveness.

## **CQRS on Multi-Database Systems**

Implementing CQRS on multiple databases involves using separate databases for read and write operations. This approach is suitable for applications that require high scalability and can tolerate [eventual consistency](https://newsletter.scalablethread.com/i/146489166/eventual-consistency-model). The command model might use a relational database for [transactional integrity](https://newsletter.scalablethread.com/p/how-transaction-isolation-provides), while the query model might use a NoSQL database for scalability and flexibility. This separation allows each database to be selected and configured based on its specific workload requirements, addressing the limitations of a single database handling diverse operations. Data synchronization between databases is typically asynchronous.

![[Pasted image 20250314162608.png]]

**CQRS on Multi-Database Systems**

For example, an e-commerce platform might use a relational database for order processing (commands) and a NoSQL database for product catalog queries. When a customer places an order, the relational database handles the transaction. Product details for display are retrieved from the NoSQL database, which is optimized for fast, scalable reads. Changes to product information in the relational database are propagated to the NoSQL database asynchronously.

#### CQRS and Event Sourcing

[Event Sourcing](https://newsletter.scalablethread.com/p/what-is-event-sourcing) is often used in conjunction with CQRS. The command model stores events in an event store, while the query model builds read models by replaying events from the event store. Eventual consistency is inherent in this approach.

## **Pros and Cons**

#### Pros

Apart from the ones already stated above,

- **Increased Flexibility:** Each model can use different database technologies and data models, providing flexibility and adaptability.
- **Improved Maintainability:** Separating concerns makes the codebase easier to understand and maintain.

#### Cons

- **Eventual Consistency:** Asynchronous synchronization can lead to eventual consistency, which may not be suitable for all applications.
- **Data Duplication:** Read models often involve data duplication, which can increase storage requirements.
- **Infrastructure Overhead:** Multiple databases and messaging systems may increase infrastructure costs.
- **Synchronization Complexity:** Ensuring data consistency between the read and write sides can be difficult.
