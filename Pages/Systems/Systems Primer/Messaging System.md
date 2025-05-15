**Functional requirements:**

1. One-one chat system.
2. System should support persistent storage of chat history.
3. Online/offline status should be seen.
4. Should support multiple device.

Non-functional requirements

1. User should have real time chatting experience with minimum latency.
2. Our system should have a very high consistency. He should see the same message in all the devices.

Extended requirements

1. The application should support small group chat of 100 people.
2. Push notifications.

**2. Back of the envelope estimations**

DAUs = 500M, if each of these send 40 messages/day, total messages = 20B messages/day.

Storage estimation: Let the message size = 100bytes, 100B x 20B = 2TB/day

To store for 5 years, 2TB x 365 x 5=3650 ~ 3.5PB

Bandwidth estimation: 2TB / 100K sec = 20 Mbps. We need this for both upload and download.

**3. Communication protocols**

For web based communication, HTTP/HTTPS suits well. It is highly compatible with web browsers and web servers, provides encryption using SSL/TLS, easy implementation. We ==need to use keep-alive to keep persistent connection. It is a one way and very good choice for sender side. Since HTTP is client initiated, it is not a good idea for the server to use to send messages. We can consider server initiated protocols like polling, long-polling and web sockets, also these two give real-time communication unlike HTTP which adds latency. In polling client keeps asking the server if he has any messages.== Most of the time it will be an empty response, incurs to increased cost. In case of Long polling, client can hold the connection open until he has some messages available or timeout is reached. Once the message is received, it will immediately send the next request. Drawback is the sender and receiver cannot connect to the same server. Even for inactive users, it has to make periodic connection after time out.

Web socket — Communication is bidirectional means unlike HTTP, which follows a request-response model where clients initiate requests and servers respond, WebSockets allow for full-duplex communication. This means both the client and server can send messages to each other asynchronously, enabling real-time interaction without the overhead of repeated HTTP requests and it maintains persistent connection, server can send updates to a client. Since it is bidirectional, it suits both sending and receiving. Push notifications, webSockets enable servers to push updates to clients in real-time, eliminating the need for clients to constantly poll or long-poll the server for new data. This allows for instant delivery of messages, notifications, and updates to connected clients, improving the overall user experience.

However, for accessing historical messages, a traditional HTTP API (such as REST or SOAP) equipped with pagination mechanisms proves to be efficient in retrieving past conversations.

**4. DB Schema**

Message apps generate high volume of traffic, we have low read and write ratio of 1:1. In real time conversation, it also is very rare that user goes back and read same messages again and again.

The app has diverse features, giving the chance to employ hybrid database solution. For user profile information, relational database is a good choice, since they offer ACID (Atomicity, Consistency, Isolation, Durability) transactions and support for complex queries. Relational databases offer strong consistency guarantees, which are important for maintaining user data integrity. They also provide features for enforcing data constraints, such as unique constraints for usernames or email addresses. For messages, it demands for fast read and write on a high volume data, NoSQL database like key-value store would be a good choice.

Why Key-value store? _Key-Value Stores_ are designed for handling large volumes of data with high write throughput, are scalable and distributed, making them suitable for applications with high scalability requirements.

Possible options: Cassandra, HBase, DynamoDB

Cassandra is a wide-column database, whose base architecture is key-value storage model. It stores data in wide rows, organized into columns and each record is identified by a unique key, and the associated data is stored against that key. Hence by using this, we can take both the advantages. Also, we know that Cassandra is known for its high availability and partition tolerance, it also offers tunable consistency. We can configure different consistency levels for read and write operation. We can employ QORUM/ALL consensus to attain this. With higher consistency levels, Cassandra ensures that data is replicated to a majority of replica nodes before acknowledging a write operation, and it waits for a majority of replica nodes to respond before returning query results. This provides stronger consistency at the expense of potential increased latency and reduced availability during network partitions.

Why not HBase? Pros: Strong consistency, horizontally scalable, fault tolerant, high performance for read and write. Cons: Demands for Hadoop eco system knowledge for deployment, configuration and maintenance, does not match the low-latency capabilities for real-time messaging scenarios where sub-second latency is critical.

Stateless: All req-response services are stateless services like login, signup, user profile, service discovery.

