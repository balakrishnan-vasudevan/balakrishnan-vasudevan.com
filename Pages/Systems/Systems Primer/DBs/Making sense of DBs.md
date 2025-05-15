
I spent 100+ hours breaking down Databases... Here’s what I found.

I was obsessed.

I dove deep into 4 different databases — both SQL and NoSQL— to understand:

- How they’re created
- How they work internally
- What they’re actually made of

The deeper I went, the more complex it seemed.
But then I saw the pattern.

No matter how fancy or complex a database looks...
They all boil down to just 3 simple layers.
Yes, just 3 layers.

If you understand these 3 layers, you can:
- Understand any database
- Build a deep intuition about its architecture
- Answer any interview question confidently

Here are the 3 layers:

1. 𝗨𝘀𝗲𝗿 𝗔𝗰𝗰𝗲𝘀𝘀 𝗟𝗮𝘆𝗲𝗿
   
This layer defines how users connect with the database.

It includes:
- SQL (Structured Query Language)
- HTTP APIs (For NoSQL databases)
- Specific Protocols (Database-specific query languages)

Examples:
- RDBMS: SQL for user access.
- Cassandra: CQL (Cassandra Query Language).
- NoSQL (DynamoDB, MongoDB): HTTP APIs for user access.

2. 𝗥𝗼𝘂𝘁𝗶𝗻𝗴 𝗟𝗮𝘆𝗲𝗿
   
This layer routes read and write requests to the correct server or node.

This layer is optional for databases on a single node (e.g., most traditional RDBMS).

But for distributed databases (NoSQL), this layer is critical.

Examples:

- DynamoDB: Uses a request router that connects to partition metadata to route reads/writes to specific partitions.

- MongoDB: Uses mongos that connects to config servers for routing.

- Cassandra: Uses snitch to find the node where the data resides.

Pro Tip:

Almost all of them use the same routing algorithm—Consistent Hashing.

It efficiently distributes data across nodes for high availability and scalability.

3. 𝗦𝘁𝗼𝗿𝗮𝗴𝗲 𝗟𝗮𝘆𝗲𝗿
   
This layer defines how data is stored on disk.

There are 2 common data structures used in this layer:

B/B+ Tree:
- Used in 80% of databases (both SQL and NoSQL).
- Provides consistent O(log n) read and write access.
- Perfect for range queries.
Examples: All SQL DBs, DynamoDB, MongoDB.

LSM Tree:
- Optimized for high write throughput.
- Uses concepts like SSTable, compaction, tombstone to manage data efficiently.
Examples: Cassandra, ScyllaDB.


That’s it.
All databases—SQL and NoSQL—are just a combination of these 3 layers.

What surprised me the most?

Despite all the marketing hype, SQL and NoSQL databases are fundamentally the same.

They just assemble these 3 layers differently.

Next time you see a new, fancy database...
Don’t get swayed by the buzzwords or social media hype.

Instead:
- Apply this 3-layer architecture.
- Break down the database into these 3 layers.
- Understand it in 2 minutes flat.

This mindset shift will make you immune to hype and unmatched in system design interviews.