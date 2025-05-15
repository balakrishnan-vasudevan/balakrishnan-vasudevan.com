- Tags: redis
  Category: Articles
  Company: general
  Status: Not started
  
  [https://medium.com/@joudwawad/redis-pub-sub-in-depth-d2c6f4334826](https://medium.com/@joudwawad/redis-pub-sub-in-depth-d2c6f4334826)
  
  Redis Pub/Sub
  
  ![https://miro.medium.com/v2/resize:fit:1388/format:webp/1*AqalcHhpwLTBJAD9xYnMhQ.png](https://miro.medium.com/v2/resize:fit:1388/format:webp/1*AqalcHhpwLTBJAD9xYnMhQ.png)
- # Redis Pub/Sub In-Depth
- Pub/Sub (short for publish/subscribe) is a messaging technology that facilitates communication between different components in a distributed system. This communication model differs from traditional point-to-point messaging, in which one application sends a message directly to another. Instead, it is an asynchronous and scalable messaging service that separates the services responsible for producing messages from those responsible for processing them.
  
  In this blog post, we delve into the concept of Pub/Sub (Publish/Subscribe) and explore how Redis, a prominent provider, has implemented this communication model. We will examine the intricacies of Redis’s approach, focusing on the implementation details down to the memory block level. This analysis aims to provide a comprehensive understanding of Pub/Sub mechanisms and their practical applications using Redis.
- # Pub/Sub 101
  
  Pub/Sub is a messaging model that allows different components in a distributed system to communicate with one another. Publishers send messages to a topic, and subscribers receive messages from that topic, allowing publishers to send messages to subscribers while remaining anonymous, though they can be identified by subscribers if they include identifying information in the message payload. The Pub/Sub system ensures that the message reaches all subscribers who are interested in the topic. If configured appropriately, it is a highly scalable and dependable messaging system that can handle large amounts of data. In addition, Pub/Sub allows services to communicate asynchronously with latencies of 1 millisecond with ***appropriate message size, network conditions, and subscriber processing time***, making it highly desirable for fast and modern distributed applications.
- ## Pub/Sub Models
  
  Pub/Sub is fundamentally a simple communication model where a [broker](https://redis.io/solutions/messaging/) receives messages from a publisher and distributes them to one or more subscribers. The messages are then delivered to the subscribers, who interpret them according to the needs of their particular use cases.
  
  They are usually classified under four models based on the number of publishers and subscribers involved in the communication, which include ***one-to-one, one-to-many, many-to-one, and many-to-many***.
  
  Pub/Sub Model Dimensions
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9KYjJF7Gp4kfOf9NVA6Gzg.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9KYjJF7Gp4kfOf9NVA6Gzg.png)
- ## Pub/Sub core concepts
  
  Before we dive into the details of Pub/Sub and integration we need to understand a few concepts related to Pub/Sub, The Pub/Sub system consists of several components; some of the main components are described in the table below:
  
  Pub/Sub System Components
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Db1PFt2HfDnDFswk23gALA.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Db1PFt2HfDnDFswk23gALA.png)
- # Redis Pub/Sub
  
  Now after we have learned some high-level components of the Pub/Sub model and how they work we need to dive into the Redis implementation of this Pub/Sub to understand how the system communicates when the publisher publishes a message and ends on the consumer level.
  
  Redis implements the Pub/Sub pattern by providing a simple and efficient messaging system between clients. In Redis, clients can “publish” messages to a named channel, and other clients can “subscribe” to that channel to receive the messages.
  
  When a client publishes a message to a channel, Redis delivers that message to all clients that are subscribed to that channel. This allows for real-time communication and the exchange of information between separate components of an application.
  
  Redis Pub/Sub provides a lightweight, fast, and scalable messaging solution that can be used for various use cases, such as implementing real-time notifications, sending messages between microservices, or communicating between different parts of a single application.
- ## Synchronous Communication
  
  Redis Pub/Sub is synchronous. ***Subscribers and publishers must be connected at the same time in order for the message to be delivered***.
  
  Think of it as a radio station. You are able to listen to a station while you’re tuned into it. However, you’re incapable of listening to any message broadcast while your radio was off. Redis Pub/Sub will only deliver messages to connected subscribers.
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tu-eoGkESFysvgZ0Kve4Kw.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tu-eoGkESFysvgZ0Kve4Kw.png)
  
  This means that if one subscriber loses connection and this connection is restored later on, it won’t receive any missed messages or be notified about them. Therefore, it limits use cases to those that can tolerate potential message loss.
