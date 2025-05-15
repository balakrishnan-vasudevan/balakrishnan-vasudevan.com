# Prioritized load shedding

Tags: load-shedding
Category: Articles
Company: Netflix
Status: Reading
URL: https://netflixtechblog.com/keeping-netflix-reliable-using-prioritized-load-shedding-6cc827b02f94

as recent as last year, our systems were susceptible to metaphorical traffic jams; we had on/off [circuit breakers](https://netflixtechblog.com/introducing-hystrix-for-resilience-engineering-13531c1ab362), but no progressive way to shed load. Motivated by improving the lives of our members, we’ve introduced priority-based progressive load shedding.

The resulting architecture that we envisioned with priority throttling and chaos testing included is captured below.

[https://miro.medium.com/v2/resize:fit:700/0*Oc0tXIGaeRBscW4f](https://miro.medium.com/v2/resize:fit:700/0*Oc0tXIGaeRBscW4f)

High level playback architecture with priority throttling and chaos testing

We decided to focus on three dimensions in order to categorize request traffic: throughput, functionality, and criticality. Based on these characteristics, traffic was classified into the following:

- **NON_CRITICAL**: This traffic does not affect playback or members’ experience. Logs and background requests are examples of this type of traffic. These requests are usually high throughput which contributes to a large percentage of load in the system.
- **DEGRADED_EXPERIENCE**: This traffic affects members’ experience, but not the ability to play. The traffic in this bucket is used for features like: stop and pause markers, language selection in the player, viewing history, and others.
- **CRITICAL**: This traffic affects the ability to play. Members will see an error message when they hit play if the request fails.

Using attributes of the request, the API gateway service ([Zuul](https://github.com/Netflix/zuul)) categorizes the requests into NON_CRITICAL, DEGRADED_EXPERIENCE and CRITICAL buckets, and computes a priority score between 1 to 100 for each request given its individual characteristics. The computation is done as a first step so that it is available for the rest of the request lifecycle.

When that happens requests with higher priority get preferential treatment. The higher priority requests will get served, while the lower priority ones will not. The implementation is analogous to a priority queue with a dynamic priority threshold. This allows Zuul to drop requests with a priority lower than the current threshold.

Zuul can apply load shedding in two moments during the request lifecycle: 

1. when it routes requests to a specific back-end service (service throttling) - Zuul can sense when a back-end service is in trouble by monitoring the error rates and concurrent requests to that service. Those two metrics are approximate indicators of failures and latency. When the threshold percentage for one of these two metrics is crossed, we reduce load on the service by throttling traffic.
2. at the time of initial request processing, which affects all back-end services (global throttling). - Another case is when Zuul itself is in trouble. As opposed to the scenario above, global throttling will affect *all* back-end services behind Zuul, rather than a *single* back-end service. The impact of this global throttling can cause much bigger problems for members. The key metrics used to trigger global throttling are CPU utilization, concurrent requests, and connection count. When any of the thresholds for those metrics are crossed, Zuul will aggressively throttle traffic to keep itself up and healthy while the system recovers.

When we’re in a bad situation (i.e. any of the thresholds above are exceeded), we progressively drop traffic, starting with the lowest priority. A cubic function is used to manage the level of throttling. If things get really, really bad the level will hit the sharp side of the curve, throttling everything.

![image.png](image%209.png)

As the overload percentage increases (i.e. the range between the throttling threshold and the max capacity), the priority threshold trails it very slowly: at 35%, it’s still in the mid-90s. If the system continues to degrade, we hit priority 50 at 80% exceeded and then eventually 10 at 95%, and so on.

Retry storms:

When Zuul decides to drop traffic, it sends a signal to devices to let them know that we need them to back off. It does this by indicating how many retries they can perform and what kind of time window they can perform them in.

The graph below shows a stable streaming availability metric [stream per second (SPS)](https://netflixtechblog.com/sps-the-pulse-of-netflix-streaming-ae4db0e05f8a) while Zuul is performing progressive load shedding based on request priority during the incident. The different colors in the graph represent requests with different priority being throttled.

[https://miro.medium.com/v2/resize:fit:700/0*_G5vqioIbN0uJ0A0](https://miro.medium.com/v2/resize:fit:700/0*_G5vqioIbN0uJ0A0)

Members were happily watching their favorite show on Netflix while the infrastructure was self-recovering from a system failure.