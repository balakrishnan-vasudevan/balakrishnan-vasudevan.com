#databases, #scaling


There are three big problems with relational databases that make it difficult to scale:

- The poor time complexity characteristics of SQL joins - In a SQL join operation, your relational database is combining results from two or more different tables. Not only are you reading quite a bit more data but you're also comparing the values in one to the other to determine which values should be returned.
- The difficulty in horizontally scaling - Horizontal scaling works best when you can shard the data in a way that a single request can be handled by a single machine. Jumping around multiple boxes and making network requests between them will result in slower performance.
- The unbounded nature of queries - There's no inherent limit to the amount of data you can scan in a single request to your database, which also means there's no inherent limit to how a single bad query can gobble up your resources and lock up your database.




## How NoSQL databases handle these relational problems[​](https://www.alexdebrie.com/posts/dynamodb-no-bad-queries/#how-nosql-databases-handle-these-relational-problems "Direct link to heading")

In the previous section, we saw how relational databases run into problems as they scale. In this section, we'll see how NoSQL databases like DynamoDB handle these problems. Unsurprisingly, they're essentially the inverse of the problems listed above:

- DynamoDB does not allow joins;
- DynamoDB forces you to segment your data, allowing for easier horizontal scaling; and
- DynamoDB puts explicit bounds on your queries.

The canonical way to model your data in a relational database is to [normalize](https://en.wikipedia.org/wiki/Database_normalization) your entities. Normalization is a complex subject that we won't cover in depth here, but essentially you should avoid repeating any singular piece of data in a relational database. Rather, you should create a canonical record of the data and reference this canonical record whenever needed.

For example, a customer in an e-commerce application may make multiple orders over the course of the year. Rather than storing all customer information on the order record itself, the order record would contain a `CustomerId` property which would point to the canonical customer record. 
There are two benefits to this approach:

1. _Storage efficiency_: Because a single data record is 'write once, refer many', relational databases require less storage than options which duplicate data into multiple records.
2. _Data integrity_: It's easier to ensure data integrity across entities with a relational database. In our example above, if you duplicate the customer information into each order record, then you may need to update each order record when the customer changes some information about themselves. In a relational database, you only need to update the customer record. All records that refer to it will receive the updates.

However, normalization means that your data is scattered all over the place. Joins allow you to reassemble data from multiple different records in a single operation. They give you enormous flexibility in accessing your data. With the flexiblity of joins and the rest of the SQL grammar, you can basically reassemble any of your data as needed. Because of this flexiblity, you don't really need to think about how you'll access your data ahead of time.

Thus, to get rid of SQL joins, NoSQL needs to handle the three benefits of joins:

1. Flexible data access - First, NoSQL databases avoid the need for _flexibility_ in your data access by requiring you to do planning up front. How will you read your data? How will you write your data? When working with a NoSQL database, you need to consider these questions thoroughly before designing your data model.
2. Data integrity - The second tradeoff of NoSQL databases is that _data integrity is now an application-level concern_. While JOINs would allow you for a 'write once, refer many' pattern for referenced items, you may need to denormalize and duplicate data in your NoSQL database. For pieces of data that are unchanging -- birth dates, order dates, sensor readings -- this duplication is no problem. For data that does change, like display names or listed prices, you may find yourself updating multiple records in the event of a change.
3. Storage efficiency - Finally, NoSQL databases are less storage efficient than their relational counterparts, but it's mostly not a concern. When RDBMS were designed, storage was at more of a premium than compute. This is no longer the case -- storage prices have dropped to the floor while Moore's Law is slowing down. Compute is the most valuable resource in your systems, so it makes sense to optimize for compute over storage.

### Why NoSQL databases can scale horizontally
NoSQL databases require you to split up your data into smaller segments and perform all queries within one of these segments. This is common across all NoSQL databases. In DynamoDB and Cassandra, it's called a [partition key](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html#HowItWorks.CoreComponents.PrimaryKey). In MongoDB, it's called a [shard key](https://docs.mongodb.com/manual/core/sharding-shard-key/).

The easiest way to think of a NoSQL database is a [hash table](https://en.wikipedia.org/wiki/Hash_table) where the value of each key in the hash table is a [b-tree](https://en.wikipedia.org/wiki/B-tree). The partition key is the key in the hash table and allows you to spread your data across an unlimited number of nodes.

Let's see how this partition key works. Assume you have a data model that is centered around users and thus you use `UserId` as your partition key. When you write your data to the database, it will use this `UserId` value to determine which node it should use to store the primary copy of the data.
Assume you have a data model that is centered around users and thus you use `UserId` as your partition key. When you write your data to the database, it will use this `UserId` value to determine which node it should use to store the primary copy of the data.

![[Pasted image 20250324152643.png]]

When a new write comes with a `UserId` value of `741`, the DynamoDB Request Router will determine which node should handle the data. In this case, it is routed to Node 3 since it is responsible for all `UserIds` between 667 and 999. 


![[Pasted image 20250324152702.png]]

At read time, all queries must include the partition key. Just as with the write, this operation can be sent to the node that is responsible for that chunk of the data without bothering the other nodes in the cluster.

![[Pasted image 20250324152713.png]]



### How DynamoDB bounds your queries
DynamoDB imposes a 1MB limit on `Query` and `Scan`, the two 'fetch many' read operations in DynamoDB. If your operation has additional results after 1MB, DynamoDB will return a `LastEvaluatedKey` property that you can use to handle pagination on the client side.

This limit is the final requirement for DynamoDB to offer guarantees of single-digit millisecond latency on any query at any scale.

However, there are two situations where you could see performance degradation as your application scales. Those situations are:

- Pagination - what happens if your operation has more than 1MB of data? DynamoDB will return a `LastEvaluatedKey` property in your response. This property can be sent up with a follow-up request to continue paging through your query where you left off. This pagination can bite you as you scale. When your data is small or in testing, you might not need to page through results, or it might just be a single follow-up request to fetch the second page of results. As your data grows, you may find this access pattern taking longer and longer as multiple pages are needed.
- Hot keys - A hot key is an item collection that is accessed significantly more frequently than the other item collections in a table. For example, imagine Twitter. [Justin Bieber](https://twitter.com/justinbieber), with his >100 million followers, is likely to be accessed significantly more frequently than me, with my slightly smaller following. If this data was read directly from DynamoDB, the Beliebers might cause a hot key on Justin's profile.




Further Reads:
1. https://levelup.gitconnected.com/system-architecture-high-throughput-reads-writes-in-databases-p1-ac8e8916d06b
2. https://levelup.gitconnected.com/system-architecture-high-throughput-reads-writes-in-databases-p2-44f92c2f383d

