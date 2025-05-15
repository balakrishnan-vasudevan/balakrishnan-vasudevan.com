https://medium.com/@adamprout/categorizing-how-distributed-databases-utilize-consensus-algorithms-492c8ff9e916

I don’t know of standard/well-known names for the two HA approaches, so I’m going to refer to them as “==_Consensus for Metadata_====” (CfM) and “====_Consensus for Data_====” (CfD). As their names suggest, both designs use a consensus algorithm (Raft, Paxos, etc.) to handle failures and store data, but they differ in the type of data that is managed by consensus.==
# ==Consensus for Metadata (CfM)==

Figure 1 one shows the CfM architecture. ==This design is used by systems such as Apache Kafka, FoundationDB and SingleStoreDB/MemSQL among others. CfM stores high level metadata about the state of the cluster (i.e., which hosts are online vs offline, which shards are stored on which hosts, etc.) in a centralized set of coordinator nodes (in green on the diagram). The coordinator nodes themselves don’t typically store any of the user’s data (i.e., they don’t store shards), just metadata. The coordinators use a consensus algorithm to replicate metadata changes and keep metadata available to the cluster if coordinators node fail. The user data itself in CfM is replicated using primary — secondary replication algorithms specific to each database system (synchronous replication of a transaction log typically). These replication algorithms only worry about transmitting data, and not about what how to elect a new primary if a primary fails (the blue replication arrows in figure 1). When a data node becomes unhealthy the centralized coordinator is responsible for electing a new primary for this nodes shards from its replica’s(triggering a failover) and updating its cluster metadata appropriately. CfM separates replication of data from the algorithms used for election/failover. This involves a protocol between the data nodes and the coordinators so the coodinators know which replica’s are safe to failover to (have all committed data).==

![[Pasted image 20250501130455.png]]

# ==Consensus for Data (CfD)==

Figure 2 shows the high level architecture of CfD. ==It uses consensus replication to store user data and keep it available. The consensus algorithm running on the data nodes is responsible for electing a new primary for each shard if a data node dies. Google Spanner and modern MongoDB are the most popular examples of this design. CfD databases may or may not have a centralized coordinator nodes for other reasons (ie., running DDL operations like adding/removing nodes), but this coordinator won’t be responsible for acting on data node failures.==

![[Pasted image 20250501130507.png]]

Below is a non-exhaustive list of examples of each type of system (to the best of my knowledge).

==**Consensus for Data examples**====:==

- ==Spanner==
- ==MongoDB==
- ==DynamoDB==
- ==CosmosDB==
- ==CockroachDB==
- ==TiDB==
- ==Yugabyte==
- ==Redpanda==

==**Consensus for Metadata examples**====:==

- ==Apache Kafka==
- ==FoundationDB (and thus Snowflake which uses FoundationDB for metadata)==
- ==MemSQL/SingleStore==
- ==Clickhouse==
- ==ElasticSearch==
- ==Redshift==
- ==PlanetScale==
- CitusDB
- ==AWS Aurora==
- ==Azure SQL Hyperscale==
- ==Neon (for WAL writes) (*)==
- HDFS

As is common in software engineering, these designs come with different trade-offs. I haven’t seen the trade-offs written down in detail anywhere, so I’ll take a stab at writing them down here. Note that some of these are my opinion as someone who has spent >10 years building distributed databases and close to 20 years building databases in general. I try to back my opinions up with examples as much as possible, but others may disagree with some of my claims none the less.

