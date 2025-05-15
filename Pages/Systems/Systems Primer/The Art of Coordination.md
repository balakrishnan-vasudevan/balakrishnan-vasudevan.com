

Tags: #distributed-coordination
Category: Articles
Company: general
Status: Complete
URL: https://www.linkedin.com/pulse/art-coordination-consensus-state-distribution-data-1-granville/

### Leader-based Consensus:

The Leader based consensus pattern is used in distributed systems where one node is designated as the Leader, and the Leader must approve all changes to the system before they are committed. In this pattern, all other nodes in the system are followers, which synchronize their state with the Leader.

One example of a leader-based consensus system is the Apache ZooKeeper service, which is often used to manage configuration information and name services for distributed systems. In ZooKeeper, one node is designated as the Leader, and the Leader must approve all changes to the system before they are committed. Clients can connect to the ZooKeeper service and read or write data, but the Leader must approve all changes.

```
.            +--------+
             | Client |
             +--------+
                 |
                 |
              Connect
                 |
                 v
             +--------+
             | Server |
             +--------+
                 |
                 |
              Request
                 |
                 v
        +-------------------+
        | ZooKeeper Ensemble|
        +-------------------+
            /      |       \
     Leader    Follower   Follower
        |         |         |
     Propose   Sync      Sync
        |         |         |
        v         v         v
     +------+  +------+  +------+
     | Data |  | Data |  | Data |
     +------+  +------+  +------+
```

Another example of a system using leader-based consensus is the Redis distributed lock. Redis is an in-memory data store that can be used for caching and other types of data storage. The distributed lock feature of Redis allows clients to obtain a lock on a resource in a distributed system. The leader node manages the locks and ensures that only one client can get a lock.

The Leader based consensus pattern is commonly used in distributed systems because it provides a simple and efficient way to manage changes to the system. By designating one node as the Leader, developers can ensure that a single node approves all changes before committing, reducing the risk of conflicts or inconsistencies. However, the Leader based consensus pattern can be vulnerable to failures if the leader node fails or becomes unavailable.

In summary, the Leader based consensus pattern is a powerful tool for managing changes in distributed systems. By using the pattern within a distributed system, developers can ensure that a single node approves changes made to the system before committing, reducing the risk of conflicts or inconsistencies.

```
             +---------+
             |  Node   |
             | (Leader)|
             +---------+
            /   |    |   \
           /    |    |    \
          v     v     v     v
     +--------+ +--------+ +--------+
     |  Node  | |  Node  | |  Node  |
     |(Follow)| |(Follow)| |(Follow)|
     +--------+ +--------+ +--------++
```

### Majority Consensus:

The majority consensus pattern ensures that most nodes agree upon changes made to the system before they are committed. In this pattern, each node in the system can propose changes, and all nodes must vote on whether to accept or reject the proposed changes. Once a majority of nodes have agreed, the changes are committed.

One example of a majority consensus is the Paxos algorithm. The Paxos algorithm is commonly used in distributed databases to ensure that changes to the database are replicated across all nodes in the system. The Paxos algorithm has three types of nodes: proposers, acceptors, and learners. Proposers propose changes to the system, and acceptors vote on whether to accept or reject the proposals. Learners listen to the votes and commit the changes once most nodes agree.

