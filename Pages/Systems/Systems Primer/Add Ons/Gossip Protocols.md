The gossip protocol is a decentralized peer-to-peer communication technique to transmit messages in an enormous distributed system [1], [8]. The key concept of gossip protocol is that every node periodically sends out a message to a subset of other random nodes [8], [2]. The entire system will receive the particular message eventually with a high probability [11], [3]. In layman’s terms, the gossip protocol is a technique for nodes to build a global map through limited local interactions [1].
The following characteristics of the gossip protocol make it an optimal choice as the communication protocol in a large-scale distributed system [12]:

- limits the number of messages transmitted by each node
- limits the bandwidth consumption to prevent the degradation of application performance
- tolerates network and node failures

The gossip protocol can be used to keep nodes consistent only when the operations executed are commutative and serializability is not necessary. The **tombstone** is a special entry to invalidate the data entries that have a matching key without actual deletion of the data. The gossip protocol deletes the data from a node using a tombstone.

### **Anti-Entropy Gossip Protocol**

The anti-entropy algorithm was introduced to reduce the entropy between replicas of a stateful service such as the database. The replicated data is compared and the difference between replicas are patched [10]. The node with the newest message shares it with other nodes in every gossip round [8].

The anti-entropy model usually transfers the whole dataset resulting in unnecessary bandwidth usage. The techniques such as checksum, recent update list, and [Merkle tree](https://en.wikipedia.org/wiki/Merkle_tree?ref=highscalability.com) can be used to identify the differences between nodes to avoid transmission of the entire dataset and reduce network bandwidth usage. The anti-entropy gossip protocol will send an unbounded number of messages without termination [8].

### **Rumor-Mongering Gossip Protocol**

The rumor-mongering protocol is also known as the **dissemination protocol**. The rumor-mongering cycle occurs relatively more frequently than anti-entropy cycles and floods the network with the worst-case load [10]. The rumor-mongering model utilizes fewer resources such as network bandwidth as only the latest updates are transferred across nodes [8].

A message will be marked as removed after a few rounds of communication to limit the number of messages. There is usually a high probability that a message will reach all the nodes [8].

### **Aggregation Gossip Protocol**

The aggregation gossip protocol computes a system-wide aggregate by sampling information across every node and combining the values to generate a system-wide value [10].**Push Model**

The push model is efficient when there are only a few update messages due to the traffic overhead. The node with the latest message sends the message to a random subset of other nodes in the push model [8].

**Pull Model**

Every node will actively poll a random subset of nodes for any update messages in the pull model. This approach is efficient when there are many update messages because it is highly likely to find a node with the latest update message [8].

**Push-Pull Model**

The push-pull model is optimal to disseminate update messages quickly and reliably [2]. The node can push a new update message and the node can also poll for new update messages. The push approach is efficient during the initial phase when there are only a very few nodes with update messages. The pull approach is efficient during the final phase when there are numerous nodes with many update messages [8].

### Gossip Algorithm

The high-level overview of the gossip algorithm is the following [6], [1]:

1. every node maintains a list of the subset of nodes and their metadata
2. gossip to a random live peer node’s endpoint periodically
3. every node inspects the received gossip message to merge the highest version number to the local dataset

The heartbeat counter of a node is incremented whenever a particular node participates in the gossip exchange. The node is labeled healthy when the heartbeat counter keeps incrementing. On the other hand, the node is considered to be unhealthy when the heartbeat counter has not changed for an extended period due to a network partition or node failure [1]. The following are the different criteria for peer node selection in the gossip protocol [12]:

- utilize library offered by programming languages such as java.util.random
- interact with the least contacted node
- enforce [network-topology-aware](https://dl.acm.org/doi/10.1109/TPDS.2006.85?ref=highscalability.com) interaction### Gossip Protocol Use Cases

The gossip protocol is used in a multitude of applications where eventual consistency is favored. The popular applications of the gossip protocol are as follows [8], [5], [4], [7], [12]:

- database replication
- information dissemination
- maintaining cluster membership
- failure detection
- generate aggregations (calculate average, maximum, sum)
- generate [overlay networks](https://en.wikipedia.org/wiki/Overlay_network?ref=highscalability.com)
- leader election

The gossip protocol can be used to detect the failure of a node in a distributed system with high probability. The failure detection of nodes can save resources such as CPU, bandwidth, and queue space. In a distributed system, it is not sufficient to assert a node failure when a single client cannot interact with the particular node because there might be an occurrence of network partition or client failure [1]. It can be concluded with certainty the failure of a particular node when several nodes (**clients**) confirm the liveness of the particular node through gossip protocol [4], [11].

- [Apache Cassandra](https://cassandra.apache.org/_/index.html?ref=highscalability.com) employs the gossip protocol to maintain cluster membership, transfer node metadata (token assignment), repair unread data using Merkle trees, and node failure detection
- [Consul](https://www.consul.io/?ref=highscalability.com) utilizes the [swim-gossip](https://www.cs.cornell.edu/projects/Quicksilver/public_pdfs/SWIM.pdf?ref=highscalability.com) protocol variant for group membership, leader election, and failure detection of consul agents
- [CockroachDB](https://www.cockroachlabs.com/docs/stable/?ref=highscalability.com) operates the gossip protocol to propagate the node metadata
- [Hyperledger Fabric](https://hyperledger-fabric.readthedocs.io/en/release-2.2/gossip.html?ref=highscalability.com) blockchain uses the gossip protocol for group membership and ledger metadata transfer
- [Riak](https://riak.com/?ref=highscalability.com) utilizes the gossip protocol to transmit [consistent hash ring](https://systemdesign.one/consistent-hashing-explained/?ref=highscalability.com) state and node metadata around the cluster
- [Amazon S3](https://aws.amazon.com/s3/?ref=highscalability.com) uses the gossip protocol to spread server state across the system
- [Amazon Dynamo](https://aws.amazon.com/dynamodb/?ref=highscalability.com) employs the gossip protocol for failure detection, and keeping track of node membership
- [Redis](https://redis.io/?ref=highscalability.com) cluster uses the gossip protocol to propagate the node metadata
- Bitcoin uses the gossip protocol to spread the nonce value across the mining nodes



The disadvantages of the gossip protocol are the following [1], [5], [8], [2], [7]:

- eventual consistency
- unawareness of network partitions
- relatively high bandwidth consumption
- increased latency
- difficulty in debugging and testing
- membership protocol is not scalable
- prone to computational errors