(*) Neon uses [Paxos to replicate WAL,](https://neon.tech/blog/paxos) but Jeremy Schnedier pointed out on twitter that it doesn’t use Paxos for leader elections. I originally had them as CfD but moved them to CfM based on this observation from Jeremy. There is more o[f design spectrum here](https://transactional.blog/blog/2024-data-replication-design-spectrum#:~:text=Consistent%20replication%20algorithms%20can%20be%20placed%20on%20a,an%20appropriate%20replication%20algorithm%20for%20a%20use%20case.) as Alex Miller recently wrote about in depth, but for the purposes of this blog the centralized coordinator Neon uses (Kubernetes) to spin up a new leader makes it more CfM then CfD in my opinion.

==**Advantages of Consensus For Metadata**==

CfM needs to store fewer copies of user data to achieve a given level of durability compared to CfD. Consensus algorithms (typically) need a majority to elect a new leader (or to commit new data), which means to survive _f_ failures, you need _2f+1_ copies of the data (i.e., to survive 2 node failures, consensus algorithms need 5 copies of the data). With CfM to survive _f_ failures you only need _f + 1_ copies of the data (see next bullet point. CfM allows a lot of flexibility on the commit quorum used — some systems may use different quorums). This means CfM has almost 50% lower storage and network costs compared to CfD — it needs to store far fewer data copies. Said another way, this means CfM designs can tolerate more node failures while maintaining HA with a given number of copies of the data.

CfM is a more flexible design. This is a handwavy claim, so I’ll try to provide some high-level intuition about why CfM is more flexible as well as give a few examples from real CfM systems. Most of the extra flexibility with CfM comes from using “simpler” replication algorithms for primary data that can be customized more easily compared to modifying a consensus algorithm. Consensus algorithms are notoriously complex which makes it harder to safely add new features to them. Because CfD uses consensus to replicate data, it’s harder (or sometimes impossible) to build particular features into the replication protocol used for user data. On the other hand, CfM replication algorithms are only concerned with replicating data (not electing leaders/doing failovers) so are simpler. This may seem like a “fuzzy” claim, so here are a few example features from real CfM systems harder to do in CfD systems:

- Kafka (a CfM system) only replicates data to other hosts in memory. It doesn’t wait for data to be durable on disk to consider it replicated / committed (it doesn’t wait for an fsync()). This is a difficult feature to build into a consensus algorithm (i.e., its not possible with vanilla Raft or Paxos to the best of my knowledge). The CfM design is flexible enough to allow Kafka to build this feature that would be hard ([or maybe impossible](https://redpanda.com/blog/why-fsync-is-needed-for-data-safety-in-kafka-or-non-byzantine-protocols)) in a CfD design.
- CfM allows user data replication to use different quorum models. For example, PlanetScale uses MySQLs [semi-sync](https://planetscale.com/blog/mysql-replication-best-practices-and-considerations) replication. [AWS Aurora uses a (4/6 write, 3/6 read)](https://www.amazon.science/publications/amazon-aurora-on-avoiding-distributed-consensus-for-i-os-commits-and-membership-changes) quorum. SingleStoreDB allows customers to choose either s[ync or async](https://docs.singlestore.com/cloud/reference/sql-reference/data-definition-language-ddl/create-database/) replication models (sync is the default). This breadth of quorum models is likely not possible with CfD (potentially some of them are).
- CfM designs have more control over who is elected a leader after a failure event. i.e., if there are 2 replica’s, the CfM coordinator can choose which specific one to elect as leader potentially based on network topology (i.e., to keep the data in the same AZ as other shards/partitions). The same goes for adding a node back into the cluster when it recovers from failure. This “placement policy” is harder to build into a consensus algorithm directly. Most CfD systems allow consensus to elect a new leader then move the leader to a higher priority location there after as a 2nd phase.
- Once a failed host has been detected, its likely the CfM design can failover and get the cluster back online faster then CfD though I have no hard data to back this up. This is because CfM can failover all shards on a dead node in batch, whereas CfD needs a series of consensus elections to happen (one for each shard typically).
- CfM replication designs more easily support replicating data out of order to avoid head-of-line blocking. That is, a large transaction that is taking a while to commit blocking a quick/small transaction from committing at the same time because the small transaction was ordered after the large transaction in the log. Note the data still needs to be replayed in order on the replica’s, but it can be sent out of order over the wire. This is more difficult to do in consensus algorithms (again, it is not allowed in vanilla Raft).

**Advantages of Consensus For Data**

CfD is much better at dealing with slow networks or otherwise replica’s that are sometimes slow to acknowledge newly replicated data for other reasons. CfD only needs to wait for a majority of replica’s to ack a transaction to commit, so slower nodes will naturally not be part of the majority. On the other hand, CfM designs typically wait for all replicas to ack a transaction. Because of this, CfD is better for replication between regions (or between hosts that are far apart) or any place there is latency variation between hosts.

CfD is also better at dealing with replica failures (when the primary is still online). CfM typically needs the coordinator to mark a dead replica as offline before data can be committed, whereas CfD will have that dead replica outside of its majority and be allowed to commit (so may not even notice a dead replica directly). The precise trade-off depends on the quorum algorithm used by the CfM database. This can show up as higher p99 latency on writes in CfM designs when replica’s are failing. This is more so the case for “[gray failures](https://blog.acolyer.org/2017/06/15/gray-failure-the-achilles-heel-of-cloud-scale-systems/)” where a node is not completely offline, but very badly degrade. These failures are hard for the CfM coordinator to detect quickly. CfD will happily drop the “gray failed” nodes from its majority automatically — its not a special case.

CfD databases don’t need a special coordinator tier that is responsible for metadata storage and triggering failovers. All nodes in the cluster can be homogenous which makes clusters easier to deploy and operate. This potentially doesn’t matter as much in managed service environments, though it will still cost the managed service operator more money to run the coordinator nodes. That said, distributed databases often have coordinator nodes for other reasons anyways, so some CfD systems may not have this advantage (i.e, Yugabyte a CfD system has YB-Master coordinator).

Assuming you have a correct consensus algorithm, CfD is a simpler design. How the coordinator triggers failovers for CfM and how the data nodes run the failovers in the face of network partitions and other nodes failing or rejoining the cluster is not easy to develop/test. CfD hides this complexity inside the consensus algorithm which I suspect is easier to test and easier to prove correct as an independent module (with TLA+ or P).



I think centralized leader election and per shard leader election is a cleaner way to describe these. Metadata is just too commonly used and is now confusing.  
Having worked on both types of distributed databases (Azure SQL and YugabyteDB) I don't agree with most of these advantages for either cfM or cfD. It might work for other systems but not databases. Also there are ways to work around them all.  
Weirdly enough I don't have a strong preference to either of them. If I had to pick one for a new db then it boils down to one question. Do I already have a replication layer or should I build one? If you already have one then go for cfM else pick cfD. Neither is easy to implement and manage. This might explain why older dbs use cfM and newer ones are cfD.