- ## Fire & Forget
  
  Fire & Forget is a messaging pattern where the sender sends a message without expecting an explicit ***acknowledgment*** from the receiver that the message was received. The sender simply sends the message and moves on to the next task, regardless of whether or not the message was actually received by the receiver.
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*fXg9ERWEyi5KIQPkOo_cIQ.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*fXg9ERWEyi5KIQPkOo_cIQ.png)
  
  Redis Pub/Sub is considered a “Fire & Forget” messaging system because it does not provide an explicit acknowledgment mechanism for confirming that a message was received by the receiver. Instead, messages are broadcast to all active subscribers, and it is the responsibility of the subscribers to receive and process the messages.
- ## Fan-out Only
  
  Redis Pub/Sub is fan-out only, meaning that when a publisher sends a message, it is broadcast to all active subscribers. All subscribers receive a copy of the message, regardless of whether they are specifically interested in the message or not.
- # Redis Pub/Sub under the hood
  
  Redis is best known as a key-value server. when a client connects to a redis-server it initializes a TCP connection to the server, and starts sending commands to it.
  
  Basic Redis Client Communication
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MRlQcEJRVpA5nkWiBnWg-Q.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MRlQcEJRVpA5nkWiBnWg-Q.png)
  
  But Redis is also a messaging server! A client interested in “topicA” can open a TCP connection to the Redis server, send “SUBSCRIBE TopicA”, then wait for topicA-related news. A news outlet can then connect to the Redis server, send “PUBLISH topicA message-data”, and the subscribing client will be notified of this lucrative offer:
  
  Basic Publish, Subscribe Model
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Hi-3hSgrtNjZDaQW8sKGXw.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Hi-3hSgrtNjZDaQW8sKGXw.png)
  
  zooming into what is happening at the redis we can imagine the Redis process keeping track of each socket’s subscription set:
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vuH0xTu86JUFjZSAA87hwA.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*vuH0xTu86JUFjZSAA87hwA.png)
  
  Let us now look more in-depth into how Redis looks like
  
  The original Pub/Sub implementation lets clients send three new kinds of commands: `PUBLISH`, `SUBSCRIBE`, and `UNSUBSCRIBE`. To track subscriptions, Redis uses a global variable `pubsub_channels` that maps channel names to sets of subscribed client objects. A client object represents a TCP-connected client by tracking that connection’s file descriptor.
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*YXslSexL20wFrQEFGjRg2w.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*YXslSexL20wFrQEFGjRg2w.png)
  
  When a client sends a `SUBSCRIBE` command, its client object gets added to the set of clients for that channel name.
  
  To `PUBLISH`, Redis looks up the subscribers in the `pubsub_channels` map, and for each client, it schedules a job to send the published message to the client’s socket.
