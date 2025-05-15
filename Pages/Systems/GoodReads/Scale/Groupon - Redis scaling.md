# Scaling Millions of Geospatial Queries per minute using Redis

Tags: redis
Category: Articles
Company: general
Status: Not started
URL: https://medium.com/groupon-eng/scaling-millions-of-geospatial-queries-per-minute-using-redis-7c05bcf6b4db

# Scaling Millions of Geospatial Queries per minute using Redis

![https://miro.medium.com/v2/resize:fill:44:44/0*b4eVdLXeRODHBo5Q.jpg](https://miro.medium.com/v2/resize:fill:44:44/0*b4eVdLXeRODHBo5Q.jpg)

![https://miro.medium.com/v2/resize:fill:24:24/1*5nh6XJWbxZv8ElrTQ7xgOQ.png](https://miro.medium.com/v2/resize:fill:24:24/1*5nh6XJWbxZv8ElrTQ7xgOQ.png)

[Vaibhav Sethi](https://medium.com/@vsethi?source=post_page---byline--7c05bcf6b4db--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F91778bfca701&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fgroupon-eng%2Fscaling-millions-of-geospatial-queries-per-minute-using-redis-7c05bcf6b4db&user=Vaibhav+Sethi&userId=91778bfca701&source=post_page-91778bfca701--byline--7c05bcf6b4db---------------------post_header-----------)

Published in

[Groupon Product and Engineering](https://medium.com/groupon-eng?source=post_page---byline--7c05bcf6b4db--------------------------------)

·

5 min read

·

Jun 4, 2021

- -

To find relevant deals near the Groupon users, a large number of geospatial searches are performed. These searches are performed on geospatial entities like postal codes, timezones, neighborhoods, or points of interest. Serving millions of queries per minute with low latency requires an efficient spatial indexer for optimization.

This article describes how Groupon uses Redis to power 2 main types of geospatial searches — find the nearest entity and find all nearby entities within a radius. We will also see how Redis clusters provide scalable and performant solutions.

# How do Geospatial Queries work in Redis?

Redis provides commands like [GEOADD](https://redis.io/commands/GEOADD), [GEORADIUS](https://redis.io/commands/georadius), [GEORADIUSBYMEMBER](https://redis.io/commands/georadiusbymember), [GEOSEARCH](https://redis.io/commands/geosearch), and [GEOSEARCHSTORE](https://redis.io/commands/geosearchstore) for geospatial indexing and searching. The spatial entities are stored in Sorted Sets using the coordinates to form 52-bit integers using the [Geohash](https://en.wikipedia.org/wiki/Geohash) technique.

Let’s go through an example to see how the spatial entities can be indexed and searched. [Redis-CLI](https://redis.io/topics/rediscli) commands are shown in these examples, though any Redis client can be used.

For the examples consider four places with the coordinates:

- San Francisco (lat: 37.774, lng: -122.419)
- Palo Alto (lat: 37.441, lng: -122.143)
- Mountain View (lat: 37.386, lng: -122.083)
- San Jose (lat: 37.338, lng: -121.886)

![https://miro.medium.com/v2/resize:fit:700/1*G0TvIHTL5qECBPe2FZ674Q.png](https://miro.medium.com/v2/resize:fit:700/1*G0TvIHTL5qECBPe2FZ674Q.png)

## How to index spatial entities?

[GEOADD](https://redis.io/commands/GEOADD) command can be used to index spatial entities in Redis. The time complexity for this command is O(log(N)) for each item added, where N is the number of elements in the sorted set.

To add these 4 locations to the ‘places’ Redis keys, run the commands:

```
> GEOADD places -122.419 37.774 “San Francisco”
> GEOADD places -122.143 37.441 “Palo Alto”
> GEOADD places -122.083 37.386 “Mountain View”
> GEOADD places -121.886 37.338 “San Jose”
```

Since these entities are stored in a sorted set, the [ZCARD](https://redis.io/commands/zcard) command would return the total count of spatial entities.

```
> ZCARD places(integer) 4
```

[ZRANGE](https://redis.io/commands/zrange) can be used to list all the entities

```
> ZRANGE places 0 -11) "San Francisco"
2) "Mountain View"
3) "Palo Alto"
4) "San Jose"
```

## How to perform spatial search?

To perform a spatial search of entities [GEORADIUS](https://redis.io/commands/georadius) or [GEORADIUSBYMEMBER](https://redis.io/commands/georadiusbymember) can be used in Redis 3.2.0 (and above) and GEOSEARCH or GEOSEARCHSTORE can be used in Redis 6.2 (and above).

The time complexity for these commands is approximately O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius, and M is the number of items inside the index.

To find all places within 20 miles radius of Mountain View along with their distance, run the command:

```
> GEORADIUSBYMEMBER places "Mountain View" 20 mi WITHDIST1) 1) "Mountain View"
   2) "0.0000"
2) 1) "Palo Alto"
   2) "5.0297"
3) 1) "San Jose"
   2) "11.3186"
```

Note that San Francisco is not returned in the response as it is more than 20 miles away from Mountain View. Let’s see the response on increasing the radius to 50 miles.

```
> GEORADIUSBYMEMBER places "Mountain View" 50 mi WITHDIST1) 1) "San Francisco"
   2) "32.5234"
2) 1) "Mountain View"
   2) "0.0000"
3) 1) "Palo Alto"
   2) "5.0297"
4) 1) "San Jose"
   2) "11.3186"
```

This time San Francisco is returned in the response, as it is 32.52 miles away from Mountain View and within 50 miles of radius.

Now suppose we want to find the nearest place to Redwood City with the coordinate 37.484° N, 122.228° W, we can run the GEORADIUS command with ASC (for ascending) and COUNT as 1 (for limiting to one result):

```
> GEORADIUS places -122.228 37.484 50 mi COUNT 1 ASC WITHCOORD WITHDIST1) 1) "Palo Alto"
   2) "5.5294"
   3) 1) "-122.14300006628036499"
      2) "37.4410011922460555"
```

## Points to Remember

- Redis uses [Haversine](https://en.wikipedia.org/wiki/Haversine_formula) formula to calculate the distances as the model assumes that the Earth is a sphere. This can result in an error of up to 0.5%.
- Valid longitudes range from -180 to 180 degrees, while valid latitudes range from -85.05112878 to 85.05112878 degrees.

# Why use Redis?

There are plenty of solutions available for implementing spatial searches. Data structures like Quadtree, R-tree, and K-d tree can be used to index the entities. Geospatial indexers like S2 and H3 can be used for similar queries.

However, Redis provides an edge when it comes to scalability, performance, and availability. Redis has several advantages over other solutions:

## 1. Scalability

From the time complexities it is evident that as the volume of Geographic data increases, the time for the command execution will increase. The used memory is also bound to increase. In such cases, Redis clusters can be scaled with the changing volume of the data.

There are two ways to scale a Redis cluster — horizontal and vertical scaling.

- Horizontal scaling allows nodes (shards) to be added or removed from the cluster. The cluster continues to serve requests even during resharding, while scaling in/out.
- Vertical scaling allows the size of the nodes to be changed for scaling up/down, while serving the requests.

![https://miro.medium.com/v2/resize:fit:700/1*L0UyHAJyVTJp-hwxoJCF3w.png](https://miro.medium.com/v2/resize:fit:700/1*L0UyHAJyVTJp-hwxoJCF3w.png)

## 2. High Availability

Redis cluster provides high availability through replication. The primary node can have multiple replicas configured across physical racks (or data centers). Automatic failover is also supported in Redis cluster.

![https://miro.medium.com/v2/resize:fit:700/1*TBmz4MVE-UOPFVcARYjzyw.png](https://miro.medium.com/v2/resize:fit:700/1*TBmz4MVE-UOPFVcARYjzyw.png)

## 3. Performance

Redis is an in-memory data store with data structures optimised for performance. However, one needs to keep the following points in mind when benchmarking and tuning the performance of Geospatial queries:

- The time complexities of the GEOADD and GEORADIUS commands are in the order of O(log(N)) and O(N + log(M)) respectively. It is important to keep the key size small and the data partitioned to avoid overloading any single node. Increases in radius can cause the command execution time to increase.
- Clients communicate with Redis servers using TCP connections. The client socket is put in non-blocking state since Redis uses multiplexing and non-blocking I/O. TCP Keepalive should be enabled for performance tuning. Keepalive is a method to allow the same TCP connection to be used instead of opening a new one for each new request.
- The horizontal scaling allows the keys to be spread across the shards and improves the performance by reducing the load per shard.
- If Redis cluster mode is enabled, then the RDB persistence and AOF are not required.
- By default, Redis allows 10,000 client connections and this can be configured.
- The performance of Redis commands can be benchmarked using the [redis-benchmark](https://redis.io/topics/benchmarks) utility.

# Conclusion

We hope you found this article interesting as you get to know how Redis can be used for indexing and searching Geospatial data. It is also interesting to know how Redis cluster provides scalable and performant solutions. Redis provides utilities for benchmarking the performance. Its support for scaling helps in improving the performance of the queries.

For further reading check the documentation for the commands to see the various options supported. RedisLabs also provides Geo Lua library for polygon searches.

For more interesting topics stay tuned!