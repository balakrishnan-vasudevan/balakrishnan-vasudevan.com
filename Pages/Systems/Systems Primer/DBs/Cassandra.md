 - [The Beauty of Cassandra](https://medium.com/p/ebff58f37cbc)
- [Cassandra Internals — SSTables : The secret sauce that makes cassandra super fast](https://medium.com/p/3d5badac8eaf)
- [Cassandra- But why?: Benefits of a columnar DB](https://medium.com/p/f519fc5c9fa9)




Key Features: ● Wide column data store (NoSQL), has a shard key and a sort key ○ Allows for flexible schemas, ease of partitioning ● Multileader/Leaderless replication (configurable) ○ Super fast writes, albeit uses last write wins for conflict resolution ○ May clobber existing writes if they were not the winner of LWW ● Index based off of LSM tree and SSTables ○ Fast writes Conclusion: Great for applications with high write volume, consistency is not as important, all writes and reads go to the same shard (no transactions) ● See chat application for a good example of when to use