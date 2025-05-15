1. N/w latency and BW constraints
	1. Use CDNs and edge computing
	2. Use load balancing
	3. use high speed connections and more BW.
	4. Implement n/w segmentation using VPCs and segments
2. Storage I?O bottlenecks  - Slow disk read/write operations, high I/O wait times, and slow application response times.
	1. Use faster storage solutions like SSDs or NVMe instead of HDDs.
	2. Implement caching - Redis/Memcached to reduce load on primary storage
	3. Optimize data access patterns - reorganize data to reduce the number of I/O operations needed for common tasks
	4. Scale horizontally - use storage solutions that can scale horizontally like distributed file systems or object storage.
3. DB Performance - Slow query performance, high database CPU and memory usage, and increased latency for database-bound operations.
	1. Indexing and query optimization - optimize queries and use proper indexing to reduce DB load.
	2. DB sharding - Split the DB into smaller, more manageable pieces to distribute the load
	3. Use read replicas - Offload read operations to replica DBs to reduce load on primary.
	4. Leverage in-memory DBs like Redis or Memcached for frequently accessed data.
4. Compute resource saturation - High CPU and memory usage, increased processing times, and application slowdowns.
	1. Scale out - add more instances/nodes
	2. Use autoscaling 
	3. Optimize application code to reduce consumption
	4. Utilize containerization to effectively manage resources
5. Concurrency and synchronization - Thread contention, increased latency, and performance degradation in multi-threaded applications.
	1. Implement async processing to avoid blocking and improve concurrency.
	2. Use lock free data structures to reduce contention. [[Lock-free datastructures]]
	3. Optimize thread management
	4. Leverage event driven architecture to handle concurrency effectively
6. API rate limits and throttling - Increased API response times, failed API calls, and limited throughput for API-bound services.
	1. Implement rate limiting on the API
	2. Use API GWs - to manage and optimize API traffic.
	3. Optimize API endpoints to reduce the load on backend services.
	4. Cache frequent API responses.
7. Dependency latencies - Increased response times due to dependencies on external services or microservices.
	1. Implement circuit breakers to isolate and manage failures
	2. Use service mesh to optimize service-service communication
	3. Caching for responses from dependent services to reduce repeated calls.
	4. Implement graceful degradation in the event of dependency failures.
8. Security - Increased latency due to security checks, slow authentication and authorization processes.
	1. Use fast cryptographic algorithms - AES (symmetric encryption), ECDHE - - - Provides strong security with relatively small key sizes, which improves performance compared to traditional Diffie-Hellman key exchange., SHA256 - Balances security and performance. SHA-256 is faster than SHA-3 and more secure than older algorithms like SHA-1. Use hardware acceleration to use h/w capabilities for crypto operations. Use appropriate key sizes - 256-bit keys good for AES, minimize amount of data being encrypted or hashed - break into smaller chunks to process them incrementally.
	2. Optimize security rules - ACLs, Intrusion detection prevention rules - rule ordering to place most frequently matched rules at the top of the list, consolidate rules to reduce complexity, audit rules, segment and distribute rules according to rules and devices or segments, implement rule caching.
	3. Leverage IAM to centralize access
	4. Implement secure caching
9. Monitoring and Logging overhead - Increased latency due to extensive logging and monitoring, high storage and network usage for log data.
	1. Implement log aggregation
	2. Optimize log levels - don't log everything
	3. Use sampling and throttling to control volume of data
	4. Leverage cloud-native monitoring tools optimized for performance 
10. Deployment and update strategies - Slow deployment times, service downtime during updates, and increased error rates during changes.
	1.  B/G deployments to minimize downtime
	2. Canary releases to identify issues
	3. CI/CD pipelines to automate deployment
	4. IaC to manage and automate infrastructure changes.