Stateful: Chat service is the only stateful service we have. It is stateful because it has to maintain a persistent network connection. The web socket connection remains the same even in case the client is offline unless there is a network disruption. Service discovery helps finding the right chat service.

Third-party: ==Notification service to inform client if there is any new message while he is away.==

**6. Design deep dive**

1. **Service discovery**: The main job of the service discovery is to suggest the best chat server to connect based on the server load, geographical location, server capacity etc. Apache Zookeeper could be used for this. It maintains all the available chat servers and picks the right one.
2. **Message flow:**

**a. 1–1 message flow**

1. The User A establishes a persistent connection with the chat server and send the message.
2. The message undergoes validation and obtains ID from the ID generator.
3. The message is then written to K-V data store and also MQ of the recipient and sends the sender that the message as received.
4. If User B is online, the message is forwarded to Chat server 2 where User B is connected. If User B is offline, a push notification is sent from push notification (PN) servers for a best-effort delivery (no guarantee of delivery, since the user might not have an internet connection).
5. Even with the duo message delivery system, it is possible that a message is never received by the client. Therefore, it is critical that all clients request the Gateway Service for the authoritative chat history upon reconnection/with fixed intervals.

**b. Group chat**

The steps are same as 1–1 chat, if it is a small group, when the sender sends the message, it will be written to all the recipients queue of the group. If it is a large group, the message is published only once to the group queue and all the members of the group would have subscribed to the queue and pulls the message. This also mitigates the redundancy of storing the same message in multiple places.

**Message synchronization:**

In case of multiple devices support, to solve the ordering issue, we can annotate every message with a _prevMsgID_ field. The recipient checks his local log and initiates history catch-ups when an inconsistency is found.

**Online Presence:**

These are responsible for managing online status and communicating with the client using web socket connection. When the web socket connection establishes between the client and the chat server, the user status is turned online with the login time. when the user logout, it is changed to offline. Whenever there is disconnection in the server as well we need to update the status, but sometimes the user would not be offline and there is just a minute disruption, changing the status for this would result in poor user experience. Thus we need to have **heartbeat** mechanism to address this, Say the client sends a heartbeat event to the server every 5 seconds. After sending 3 heartbeat events, the client is disconnected and does not reconnect within x = 30 seconds (This number is arbitrarily chosen to demonstrate the logic). The online status is changed to offline.

**7. Optimizations:**

1. Employ push and pull models for messages in group chats.
2. Introduce parallelism: Build a loosely coupled systems by introducing message queues between chat servers.

**8. Fault Tolerance**: Replicating data across multiple nodes and multiple data centers to ensures redundancy and fault tolerance. Use consistant hashing for mitigate hotkey problem. Introduce load balancing so that traffic can be evenly routed without causing bottleneck to servers causing them to fail. Introduce redundancy and failover by configuring automated failover mechanisms to detect failures and switch to standby components seamlessly. Graceful degradation can also help during failures by rendering limited data from cache until the server comes up instead of completely halting service. Implement circuit breakers to detect and handle failures in external dependencies, such as downstream services or APIs. Circuit breakers monitor the health of external services and temporarily halt requests if they detect failures. This prevents cascading failures and allows the system to recover gracefully. Implement robust monitoring and alerting systems to detect anomalies, performance issues, and failures in real-time. Implement automated recovery mechanisms to restore service and recover from failures quickly. Use automated scripts or orchestration tools to restart failed components, reconfigure load balancers, and perform failover procedures automatically.

**9. Performance**

1. Cache data as much as possible.
2. Asynchronous Processing: Use message queuing systems like RabbitMQ or Apache Kafka to decouple components and enable asynchronous processing. Use pub/sub mechanisms to notify subscribers of new events or changes in data.
3. Optimized API Design: Implement pagination, filtering, and sorting mechanisms to limit the amount of data returned in each API response and improve query performance.

**10. Scalability:** We use horizontal scaling to scale servers.

**11.** **CAP theorem:** Based on the requirements, I am choosing consistency and network partition over availability.


![[Pasted image 20250429204612.png]]


[[Unread message indicator]]
[[LinkedIn messaging]]
[[LinkedIn Messaging extensibility]]
[[Slack Real Time messaging]]
