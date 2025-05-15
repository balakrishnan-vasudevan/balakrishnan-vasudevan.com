# Cache made consistent

Tags: caching
Category: Articles
Company: Facebook
Status: Reading
URL: https://engineering.fb.com/2022/06/08/core-infra/cache-made-consistent/

Cache invalidation involves an action that has to be carried out by something other than the cache itself. Something (e.g., a client or a pub/sub system) needs to tell the cache that a mutation happened. A cache that solely depends on time to live (TTL) to maintain its freshness contains no cache invalidations and, as such, lies out of scope for this discussion. For the rest of this post, we’ll assume the presence of cache invalidation.

Why is this seemingly straightforward process considered such a difficult problem in computer science? Here’s a simple example of how a cache inconsistency could be introduced:

![https://engineering.fb.com/wp-content/uploads/2022/06/Cache-made-consisent-image-1.png?w=1024](https://engineering.fb.com/wp-content/uploads/2022/06/Cache-made-consisent-image-1.png?w=1024)

The cache first tries to fill *x* from the database. But before the reply “x=42” reaches the cache host, someone mutates *x* to 43. The cache invalidation event for “x=43” arrives at the cache host first, setting *x* to 43. Finally, “x=42” in the cache fill reply gets to the cache, setting *x* to 42. Now we have “x=43” in the database and “x=42” in the cache indefinitely.

There are different ways to solve this problem, one of which involves maintaining a version field. This allows us to perform conflict resolution, as older data should never overwrite newer data. But what if the cache entry “x=43 @version=2” gets evicted from cache before “x=42” arrives? In that case, the cache host would lose knowledge of the newer data.

The challenge of cache invalidation arises not only from the complexity of invalidation protocols, but also from monitoring cache consistency and determining why these cache inconsistencies occur. Designing a consistent cache is very different from operating a consistent cache — much like designing [Paxos](https://engineering.fb.com/2022/03/07/core-data/augmenting-flexible-paxos-logdevice/), where the protocol is different from building Paxos that actually works in production.

Let’s examine another example of how cache inconsistencies can lead to split-brain. A messaging use case at Meta stores its mapping from user to primary storage in [TAO](https://engineering.fb.com/2013/06/25/core-data/tao-the-power-of-the-graph/). It performs shuffling frequently to keep the user’s primary message storage close to where the user accesses Meta. Every time you send a message to someone, behind the scenes, the system queries TAO to find out where to store the message. Many years ago, when TAO was less consistent, some TAO replicas would have inconsistent data after reshuffling, as illustrated in the example below.

Imagine that after shuffling Alice’s primary message store from region 2 to region 1, two people, Bob and Mary, both sent messages to Alice. When Bob sent a message to Alice, the system queried the TAO replica in a region close to where Bob lives and sent the message to region 1. When Mary sent a message to Alice, it queried the TAO replica in a region close to where Mary lives, hit the inconsistent TAO replica, and sent the message to region 2. Mary and Bob sent their messages to different regions, and neither region/store had a complete copy of Alice’s messages.