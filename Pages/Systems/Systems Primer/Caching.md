#sdp
![[Pasted image 20250430085501.png]]
_[Source: Scalable system design patterns](http://horicky.blogspot.com/2010/10/scalable-system-design-patterns.html)_

Caching improves page load times and can reduce the load on your servers and databases. In this model, the dispatcher will first lookup if the request has been made before and try to find the previous result to return, in order to save the actual execution.

Databases often benefit from a uniform distribution of reads and writes across its partitions. Popular items can skew the distribution, causing bottlenecks. Putting a cache in front of a database can help absorb uneven loads and spikes in traffic.

### Client caching



Caches can be located on the client side (OS or browser), [server side](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#reverse-proxy-web-server), or in a distinct cache layer.

### CDN caching



[CDNs](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#content-delivery-network) are considered a type of cache.

### Web server caching



[Reverse proxies](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#reverse-proxy-web-server) and caches such as [Varnish](https://www.varnish-cache.org/) can serve static and dynamic content directly. Web servers can also cache requests, returning responses without having to contact application servers.

### Database caching



Your database usually includes some level of caching in a default configuration, optimized for a generic use case. Tweaking these settings for specific usage patterns can further boost performance.

### Application caching

In-memory caches such as Memcached and Redis are key-value stores between your application and your data storage. Since the data is held in RAM, it is much faster than typical databases where data is stored on disk. RAM is more limited than disk, so [cache invalidation](https://en.wikipedia.org/wiki/Cache_algorithms) algorithms such as [least recently used (LRU)](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_\(LRU\)) can help invalidate 'cold' entries and keep 'hot' data in RAM.

Redis has the following additional features:

- Persistence option
- Built-in data structures such as sorted sets and lists

There are multiple levels you can cache that fall into two general categories: **database queries** and **objects**:

- Row level
- Query-level
- Fully-formed serializable objects
- Fully-rendered HTML

Generally, you should try to avoid file-based caching, as it makes cloning and auto-scaling more difficult.

### Caching at the database query level

Whenever you query the database, hash the query as a key and store the result to the cache. This approach suffers from expiration issues:

- Hard to delete a cached result with complex queries
- If one piece of data changes such as a table cell, you need to delete all cached queries that might include the changed cell

### Caching at the object level

See your data as an object, similar to what you do with your application code. Have your application assemble the dataset from the database into a class instance or a data structure(s):

- Remove the object from cache if its underlying data has changed
- Allows for asynchronous processing: workers assemble objects by consuming the latest cached object

Suggestions of what to cache:

- User sessions
- Fully rendered web pages
- Activity streams
- User graph data

### When to update the cache



Since you can only store a limited amount of data in cache, you'll need to determine which cache update strategy works best for your use case.

#### Cache-aside

![[Pasted image 20250430085446.png]]
_[Source: From cache to in-memory data grid](http://www.slideshare.net/tmatyashovsky/from-cache-to-in-memory-data-grid-introduction-to-hazelcast)_

The application is responsible for reading and writing from storage. The cache does not interact with storage directly. The application does the following:

- Look for entry in cache, resulting in a cache miss
- Load entry from the database
- Add entry to cache
- Return entry

```python
def get_user(self, user_id):
    user = cache.get("user.{0}", user_id)
    if user is None:
        user = db.query("SELECT * FROM users WHERE user_id = {0}", user_id)
        if user is not None:
            key = "user.{0}".format(user_id)
            cache.set(key, json.dumps(user))
    return user
```

[Memcached](https://memcached.org/) is generally used in this manner.

Subsequent reads of data added to cache are fast. Cache-aside is also referred to as lazy loading. Only requested data is cached, which avoids filling up the cache with data that isn't requested.

##### Disadvantage(s): cache-aside

- Each cache miss results in three trips, which can cause a noticeable delay.
- Data can become stale if it is updated in the database. This issue is mitigated by setting a time-to-live (TTL) which forces an update of the cache entry, or by using write-through.
- When a node fails, it is replaced by a new, empty node, increasing latency.

#### Write-through

![[Pasted image 20250430085436.png]]
_[Source: Scalability, availability, stability, patterns](http://www.slideshare.net/jboner/scalability-availability-stability-patterns/)_

The application uses the cache as the main data store, reading and writing data to it, while the cache is responsible for reading and writing to the database:

- Application adds/updates entry in cache
- Cache synchronously writes entry to data store
- Return

Application code:

```python
set_user(12345, {"foo":"bar"})
```

Cache code:

```python
def set_user(user_id, values):
    user = db.query("UPDATE Users WHERE id = {0}", user_id, values)
    cache.set(user_id, user)
```

Write-through is a slow overall operation due to the write operation, but subsequent reads of just written data are fast. Users are generally more tolerant of latency when updating data than reading data. Data in the cache is not stale.

##### Disadvantage(s): write through



- When a new node is created due to failure or scaling, the new node will not cache entries until the entry is updated in the database. Cache-aside in conjunction with write through can mitigate this issue.
- Most data written might never be read, which can be minimized with a TTL.

#### Write-behind (write-back)



![[Pasted image 20250430085422.png]]
_[Source: Scalability, availability, stability, patterns](http://www.slideshare.net/jboner/scalability-availability-stability-patterns/)_

In write-behind, the application does the following:

- Add/update entry in cache
- Asynchronously write entry to the data store, improving write performance

##### Disadvantage(s): write-behind

[](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#disadvantages-write-behind)

- There could be data loss if the cache goes down prior to its contents hitting the data store.
- It is more complex to implement write-behind than it is to implement cache-aside or write-through.

#### Refresh-ahead



![[Pasted image 20250430085409.png]]

You can configure the cache to automatically refresh any recently accessed cache entry prior to its expiration.

Refresh-ahead can result in reduced latency vs read-through if the cache can accurately predict which items are likely to be needed in the future.

##### Disadvantage(s): refresh-ahead



- Not accurately predicting which items are likely to be needed in the future can result in reduced performance than without refresh-ahead.

### Disadvantage(s): cache



- Need to maintain consistency between caches and the source of truth such as the database through [cache invalidation](https://en.wikipedia.org/wiki/Cache_algorithms).
- Cache invalidation is a difficult problem, there is additional complexity associated with when to update the cache.
- Need to make application changes such as adding Redis or memcached.

### Source(s) and further reading


- [From cache to in-memory data grid](http://www.slideshare.net/tmatyashovsky/from-cache-to-in-memory-data-grid-introduction-to-hazelcast)
- [Scalable system design patterns](http://horicky.blogspot.com/2010/10/scalable-system-design-patterns.html)
- [Introduction to architecting systems for scale](http://lethain.com/introduction-to-architecting-systems-for-scale/)
- [Scalability, availability, stability, patterns](http://www.slideshare.net/jboner/scalability-availability-stability-patterns/)
- [Scalability](http://www.lecloud.net/post/9246290032/scalability-for-dummies-part-3-cache)
- [AWS ElastiCache strategies](http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/Strategies.html)
- [Wikipedia](https://en.wikipedia.org/wiki/Cache_\(computing\))



## Why cache invalidation is hard

Distributed Systems and Network Latency
In distributed systems, data can be cached across numerous nodes. When the original data is updated, the invalidation signal must reach all the nodes holding the cached copy. This process is inherently susceptible to network latency and potential failures. Sending invalidation messages across a large network takes time, and there's no guarantee that all messages will be delivered on time. This delay can lead to temporary inconsistencies where some users see the updated data. In contrast, others still see the stale version.

![[Pasted image 20250328163402.png]]

Concurrency and Ordering of Operations
In high-throughput systems, multiple read and write operations can occur concurrently. Ensuring that invalidation messages are processed in the correct order relative to data updates can be challenging. Suppose an invalidation message arrives before the update is fully committed to the primary data store. In that case, the cache might prematurely remove a non-stale entry. On the other hand, the cache will serve stale data if the update is complete before the invalidation.
Balancing Freshness and Performance
There's an inherent trade-off between data freshness and performance. Aggressive invalidation strategies immediately removing cached data upon any update ensure high freshness but can lead to increased load on the primary data store as caches are frequently repopulated. On the other hand, less aggressive strategies that rely on time-based expiration might improve performance by reducing the frequency of invalidation but risk serving stale data for longer periods.
Cache Size Limitations and Eviction Policies
Caches have finite storage capacity. When a cache reaches its limit, it needs to evict some entries to make space for new ones. The eviction policy (e.g., Least Recently Used, Least Frequently Used) can inadvertently remove data that is still valid and might be requested again soon, leading to cache misses and increased load on the primary data store.

![[Pasted image 20250328163427.png]]

False Sharing
False sharing is a performance issue in multi-core processors where two or more data items reside within the same cache line. When one core modifies a data item, the entire cache line is invalidated for other cores, even if they accessed different data items within the same line, which degrades performance. For example, two variables stored contiguously in memory might share a cache line. Updating one variable invalidates the entire line, even if the other remains unchanged.

![[Pasted image 20250328163457.png]]

Resource Constraints and Cost Considerations
Implementing sophisticated cache invalidation mechanisms can be resource-intensive. Maintaining metadata about cached entries, tracking dependencies, and reliably propagating invalidation messages require computational resources, network bandwidth, and storage. The cost of implementing and maintaining these mechanisms must be carefully considered, especially in large-scale systems where even small inefficiencies can have a significant impact.
Predicting Future Access Patterns
An ideal invalidation strategy would proactively invalidate data that is likely to become stale or is unlikely to be accessed again soon. However, accurately predicting future access patterns is a complex problem. Relying on heuristics or historical data might not always be effective in dynamic environments where access patterns can change rapidly. For example, a video streaming service might prefetch content based on user behavior, but unexpected viral trends could render predictions obsolete, flooding caches with irrelevant data.



#caching, #sharding , #consistent-hashing, #redis, #memcached




![[Pasted image 20250430085257.png]]



Caching can be implemented in various ways, including in-memory caching, disk caching, database caching, and CDN caching. In-memory caching stores data in the main memory of the computer, which is faster to access than disk storage. Disk caching stores data on the hard disk, which is slower than main memory but faster than retrieving data from a remote source. Database caching stores frequently accessed data in the database itself, reducing the need to access external storage. CDN caching stores data on a distributed network of servers, reducing the latency of accessing data from remote locations.
## Types of Caching

Caching can be implemented in various ways, depending on the specific use case and the type of data being cached. Here are some of the most common types of caching:

1. **In-memory caching:** In-memory caching stores data in the main memory of the computer, which is faster to access than disk storage. In-memory caching is useful for frequently accessed data that can fit into the available memory. This type of caching is commonly used for caching API responses, session data, and web page fragments. To implement in-memory caching, software engineers can use various techniques, including using a cache library like Memcached or Redis, or implementing custom caching logic within the application code.
    
2. **Disk caching:** Disk caching stores data on the hard disk, which is slower than main memory but faster than retrieving data from a remote source. Disk caching is useful for data that is too large to fit in memory or for data that needs to persist between application restarts. This type of caching is commonly used for caching database queries and file system data.
    
3. **Database caching:** Database caching stores frequently accessed data in the database itself, reducing the need to access external storage. This type of caching is useful for data that is stored in a database and frequently accessed by multiple users. Database caching can be implemented using a variety of techniques, including database query caching and result set caching.
    
4. **CDN caching:** CDN caching stores data on a distributed network of servers, reducing the latency of accessing data from remote locations. This type of caching is useful for data that is accessed from multiple locations around the world, such as images, videos, and other static assets. CDN caching is commonly used for content delivery networks and large-scale web applications.
    
5. **DNS caching:** DNS cache is a type of cache used in the Domain Name System (DNS) to store the results of DNS queries for a period of time. When a user requests to access a website, their computer sends a DNS query to a DNS server to resolve the website’s domain name to an IP address. The DNS server responds with the IP address, and the user’s computer can then access the website using the IP address. DNS caching improves the performance of the DNS system by reducing the number of requests made to DNS servers. When a DNS server receives a request for a domain name, it checks its local cache to see if it has the IP address for that domain name. If the IP address is in the cache, the DNS server can immediately respond with the IP address without having to query other servers. This can significantly reduce the response time for DNS queries and improve the overall performance of the system.
    

![Image](https://www.designgurus.io/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fdownload%2Fstorage%2Fv1%2Fb%2Fdesigngurus-prod.appspot.com%2Fo%2FdocImages%252F644796ec9e75207db7273ef4%252Fimg%3A4fda57-2d4f-1131-fbb1-5d1043bcc1de.png%3Fgeneration%3D1682413581453636%26alt%3Dmedia&w=3840&q=75)

## Cache Replacement Policies

When implementing caching, it’s important to have a cache replacement policy to determine which items in the cache should be removed when the cache becomes full. Here are some of the most common cache replacement policies:

- **Least Recently Used (LRU):** LRU is a cache replacement policy that removes the least recently used item from the cache when it becomes full. This policy assumes that items that have been accessed more recently are more likely to be accessed again in the future.
    
- **Least Frequently Used (LFU):** LFU is a cache replacement policy that removes the least frequently used item from the cache when it becomes full. This policy assumes that items that have been accessed more frequently are more likely to be accessed again in the future.
    
- **First In, First Out (FIFO):** FIFO is a cache replacement policy that removes the oldest item from the cache when it becomes full. This policy assumes that the oldest items in the cache are the least likely to be accessed again in the future.
## Cache Invalidation Strategies

Cache invalidation is the process of removing data from the cache when it is no longer valid. Invalidating the cache is essential to ensure that the data stored in the cache is accurate and up-to-date. Here are some of the most common cache invalidation strategies:

- **Write-through cache:** Under this scheme, data is written into the cache and the corresponding database simultaneously. The cached data allows for fast retrieval and, since the same data gets written in the permanent storage, we will have complete data consistency between the cache and the storage. Also, this scheme ensures that nothing will get lost in case of a crash, power failure, or other system disruptions. Although, write-through minimizes the risk of data loss, since every write operation must be done twice before returning success to the client, this scheme has the disadvantage of higher latency for write operations.
    
- **Write-around cache:** This technique is similar to write-through cache, but data is written directly to permanent storage, bypassing the cache. This can reduce the cache being flooded with write operations that will not subsequently be re-read, but has the disadvantage that a read request for recently written data will create a “cache miss” and must be read from slower back-end storage and experience higher latency.
    
- **Write-back cache:** Under this scheme, data is written to cache alone, and completion is immediately confirmed to the client. The write to the permanent storage is done based on certain conditions, for example, when the system needs some free space. This results in low-latency and high-throughput for write-intensive applications; however, this speed comes with the risk of data loss in case of a crash or other adverse event because the only copy of the written data is in the cache.
    
- **Write-behind cache:** It is quite similar to write-back cache. In this scheme, data is written to the cache and acknowledged to the application immediately, but it is not immediately written to the permanent storage. Instead, the write operation is deferred, and the data is eventually written to the permanent storage at a later time. The main difference between write-back cache and write-behind cache is when the data is written to the permanent storage. In write-back caching, data is only written to the permanent storage when it is necessary for the cache to free up space, while in write-behind caching, data is written to the permanent storage at specified intervals.
    

Overall, the cache invalidation strategy used should be chosen carefully to balance the trade-off between performance and data accuracy. By understanding the different cache invalidation strategies available, software engineers can select the appropriate strategy to optimize cache performance and reduce latency while ensuring that the data stored in the cache is accurate and up-to-date.

## Cache Invalidations Methods

Here are the famous cache invalidation methods:

- **Purge:** The purge method removes cached content for a specific object, URL, or a set of URLs. It’s typically used when there is an update or change to the content and the cached version is no longer valid. When a purge request is received, the cached content is immediately removed, and the next request for the content will be served directly from the origin server.
    
- **Refresh:** Fetches requested content from the origin server, even if cached content is available. When a refresh request is received, the cached content is updated with the latest version from the origin server, ensuring that the content is up-to-date. Unlike a purge, a refresh request doesn’t remove the existing cached content; instead, it updates it with the latest version.
    
- **Ban:** The ban method invalidates cached content based on specific criteria, such as a URL pattern or header. When a ban request is received, any cached content that matches the specified criteria is immediately removed, and subsequent requests for the content will be served directly from the origin server.
    
- **Time-to-live (TTL) expiration:** This method involves setting a time-to-live value for cached content, after which the content is considered stale and must be refreshed. When a request is received for the content, the cache checks the time-to-live value and serves the cached content only if the value hasn’t expired. If the value has expired, the cache fetches the latest version of the content from the origin server and caches it.
    
- **Stale-while-revalidate:** This method is used in web browsers and CDNs to serve stale content from the cache while the content is being updated in the background. When a request is received for a piece of content, the cached version is immediately served to the user, and an asynchronous request is made to the origin server to fetch the latest version of the content. Once the latest version is available, the cached version is updated. This method ensures that the user is always served content quickly, even if the cached version is slightly outdated.
    

![Image](https://www.designgurus.io/_next/image?url=https%3A%2F%2Fstorage.googleapis.com%2Fdownload%2Fstorage%2Fv1%2Fb%2Fdesigngurus-prod.appspot.com%2Fo%2FdocImages%252F644796ec9e75207db7273ef4%252Fimg%3Ad1110a-d4c6-cb20-260f-60235f5f862e.png%3Fgeneration%3D1682413759825348%26alt%3Dmedia&w=3840&q=75)


## Performance Metrics
1. Hit Rate
2. Miss Rate
3. Cache size
4. Cache latency
   


**

### Sharding caches

1. Dedicated cache servers
    
2. Co-located cache - blends cache and service functionality in the same host
    

  

Each cache client should use three mechanisms to store and evict entries from the cache servers:

- Hash map: The cache server uses a hash map to store or locate different entries inside the RAM of cache servers. The illustration below shows that the map contains pointers to each cache value.
    
- Doubly linked list: If we have to evict data from the cache, we require a linked list so that we can order entries according to their frequency of access. The illustration below depicts how entries are connected using a doubly linked list.
    
- Eviction policy: The eviction policy depends on the application requirements. Here, we assume the least recently used (LRU) eviction policy.
    

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXdm6zmXJvOEYdrFvJvU7kgx7OKSsZOL4kTKzlbopHbASmml1FHyZ_sRS7fphwH9B4qkb5eMhbsw6aEL6QlAqI-ceRSziRzeDTE2XMW9miVx5mwzzQVvxXANZhcp1vfNeK2LUZj3i1JDfqDlwRhZmJBdU9Y?key=j4FcJWeNiYnhIt4RY32tSQ)

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXe1aJ4UyaTX4moFTeyjoOTQOBFA1tcJOVOtDCmreC1zHB-FWdZHUHxzv8sFyYTFAtirre1YJzfJ7YcAp0i8SB8a5PKdLRzsTrZXGNLnPWDYfz7yZ_cmMvxFP-zXWhTJkGRDx0phHt6rxDPw3R8pQrPkJAs?key=j4FcJWeNiYnhIt4RY32tSQ)

  

- The client’s requests reach the service hosts through the load balancers where the cache clients reside.
    
- Finding a key under this algorithm requires a time complexity of O(log(N)), where N represents the number of cache shards.
    
- Each cache client uses consistent hashing to identify the cache server. Next, the cache client forwards the request to the cache server maintaining a specific shard. 
    
- The cache server uses a hashmap to store or locate different entries inside the RAM of cache servers. Inside a cache server, keys are located using hash tables that require constant time on average.
    
- Each cache server has primary and replica servers. Internally, every server uses the same mechanisms to store and evict cache entries.
    
- The LRU eviction approach uses a constant time to access and update cache entries in a doubly linked list.
    
- An important feature of the design is adding, retrieving, and serving data from the RAM. Therefore, the latency to perform these operations is quite low.
    
- Configuration service ensures that all the clients see an updated and consistent view of the cache servers.
    
- Monitoring services can be additionally used to log and report different metrics of the caching service.
    

  

How to avoid overloading of nodes in consistent hashing?

A number of consistent hashing algorithms’ flavors have been suggested over time. We can use one such flavor (used in DynamoDB) that distributes load uniformly and even makes multiple copies of the same data on different cache servers. Each cache server can have virtual servers inside it, and the number of virtual servers in a machine depends on the machine’s capability. This results in a finer control on the amount of load on a cache server. At the same time, it improves availability.

### Scalability:

Add shards based on requirements and changing server loads. When new cache servers are added to the cluster, a limited number of rehash computations are required due to consistent hashing.

If hotkeys are present, clients can use dynamic replication for those keys.

  

### High Availability:

Availability is increased through redundant cache servers. Leader-follower algorithm is used to manage a cluster shard (not within a datacenter, but among different datacenters). But this comes at the cost of consistency. Synchronous writing can work within a datacenter, asynchronous replication would be needed across DCs.

  

### Consistency:

Asynchronous mode is preferred for increased performance. We can avoid such scenarios for any joining or rejoining server by not allowing it to serve requests until it’s reasonably sure that it’s up to date.

**

Related

[[Redis vs Memcached]]
[[Practical Caching]]




https://newsletter.systemdesigncodex.com/p/caching-at-multiple-levels?utm_source=%2Finbox%2Fsaved&utm_medium=reader2



[[Backend Services]]