```
                           +------——-+
                           | Proposer|
                           +------——-+
                                |
                                |
                     Prepare(n) |
                                |
                                v
             +--------+    +--------+   +--------+
             | Acceptor|    | Acceptor|   | Acceptor|
             +--------+    +--------+   +--------+
                |  |           |  |         |  |
      Promise(n)|  |           |  |         |  | Promise(n)
                |  +----------->|  |<--------+  |
                |              |  |            |
                | Promise(n)   |  | Promise(n)|
                |      |       |  |      |     |
                |      v       |  |      v     |
      +---------+  Accept!(value, n) +----------+
      |                    |                    |
      |                    v                    |
      |              +--------+                 |
      |              | Acceptor|                 |
      |              +--------+                 |
      |                 |  |                     |
      |   Accepted(n, value)|                     |
      |                 |  |                     |
      |                 v  |                     |
      |              +--------+                 |
      |              | Acceptor|                 |
      |              +--------+                 |
      |                    |                     |
      |   Accepted(n, value)|                     |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Acceptor|                 |
      |              +--------+                 |
      |                    |                     |
      |   Accepted(n, value)|                     |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Learner |                 |
      |              +--------+                 |
      |                    |                     |
      |              Learn(value)                |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Learner |                 |
      |              +--------+                 |
      |                    |                     |
      |              Learn(value)                |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Learner |                 |
      |              +--------+                 |
      |                    |                     |
      |              Learn(value)                |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Proposer|                 |
      |              +--------+                 |
      |                    |                     |
      |              Learn(value)                |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Learner |                 |
      |              +--------+                 |
      |                    |                     |
      |              Learn(value)                |
      |                    |                     |
      |                    v                     |
      |              +--------+                 |
      |              | Learner |                 |
      |              +--------+                 |
      |                                         |
      |             (Proposer learns)            |
      |                                         |
      |                                         |
      +-----------------------------------------+
```

Another example of a majority consensus is the Raft algorithm. The Raft algorithm is similar to the Paxos algorithm but is designed to be easier to understand and implement. The Raft algorithm has three nodes: leaders, followers, and candidates. Leaders propose changes to the system, and followers vote on whether to accept or reject the proposals. If a leader fails, a candidate is elected to replace the Leader.

```
 +----------
                          | Candidate|
                          +----------+
                                |
                VoteRequest(term, candidateId)
                                |
                                v
                       +-------------+
                       |   Follower  |
                       +-------------+
                                |
                 VoteResponse(term, voteGranted)
                                |
                                v
                          +--------+
                          |  Leader|
                          +--------+
                         /    |    \
       AppendEntries(term, prevLogIndex, prevLogTerm,
                      entries[], leaderCommit)
                          |     |
       +------------------+     +------------------+
       |                                            |
       v                                            v
 +-------------+                           +-------------+
 |   Follower  |                           |   Follower  |
 +-------------+                           +-------------+
       |                                            |
    AppendEntriesResponse(term, success)    AppendEntriesResponse(term, success)
       |                                            |
       v                                            v
```

The majority consensus pattern is commonly used in distributed systems because it provides a simple and effective way to ensure that most nodes agree upon changes made to the system. However, it can be vulnerable to failure if too many nodes fail or malicious nodes manipulate the voting process.

[[Pages/General/Readwise/Books/Paxos vs Raft]]
### Byzantine Fault Tolerance:

The Byzantine Fault Tolerance (BFT) algorithm is a consensus algorithm designed to tolerate failures of up to one-third of the nodes in a distributed system, including malicious nodes that may be actively trying to disrupt the consensus process.

In a BFT system, each node can propose changes to the system, and all nodes must vote on whether to accept or reject the proposed changes. The system is said to be "Byzantine fault tolerant" because it can continue to function correctly even if some of the nodes in the system are behaving maliciously or are otherwise unreliable.

To achieve Byzantine fault tolerance, the BFT algorithm uses cryptographic techniques to ensure the voting process is secure and malicious nodes cannot manipulate the results. The voting process typically involves a three-step process:

1. The proposer sends a proposal to all nodes in the system.
2. Each node votes on whether to accept or reject the proposal. Nodes send their votes to all other nodes in the system.
3. Once a node has received the most votes in favor of the proposal, it sends a message to all nodes in the system indicating that the proposal has been accepted. If a node receives messages indicating that most nodes have accepted the proposal, it accepts it.

If the system detects a node behaving maliciously or is unreliable, it can be replaced with a new node. The BFT algorithm also includes mechanisms for detecting and handling nodes behaving incorrectly or failing to respond.

