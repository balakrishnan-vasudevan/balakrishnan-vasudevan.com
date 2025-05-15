#rate-limiting
Controls the rate of requests from clients to a server to avoid overhead and ensure fair usage.

https://scalabrix.medium.com/system-design-concepts-rate-limiter-9d4b27af2d90

Why?
- **_Prevent Resource Exhaustion:_** _Ensures that no single client or group of clients consumes excessive resources, preserving system capacity for other users._
- **_Improve System Resilience:_** _Shields backend systems from sudden surges in traffic, preventing crashes or degraded performance during spikes._
- **_Enforce fair usage policies:_** _Allocates resources evenly across users or tenants, preventing monopolization by high-traffic clients._

## Token Bucket
The **Token Bucket Algorithm** is like a bucket that gets filled with tokens over time. Each token lets you make one request. If you make too many requests and the bucket runs out of tokens, you have to wait until more tokens are added. It helps control how many requests you can make while allowing some flexibility for quick bursts.

**Eg.** : _Imagine you can make 10 requests per second. Every second, the bucket gets 10 new tokens (1 token = 1 request). If you make a request, a token is removed. If the bucket runs out of tokens because you made too many requests, you’ll have to wait for more tokens to be added. This way, it allows short bursts (if tokens are available) but controls the overall request rate to stay within the limit._

![[Pasted image 20250324234844.png]]


**Concept**

1. **Tokens as Currency:** The bucket is a container that holds “tokens.” Each token represents permission for a single request.
2. **Token Generation:** Tokens are added to the bucket at a fixed rate (RRR) over time, which defines the rate-limiting threshold. For example, if the rate is 10 tokens per second, the bucket will accumulate up to 10 tokens every second.

**3. Request Consumption:** When a request arrives, the algorithm checks if there are enough tokens in the bucket. If a token is available, it is consumed, and the request is processed. If no tokens are left, the request is denied or queued.

**4. Bucket Capacity (CCC):** The bucket has a maximum capacity (CCC) that defines the maximum number of tokens it can hold. Once the bucket is full, any new tokens generated are discarded until a token is consumed.

![[Pasted image 20250324234850.png]]
## Leaky Bucket

The **Leaky Bucket Algorithm** is like a bucket with a small hole at the bottom. Water (requests) drips out at a steady rate, no matter how fast it’s poured in. If the bucket overflows because too much water is added too quickly, the extra water is spilled (requests are rejected). This ensures a smooth, consistent flow of requests to the system.

![[Pasted image 20250324234942.png]]

**Concept**

1. **Incoming Requests as Water:** Requests (or packets) are treated as drops of water poured into the bucket.
2. **Fixed Outflow Rate:** The bucket leaks water at a constant rate, symbolizing the system’s capacity to process requests. This rate is predefined based on the system’s throughput capabilities.
3. **Bucket Overflow:** If incoming requests exceed the rate at which the bucket leaks and the bucket becomes full, any additional requests are dropped (rejected). This ensures that the system is not overwhelmed by sudden bursts of traffic.
4. **Queue-Like Behavior:** Requests are processed in the order they arrive, akin to a first-in, first-out (FIFO) queue, but limited by the bucket’s capacity.

**Rate Enforcement**

_Unlike the_ **_Token Bucket Algorithm_**_, which allows bursts of traffic up to a limit, the_ **_Leaky Bucket Algorithm_** _strictly enforces a constant outflow rate, smoothing traffic spikes and ensuring predictable load on downstream systems._

![[Pasted image 20250324235005.png]]


**Use Cases**

1. **_Video Streaming Services:_** _Video streaming platforms like Netflix or YouTube require a constant rate of data transfer to ensure uninterrupted playback. The Leaky Bucket smooths out bursts in data requests and ensures consistent stream delivery._
2. **_Payment Processing:_** _Payment gateways enforce rate limits to prevent overload or fraud detection systems from being triggered unnecessarily._


## Fixed Window Algorithm
The **Fixed Window Algorithm** works by splitting time into fixed intervals (like 1 minute) and allows a certain number of requests per interval (e.g., 100 requests per minute). If the limit is reached within the interval, extra requests are rejected until the next interval starts. It’s simple but can allow bursts of traffic at the boundaries of intervals.

![[Pasted image 20250324235041.png]]

**Concept**

1. **Time-Based Buckets:** The algorithm divides time into discrete, fixed intervals, known as **windows** (e.g., 1 second, 1 minute, 1 hour). Each window is assigned a counter that tracks the number of requests made during that interval.
2. **Request Count:** When a request is received, the algorithm checks if the total requests in the current window exceed the predefined limit. If the request count is under the limit, the request is allowed, and the counter is incremented. If the limit has already been reached, the request is rejected.
3. **Reset at Window Boundary:** At the end of each fixed window, the counter resets to zero, and a new counting cycle begins.

![[Pasted image 20250324235055.png]]

## Sliding Window Log Algorithm

The **Sliding Window Log Algorithm** is a rate-limiting technique designed for **high-precision rate enforcement**. Unlike previous algorithms such as the Fixed Window Algorithm, it provides fine-grained control by tracking each individual request within a sliding time window. This precision makes it particularly useful for scenarios like financial systems or APIs requiring strict compliance with rate limits.

![[Pasted image 20250324235124.png]]

**Concept**

1. **Timestamp Tracking:** Every incoming request is logged with a precise timestamp. These timestamps are stored in a data structure, typically a sorted list or a queue.
2. **Sliding Window Definition:** A **sliding window** is defined as the most recent TTT seconds (e.g., the last 1 minute). Only requests within this window are considered for rate limiting.
3. **Rate Checking:** When a new request arrives, the algorithm removes timestamps outside the current sliding window. The total count of requests in the sliding window is then checked against the allowed limit.
4. **Decision Making:** If the number of requests in the sliding window is less than the limit, the request is allowed. If the limit has been reached, the request is denied.

![[Pasted image 20250324235143.png]]





![[Pasted image 20250324235156.png]]

**Rate Limiting for Scalable System Design**

1. **_Set Dynamic and Scalable Limits:_** _Analyze historical traffic patterns to define limits that optimize resource usage while protecting the system under peak loads._
2. **_Implement Graceful Failure Responses:_** _Use HTTP 429 responses with clear retry instructions to ensure clients handle limits gracefully without degrading user experience._
3. **_Leverage Monitoring and Metrics:_** _Continuously log rate-limiting decisions for real-time auditing, debugging, and system performance insights._
4. **_Adopt Adaptive Rate Limiting:_** _Dynamically adjust limits based on system health, traffic patterns, or user tiers to ensure optimal scaling under varying conditions._

[[API GW]]