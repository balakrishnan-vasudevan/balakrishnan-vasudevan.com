

| **Criteria**                                           | **Option**                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| Read-heavy system                                      | Use a cache                                                  |
| Write-heavy system                                     | Use Message queues for async processing                      |
| Low-latency                                            | Use a cache and CDN                                          |
| ACID-compliant DB                                      | RDBMS/SQL DB                                                 |
| Unstructured Data                                      | NoSQL DB                                                     |
| Complex Data (Videos, Images, Files)                   | Use Blob/Object storage                                      |
| High-volume data search                                | Search index, tries, or search engine                        |
| Complex pre-computation                                | Use message queue + cache                                    |
| Scaling SQL DB                                         | Implement DB sharding                                        |
| High availability, performance, throughput             | Use LB                                                       |
| Global Data delivery                                   | Use a CDN                                                    |
| Graph Data (data with nodes, edges, and relationships) | Use a graph DB                                               |
| Scaling components                                     | Horizontal Scaling                                           |
| High performing DB queries                             | Use DB indexes                                               |
| Bulk job processing                                    | Consider batch processing + message queues                   |
| Server load mgmt + Preventing DOS attacks              | Use a rate limiter                                           |
| Microservices architecture                             | Use an API GW                                                |
| Single point of failure                                | Implement redundancy                                         |
| Fault tolerance and durability                         | Implement data replication                                   |
| User-to-user fast communication                        | Use websockets                                               |
| Failure detection in distributed systems               | Implement a heartbeat                                        |
| Data integrity                                         | Use a checksum algorithm                                     |
| Efficient server scaling                               | Implement consistent hashing                                 |
| Decentralized Data transfer                            | Use gossip protocol                                          |
| Location-based functionality                           | Use quadtree/geohash etc.                                    |
| Avoid specific technology names                        | Use generic terms                                            |
| High availability and consistency tradeoff             | Eventual consistency                                         |
| IP resolution and domain name query                    | DNS                                                          |
| Handling large data in network requests                | implement pagination                                         |
| Cache eviction policy                                  | LRU preferred                                                |
| Handling traffic spikes                                | Implement autoscaling                                        |
| Analytics and audit trails                             | Use data lakes or append-only DBs                            |
| Handling large-scale simultaneous connections          | Connection pooling and use Protobuf to minimize data payload |