One of the key advantages of the BFT algorithm is its ability to provide a high degree of fault tolerance even in the presence of malicious nodes or other types of failures. However, the BFT algorithm can be more complex and resource-intensive than other consensus algorithms and may only be suitable for some distributed systems.

In summary, the BFT algorithm is a consensus algorithm designed to tolerate failures of up to one-third of a distributed system's nodes, including malicious ones. It uses cryptographic techniques to ensure the voting process is secure and malicious nodes cannot manipulate the results. The BFT algorithm provides high fault tolerance but can be more complex and resource-intensive than other consensus algorithms.

```
 +--------+
                       |  Node  |
                       |        |
                       +--------+
                     /          \
         Vote: Accept (1)    Vote: Accept (2)
              /                \
             v                  v
        +--------+          +--------+
        |  Node  |          |  Node  |
        |        |          |        |
        +--------+          +--------+
           /   \              /   \
Vote: Accept (3) v    Vote: Reject (4) v
        +--------+          +--------+
        |  Node  |          |  Node  |
        |        |          |        |
        +--------+          +--------+
              \                /
               v              v
           +--------+    +--------+
           |  Node  |    |  Node  |
           |        |    |        |
           +--------+    +--------+
             |    |        |    |
             v    v        v    v
        +--------+    +--------+    +--------+
        |  Node  |    |  Node  |    |  Node  |
        |        |    |        |    |        |
        +--------+    +--------+    +--------+
           /   \        /   \        /   \
Vote: Accept (5) v  Vote: Accept (6) v Vote: Reject (7) v
        +--------+    +--------+    +--------+
        |  Node  |    |  Node  |    |  Node  |
        |        |    |        |    |        |
        +--------+    +--------+    +--------+
              \          /              /
               v        v              v
                       +--------+
                       |  Node  |
                       |        |
                       +--------+
```

## Distributing State in Distributed Systems

Distributing state ensures that all nodes in a distributed system have access to the same data. There are various approaches to distributing state, each with strengths and weaknesses. Here are some commonly used patterns for distributing state:

### Primary-Secondary Replication:

Primary-secondary replication is a type of data replication in distributed systems where one primary node is responsible for accepting updates, and multiple secondary nodes synchronize their state with the primary. In this pattern, all updates are made to the primary node, and the secondary nodes replicate those updates to ensure that they have the same data as the primary.

MongoDB and MySQL are two databases that use this pattern. Both databases have a primary node responsible for processing all updates and secondary nodes synchronizing their state with the primary. The key difference between the two is their communication protocols. MongoDB uses the replica set protocol to ensure that all nodes in the system are consistent. MySQL uses a protocol called binary log replication to ensure that all nodes in the system are consistent.

Primary-secondary replication is commonly used in distributed systems because it provides a simple and efficient way to manage data replication. By designating one node as the primary, developers can ensure that all updates are made to a single node before they are replicated, reducing the risk of conflicts or inconsistencies. Additionally, secondary nodes can provide fault tolerance by ensuring multiple copies of the data in case the primary node fails.

In summary, primary-secondary replication is a powerful tool for managing data replication in distributed systems. It can ensure that updates are made to a single primary node and that secondary nodes synchronize their state with the primary. This reduces the risk of conflicts or inconsistencies and provides fault tolerance if the primary node fails.

```
  .    +----------+
       |  Client  |
       +----------+
            |
            |
         Request
            |
            v
       +-----------+
       |  Primary  |
       +-----------+
            |
            |
         Update
            |
            v
       +-----------+
       | Secondary |
       +-----------+
            |
            |
       Synchronize
            |
            v
       +-----------+
       | Secondary |
       +-----------+
```

### Multi-Primary Replication:

Multi-primary replication is a type of data replication in distributed systems where multiple nodes are designated as primaries, and each primary node can accept updates. In this pattern, updates can be made to any primary node, and all other primary nodes synchronize their state with the updated node.