- ## Handling disconnections
  
  Client connections can drop. Perhaps the client closed the connection, or a network cable was pulled. When this happens, Redis must clean up the client’s subscriptions. Let’s say Client A disconnects. To remove the client from the `pubsub_channels` structure, Redis would have to visit every channel (“topicA” and “topicB”) and remove the client from each channel’s subscription set.
  
  But visiting every channel is ***inefficient***: Redis should only need to visit the “topicA” channel because that is the only one that Client A is subscribed to. To enable this, Redis annotates each client with its set of subscribed channels, and keeps this in sync with the main `pubsub_channels` structure. With this, instead of iterating over *every* channel, Redis only needs to visit the channels which it knows the client was subscribed to. Let’s draw these sets as green circles:
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-M3qjF8t4GDufWOyR_3Aag.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*-M3qjF8t4GDufWOyR_3Aag.png)
- ## Getting concrete
  
  I’ve described the data structures as “maps” and “sets”: the global `pubsub_channels` variable is *logically* a `Map<ChannelName, Set<Client>>`, and each client’s subscription set is a `Set<ChannelName>`. But these are *abstract* data structures; they do not say how we represent them in memory. Let’s start zooming in to allocated memory blocks.
  
  The `pubsub_channels` map is actually a hash table. The channel name is hashed to a position in a `2^n-sized` array, like this:
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cbgdZzP899DFFuQoBvSwHA.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cbgdZzP899DFFuQoBvSwHA.png)
  
  The `pubsub_channels` array, with buckets from `0` to `7`, is a single allocated block of memory. To publish to a channel, we hash the channel’s name to find its bucket, then iterate over that channel’s set of clients. But different channel names can hash to the same bucket. Redis handles these collisions by “hash chaining”, which means each bucket points to a linked list of channels.
  
  In the example, both channels hashed to bucket `2`. But anything could happen, because Redis picks a random seed for its hash function at start-up, to protect you against collision attacks, in which a malicious user could subscribe to a large number of channels that all hash to the same bucket, causing poor performance.
  
  The keys in the channel hash table are *strings*, colored green, and the values are *sets of clients*, colored red. But “set” is also an abstract data structure; how is it implemented in Redis? Well, the set of clients is another linked list!
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*FPf14PtqcrKDd_6d1ZGhHw.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*FPf14PtqcrKDd_6d1ZGhHw.png)
  
  It’s nice to think of the strings “topicA” and “topicB” as embedded in the hash chain objects. But this is not true: each string has a separate allocation. Redis uses strings extensively, and has its own representation for them: “Simple Dynamic Strings”. This is a character array prefixed by its length and the number of free bytes. We can draw it like this:
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tSCkTVajwxDvkxBpOsz5Ig.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*tSCkTVajwxDvkxBpOsz5Ig.png)
  
  We are almost at the level of memory blocks, except for one thing: each client’s set of channels. Redis chooses to *not* use a linked list here; instead, Redis uses another hash table. The channel names are the keys of the table:
  
  ![https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MJsnS7YVYaATXZFwapd7pQ.png](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MJsnS7YVYaATXZFwapd7pQ.png)
  
  Why does Redis use a linked list to represent the channel’s client set, but a hash table to represent the client’s channel set? We’re not sure. We suspect the channel’s client set is a linked list because it’s optimized for publishing, where it iterates over the set. The client’s channel set is a hash table because it’s optimized for subscribe/unsubscribe, where it does a lookup in the set. Let us know if you have any insights on this.
  
  Notice also that the *value* pointers in each client’s hash chain are ignored; they are unused memory. Only the keys are used when using a hash table to represent a set. The memory waste is okay compared to the code reuse we gain.
  
  Finally, we’re pretty close to the truth: each block in the diagram represents a memory allocation in the redis-server process. Let’s recap our `PUBLISH` and `SUBSCRIBE` algorithms:
