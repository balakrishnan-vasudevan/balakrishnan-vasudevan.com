# Transaction with NoSQL Databases

Tags: databases, no-sql
Category: Articles
Company: general
Status: Not started
URL: https://medium.com/@patrickkoss/interview-so-how-do-you-do-a-transaction-with-nosql-databases-c3d80bc7d314

I’ve always enjoyed conducting technical interviews, especially when it comes to challenging candidates with questions that require them to think critically about core engineering concepts. One of my favorite ways to kick off these conversations is by diving into problems that mirror real-world scenarios we face in backend development — problems that involve databases, message queues, and distributed systems. My goal isn’t just to quiz candidates, but to engage them in a discussion, just like we would in the day-to-day work of an engineering team.

Here’s a scenario I often present to candidates:

> Imagine we’re working within a large, distributed system. We frequently exchange messages, both asynchronously and synchronously, and sometimes we need to write data to a database while simultaneously publishing a message to a queue. How would you design a mechanism to ensure that both the write and the publish happen reliably?
> 

The conversation usually steers towards the dual-write problem, a common issue when dealing with multiple external systems. It’s important for candidates to grasp that simply writing to the database and then publishing to the queue isn’t enough. What happens if the database write succeeds, but the queue publish fails? Or, worse yet, what if an attempt to roll back the transaction also fails? You’re left with an inconsistent state across your systems, which can lead to bigger issues down the road.

Many candidates recognize this problem and suggest implementing the transactional outbox pattern. This pattern addresses the consistency issue by writing the data to the database first, then, in the same transaction, writing the message intended for the queue into an outbox table within that database. This approach allows for a reliable, consistent state between the two external systems, which is exactly what we’re aiming for.

