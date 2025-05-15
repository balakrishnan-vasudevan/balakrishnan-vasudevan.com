# Regional evacuation

Tags: disaster-recovery
Category: Articles
Company: Netflix
Status: Reading
URL: https://netflixtechblog.com/evolving-regional-evacuation-69e6cc1d24c6

we leverage an N+1 architecture where we treat Amazon Web Services (AWS) regions as fault domains, allowing us to withstand single region failures. In the event of an isolated failure we first pre-scale microservices in the healthy regions after which we can shift traffic away from the failing one. This pre-scaling is necessary due to our use of autoscaling, which generally means that services are right-sized to handle their current demand, not the surge they would experience once we shift traffic.

Two assumptions:

- Regional demand for all microservices (i.e. requests, messages, connections, etc.) can be abstracted by our key performance indicator, [stream starts per second](https://medium.com/netflix-techblog/sps-the-pulse-of-netflix-streaming-ae4db0e05f8a) (SPS).
- Microservices within healthy regions can be scaled uniformly during an evacuation.

player logging, authorization, licensing, and bookmarks were initially handled by a single monolithic service whose demand correlated highly with SPS. However, in order to improve developer velocity, operability, and reliability, the monolith was decomposed into smaller, purpose-built services with dissimilar function-specific demand.

Our edge gateway ([zuul](https://medium.com/netflix-techblog/zuul-2-the-netflix-journey-to-asynchronous-non-blocking-systems-45947377fb5c)) also sharded by function to achieve similar wins. The graph below captures the demand for each shard, the combined demand, and SPS. Looking at the combined demand and SPS lines, SPS roughly approximates combined demand for a majority of the day. Looking at individual shards however, the amount of error introduced by using SPS as a demand proxy varies widely.

![https://miro.medium.com/v2/resize:fit:670/1*lZ1vzIoNNEEl7dLrzGdyBA.png](https://miro.medium.com/v2/resize:fit:670/1*lZ1vzIoNNEEl7dLrzGdyBA.png)

Time of Day vs. Normalized Demand by Zuul Shard

Because of service decomposition, we understood that using a proxy demand metric like SPS wasn’t tenable and we needed to transition to microservice-specific demand. Unfortunately, due to the diversity of services, a mix of Java ([Governator](https://medium.com/netflix-techblog/governator-lifecycle-and-dependency-injection-ccb8011c7d5b)/Springboot with [Ribbon](https://medium.com/netflix-techblog/announcing-ribbon-tying-the-netflix-mid-tier-services-together-a89346910a62)/gRPC, etc.) and Node (NodeQuark), there wasn’t a single demand metric we could rely on to cover all use cases. To address this, we built a system that allows us to associate each microservice with metrics that represent their demand.

The microservice metrics are configuration-driven, self-service, and allows for scoping such that services can have different configurations across various shards and regions. Our system then queries [Atlas](https://medium.com/netflix-techblog/introducing-atlas-netflixs-primary-telemetry-platform-bd31f4d8ed9a), our time series telemetry platform, to gather the appropriate historical data.

The approach we took was to partition a microservice’s regional demand by aggregated device types (CE, Android, PS4, etc.). Unfortunately, the existing metrics didn’t uniformly expose demand by device type, so we leveraged distributed tracing to expose the required details. Using this sampled trace data we can explain how a microservice’s regional device type demand changes over time.

We can use historical device type traffic to understand how to scale the device-specific components of a service’s demand. For example, the graph below shows how CE traffic in us-east-1 changes when we evacuate us-west-2. The nominal and evacuation traffic lines are normalized such that 1 represents the ***max(nominal traffic)*** and the demand scaling ratio represents the relative change in demand during an evacuation **(i.e. *evacuation traffic/nominal traffic*)**.

![https://miro.medium.com/v2/resize:fit:700/1*Gjo6bvqjEtNjot68OAsW_g.png](https://miro.medium.com/v2/resize:fit:700/1*Gjo6bvqjEtNjot68OAsW_g.png)

Nominal vs Evacuation CE Traffic in US-East-1

We can now combine microservice demand by device and device-specific evacuation scaling ratios to better represent the change in a microservice’s regional demand during an evacuation — i.e. the microservice’s device type weighted demand scaling ratio. To calculate this ratio (for a specific time of day) we take a service’s device type percentages, multiply by device type evacuation scaling ratios, producing each device type’s contribution to the service’s scaling ratio. Summing these components then yields a device type weighted evacuation scaling ratio for the microservice.