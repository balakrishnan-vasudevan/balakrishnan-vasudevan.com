#databases , #leader, #replication
![[Pasted image 20240507202705.png]]

But what happens when the unavailable node comes back online? It might start reading data and end up with stale information — the data it missed while it was down. To avoid this, the client sends read requests to multiple replicas and then chooses the node with the most recent response. This way, even if one node has stale data, the client can still get the most up-to-date information from the others.

**Read Repair**: Imagine a client requests data from several nodes. If it gets a stale response from, say, Replica 3, it can immediately write back the updated value to that replica. This method is effective for data that’s read frequently. For example, if a popular product’s price is updated, read repair ensures all replicas quickly reflect the new price.

1. **Anti-Entropy**: This is a more passive approach. Databases continuously run background processes to find discrepancies between replicas. They then sync the data, but not in any particular order. Unlike the replication log in leader-based systems, anti-entropy may result in significant delays before data is copied. For instance, if a rarely updated user profile is changed, it might take some time for all replicas to show the new information.

![](https://miro.medium.com/v2/resize:fit:1400/0*yHeorsXdTD1wHRjJ)

Image is from book [Designing Data-Intensive Applications](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/B08VL1BLHB/ref=sr_1_1?hvadid=557505114617&hvdev=c&hvlocphy=9009667&hvnetw=g&hvqmt=e&hvrand=15202424186466237583&hvtargid=kwd-831955295897&hydadcr=24391_13517605&keywords=design+data-intensive+application&qid=1705674093&sr=8-1)

The concept of quorums for reading and writing is fundamental in leaderless replication systems. Let’s delve into it with an example.

Imagine you have a distributed database with five replicas. In this system, to ensure consistency, you define quorums for both reading and writing operations. Let’s say you set a write quorum (W) of 3 and a read quorum (R) of 3. This means that for a write operation to be considered successful, at least 3 out of the 5 replicas must acknowledge the write. Similarly, for a read operation to be reliable, it must gather data from at least 3 replicas.

By setting the quorums this way, you strike a balance between availability and consistency. If W + R > N (the total number of replicas), the system guarantees strong consistency, meaning every read receives the most recent write. In our example, W (3) + R (3) is greater than N (5), thus ensuring strong consistency.

Let’s break down some edge cases where even W + R > N can result in stale data:

**Sloppy Quorum**: This occurs when the write quorum ends up on different nodes than the read quorum, resulting in no guaranteed overlap. Consequently, a read might not fetch the most recent write, leading to stale data.

**Concurrent Writes During Reads**: If a write happens concurrently with a read, the write may only be reflected on some replicas. This uncertainty makes it unclear whether the read is retrieving old or new data.

**Partial Write Success**: Imagine a scenario where a write is successful on some replicas but fails on others, and the overall operation is deemed successful on fewer than ‘W’ nodes without a rollback. In this case, a subsequent read may or may not report the value from that write, creating inconsistency.

**Node Failure and Data Recovery:** If a node carrying the new value fails and its data is recovered from a replica with the old value, the number of replicas storing the new value might fall below ‘W’. This break in the quorum condition can lead to stale reads.