#sdp


![[Pasted image 20250506135246.png]]
_[Source: Scalable system design patterns](http://horicky.blogspot.com/2010/10/scalable-system-design-patterns.html)_

Load balancers distribute incoming client requests to computing resources such as application servers and databases. In each case, the load balancer returns the response from the computing resource to the appropriate client. Load balancers are effective at:

- Preventing requests from going to unhealthy servers
- Preventing overloading resources
- Helping to eliminate a single point of failure

Load balancers can be implemented with hardware (expensive) or with software such as HAProxy.

Additional benefits include:

- **SSL termination** - Decrypt incoming requests and encrypt server responses so backend servers do not have to perform these potentially expensive operations
    - Removes the need to install [X.509 certificates](https://en.wikipedia.org/wiki/X.509) on each server
- **Session persistence** - Issue cookies and route a specific client's requests to same instance if the web apps do not keep track of sessions

To protect against failures, it's common to set up multiple load balancers, either in [active-passive](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#active-passive) or [active-active](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#active-active) mode.

Load balancers can route traffic based on various metrics, including:

- Random
- Least loaded
- Session/cookies
- [Round robin or weighted round robin](https://www.g33kinfo.com/info/round-robin-vs-weighted-round-robin-lb)
- [Layer 4](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#layer-4-load-balancing)
- [Layer 7](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#layer-7-load-balancing)

### Layer 4 load balancing
Layer 4 load balancers look at info at the [transport layer](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#communication) to decide how to distribute requests. Generally, this involves the source, destination IP addresses, and ports in the header, but not the contents of the packet. Layer 4 load balancers forward network packets to and from the upstream server, performing [Network Address Translation (NAT)](https://www.nginx.com/resources/glossary/layer-4-load-balancing/).

### Layer 7 load balancing
Layer 7 load balancers look at the [application layer](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#communication) to decide how to distribute requests. This can involve contents of the header, message, and cookies. Layer 7 load balancers terminate network traffic, reads the message, makes a load-balancing decision, then opens a connection to the selected server. For example, a layer 7 load balancer can direct video traffic to servers that host videos while directing more sensitive user billing traffic to security-hardened servers.

At the cost of flexibility, layer 4 load balancing requires less time and computing resources than Layer 7, although the performance impact can be minimal on modern commodity hardware.

### Horizontal scaling
Load balancers can also help with horizontal scaling, improving performance and availability. Scaling out using commodity machines is more cost efficient and results in higher availability than scaling up a single server on more expensive hardware, called **Vertical Scaling**. It is also easier to hire for talent working on commodity hardware than it is for specialized enterprise systems.

#### Disadvantage(s): horizontal scaling
- Scaling horizontally introduces complexity and involves cloning servers
    - Servers should be stateless: they should not contain any user-related data like sessions or profile pictures
    - Sessions can be stored in a centralized data store such as a [database](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#database) (SQL, NoSQL) or a persistent [cache](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#cache) (Redis, Memcached)
- Downstream servers such as caches and databases need to handle more simultaneous connections as upstream servers scale out

### Disadvantage(s): load balancer
- The load balancer can become a performance bottleneck if it does not have enough resources or if it is not configured properly.
- Introducing a load balancer to help eliminate a single point of failure results in increased complexity.
- A single load balancer is a single point of failure, configuring multiple load balancers further increases complexity.


1. Round Robin 
- Allocates incoming requests to each server in a circular sequence. It ensures an equal distribution of the workload among servers.  
  
1. Sticky Round Robin 
- Similar to Round Robin, but with the added feature of maintaining session persistence. Once a client is assigned to a server, subsequent requests from that client continue to be directed to the same server.  
  
1. Least Time
- Assigns requests to the server with the least expected processing time. This algorithm considers factors like server response time and current load.  
  
1. Least Connections 
- Directs traffic to the server with the fewest active connections. This helps distribute the load more evenly across servers, preventing overload on any single server.  
  
1. IP/URL Hash 
- Uses a hash function on the client's IP address or URL to determine which server should handle the request. This ensures that requests from the same client are consistently directed to the same server.  
  
1. Weighted Round Robin 
- Similar to Round Robin, but assigns different weights to servers based on their capacity or processing power. Servers with higher weights receive more requests, allowing for proportional load distribution.  
  
Each of these load balancing algorithms plays a crucial role in optimizing the performance and reliability of server clusters by efficiently distributing incoming requests.  

![[1700181216371.gif]]
### Source(s) and further reading

- [NGINX architecture](https://www.nginx.com/blog/inside-nginx-how-we-designed-for-performance-scale/)
- [HAProxy architecture guide](http://www.haproxy.org/download/1.2/doc/architecture.txt)
- [Scalability](http://www.lecloud.net/post/7295452622/scalability-for-dummies-part-1-clones)
- [Wikipedia](https://en.wikipedia.org/wiki/Load_balancing_\(computing\))
- [Layer 4 load balancing](https://www.nginx.com/resources/glossary/layer-4-load-balancing/)
- [Layer 7 load balancing](https://www.nginx.com/resources/glossary/layer-7-load-balancing/)
- [ELB listener config](http://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-listener-config.html)


Here’s a clear comparison between **client-side** and **server-side load balancing**:

---

## Client-Side Load Balancing

**How it works:**
- The client (or a client-side library) is responsible for deciding which server instance to send requests to.
- The client maintains a list of available servers (often fetched from a service registry like Consul, Eureka, or etcd).
- The client uses a load balancing algorithm (e.g., round-robin, random, least connections) to pick a server for each request.

**Examples:**
- Netflix Ribbon (Java)
- Spring Cloud LoadBalancer
- gRPC built-in load balancing
- Some JavaScript/TypeScript SDKs for microservices

**Pros:**
- Reduces load on a central load balancer.
- Can be more resilient to failures (clients can retry or switch servers quickly).
- Scales well as the number of clients increases.

**Cons:**
- Each client must implement load balancing logic.
- Clients need to keep the server list up-to-date (may require integration with a service registry).
- Harder to enforce global policies (e.g., rate limiting, security).

---

## Server-Side Load Balancing

**How it works:**
- Clients send requests to a single endpoint (the load balancer).
- The load balancer (hardware or software) forwards requests to backend servers based on its own algorithm.
- The client is unaware of the backend server topology.

**Examples:**
- NGINX, HAProxy, AWS Elastic Load Balancer, Google Cloud Load Balancer, F5, Traefik, Envoy

**Pros:**
- Centralized control and configuration.
- Easier to enforce security, rate limiting, and logging.
- Clients are simpler (just send requests to one endpoint).

**Cons:**
- The load balancer can become a bottleneck or single point of failure (unless made highly available).
- May add extra network hop/latency.
- Scaling the load balancer itself can be complex.

---

## Summary Table

| Feature                | Client-Side LB                | Server-Side LB                |
|------------------------|-------------------------------|-------------------------------|
| Who chooses backend?   | Client                        | Load balancer (server)        |
| Client needs registry? | Yes                           | No                            |
| Centralized control?   | No                            | Yes                           |
| Single point of failure?| No (unless registry fails)   | Yes (unless HA setup)         |
| Example tools          | Ribbon, gRPC, Spring Cloud    | NGINX, HAProxy, AWS ELB       |

---

**In short:**  
- Use **client-side** load balancing for microservices architectures where clients are smart and can handle service discovery.
- Use **server-side** load balancing for simpler clients, centralized control, or when you want to offload complexity from the client.



[[Deterministic Aperture]]

- [[Proxy]]