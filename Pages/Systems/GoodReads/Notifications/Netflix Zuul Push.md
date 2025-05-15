# Netflix Zuul Push

Tags: #notification-system
Category: Articles
Company: Netflix
Status: Complete
URL: https://youtube.com/watch?v=6w6E_B55p0E&si=SrZU1LjTIheKKNhd

Push - Persistent connection for the entirety of the connection

Server initiates data transfer

background push messages

Upstream uses HTTP - Zuul is for downstream

Similar to other notification systems - but works across multiple platforms (cross platforms)

Websockets or SSE is used

Push registry - which client is connected to which pull server (customer ID: Zuul push server IP address)

Push library - robust way to send messages - push messages to given client ID

Single async send message call

Push message queue - Decoupling senders and receivers, withstands wide variations in incoming messages

Message processor - ties all components together, performs push message delivery after performing lookup

![[Pasted image 20250301154617.png]]

De-duplication of messages handled at client end.

## Push Server:

10 million persistent connections at peak

Zuul Cloud GW - API GW - handles all API traffic that comes in

Non blocking async IO - Why? C10K challenge support 10K concurrent connections on single server - Zuul push has to support multiple connections

Traditional N/W programming - thread for every incoming connection and blocking IO on that thread. Doesn’t scale, server memory will get exhausted, server CPUs will be get exhausted, server CPUs will be overwhelmed due to constant context switches.

![[Pasted image 20250301154704.png]]

Async IO - uses OS multiplexing IO primitives like K queue or E Poll to register read/write call backs for all open connections on single thread. All invocations done on single thread. Tradeoff - Application becomes complicated, because code needs to keep track of all connections, can’t use thread stack - thread stack is used by all connections.

![[Pasted image 20250301154754.png]]

Netflix uses Netty for non-blocking I/O . Cassandra and Hadoop use it too.

![[Pasted image 20250301154738.png]]

Each client that connects to Zuul push server for first time must authenticate itself - authenticate by cookies, JWT.

## Push Registry:

Keeps mapping of push clients and servers.

Redis store used to serialize mapping.

Datastore has to have following characteristics:

1. Low read latency (read multiple times, write only once)
2. Record expiry support (per record) or TTL (to avoid phantom registration record)
3. Sharding for HA
4. Replication for fault tolerance

Redis/Cassandra/DynamoDB are choices

Netflix uses Dynomite (OS project) = Redis + Auto-sharding + Cross-region replication + RW quorums

## Message processing:

Does message writing, queueing and delivery

Kafka is used

Fire and forget approach - but some senders care about delivery, can be done using subscribing to push delivery status queue or read it off hive table in a batch mode (every push message logged)

Cross-region replication: Three regions

Kafka message cure is used to replicate messages in all three regions

Different queues for different priorities

Priority inversion - higher priority messages stuck behind lower priority messages in single queue

Multiple message processor instances run in parallel to scale throughput

Message processors use Mantis (Netflix’s own) - similar to Apache Flink - Uses Mesos container management system - faster spin-up - out of box for scaling number of message processors based on number of messages in message queue

## Operation:

Different than normal stateless REST services.

Long-lived stable connections - makes it stateful = great from client’s point of view - Terrible for quick deploy or rollback - thundering herd problem when switching servers

How they handle?

1. Tear down connections periodically. Single clients don’t stick to single servers.
2. Randomize each connection’s lifetime - dampens any thundering herd issue and recurring thundering herd
3. Ask client to close connection - TCP - any party that initiates closing should initiate TIME_WAIT state, on Linux this can can consume the connection file descriptor for about 2 minutes. Server ends up handling thousands of concurrent concurrent connections.

## How to optimize push server?

Most connections are idle - Don’t run service to be too hot or too cold. M4-large is used - 84K concurrent connections. One server going down won’t impact service.

Optimize for cost and not instance count. More number of small servers >> few big servers

Autoscaling number of push servers - Not RPS or CPU load (ineffective for push clusters - persistent connections, so no RPS, low CPU load) - Avg # of open connections is used as the metric for scaling

ELB cannot proxy websockets - ELBs don’t understand initial request the client makes (Websocket upgrade request, special HTTP request) - ELB handles it as any other HTTP request, after the message is sent, connection is taken down - persistent websocket connection is not possible.

Run ELB as a TCP Load Balancer (L4), ELB runs over L7 - TCP packets processed back and forth

ALB - support web-sockets

use webosocket aware load balancer.

## Other uses:

On-demand diagnostics (clients with issues)

Remote recovery (restart remotely)

User messaging