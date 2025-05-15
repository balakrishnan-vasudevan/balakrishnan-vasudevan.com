**Name:** The four Golden Signals of Monitoring
**Type:** Article/Blog
**Status:** Pending
**Link:** https://sysdig.com/blog/golden-signals-kubernetes/

The four golden signals of monitoring are latency, traffic, errors, and saturation. If you can only measure four metrics of your user-facing system, focus on these four.

**Table of Contents**

- [Latency](#Latency)
- [Traffic](#Traffic)
- [Errors](#Errors)
- [Saturation](#Saturation)

# Latency

The time it takes to service a request. It’s important to distinguish between the latency of successful requests and the latency of failed requests. For example, an HTTP 500 error triggered due to loss of connection to a database or other critical backend might be served very quickly; however, as an HTTP 500 error indicates a failed request, factoring 500s into your overall latency might result in misleading calculations. On the other hand, a slow error is even worse than a fast error! Therefore, it’s important to track error latency, as opposed to just filtering out errors.

# Traffic

A measure of how much demand is being placed on your system, measured in a high-level system-specific metric. For a web service, this measurement is usually HTTP requests per second, perhaps broken out by the nature of the requests (e.g., static versus dynamic content). For an audio streaming system, this measurement might focus on network I/O rate or concurrent sessions. For a key-value storage system, this measurement might be transactions and retrievals per second.

# Errors

The rate of requests that fail, either explicitly (e.g., HTTP 500s), implicitly (for example, an HTTP 200 success response, but coupled with the wrong content), or by policy (for example, "If you committed to one-second response times, any request over one second is an error"). Where protocol response codes are insufficient to express all failure conditions, secondary (internal) protocols may be necessary to track partial failure modes. Monitoring these cases can be drastically different: catching HTTP 500s at your load balancer can do a decent job of catching all completely failed requests, while only end-to-end system tests can detect that you’re serving the wrong content.

One thermometer for the errors happening in Kubernetes is the Kubelet. You can use several Kubernetes State Metrics in Prometheus to measure the amount of errors.

The most important one is `kubelet_runtime_operations_errors_total`, which indicates low level issues in the node, like problems with container runtime.

If you want to visualize errors per operation, you can use `kubelet_runtime_operations_total` to divide.

# Saturation

How "full" your service is. A measure of your system fraction, emphasizing the resources that are most constrained (e.g., in a memory-constrained system, show memory; in an I/O-constrained system, show I/O). Note that many systems degrade in performance before they achieve 100% utilization, so having a utilization target is essential.

In complex systems, saturation can be supplemented with higher-level load measurement: can your service properly handle double the traffic, handle only 10% more traffic, or handle even less traffic than it currently receives? For very simple services that have no parameters that alter the complexity of the request (e.g., "Give me a nonce" or "I need a globally unique monotonic integer") that rarely change configuration, a static value from a load test might be adequate. As discussed in the previous paragraph, however, most services need to use indirect signals like CPU utilization or network bandwidth that have a known upper bound. Latency increases are often a leading indicator of saturation. Measuring your 99th percentile response time over some small window (e.g., one minute) can give a very early signal of saturation.

Finally, saturation is also concerned with predictions of impending saturation, such as "It looks like your database will fill its hard drive in 4 hours."

In order to correctly measure, you should be aware of the following:

- What are the consequences if the resource is depleted? It could be that your entire system is unusable because this space has run out. Or maybe further requests are throttled until the system is less saturated.
- Saturation is not always about resources about to be depleted. It’s also about over-resourcing, or allocating a higher quantity of resources than what is needed. This one is crucial for cost savings.

Measuring saturation in Kubernetes

Since saturation depends on the resource being observed, you can use different metrics for Kubernetes entities:

- `node_cpu_seconds_total` to measure machine CPU utilization.
- `container_memory_usage_bytes` to measure the memory utilization at container level (paired with `container_memory_max_usage_bytes`).
- The amount of Pods that a [Node](https://sysdig.com/learn-cloud-native/kubernetes-101/what-is-a-kubernetes-node/) can contain is also a Kubernetes resource.


### Apdex Score

As described above, latency information may not be informative enough:

- Some users might perceive applications as slower, depending on the action they are performing.
- Some users might perceive applications as slower, based on the default latencies of the industry.

This is where the Apdex (Application Performance Index) comes in. It’s defined as:

[![Apdex formula](https://sysdig.com/wp-content/uploads/GoldenSignals-06.png)](https://sysdig.com/wp-content/uploads/GoldenSignals-06.png)

Where t is the target latency that we consider as reasonable.

- Satisfied will represent the amount of users with requests under the target latency.
- Tolerant will represent the amount of non-satisfied users with requests below four times the target latency.
- Frustrated will represent the amount of users with requests above the tolerant latency.

The output for the formula will be an index from 0 to 1, indicating how performant our system is in terms of latency.