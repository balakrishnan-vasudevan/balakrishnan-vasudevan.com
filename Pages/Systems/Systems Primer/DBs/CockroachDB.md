--- 
annotation-target: https://dl.acm.org/doi/pdf/10.1145/3318464.3386134
---


- Link to paper: https://dl.acm.org/doi/pdf/10.1145/3318464.3386134

- To serve their global user base, organizations are replacing their legacy DBMSs with cloud-based systems capable of scaling OLTP workloads to millions of users CockroachDB is resilient to disasters through replication and automatic recovery mechanisms.
- Use Case:
	- Consider, for example, a large company with a core user
	  base in Europe and Australia and a fast growing user base
	  in the US. To power its global platform while reducing operational costs, the company has made the strategic decision
	  to migrate to a cloud-based database management system
	  (DBMS). It has the following requirements: to comply with
	  the EU’s General Data Protection Regulation (GDPR), personal data for its European users must be domiciled within
	  the EU. **To avoid high latencies due to cross-continental communication, data should reside close to the users accessing it
	  most frequently, and follow them (within regulatory limits)
	  if they travel. Users expect an łalways onž experience, so the
	  DBMS must be fault tolerant, even surviving a full regional
	  failure. Finally, to avoid data anomalies and to simplify application development, the DBMS must support SQL with
	  serializable transactions.**
- (1) Fault tolerance and high availability To provide fault
  tolerance, CRDB maintains at least three replicas of every
  partition in the database across diverse geographic zones.
  It maintains high availability through automatic recovery
  mechanisms whenever a node fails.
  (2) Geo-distributed partitioning and replica placement
  CRDB is horizontally scalable, automatically increasing
  capacity and migrating data as nodes are added. By default it uses a set of heuristics for data placement , but it also allows users to control, at a fine
  granularity, how data is partitioned across nodes and
  where replicas should be located.
  (3) High-performance transactions CRDB’s novel transaction protocol supports performant geo-distributed transactions that can span multiple partitions. It provides serializable isolation using no specialized hardware; a standard clock synchronization mechanism such as NTP is
  sufficient. As a result, CRDB can be run on off-the-shelf
  servers, including those of public and private clouds.
- CRDB uses a standard shared-nothing [62] architecture,
  in which all nodes are used for both data storage and computation. A CRDB cluster consists of an arbitrary number
  of nodes, which may be colocated in the same datacenter or
  spread across the globe. Clients can connect to any node in
  the cluster
- Within a single node, CRDB has a layered architecture.
- 2.1.1 SQL. At the highest level is the SQL layer, which is
  the interface for all user interactions with the database. It
  includes the parser, optimizer, and the SQL execution engine,
  which convert high-level SQL statements to low-level read
  and write requests to the underlying key-value (KV) store.
  In general, the SQL layer is not aware of how data is
  partitioned or distributed, because the layers below present
  the abstraction of a single, monolithic KV store. Section 5 will
  describe how certain queries break this abstraction, however,
  for more efficient distributed SQL computation.
  2.1.2 Transactional KV. Requests from the SQL layer are
  passed to the Transactional KV layer that ensures atomicity of changes spanning multiple KV pairs. It is also largely
  responsible for CRDB’s isolation guarantees.
  2.1.3 Distribution. This layer presents the abstraction of
  a monolithic logical key space ordered by key. All data is
  addressable within this key space, whether it be system data
  (used for internal data structures and metadata) or user data
  (SQL tables and indexes).
  CRDB uses range-partitioning on the keys to divide the
  data into contiguous ordered chunks of size ~64 MiB, that
  are stored across the cluster. We call these chunks Ranges