![https://miro.medium.com/v2/resize:fit:1400/1*B8gg0bhYBVRuHJkVLj-RFw.png](https://miro.medium.com/v2/resize:fit:1400/1*B8gg0bhYBVRuHJkVLj-RFw.png)

So, here’s where we really start to get into the weeds:

> Unfortunately, we’ve hit a point where the sheer volume of data we’re dealing with makes it impossible to store everything on a single machine. To handle this, we’ve moved away from a single-leader relational database and shifted to a NoSQL solution like Cassandra, distributing the data across multiple replicas. The trade-off, however, is that we lose the luxury of transactions. So, how do we implement the same level of reliability in a NoSQL environment?
> 

This is where many candidates stumble. The dual-write problem persists, so simply performing two separate writes isn’t going to work.

The solution, though, is surprisingly straightforward: we denormalize the data. Wait, what? Isn’t normalization something we’re all taught to prioritize in order to avoid anomalies and representation issues? Normally, yes. But this situation is different. Since we can’t rely on sequential writes, denormalizing the data allows us to condense everything into a single write operation.

```
{
  "resource": {},
  "outbox": [{"message": "something to publish"}]
}
```

> How do you prevent lost updates when reading from the outbox, especially when another process could be modifying the same document at the same time?
> 

This is the first question I typically pose after introducing the outbox problem. It’s a relatively standard scenario in distributed systems, and while many candidates are familiar with it, the real challenge lies in understanding the underlying problem and applying the right solution effectively.

Let’s break it down: The problem we’re addressing is what’s known as the `lost update` problem. This occurs when two or more processes are attempting to modify the same piece of data simultaneously. In a NoSQL distributed environment, where transactions and locks aren’t always available, this can easily lead to inconsistencies.

Imagine two processes are reading from the outbox at nearly the same time. Process A reads the document, then Process B reads the same document shortly after. Now, both processes think they have an accurate version of the document. Process A updates the outbox and writes it back to the database. Shortly after, Process B does the same. However, Process B is unaware of the changes made by Process A and overwrites them, leading to the loss of Process A’s update. In a distributed system, this type of situation can happen frequently, especially under high load or with complex workflows involving multiple services.

To prevent these kinds of lost updates, most candidates suggest using **optimistic locking**, which is a widely accepted pattern in distributed systems for handling concurrent updates without requiring traditional locks. The core idea behind optimistic locking is to assume that collisions (i.e., multiple processes trying to update the same data) are rare and that it’s more efficient to check for conflicts only when they happen rather than locking data preemptively.

Here’s how it works:

1. **Version Control:** We add a version field to each document in the outbox. This version field is an integer that gets incremented each time the document is updated. When a process reads the document, it also reads the version number.
2. **Compare and Increment:** Before making any updates, the process reads the current version of the document. When it attempts to write back its changes, it checks if the version of the document in the database matches the version it originally read. If the versions match, the update proceeds, and the version is incremented. If the versions don’t match (indicating another process has already updated the document), the update is rejected, and the process must retry.

Next, things get a bit more challenging as we move into the realm of partitioning in distributed NoSQL systems.

> Once we’ve implemented the outbox, how do we clear it efficiently? Specifically, how do we identify which documents have non-empty outboxes?
> 

In a traditional relational database, this might seem straightforward: you could issue a simple query to filter out the non-empty outboxes. But in a NoSQL environment like Cassandra, the situation becomes more complicated due to how data is partitioned and distributed across multiple nodes. NoSQL databases, especially those like Cassandra, are designed with scalability and performance in mind. They prioritize fast, distributed reads and writes over complex querying capabilities. As a result, querying for specific records across distributed nodes isn’t as seamless as it would be in a centralized relational database.

Here’s an example of how this challenge plays out:

You could create a simple table like this:

```
CREATE TABLE resource_outbox (
  resource_id UUID PRIMARY KEY,
  resource_data text,
  outbox list<text>,
  outbox_size int
);
```

Then, you might try to query it like this:

```
SELECT resource_id, resource_data, outbox
FROM resource_outbox
WHERE outbox_size > 0 ALLOW FILTERING;
```

However, the `ALLOW FILTERING` clause here is a warning sign. In Cassandra, filtering results after a query has been distributed across multiple nodes is inefficient because the database essentially has to perform a full table scan across all nodes, filtering the results after the fact. This might work fine for small datasets or testing environments, but in production, with large-scale distributed data, this approach quickly becomes untenable. Cassandra’s architecture simply isn’t designed for such queries, and performance will degrade as your dataset grows.

To address this, we need to rethink our schema to optimize for these kinds of queries. In distributed systems, efficient querying often comes down to choosing the right partition and clustering keys. By adjusting our schema design, we can minimize the need for filtering and allow Cassandra to locate the relevant data more effectively.

Here’s an example of how you could evolve the schema:

```
CREATE TABLE resource_outbox (
  resource_id UUID,
  outbox_status boolean,
  resource_data text,
  outbox list<text>,
  PRIMARY KEY (outbox_status, resource_id)
);
```

In this improved design, we introduce an `outbox_status` column as part of the primary key. This column acts as a marker indicating whether the outbox is empty or not. Now, instead of using inefficient filtering to identify non-empty outboxes, we can directly query for rows where `outbox_status` is `true`.

Here’s how the query might look:

```
SELECT resource_id, resource_data, outbox
FROM resource_outbox
WHERE outbox_status = true;
```

By making `outbox_status` part of the primary key, Cassandra can efficiently route the query to the appropriate partitions, rather than scanning all nodes. This reduces the overhead of filtering and makes the query scalable, even as your dataset grows. Essentially, you’re telling Cassandra exactly where to look rather than asking it to find the relevant data after the fact.

> Fantastic! This solution addresses the efficiency problem well. But let’s take it a step further: in our current setup, we’re still querying the entire table. In the relational database world, we might use a query like SELECT * FROM outbox FOR UPDATE SKIP LOCKED LIMIT 1 to avoid scanning the whole table. This approach lets us pick one item, process it, and then delete the entry—all without locking the entire table. So how do we replicate that behavior in our Cassandra example?
> 

Cassandra, as a distributed NoSQL database, lacks row-level locks and transaction-based mechanisms that are common in relational databases like PostgreSQL. Features such as `FOR UPDATE SKIP LOCKED` don’t have direct equivalents in Cassandra because its architecture is designed for eventual consistency and horizontal scaling. In distributed systems like Cassandra, locking mechanisms that work in relational databases become impractical because data is spread across many nodes. So, to solve this problem, we need to apply strategies that fit Cassandra’s distributed, lock-free model.

While Cassandra doesn’t support row-level locking, we can achieve similar functionality by introducing a pattern where rows are “claimed” for processing. This ensures that only one process can work on a row at a time, preventing race conditions and guaranteeing that each outbox entry is processed only once.

Here’s how this works:

- **Add a Processing Column:** Introduce a boolean or timestamp column (e.g., `processing_status` or `processing_time`) that indicates when a row is being processed.
- **Query for Unprocessed Rows:** Write a query to locate rows that haven’t been processed yet, and pick one to mark as “in progress.”
- **Mark the Row as In Progress:** Use a lightweight transaction to safely mark a row for processing, which helps avoid race conditions that could occur in a distributed system.

To implement this, we need to make some adjustments to the schema. Here’s how the table would evolve:

```
CREATE TABLE resource_outbox (
  resource_id UUID,
  outbox_status boolean,
  processing_status boolean,
  resource_data text,
  outbox list<text>,
  PRIMARY KEY (outbox_status, resource_id)
);
```

In this updated schema, we’ve introduced the `processing_status` column to track whether the row is currently being processed.

Once the schema is updated, we can query the table for a single unprocessed row:

```
SELECT resource_id, resource_data, outbox
FROM resource_outbox
WHERE outbox_status = true AND processing_status = false LIMIT 1;
```

After fetching the `resource_id`, immediately attempt to claim it:

```
UPDATE resource_outbox
SET processing_status = true
WHERE resource_id = <resource_id>
IF processing_status = false;
```

If this `UPDATE` is successful (returns `true`), you have claimed the row, and you can safely process the outbox. If this `UPDATE` fails (returns `false`), it means another client claimed the row at the same time, and you should retry the process by querying for the next available row.

By introducing this “claim and process” pattern, we’ve effectively replicated the behavior of `FOR UPDATE SKIP LOCKED LIMIT 1` in Cassandra. We’re able to sequentially process outbox entries without locking the entire table, ensuring that no two processes work on the same entry at the same time.

Lightweight transactions play a critical role here by providing just enough transactional guarantees to prevent race conditions while still aligning with Cassandra’s distributed architecture. This method leverages Cassandra’s strengths — horizontal scalability and eventual consistency — while addressing the need for safe, sequential processing of outbox entries.