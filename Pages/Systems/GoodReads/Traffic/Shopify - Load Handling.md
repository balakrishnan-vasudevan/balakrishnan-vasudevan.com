

https://betterengineers.substack.com/p/how-shopify-handles-16000-request?utm_source=%2Finbox%2Fsaved&utm_medium=reader2


> [!Question] 
> Shopify faced significant scaling challenges due to unpredictable traffic spikes from flash sales, leading to database bottlenecks and affecting overall platform stability.
> - Flash sales occur when merchants announce limited inventory sales, leading to unpredictable spikes in traffic that are difficult to manage.
> - These events typically result in heavy write traffic to the database, complicating caching and resource provisioning.  
> - Shopify's architecture needed to be over-provisioned to handle these unpredictable traffic surges.

Evolution:
## Share Everything 
Multiple tenants share same resources enhancing capacity and resource utilization but risking outages affecting all tenants.
**Drawbacks**:
- The flash sales the database was used usually the the first thing that became a bottleneck just because there was so much write heavy traffic and lots of locking and contention and stuff like that so it was quickly becoming obvious that this one database is a single point of failure it was super expensive and basically the only way we could scale this product was to scale it vertically and throw more money on it.
    
- This led Shopify to implement database isolation and eventually move towards a "Parting" approach, where subsets of shops get dedicated resources, reducing the blast radius of potential issues

## Share Nothing
- Each tenant (shop) operates with completely isolated resources, meaning:
- Dedicated databases
- Separate application servers
- Independent infrastructure components

**The main trade-offs of this approach are:**

> Super expensive and wasteful and it's a nightmare to maintain

This architecture concept eventually influenced Shopify's "Parting" strategy, where they found a middle ground by isolating groups of shops rather than individual shops.

## Database Isolation + Scalability

In flash sales the database was used usually the the first thing that became a bottleneck just because there was so much write heavy traffic .  
we can solve this using vertical Scaling but It will increase Cost and for long term it will not be feasible to maintain.

- The implementation of database isolation allowed Shopify to partition data by shop, enabling better management of write-heavy traffic.
    
    Every single web worker and every single job worker would connect to all the databases and depending on which shop the request is for it would switch the connection to the to one of those databases.
- This approach provided more flexibility and scalability, allowing for the handling of flash sales without overwhelming the database.

## DR + Multi-DC

#### Initial Problem:

- Shopify was operating from a single datacenter
- If that datacenter failed, recovery would take an extremely long time
- The original datacenter had become difficult to maintain due to organic, unplanned growths
#### Solution Implementation:

- Added a second datacenter for redundancy
- Both datacenters were made identical, with one being active and the other idle
- The idle datacenter served as a backup for disaster recovery
- Could "flip" traffic between datacenters if needed
#### Evolution of the Strategy:

- Initially used manual failover processes
- Gradually moved towards automated solutions
- This setup allowed Shopify to:
    - Perform maintenance more easily
    - Reduce the risk of complete system failure
    - Have a clean, well-planned infrastructure in the second datacenter

## Podding
Still have this problem if one shop causes an outage it can affect the entire platform or if one shop has a flash sale it can theoretically stop all the other shops of resources**_.

So it might be possible that one shop is using all the web workers and the other shops don't handle any requests so the idea is that Shopify introduce a more strict level of isolation and this is :
![[Pasted image 20250330094353.png]]
**Podding** we basically mean is a group of resources that are dedicated to a subset of those shops and they have their own database they have their own web workers and so on. Each pod is active in exactly one data center at a time so you can think of this as the ideas that you take the shared everything architecture that we had before and instead of making it bigger you just have more of those and set them next to each other so this is much better for isolation because now if one of the shops in Pod 2 for example causes some kind of outage then that will only affect other shops in Pod 2 but none of the other parts will be affected by that.

## Sorting Hat - Routing
#### 1. DNS Routing Challenge:

- Shopify can't use DNS-based routing because they don't control their merchants' DNS
- Merchants point their custom domains to Shopify's IP addresses
- Multiple shops might share the same IP address but be in different datacenters or parts

#### 2. Solution: Layer Seven Routing

- Implemented routing at the HTTP level.
- Created custom software called "**Sorting Hat**" (named after Harry Potter reference).
- Functions as an HTTP request router.
#### 3. Technical Implementation:

- Uses Nginx with Lua scripting.
- Nginx is extended using custom Lua scripts.

**This allows Shopify to:**

- Create custom load balancing algorithms
- Route requests intelligently despite shared IP addresses

**This approach enables Shopify to manage complex routing requirements without relying on DNS or IP-layer solutions, making their multi-datacenter architecture possible.**

## Floating pods with floating capacity
Floating capacity refers to the ability of a multi-tenant architecture to dynamically allocate unused resources across various tenants, enhancing scalability and resource utilization.
So in a pods, if one the shop in one of the pods has a flash sale for example it would use all the dedicated capacity and if that's not enough then it would it can access this Floating capacity so it still has more resources available without being able to stop any of the other pods and the way this is implemented is as custom load balancing algorithm in nginx.

> **What will happen if one Datacenter fails , How request route to backup datacenter ,lets see in next section:**

## DC Failover
![[Pasted image 20250330094605.png]]

#### BGP (Border Gateway Protocol) Implementation:

- Shopify uses BGP for managing traffic between datacenters
    
- In case of failover ,they:
    - Withdraw IP addresses from the old datacenter.
    - Announce them in the new datacenter.
- This allows traffic redirection without requiring DNS changes.

#### Challenges:

- BGP propagation isn't instant.
- Takes seconds or minutes for changes to propagate across internet routers.
- During this delay, traffic might still route to the old datacenter.

## Load balancers
TCP connection that usually consists of multiple IP packets and you need to make sure that those packets are get routed to the same load balancer.  
if the first packet gets routed to correct Load Balancer and the second one gets write to a different one then ,the TCP session it doesn't know what to do with the second packet.

Shopify use multiple load balancers to Route the request.


![[Pasted image 20250330094657.png]]
