Source: https://medium.com/nerd-for-tech/ever-wondered-how-the-unread-message-indicator-works-at-scale-of-millions-6ee319d26bb8

Let us say user A sent a message to user B, but user B is offline or did not view the message. Once userB comes back online, the user should be able to see 1 at the message indicator. One major thing to note here is that if user A sent 4–5 messages to user B, the value of the indicator should be 1 because it was sent by 1 unique user.

**Write Path: Mapping Users to Senders** To build this feature, we need to map each user to the IDs of users who have sent them messages. Here’s how we can implement it:

1. **User-Message Mapping:** We’ll store this mapping as a key-value pair in Redis. For example, for User B, the mapping might look like `userId: {A, C, D}`, where A, C, and D are users who have sent messages.
2. **Message Read Service:** Whenever a user sends a message, the messaging system triggers an event in Kafka/Kinesis. Our message read service consumes this event and updates Redis with the new sender’s ID.

![[Pasted image 20250303150956.png]]

**Read Path: Fetching Unread Senders** When User B comes back online, they should see how many unique users sent them messages while they were offline. The process works like this:

1. **Get Request:** User B’s app sends a GET request to the messaging service to retrieve the number of unique users who sent messages.
2. **Redis Lookup:** The messaging service checks Redis for User B’s sender mapping and returns the count to the user.

 ![[Pasted image 20250303151018.png]]

# Can we make this system better?

As we’ve seen, Redis plays a crucial role in both the write and read paths. However, Redis can become a bottleneck, especially in the write path. For example, if User A sends multiple messages to User B, the system needs to check Redis repeatedly to determine if User A is already in the set of unique users.

**Introducing Auxiliary Redis:** To optimize this, we can introduce an auxiliary Redis instance. The purpose of this auxiliary Redis is to store a temporary mapping of users who have already sent messages while the recipient was offline. This helps reduce the load on our main Redis instance.

**How It Works:**

- **Temporary Mapping:** Suppose User A sends a message to User B. In the auxiliary Redis, we store the key `A_B` with a value of `true`.
- **Event Handling:** When a message event from A to B is received, the system first checks the auxiliary Redis. If the key `A_B` exists, we skip updating the main Redis. Otherwise, we update it and add the key to the auxiliary Redis.

![[Pasted image 20250303151104.png]]