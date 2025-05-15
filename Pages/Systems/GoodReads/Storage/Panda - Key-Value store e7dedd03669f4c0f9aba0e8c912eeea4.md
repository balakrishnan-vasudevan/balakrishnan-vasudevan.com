# Panda - Key-Value store

Tags: foundationdb, key-value
Category: Articles
Company: Dropbox
Status: Not started
URL: https://dropbox.tech/infrastructure/panda-metadata-stack-petabyte-scale-transactional-key-value-store

Dropbox operates two large-scale metadata storage systems powered by **sharded MySQL**. One is the **Filesystem** which contains metadata related to files and folders. The other is **Edgestore**, which powers all other internal and external Dropbox services. Both operate at a massive scale. 

Edgestore was originally built directly on sharded MySQL, with each of our storage servers holding multiple database shards. Data within Edgestore was evenly distributed, so that most of the disks reached capacity around the same time. When it came time to expand, we split each machine in two, with each holding half of the shards.

Our solution was to introduce a new layer to our metadata stack, a petabyte-scale transactional key-value store we call **Panda,** which sits between Edgestore and our sharded MySQL. Panda abstracts MySQL shards, supports ACID transactions, enables incremental capacity expansion, and unifies the implementations of complicated features used by multiple backends within Dropbox.

![Untitled](Untitled.png)

Advantages:

1. we can implement features in Panda independent of the underlying storage engine—such as data rebalancing and two-phase commit, neither of which are inherent to sharded MySQL
2. we can even migrate metadata back and forth between entirely different storage engine implementations if we choose.
3. Panda also enables us to reduce complexity in the application layer. For a number of historical reasons, Edgestore and the Filesystem have traditionally had separate backends. But with Panda we can eventually unify the two.

Options:

FoundationDB will not work - single instance is set to work with up to 500 storage processes. Edgestore and Filesystem clusters have more htan 10,000 cores each. There was a hard limit on the number of latest read requests FoundationDB could serve.

Vitess - Vitess does not support ACID cross-shard transactions. It has only implemented two-phase commit as an experimental feature. One of the fundamental [design choices](https://github.com/vitessio/vitess/blob/main/doc/Vision.md) in Vitess is that it embraces relaxed consistency. Stale reads make a lot of sense if you are building YouTube, but not if you are building a file system.

CockroachDB - One hard blocker was that CockroachDB does not support Dropbox's current replication model. Dropbox uses MySQL semi-sync replication to replicate between two regions located thousands of miles (or 80ms) apart. The asynchronous model allows us to serve reads and writes with single digit millisecond latency while being [resilient to natural disasters](https://dropbox.tech/infrastructure/disaster-readiness-test-failover-blackhole-sjc) that could wipe out a whole region. The downside is that in the case of an abrupt region outage, we will lose the writes that didn’t replicate to the other region. CockroachDB, on the other hand, uses a quorum replication model which can survive region outages without data loss—but with an inter-region latency cost of 80ms for all writes.