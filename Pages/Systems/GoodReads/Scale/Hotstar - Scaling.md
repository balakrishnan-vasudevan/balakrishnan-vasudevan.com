# Scaling Disney Hotstar

Tags: scale
Category: Articles
Company: Disney
Status: Not started
URL: https://blog.hotstar.com/scaling-infrastructure-for-millions-from-challenges-to-triumphs-part-1-6099141a99ef

[https://miro.medium.com/v2/resize:fit:700/0*UmmWIe_9UexckOQv](https://miro.medium.com/v2/resize:fit:700/0*UmmWIe_9UexckOQv)

Disney+ Hotstar is one of the largest OTT providers in India. The platform also provides live-streaming services to millions of customers nationwide. This is the first article in a series of blogs that will describe how we **scaled the Disney+ Hotstar infrastructure** to serve record-breaking 59 Million Concurrent streams. 🚀

Before the ODI 🏏 World Cup 2023, we had hit a peak concurrency of around 25 million — managed on two Kubernetes clusters.

For the 2023 Asia Cup and World Cup events, we introduced the ‘Free on Mobile’ 🆓 offering, to provide a delightful experience to as many cricket lovers as possible.

This change prompted a re-evaluation and redesign of our infrastructure landscape as free viewership was expected to attract more users to the platform (Remember, We are a nation crazy for cricket 🏏 😀). Based on our modeling, we ought to be prepared to cater to anywhere near 50 million concurrent streams, an unprecedented number for anyone in the industry.

This challenge became even more exciting as we needed to support this on our brand new X architecture, which had yet to be tested at such a high scale. ⚔️ [[Refer to this interesting blog from our Chief Architect to know why we rearchitected our app](https://blog.hotstar.com/hotstar-x-journey-part-1-why-rewrite-d7042de21bcf)].

![https://miro.medium.com/v2/resize:fit:480/0*ufR1abjkh8mwJdgk.gif](https://miro.medium.com/v2/resize:fit:480/0*ufR1abjkh8mwJdgk.gif)

# Background

We serve our users through multiple client platforms like mobile 📱(Android and iOS), Web 💻, and Connected TVs 📺to name a few. These client apps make calls to the external API Gateway (we use the CDNs as our external API Gateway), which runs security checks and executes a bunch of routing rules to forward the request to our internal API gateway. Our internal API gateway is fronted by a fleet of Application Load Balancers.

![https://miro.medium.com/v2/resize:fit:700/1*2I3EZdCTxMvynhcklucTaw.png](https://miro.medium.com/v2/resize:fit:700/1*2I3EZdCTxMvynhcklucTaw.png)

The internal API Gateway forwards the request to the relevant backend service, which processes it and sends back the response 🔁. These backend services use a bunch of managed and self-hosted database solutions. Every layer of this architecture needs carefully calibrated scaling to serve our users.

# Limits are not walls, but stepping stones to growth 📈

Our external API gateway (CDNs) scale themselves by deploying a cluster of edge and mid-gress nodes. These nodes serve well in most cases and are specially optimized for cache-hit scenarios (aka typical CDN use cases). However, for the cases where you have millions of requests being processed per second and the nodes are also acting as API gateway proxies, they must undertake responsibilities of running security checks 🛡, rate controls, request unpacking, etc. This puts stress on the compute capacity of these nodes and therefore caps the overall throughput that one can push through the external gateway.

Alright, so how do we figure out the spillover and what do we do about it?

Well, we ought to know our target throughput first, right? This is where the first challenge arose ⚠️. As we migrated from our legacy architecture to the new one, which is largely server-driven, the traffic patterns shifted and we had no baseline to understand the amount of traffic that our external API gateway should expect at peak. ⛰

We collected data from the past couple of months (including a mid-scale tournament from January 2023) to plot user journey-level traffic distributions during a Live stream. We mapped this data to the underlying API calls.

With the data, we identified our top 10 APIs in descending order of throughput. The initial numbers we arrived at were a clear show-stopper, and scaling our CDNs for that volume was neither cost nor time-effective.

We asked ourselves if we must treat all these requests the same way❓.

And that’s where we got our first breakthrough. 🥂

## Segregate to Accelerate 🚀

We segregated our APIs into two major buckets: cacheable and non-cacheable. Some of the features that are used during live-streaming events are highly cacheable (like scorecard, concurrency, key moments, etc). Serving highly cacheable features through leaner but optimal security checks 🛡 and rate controls helps reduce the stress on the compute capacity of the nodes, thereby multiplying the overall throughput capacity of our external gateways.

[https://miro.medium.com/v2/resize:fit:700/0*YTPC_eoAtcs6woGS](https://miro.medium.com/v2/resize:fit:700/0*YTPC_eoAtcs6woGS)

To ensure the availability of our critical features at a high scale, **we created a new CDN domain that offered optimized security and configuration rules for the cacheable paths**. This ensured better isolation and prevented any side effects from misconfigurations. We worked with multiple teams across the Disney+ Hotstar tech to migrate their cacheable API calls to this new CDN domain.

![https://miro.medium.com/v2/resize:fit:700/1*0Oqkm3yJzw1c8z-af_1XSQ.png](https://miro.medium.com/v2/resize:fit:700/1*0Oqkm3yJzw1c8z-af_1XSQ.png)

Next, to handle the massive network load for live streaming, we analyzed both peak RPS/RPM and network bandwidth at different concurrency levels. The demand was far beyond what our CDN providers could handle. To solve this, we went back to basics again. Our top priority always is to ensure:

***The video must play!***

**By adjusting the refresh rates for features like scorecards, Watch-more, live feeds, and key moments, we reduced the strain on our peak network bandwidth**. Additionally, we optimized routing and security configurations to save compute resources, as complex rule sets can spike up compute utilization at the edge servers.

# Spread and Scale

In a typical cloud environment ☁️, infrastructure involves multiple components like VPCs for network isolation, NAT Gateways for networking, Kubernetes clusters for container orchestration ☸️ (which is what we use at D+ Hotstar), and nodes for compute resources, all working in tandem to manage the network traffic flow and API orchestrations.

[https://miro.medium.com/v2/resize:fit:458/0*IB3f6Z7IAKgwxSXz](https://miro.medium.com/v2/resize:fit:458/0*IB3f6Z7IAKgwxSXz)

To effectively scale, it’s essential to understand the limitations of each infrastructure component.

## 1. NAT Gateways

We started by gathering data on the NAT Gateway network throughput, active connections, and packet transfers across all VPCs. Our analysis showed that one of the Kubernetes clusters was already using 50% of its network throughput capacity at just 1/10th of the peak traffic load. We enabled VPC flow logs for the NAT Gateway’s Elastic Network Interfaces (ENIs) and discovered that several services within the cluster were generating a significant amount of external traffic. Bummer 😿

***When it is not possible to scale up, scale out.***

In a standard private VPC setup, we usually configure one NAT Gateway per Availability Zone (AZ), with all subnets in that AZ routing external traffic through this single gateway. While this setup works for most applications, it can become a bottleneck if your application generates significant external traffic.

To resolve this, **we scaled out by provisioning NAT Gateways at the subnet level instead of the AZ level**. Additionally, we migrated some services to other clusters to rebalance the workloads. This adjustment significantly alleviated the pressure on the stressed NAT Gateways.

## 2. Kubernetes Worker Nodes

After resolving the NAT Gateway scaling issue, we turned our attention to network throughput at the Kubernetes worker node level. A high-scale load test revealed that several services were consuming substantial bandwidth — around 8 to 9 Gbps. The internal API Gateway which is deployed across all the clusters as the fronting ingress controller, was a major contributor to this. Nodes that ran multiple internal API Gateway pods simultaneously faced particularly high utilization, indicating an opportunity for optimization.

![https://miro.medium.com/v2/resize:fit:700/1*6Lve8tlXKu_VUan76mqPvQ.png](https://miro.medium.com/v2/resize:fit:700/1*6Lve8tlXKu_VUan76mqPvQ.png)

***In shared environments, distribute resources as evenly as you can.***

To address this, **we deployed high-throughput nodes (minimum 10 Gbps) across all clusters and applied topology spread constraints to the API Gateway**, ensuring each node hosted only a single pod. This strategy kept throughput per node at 2–3 Gbps, even during peak load. ⚖️

![https://miro.medium.com/v2/resize:fit:700/1*xy_D5quaHrQ5N9QwkOl_2Q.png](https://miro.medium.com/v2/resize:fit:700/1*xy_D5quaHrQ5N9QwkOl_2Q.png)

# Peeling the layers of K8s — Disney+ Hotstar way

After resolving network bandwidth challenges at various levels within our VPCs, we turned our attention to capacity planning for our Kubernetes clusters and began benchmarking to identify their limits. Prior to the 2023 tournaments, we had two self-managed Kubernetes clusters, but these clusters were hitting infrastructure limits and couldn’t scale up to support 50 million concurrency.

## Flattening the curve🌟

The Kubernetes control plane manages the cluster and the workloads running within it, comprising of key components like the API Server, Scheduler, Controller Manager, etc. We migrated to Amazon EKS, a cloud-managed service, where AWS handles the control plane, allowing us to focus solely on managing the data plane. This decision streamlined our operations and let us prioritize workload optimization over control plane maintenance.

During our migration to EKS clusters, we began benchmarking the EKS clusters to assess their ability to handle node scheduling, API server limits, and control plane scaling. This was crucial to ensure they could manage spikes in API server requests triggered by cluster scaling activities, which is typically how we scale up during live events.

We ran multiple tests to identify the limits, and had the following key takeaways:

- During the load test, the API server, Kubernetes controller manager, and scheduler remained operational. ✅
- When scaling the cluster to over 400 nodes simultaneously, we began experiencing API server errors. Although there was no downtime, the retries introduced a slight delay in scheduling pods and nodes during the scale-up process. ⚠️

We optimized our scaling configurations to minimize API server throttling during pre-scale-up. **By setting a step size that limited provisioning to 100–300 nodes per step, we reduced throttling risks** and automated the process to eliminate human error, resulting in smoother scaling and more efficient resource management.

## Make every resource count 🔧

Ahead of the 2023 World Cup, we faced a critical production incident in one of our Kubernetes clusters due to an IP address shortage. Our platform required over 400 worker nodes to schedule the requisite pods, but we couldn’t scale beyond 350 nodes. To understand this issue, let’s first explore how networking works in EKS clusters.

**Private Subnets**: We set up private subnets within a private VPC to assign IP addresses to the nodes and the pods running on them. Our configuration included three subnets across multiple availability zones, each with a /20 CIDR block, allowing approximately 4,090 IP addresses per subnet. With around 12.3K total IP addresses available, one might assume this would be sufficient for 12.3K pods and nodes. However, the situation is more complex, primarily due to the way IPs are managed in the EKS cluster.

**VPC CNI Plugin**: The VPC CNI plugin handles networking for EKS clusters, and two key settings directly affect how IPs are allocated to nodes and pods:

> MINIMUM_IP_TARGET: This defines the minimum number of IP addresses allocated to each node for pods. Initially set to 35, it meant each node reserved 35 IP addresses, regardless of actual usage.
> 
> 
> *WARM_IP_TARGET*: This setting controls how many additional IP addresses are pre-allocated for scaling. We set this to 10, which led to further over-allocation.
> 

With 35 IP addresses reserved for each node, even if the node didn’t have enough pods to use them, the result was that we could only scale to around 350 nodes (12.3k/35) across the three subnets.

To resolve this issue, **we quickly added new subnets with a larger /19 CIDR block, increasing the available IP addresses to approximately 48K**. We also updated our internal guidelines to use a /18 CIDR block for future clusters to prevent similar situations. We were fortunate that the cluster creation process was just starting, allowing us to make these changes without major disruptions.

The MINIMUM_IP_TARGET was set too high, forcing each node to reserve 35 IP addresses for pods, even when far fewer were needed. Combined with a WARM_IP_TARGET of 10, this configuration led to a 40–50% waste of IP addresses across nodes.

[https://miro.medium.com/v2/resize:fit:640/0*c4HNam9TKOxh6LO2](https://miro.medium.com/v2/resize:fit:640/0*c4HNam9TKOxh6LO2)

To optimize our usage, **we fine-tuned the VPC CNI settings. After several iterations, we reduced the MINIMUM_IP_TARGET to 20 and the WARM_IP_TARGET to 5**. This adjustment provided enough IP addresses for expected pod scaling while avoiding excessive pre-allocation.

The optimization worked perfectly 🎯. We reduced resource wastage, and throughout the World Cup 2023, we maintained just 40% IP utilization across our subnets, allowing us to scale services efficiently without any further resource shortages. 🚀

## Vertical Scaling to the rescue

During an internal high-scale load test, we observed one of our services experiencing unexpected traffic fluctuations across its pods, ranging from zero to several thousand requests per second. All the pods were healthy, and resources were within limits. The only thing unique to this service was that it had scaled beyond 1000 pods. After debugging the issue we identified a limit on the *Kubernetes Endpoint* object.

The Endpoints API provides a simple way to track network endpoints in Kubernetes. However, as clusters and services grow, the limitations of this API become apparent, particularly when scaling to large numbers of network endpoints. Since all endpoints for a service are stored in a single resource, this can lead to performance issues for Kubernetes components (especially the control plane) and increased network traffic and processing when endpoints change. When a service has over 1000 endpoints, Kubernetes truncates the data in the Endpoints object and sets an annotation***: endpoints.kubernetes.io/over-capacity: truncated***. This annotation is removed if the number of backend pods drops below 1000.

Although traffic continues to be sent to backends, any load balancing mechanism relying on the legacy Endpoints API only sends traffic to a maximum of 1000 endpoints. The same limit prevents manual updates to an Endpoint with more than 1000 endpoints. [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/service/#over-capacity-end) mitigate these issues and provide a platform for additional features like topological routing.

However, our API Gateway did not support service discovery using EndpointSlices, prohibiting us from adopting this alternative.

***When horizontal scaling is impractical, scale vertically*** 🔼

We went on to then identify all the services that required more than 1000 pods at higher concurrencies and collaborated with them to vertically scale up and cap the number of pods below 1000.

# Recap

To sum up, we learnt a good set of lessons in our journey to scale the Disney+ Hotstar infrastructure. The solutions stemmed from a deep dive into identifying bottlenecks, challenging conventional wisdom through first-principles thinking, and maintaining an unwavering focus on our end goals. Techniques like workload isolation, implementing graceful degradation levers, leveraging both horizontal and vertical scaling, distributing workloads across space and time, and fine-tuning system configurations played a pivotal role in our success. In our strive to ensure a seamless consumer experience, we also unlocked significant operational and efficiency wins for the platform 🚀

In the next set of articles, we will dive deep into the various technical choices we made and how we pulled together a mammoth task of setting up 10+ EKS clusters and migrating 200+ services across the organization to handle this scale. Stay tuned!

Passionate about breaking the barriers and solving problems at scale 👨‍💻? *Join us: [https://careers.hotstar.com/jobs](https://careers.hotstar.com/jobs)*