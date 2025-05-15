# Improving key expiration in Redis

Tags: caching, redis
Category: Articles
Company: Twitter
Status: Not started
URL: https://blog.x.com/engineering/en_us/topics/infrastructure/2019/improving-key-expiration-in-redis

Internally Twitter runs multiple cache services. One of them is backed by Redis. Our Redis clusters store data for some Twitter’s most important use cases such as impression and engagement data, ad spend counting, and Direct Messages.
Back in early 2016 Twitter’s Cache team did a large update to the architecture of our Redis clusters. A few things changed, among them was an update from Redis version 2.4 to version 3.2. After this update a couple issues came up. Users started to see memory use that didn’t align with what they expected or were provisioned to use, latency increases and key evictions. The key evictions were a big problem because data was removed that was expected to be persistent or traffic was now going to origin data stores that originally wasn’t.
We found that the latency increase was related to the key evictions that were now happening. When Redis receives a write request but doesn’t have memory to save the write, it will stop what it is doing, evict a key then save the new key. We still needed to find where the increase in memory usage was happening that was causing these new evictions.

We suspected that memory was full of keys that were expired but haven’t been deleted yet. One idea someone suggested was to use a scan, which would read all of the keys, causing expired ones to be deleted.

In Redis there are two ways keys can be expired, actively and passively. Scan would trigger passive key expiration, when the key is read the TTL will be checked and if it is expired throw it away and return nothing. Active key expiration in version 3.2 is described in the [Redis documentation](https://redis.io/commands/expire#how-redis-expires-keys). It starts with a function called activeExpireCycle. It runs on an internal timer Redis refers to as cron, that runs several times a second. What this function does is cycle through each keyspace, check random keys that have a TTL set, and if a percentage threshold  was met of expired keys, repeat this process until a time limit is met.

This idea of scanning all keys worked, memory use dropped when a scan completed. It seemed that Redis wasn’t efficiently expiring keys any more. Unfortunately, the resolution at the time was to increase the size of the cluster and more hardware so keys would be spread around more and there would be more memory available. This was disappointing because the project to upgrade Redis mentioned earlier reduced the size and cost of running these clusters by making them more efficient.
In 2.4 every database was checked each time it ran, in 3.2 there is now a maximum to how many databases can be checked. Version 3.2 also introduced a fast option to the function. “Slow” runs on the timer and “fast” runs before checking for events on the event loop. Fast expiration cycles will return early under certain conditions and it also has a lower threshold for the function to timeout and exit. The time limit is also checked more frequently. Overall 100 lines of code were added to this function.
We wanted to explore why there was a regression and then see how we could make key expiration better. Our first theory was that with so many keys in an instance of Redis sampling 20 wasn’t enough. The other thing we wanted to investigate was the impact of the database limit introduced in 3.2.

Scale and the the way sharding is handled makes running Redis at Twitter unique. We have large keyspaces with millions of keys. This isn’t typical for users of Redis. Shards are represented by a keyspace, so each instance of Redis can have multiple shards. Our instances of Redis have a lot of keyspaces. Sharding combined with the scale of Twitter create dense backends with lots of keys and databases.

