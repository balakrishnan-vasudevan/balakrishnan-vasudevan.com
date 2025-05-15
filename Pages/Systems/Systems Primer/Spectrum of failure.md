## Fail-stop Failures
collapsed:: true
	- a system component fails by stopping entirely, and its failure is immediately visible to the rest of the system. The failed component no longer sends or receives any messages, and other components can detect this state, often via timeout mechanisms.
	  **Characteristics:**
		- The component halts and is easily detectable.
		- No partial failures or erratic behavior.
		- Ideal for designing systems where failover mechanisms are in place.
	- Imagine a cloud service node that experiences hardware failure. In a fail-stop scenario, the node simply stops functioning and other nodes in the system quickly realize that it's gone. They can then reassign workloads or trigger recovery mechanisms.
	- The easiest way to deal with fail-stop failures is to implement health checks and timeouts. Systems such as ***Apache Kafka*** and ***Kubernetes*** use ***leader election*** mechanisms to redistribute responsibilities when a node fails to respond within a set timeframe.
## Crash Failures
  collapsed:: true
	- Here, the component fails and stops functioning, but its failure may not be immediately obvious to the rest of the system.
	- **Characteristics:**
		- The component crashes silently without immediately alerting the system.
		- Detection might involve waiting for timeouts or errors in communication.
		- The system might mistakenly continue interacting with the failed component, causing delays.
	- In a distributed database, a replica node might*** crash without the leader realizing immediately.*** The leader may continue sending queries to the replica, unaware that it has already stopped processing.
	- To mitigate crash failures, ***redundancy is crucial***. ***Data replication***, ***failover protocols***, and consistent monitoring can help detect failures early and reduce the impact.
	- For example, Apache Cassandra uses quorum-based reads and writes to maintain availability in the presence of crash failures.
## Omission Failures
  collapsed:: true
	- Omission failures occur when a component in a distributed system fails to send or receive messages. This can be due to hardware malfunctions, software bugs, or network congestion. Omission failures are divided into:
	  collapsed:: true
		- **Send omission failures**: A component fails to send a message.
		- **Receive omission failures**: A component fails to receive a message.
	- **Characteristics:**
	  collapsed:: true
		- The system continues operating, but messages are lost or not delivered.
		- Can result in degraded performance or stale data.
		- Difficult to detect, as the component itself appears to be working.
	- In a microservices architecture, a service may fail to send logs to a centralized logging service. The service might still be operational, but the lack of logs leads to difficulties in debugging issues.
	- ***Retry mechanisms***, ***message acknowledgments***, and monitoring network health are common strategies. ***Message brokers like RabbitMQ or Kafka can buffer messages and retry failed deliveries to address omissions (deda-letter queues).***
## Temporal Failures
  collapsed:: true
	- Temporal failures occur when a system component delivers messages outside the expected timeframe, leading to performance degradation or incorrect ordering of operations.
	- **Characteristics:**
		- Components send or receive messages too late or too early.
		- Can lead to data inconsistency, race conditions, or synchronization issues.
		- Latency-sensitive applications are particularly vulnerable to temporal failures.
	- Consider a stock trading platform where buy/sell requests must be processed in real-time. If a network partition causes one component to delay its processing, it might lead to transactions being executed in the wrong order.
	- Mechanisms like ***logical clocks***, ***vector clocks***, or ***consensus*** algorithms (will be covered in an upcoming articles) **such as Paxos and Raft address temporal failures. Distributed systems often use timestamps to ensure correct operation despite delays.**
## Byzantine Failures
  collapsed:: true
	- Byzantine failures represent the most challenging and severe type of failure. In this model, a component behaves unpredictably or maliciously, sending conflicting or incorrect data to different parts of the system.
	- **Characteristics:**
		- A component may act inconsistently or maliciously.
		- The failure is unpredictable and can involve corrupted or falsified messages.
		- Handling Byzantine failures requires detecting and mitigating conflicting states.
	- A distributed voting system might experience Byzantine failures where a malicious node submits different voting results to different replicas, leading to an incorrect final tally.
	- ***Byzantine Fault Tolerance (BFT) algorithms***, like P***ractical Byzantine Fault Tolerance (PBFT)***, use majority consensus to filter out malicious components. Blockchain systems like Bitcoin and Ethereum use BFT-inspired techniques for transaction security.
## Network Partitions
  collapsed:: true
	- Network partitions occur when communication between components is interrupted, but each component continues to operate independently. Partitions can result in split-brain scenarios with conflicting decisions across partitions.
	- **Characteristics:**
		- Components operate independently, causing state divergence.
		- Recovery is complex, especially if significant divergence occurs.
	- In a cloud-based file storage system, a network partition might isolate two data centers. Both allow clients to modify files, creating conflicting versions upon partition recovery.
	- Systems like Cassandra and DynamoDB allow writes in multiple locations and resolve conflicts using quorum-based reads/writes or timestamps.
## Arbitrary Failures
  collapsed:: true
	- Arbitrary failures are unpredictable and can result from hardware issues, memory corruption, or software bugs. These failures don’t follow a standard pattern, making them hard to diagnose.
	- **Characteristics:**
		- Erratic behavior that is difficult to reproduce.
		- Can result in data loss or corruption.
	- A distributed database might encounter memory corruption, causing random data loss across nodes. Diagnosing such failures can be time-consuming.
	- Comprehensive testing, redundancy, and failover mechanisms mitigate these failures. Regular health audits and data integrity checks help identify them early.