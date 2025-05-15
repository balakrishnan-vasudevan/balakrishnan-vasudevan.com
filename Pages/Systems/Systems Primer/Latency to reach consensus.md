
> [!Question] what is the general total latency for paxos to reach a consensus of 1 value (not counting latency between different regions packet travel)? How is this different for raft and multi-paxos or other commonly used variants of paxos?

The general total latency for Paxos to reach consensus on a single value, assuming no packet travel latency between regions, is determined by the number of round trips (RTTs) required for the protocol’s phases to complete:
  

Latency for Paxos

1. Phases in Paxos:

• Phase 1 (Prepare/Promise):

• The leader (proposer) sends Prepare requests to a majority of acceptors.

• A majority of acceptors respond with Promise messages.

• Phase 2 (Accept/Accepted):

• The leader sends Accept requests to the majority of acceptors.

• A majority of acceptors respond with Accepted messages.

2. Total RTTs:

• 2 RTTs are required:

• 1 RTT for Prepare/Promise.

• 1 RTT for Accept/Accepted.

3. Additional Considerations:

• If a leader is already established and the protocol runs in a steady state (e.g., Multi-Paxos), Phase 1 can be skipped, reducing the latency to 1 RTT.

• In case of contention or leader election, additional time is needed to resolve conflicts, which increases latency.

  

  

  

Latency for Raft

1. Phases in Raft:

• Leader Election:

• If there’s no leader, a new leader must be elected. This process typically requires 1 RTT.

• Log Replication:

• Once a leader is established, the leader appends the log entry and replicates it to a majority of followers.

• Followers acknowledge the log entry.

• This takes 1 RTT.

2. Total RTTs:

• In steady state, Raft requires 1 RTT for log replication.

• If a leader election is needed, an additional 1 RTT is required.

  

  

  

Latency for Multi-Paxos

1. Optimization in Multi-Paxos:

• Multi-Paxos optimizes the consensus process by reusing an elected leader for multiple consecutive decisions.

• Phase 1 (Prepare/Promise) is only performed during the initial leader election.

• Phase 2 (Accept/Accepted) is used for each subsequent consensus decision.

2. Total RTTs:

• For steady-state operation, Multi-Paxos requires 1 RTT per value.

• If a leader election is needed, the additional overhead for Phase 1 (2 RTTs) applies.

  

  

  

Comparison of Latency

|   |   |   |
|---|---|---|
|Protocol|Leader Election RTTs|Steady-State RTTs (Per Value)|
|Paxos|N/A|2 RTTs|
|Multi-Paxos|2 RTTs|1 RTT|
|Raft|1 RTT|1 RTT|

  

  

  

  

Key Differences

1. Leader Election:

• Raft elects a leader in 1 RTT, while Paxos (or Multi-Paxos) requires 2 RTTs for a new leader to prepare and take control.

2. Steady-State Efficiency:

• Multi-Paxos and Raft are optimized for steady-state operations, requiring only 1 RTT per value.

• Basic Paxos always requires 2 RTTs for every value, making it less efficient in steady state.

3. Complexity:

• Raft is often considered simpler and easier to implement compared to Paxos and its variants.

4. Suitability for Real-World Use:

• Multi-Paxos and Raft are widely adopted in distributed systems due to their efficiency in steady-state operation and ability to handle leader-based optimizations effectively.

  

By reducing the number of RTTs in steady-state operation, Raft and Multi-Paxos offer significant latency advantages over basic Paxos in practical distributed systems.