- To `PUBLISH`, hash the channel name to get a hash chain. Iterate over the hash chain, comparing each channel name to our target channel name. Once we’ve found our target channel name, get the corresponding list of clients. Iterate over the linked list of clients, sending the published message to each client.
- To `SUBSCRIBE`, find the linked list of clients as before. Append the new client to the end of the linked list. (Actually, this is a constant-time operation, because the linked lists have a tail pointer.) Also, add the channel to the client’s hash table.
- ## Real-time hash tables!
  
  Notice that the hash tables are different sizes, roughly proportional to how many elements they have. Redis resizes hash tables in response to their number of elements. But Redis is built for low latency, and resizing a hash table is a time-consuming operation. How can it resize the hash table without causing latency spikes?
  
  Answer: Redis *gradually* resizes the hash table. It keeps *two* underlying hash tables, the old and the new. Consider this `pubsub_channels` hash table in the middle of a resize:
  
  Whenever Redis performs an operation on the hash table (lookup, insert, delete …), it does a little bit of resizing work. It keeps track of how many old buckets have been moved to the new table, and on each operation, it moves a few more buckets over. This bounds the amount of work, so that Redis remains responsive.
  
  ![https://miro.medium.com/v2/resize:fit:2000/format:webp/1*Mf-1-9MF9X2W5coFlfPHfg.png](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*Mf-1-9MF9X2W5coFlfPHfg.png)
  
  Whenever Redis performs an operation on the hash table (lookup, insert, delete …), it does a little bit of resizing work. It keeps track of how many old buckets have been moved to the new table, and on each operation, it moves a few more buckets over. This bounds the amount of work, so that Redis remains responsive.
- ## Expensive unsubscribed
  
  There’s one more important command in Redis Pub/Sub: `UNSUBSCRIBE`. `UNSUBSCRIBE` does the inverse of `SUBSCRIBE`: the client will no longer receive messages published to that channel.
  
  How would you write `UNSUBSCRIBE`, using the data structures above? Here’s how Redis does it:
- To `UNSUBSCRIBE`, find the linked list of clients for the channel, as before. Then iterate over the entire list until you find the client to remove.
  
  The `UNSUBSCRIBE` operation is therefore O(*n*), where *n* is the number of subscribed clients. With a very large number of clients subscribed to a Redis channel, an `UNSUBSCRIBE` can be expensive. ***This means you should either limit your clients or the number of subscriptions that they are allowed.*** One of Pusher’s important optimizations is de-duplicating subscriptions: millions of Pusher subscriptions are collapsed into a much smaller number of Redis subscriptions.
  
  Redis could optimize this by using a hash table instead of a linked list to represent the set of subscribed clients. However, this might not be desirable, because publishes will be a little slower: iterating over a hash table is slower than iterating over a linked list.
  
  Redis optimizes for `PUBLISH` operations, since they are more common than subscription changes.
- ## Pattern subscriptions
  
  The original Redis Pub/Sub API provides `PUBLISH`, `SUBSCRIBE`, and `UNSUBSCRIBE`. Shortly afterwards, Redis introduced [“pattern subscriptions”](https://redis.io/topics/pubsub#pattern-matching-subscriptions). Pattern subscriptions let a client subscribe to all channels matching a Regex-like pattern, instead of only subscribing to a single literal channel name.
  
  The important new command is `PSUBSCRIBE`. Now, if a client sends `PSUBSCRIBE food.donuts.*`, and a news outlet sends `PUBLISH food.donuts.glazed 2-for-£2`, the subscribed client will be notified, because `food.donuts.glazed` matches the pattern `food.donuts.*`.
  
  The pattern subscription system is completely separate to the normal channel subscription system. Alongside the global `pubsub_channels` hash table, there is the global `pubsub_patterns` list.
  
  This is a linked list of pubsubPattern objects, each of which associates one pattern with one client.
  
  Similarly, each client object has a linked list of the patterns it is subscribed to. Here’s what `redis-server` memory looks like after client B subscribes to `drink?`, and clients A and B subscribe to `food.*`:
  
  ![https://miro.medium.com/v2/resize:fit:2000/format:webp/1*4gxatBkdKfDGroOGJAhmZA.png](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*4gxatBkdKfDGroOGJAhmZA.png)
  
  There is a global linked list down the left-hand side, each pointing to a `pubsubPattern`. Each pattern is represented as its literal string in memory. On the right-hand side, each client has its own linked list of patterns.
  
  Now, when a client sends `PUBLISH food.donuts 5-for-$1`, Redis will iterate through the global `pubsub_patterns` list, and test the string `food.donuts` against each pattern. For each successful match, Redis will send the message `5-for-$1` to the linked client.
  
  This system may surprise you: multiple clients subscribed to the same pattern do not get grouped together! If 10,000 clients subscribe to `food.*`, you will get a linked list of 10,000 patterns, each of which is tested on every publish! This design assumes that the set of pattern subscriptions will be small and distinct.
  
  Another cause for surprise is that patterns are stored in their surface syntax. They are not compiled (e.g. to DFAs). This is especially interesting since Redis’s matching function `stringmatch` has some … *interesting* worst-cases. Here is how Redis tests the pattern `*a*a*b` against the string `aa`:
  
  ```
  stringmatch("*a*a*b", "aa")
    stringmatch("a*a*b", "aa")
        stringmatch("*a*b", "a")
            stringmatch("a*b", "a")
                stringmatch("*b", "")
                    stringmatch("b", "")
                        false
            stringmatch("a*b", "")
                false
    stringmatch("a*a*b", "a")
        stringmatch("*a*b", "")
            stringmatch("a*b", "")
                false
    stringmatch("a*a*b", "")
        false
  ```
  
  This malicious pattern with many “globs” causes an exponential blowup in the running time of the match! Redis’s pattern language could be compiled to a DFA, which would run in linear time. But it is not.
  
  In short, you should not expose Redis’s pattern subscriptions to untrusted clients, because there are at least two attack vectors: multiple pattern subscriptions, and crafted patterns. At Pusher, we tread very carefully with Redis pattern subscriptions.
- # Pub/Sub use cases
  
  Now that we understand Pub/Sub in detail and how they are implemented in Redis we now need to go through a couple of use cases of Pub/Sub use cases.
  
  The asynchronous integration offered by Pub/Sub increases the system’s overall flexibility and robustness, which enables having various use cases, including:
  
  1. **Real-time messaging and chat:** Pub/Sub can create real-time messaging and chat applications, such as in social media platforms, instant messaging apps, and collaborative work environments.
  2. **IoT devices:** Pub/Sub can be used to link IoT devices to the cloud, where they can communicate with a centralized broker and send and receive data. With this method, massive amounts of data they produce can be gathered and processed, which can later be used for data analysis..
  3. **News updates and alerts:** Subscribers can receive real-time news updates and alerts. This use case is typical in stock trading platforms, news applications, and emergency response systems.
  4. **Distributed computing and microservices:** Pub/Sub can be used to build distributed systems and microservices architectures in which different components of an application communicate in a decoupled manner allowing for greater scalability and flexibility.
  5. **Event-driven architectures:** Pub/Sub supports event-driven architectures, in which various components of an application react to actions taken by other components. It allows flexibility in the application design and simplifies complicated workflows.
  6. **Decoupling components and reducing dependencies:** Pub/Sub can decouple and reduce dependencies between application components, allowing easier application maintenance over time.
  7. **Fan-out processing:** The process of sending a single message simultaneously to numerous subscribers is known as fan-out processing. It is used in distributing data or events to numerous consumers. For instance, pub/sub can be used to fan out data to multiple subscribers, each of which can independently process the data in parallel and feed it to multiple downstream systems.
  8. **Fan-in processing:** The process of combining multiple messages into a single message is known as fan-in processing. It is useful in combining the processing of data from various sources. For instance, pub/sub can gather the data from each component and fan it into a single stream for subsequent processing where multiple components generated data could be aggregated and analyzed.
  9. **Refreshing distributed caches:** Maintaining consistency across multiple instances of a distributed cache can be difficult. This issue can be resolved using pub/sub, which offers a [cache invalidation](https://redis.io/glossary/cache-invalidation/) and refreshing mechanism. A message is published to a pub/sub topic when data in the backend data source is updated, and this causes all instances of the cache to be refreshed. As a result, it lowers the possibility of serving users with out-of-date data and ensures that all cache instances are kept in sync.
- # Conclusion
  
  One of the most used tools for implementing Pub/Sub is Redis which is famous because it is widely adopted for its scalability, low latency, and ease of integration, we went in-depth into how Redis works up to the memory block level.
  
  Redis Pub/Sub is an efficient way to distribute messages. But you should know what it is optimized for, and where the pitfalls are. To truly understand this, study the source! In short: only use Redis in a trusted environment, limit the number of clients, and handle pattern subscriptions with gloves.
  
  I hope you find this helpful let me know if you have any questions.