One example of where multi-primary replication is used is the Galera Cluster for MySQL. In Galera Cluster, there are multiple primary nodes, and each primary node can accept updates. Galera Cluster uses a protocol called Galera Replication to ensure that all nodes in the system are consistent.

Another example of where multi-primary replication is used is the Couchbase database. In Couchbase, there are multiple primary nodes, and each primary node can accept updates. Couchbase uses a protocol called Cross Data Center Replication (XDCR) to ensure that all nodes in the system are consistent.

Multi-primary replication is commonly used in distributed systems where there is a need for high availability and scalability. By allowing multiple nodes to accept updates, developers can ensure the system can handle a high traffic volume and provide fault tolerance in case a primary node fails.

In summary, multi-primary replication provides high availability, scalability, and fault tolerance, making it an excellent choice for applications with a high volume of traffic.

### Eventual Consistency:

Eventual consistency replication is a type of data replication in distributed systems where there is no requirement for all nodes to have consistent data at all times. Instead, updates are propagated asynchronously across the system, and it may take some time for all nodes to reach a consistent state. In this pattern, the system may be temporarily inconsistent but eventually converge to a consistent state.

One example of an eventual consistency replication pattern is using vector clocks. In a system that uses vector clocks, each node maintains a vector clock that tracks the version of the data on that node. When an update is made to the data on a node, the node increments its version of the vector clock and sends the updated vector clock along with the update to all other nodes in the system. Each node uses the vector clock to determine which updates it needs to apply and which updates it can discard.

```
 Node 1                      Node

      +---------+                 +---------+
      | Version |                 | Version |
      |   1     |                 |   1     |
      +---------+                 +---------+
           |                            |
           | Update A                  |
           v                            v
      +---------+                 +---------+
      | Version |                 | Version |
      |   2     |                 |   1     |
      |    A    |                 |         |
      +---------+                 +---------+
           |                            |
           | Update B                  |
           v                            v
      +---------+                 +---------+
      | Version |                 | Version |
      |   2     |                 |   2     |
      |    A    |                 |    B    |
      +---------+                 +---------+
```

Vector clocks are used in many distributed systems, including Riak, Cassandra, and DynamoDB.

Another example of an eventual consistency replication pattern is the use of Conflict-Free Replicated Data Types (CRDTs). CRDTs are a family of algorithms that enable eventual consistency in distributed systems. CRDTs can be implemented as either state-based or operation-based. In state-based replication, the entire data state is sent to all nodes in the system, ensuring that all nodes eventually converge to a consistent state. In operation-based replication, only the operations are sent to all nodes, and the nodes apply the operations locally to ensure convergence.

```
 Node 1                      Node

      +---------+                 +---------+
      | Version |                 | Version |
      |   1     |                 |   1     |
      |   {A}   |                 |         |
      +---------+                 +---------+
           |                            |
           | Update {B}                |
           v                            v
      +---------+                 +---------+
      | Version |                 | Version |
      |   2     |                 |   1     |
      | {A, B}  |                 |         |
      +---------+                 +---------+
                                    |
                                    | Update {C}
                                    v
                               +---------+
                               | Version |
                               |   2     |
                               | {A, B, C}|
                               +---------+
```

CRDTs are used in many distributed systems, including Riak, Cassandra, and Redis. CRDTs manage data types like sets, maps, and counters in these systems and ensure that all nodes eventually converge to a consistent state.

In practice, vector clocks and CRDTs can be used together to achieve strong consistency in a distributed system. Vector clocks can be used to maintain causal ordering of updates and detect conflicts, while CRDTs can merge concurrent updates without conflicts.

In summary, eventual consistency replication is a powerful tool for managing data replication in distributed systems. Using techniques and patterns like vector clocks and CRDTs, developers can ensure that all nodes eventually converge to a consistent state, even if updates are made concurrently. This provides high availability, scalability, and fault tolerance, making it an excellent choice for applications where temporary inconsistencies can be tolerated.