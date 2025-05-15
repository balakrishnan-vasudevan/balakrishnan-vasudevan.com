# How Agoda Solved Retry Storms to Boost System Reliability

Tags: reliability
Category: Articles
Company: Agoda
Status: Not started
URL: https://medium.com/agoda-engineering/how-agoda-solved-retry-storms-to-boost-system-reliability-9bf0d1dfbeee



# **How** Agoda Solved Retry Storms to Boost System Reliability


![https://miro.medium.com/v2/resize:fit:700/1*_FJcVWfGMB6yQkLM9d4HnA.png](https://miro.medium.com/v2/resize:fit:700/1*_FJcVWfGMB6yQkLM9d4HnA.png)

# Introduction

Have you ever found your service under siege by a relentless storm of retries from your clients? Or even from your clients’ clients? Maybe your service has unknowingly been the culprit, overwhelming others with a deluge of retries?

**Retry Storms** occur when a sudden surge in retries — often triggered by system slowdowns — leads to an overload, causing further degradation in service quality and potentially cascading failures. This article aims to explain the concept of Retry Storm and introduce a practical guide for using Envoy’s Retry Budgets to control and prevent such issues. By the end of this article, you’ll understand the mechanics behind Retry Storms and also some practical strategies to enhance your system’s resilience to maintain a seamless user experience.

# Understanding Retry Storms

Let’s start by imagining a digital enterprise dependent on a network of several interconnected microservices. Microservices are small, independent services that work together to perform complex tasks in modern applications.

Suppose you have ten microservices. Let’s call them S0 to S9, handling 100 requests per second(rps) initially. Each service interface includes a single retry meant to enhance resiliency. However, problems begin when S9 slows down, causing S8 to initiate retries. However, the retry from S8 to S9 fails because of the slowdown of S9 which leads to failure of its upstream client, S7. S7, in turn, starts its own retries, further burdening the already struggling S9. This additional load causes even more request failures, generating yet more retries. The retries propagate upward through the entire service chain, causing a cascade effect.

To better understand the scale of this issue, consider the original request volume as *N.* With each service interface allowing a retry, the subsequent level sends *2 × N* requests downstream. For *K* microservices in a request path, the bottom service faces 2*ᵏ ⁻¹ × N* requests. We can denote the total number of requests generated across the infrastructure with the following equation,

Exponential growth of requests in a retry storm

![https://miro.medium.com/v2/resize:fit:426/1*MdsxxYvUZlHDnTWq5kgYHQ.png](https://miro.medium.com/v2/resize:fit:426/1*MdsxxYvUZlHDnTWq5kgYHQ.png)

This geometric series shows how retries, originally designed to enhance reliability, can lead to significant overloads and outages in a Retry Storm. Let’s visualize the exponential growth of requests in the infrastructure due to retry storms.

Exponential growth of requests in a retry storm

[https://miro.medium.com/v2/resize:fit:700/0*fTFvi0SUI2OcCuRy](https://miro.medium.com/v2/resize:fit:700/0*fTFvi0SUI2OcCuRy)

Typically, Service 9 handles 100 requests per second (rps). During a Retry Storm, this can surge to 51,200 rps — 512 times the usual load!

![https://miro.medium.com/v2/resize:fit:630/0*U_Ww6FXA1bCxj63R.jpeg](https://miro.medium.com/v2/resize:fit:630/0*U_Ww6FXA1bCxj63R.jpeg)

# Introducing Retry Budgets

In the context of networked systems, a Retry Budget is a mechanism designed to control the number of retries allowed within a given period, thereby preventing the system from being overwhelmed by excessive retry attempts. The fundamental idea is to allocate a fixed percentage of the total requests as permissible retries, ensuring that retries do not exceed a manageable threshold.

Mathematically, this can be expressed as:

![https://miro.medium.com/v2/resize:fit:355/1*g6A1NLbFVY1hVQAFLdYRXg.png](https://miro.medium.com/v2/resize:fit:355/1*g6A1NLbFVY1hVQAFLdYRXg.png)

This equation ensures that the number of retries remains proportional to the outgoing request rate, thereby preventing exponential growth in retry traffic.

To illustrate the impact of retry budget, we can model the total number of requests generated in the infrastructure after applying a retry budget. For a system with 𝑘 services in its request path and a retry budget of *b*%, the total number of generated requests is:

![https://miro.medium.com/v2/resize:fit:439/1*nlX6AaXUG5Og4PMcywFNnw.png](https://miro.medium.com/v2/resize:fit:439/1*nlX6AaXUG5Og4PMcywFNnw.png)

Comparing this to the exponential growth of retries without a retry budget, we can see that the growth rate with a retry budget could be significantly lower, thus reducing the risk of infrastructure meltdown due to retry storm.

[https://miro.medium.com/v2/resize:fit:700/0*xdJWy_4Ho97nRFpn](https://miro.medium.com/v2/resize:fit:700/0*xdJWy_4Ho97nRFpn)

With a 5% Retry Budget applied, Service 9 would receive a maximum of 156 rps, which is just 1.56 times the usual load. Given proper provisioning for peak traffic and added safety factors, Service 9 should be able to handle this load comfortably.

# Retry Budget in Service Mesh

In modern microservice architectures, service mesh has become a critical component for managing service-to-service communication. A service mesh is a dedicated infrastructure layer that you can add to your applications. It allows you to transparently add capabilities like observability, traffic management, and security, without embedding them into your application code. This infrastructure layer is crucial for managing the complexity of distributed systems, especially as they scale.

At Agoda, we use Istio as our Service Mesh of choice to run on our private cloud. At the core of Istio’s data plane is Envoy, a high-performance proxy that handles all inbound and outbound traffic for the services within the mesh. Envoy is deployed as a sidecar proxy alongside each service pod, intercepting all network traffic to and from the service. This setup allows Envoy to provide advanced traffic management capabilities, including load balancing, traffic routing, failure recovery, and observability.

One of the key features of Envoy is its ability to implement sophisticated retry mechanisms, which can be fine-tuned using Retry Budgets. While Envoy natively supports Retry Budgets as part of its [**circuit breaker**](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/circuit_breaker.proto#config-cluster-v3-circuitbreakers-thresholds-retrybudget) settings, the official version of Istio which uses an extended version of envoy does not include this feature. At Agoda, we have implemented this feature in our custom fork of Istio to leverage Envoy’s Retry Budget capabilities within our service mesh.

## Key Terminologies

Before we dive into the Retry Budget configuration, let’s clarify some key Envoy terminologies:

- **Active Requests**: Defined in the global ResourceManager class, active requests refer to the requests that are currently bound to a connection pool connection and are awaiting response. In short, it means current requests inflight.
- **Active Pending Requests**: These are requests that have been accepted by the envoy worker thread but have yet to be attached to a connection from the connection pool.
- **Active Retries**: Concurrent retries or active retries are current retries inflight.
- **Retry Overflow**: It’s an envoy counter representing total requests not retried due to circuit breaking or exceeding the retry budget.

## Retry Budget in Envoy

Retry Budget in Envoy limits the number of concurrent retries based on two main criteria:

1. **Budget Percentage:** This specifies the limit on concurrent retries as a percentage of the sum of active requests and active pending requests. For example, if there are 100 active requests, 0 active pending requests and the budget percentage is set to 20%, Envoy will allow up to 20 concurrent retries.
2. **Minimum Retry Concurrency:** This defines the minimum number of concurrent retries that Envoy will allow, regardless of what the budget percentage yields. For instance, if this number is set to 5, but the budget percentage only allows for 4 retries, Envoy will still permit 5 retries.

By configuring Retry Budgets in Envoy, you can effectively control the retry behavior of your services, preventing the cascading failures typical of Retry Storms. In the next section, we will delve into the calculations and configurations required to implement Retry Budgets in your service mesh using Envoy.

![https://miro.medium.com/v2/resize:fit:630/0*qmOJuLjhMW3MOHDB.jpeg](https://miro.medium.com/v2/resize:fit:630/0*qmOJuLjhMW3MOHDB.jpeg)

# How to Calculate Envoy Retry Budget

Calculating the retry budget using Envoy’s cluster level statistics like **active requests** can be challenging. Instead, we’ll use more accessible, high-level metrics that most of us are already familiar with: requests and retry rates per second. Here’s how to step through the calculations based on the following assumption:

## Step-by-Step Calculation

1. **Assumptions and Baseline Metrics**:
- Collect metrics during peak load periods, such as traffic failover events. These peak values help set a retry budget that accommodates normal operations while protecting against retry storms.
- Focus on high-level metrics: Average Requests per Second and Max Retries per Second, rather than low-level metrics like active requests.

2. **Establishing the Relationship:** We assume the following relationship under nominal conditions, optimized to allow retries for transient failures:

![https://miro.medium.com/v2/resize:fit:544/1*AQ_wPpy_8co86Ts3ddrkjw.png](https://miro.medium.com/v2/resize:fit:544/1*AQ_wPpy_8co86Ts3ddrkjw.png)

From this, we can derive the formula for Max Active Retries:

Request and retry RPS over time

![https://miro.medium.com/v2/resize:fit:640/1*eSIj8IKaHmdG2ExjlkkJIw.png](https://miro.medium.com/v2/resize:fit:640/1*eSIj8IKaHmdG2ExjlkkJIw.png)

3. **Calculating the Retry Budget**:

Given the Retry Budget is defined as the ratio of Max Active Retries to Active Requests:

Request and retry RPS over time

![https://miro.medium.com/v2/resize:fit:384/1*CgAmdSjfJbQ0sCkY7vj-Yg.png](https://miro.medium.com/v2/resize:fit:384/1*CgAmdSjfJbQ0sCkY7vj-Yg.png)

Substituting the expression for Max Active Retries into this equation gives us:

Request and retry RPS over time

![https://miro.medium.com/v2/resize:fit:640/1*QTVfIZLMxyJZWRxXonaRYQ.png](https://miro.medium.com/v2/resize:fit:640/1*QTVfIZLMxyJZWRxXonaRYQ.png)

To illustrate this, let’s consider a service interface for which data was collected during peak traffic under nominal conditions.

Request and retry RPS over time

[https://miro.medium.com/v2/resize:fit:700/0*THAVWaWJ4ERFqj-b](https://miro.medium.com/v2/resize:fit:700/0*THAVWaWJ4ERFqj-b)

From the graph, we can observe the following metrics:

- **Max Retries per Second**: 5.77
- **Average Requests per Second**: 100.77

Using these values in our simplified formula:

![https://miro.medium.com/v2/resize:fit:648/1*E9B7v3_1eSMqObFqYCnJ_A.png](https://miro.medium.com/v2/resize:fit:648/1*E9B7v3_1eSMqObFqYCnJ_A.png)

This calculation indicates that the Retry Budget is approximately 0.057, or 5.7%. Therefore, to accommodate the retries generated during peak traffic under nominal conditions, we can set the Retry Budget at around 6%.

# Setting a Sensible Timeout for Reliable Retry Budgets

During downstream slowdowns, active requests might increase because the client Envoy now has to wait longer for a response from the downstream service. From the definition of retry budget, we know that the number of allowable active retries is directly proportional to the active requests and active pending requests, which means we might see the percentage of outbound retry rps compares to outbound request rps increases and might exceeds the configured retry budget percentage.

The configured timeout between service interfaces might influence this: a higher timeout on a slow downstream means more in-flight requests to a downstream, potentially overwhelming the connection pool of Envoy workers and resulting in a higher percentage of allowed retry rate during that period.

[https://miro.medium.com/v2/resize:fit:700/0*Dh9FCi71_3hWxUkx](https://miro.medium.com/v2/resize:fit:700/0*Dh9FCi71_3hWxUkx)

For example, during this particular production incident at Agoda, we observed an 8% of retry-rps compared to request-rps during the downstream slowdown with a 5% retry budget.

# Monitoring Retry Overflow

Once the retry budget is set, it’s crucial to monitor the retry overflow metrics. Observing retry overflows helps in identifying if the retry budget is too aggressive, which could impact the client-side success rate and potentially have business implications.

During the above incident, our retry budget mechanism effectively rejected excessive retries, preventing a possible retry storm and protecting the downstream services.

[https://miro.medium.com/v2/resize:fit:700/0*t-tExcA6G_1NERSe](https://miro.medium.com/v2/resize:fit:700/0*t-tExcA6G_1NERSe)

Future adjustment of the retry budget configuration based on real-time monitoring might be necessary to ensure that your system remains robust and resilient against fluctuations in traffic and transient failures.

# Tuning Retry Budget for Low Concurrency Services

The formula for calculating retry budgets works well for highly concurrent services. However, in cloud-based infrastructures, individual pods might experience lower concurrency while sending requests to a downstream cluster. This can result in retry budget yielding impractically low allowable retry numbers, sometimes less than one. Since any system can encounter transient issues that necessitate retries, it’s essential to address this issue.

![https://miro.medium.com/v2/resize:fit:700/1*ViZ-eu2Ibvo4vz-5gHLckg.png](https://miro.medium.com/v2/resize:fit:700/1*ViZ-eu2Ibvo4vz-5gHLckg.png)

## Setting a Minimum Retry Concurrency

Recalling our definition of minimum retry concurrency, we can define the **max allowable active retries** in the following formula,

aggregating traffic to internal gateway for clients having low outbound concurrency per pod.

![https://miro.medium.com/v2/resize:fit:652/1*qCNmgldyxtSMk8URaqmkBA.png](https://miro.medium.com/v2/resize:fit:652/1*qCNmgldyxtSMk8URaqmkBA.png)

By setting a minimum retry concurrency, we ensure that our system can still perform retries on any transient request failures, even when the number of active requests is low. This helps maintain reliability across a variety of traffic conditions.

## Aggregating Traffic to Internal Gateway

At Agoda, we use another approach to manage retries more effectively by converging traffic from all client pods to an internal gateway cluster which acts as a proxy middleware between a client and its downstream. By applying the retry budget at this gateway, we achieve higher overall concurrency and better control over the percentage of retries directed to downstream services. This method not only optimizes retry handling but also offers additional benefits, such as improved load balancing.

aggregating traffic to internal gateway for clients having low outbound concurrency per pod.

[https://miro.medium.com/v2/resize:fit:700/0*s3W63Ogd9gfD48pi](https://miro.medium.com/v2/resize:fit:700/0*s3W63Ogd9gfD48pi)

To ensure high availability and fault tolerance, we always set up the internal gateway with a minimum of 3 replicas and we built an auto scaling feature for it which depends on the CPU utilization of the gateway pods. Besides that we operate on active-active mode in our data centers for most of our API services, which helps us to do traffic failover to another DC in case we’ve some problem with the infrastructure. Read here to learn more about our [private cloud infrastructure](https://blog.pragmaticengineer.com/inside-agodas-private-cloud/).

# Configuring Retry Budgets: Service-Level vs. Endpoint-Level

When setting retry budgets, you have the choice of applying them at the service level or the endpoint level within a service. Each approach has distinct benefits and drawbacks.

## Service-Level Retry Budget

Setting a retry budget at the service level applies a unified budget across all endpoints of a downstream service. This method simplifies configuration and monitoring because you’re dealing with a single budget for the entire service. However, it can lead to issues if endpoints have different resource requirements and traffic patterns. High traffic on lightweight endpoints might permit excessive retries for resource-intensive endpoints, potentially overwhelming the service.

During this production incident, setting a 5% retry budget at the service level resulted in an overall allowance of retry rps of 6.5%, but heavy endpoints ended up using most of the budget, reaching up to 35%.

[https://miro.medium.com/v2/resize:fit:700/0*Pq2w8SKXxieu9Uug](https://miro.medium.com/v2/resize:fit:700/0*Pq2w8SKXxieu9Uug)

## Endpoint-Level Retry Budget

Applying retry budgets at the endpoint level offers granular control, allowing budgets to be tailored to the specific resource usage and traffic patterns of each endpoint. This prevents any single endpoint from dominating the retry budget and potentially affecting the performance of others. However, it increases the complexity of configuration and maintenance.

## **Comparison: Service-Level vs. Endpoint-Level Retry Budgets**

![https://miro.medium.com/v2/resize:fit:700/1*bcdUnhqfeAuadxYdjiXlPA.png](https://miro.medium.com/v2/resize:fit:700/1*bcdUnhqfeAuadxYdjiXlPA.png)

By choosing the right retry budget configuration, you can optimize for either simplicity or granularity, depending on the specific needs and characteristics of your services and endpoints.

# Conclusion

At Agoda, implementing Envoy’s retry budget has been proven effective in preventing retry storms, ensuring service uptime under varying load conditions. This strategic approach not only safeguards against potential outages but also optimizes resource utilization across our distributed systems by ensuring faster recovery. By judiciously managing retries, we uphold Agoda’s commitment to delivering unparalleled reliability and performance, essential in our journey to redefine excellence in global travel technology.

# References

- [Retry Budget Documentation](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/circuit_breaker.proto#config-cluster-v3-circuitbreakers-thresholds-retrybudget)
- [ResourceManager class in Envoy](https://github.com/envoyproxy/envoy/blob/85cfc785038e15b4d0231aa8e734c144545a2602/envoy/upstream/resource_manager.h)
- [Retry Budget calculation in ResourceManagerImpl](https://github.com/envoyproxy/envoy/blob/85cfc785038e15b4d0231aa8e734c144545a2602/source/common/upstream/resource_manager_impl.h#L156)
- [Istio as a Service Mesh](https://istio.io/latest/about/service-mesh/)

![https://miro.medium.com/v2/resize:fit:700/1*qKAAoep6HRc8EBXkqWLK5g.jpeg](https://miro.medium.com/v2/resize:fit:700/1*qKAAoep6HRc8EBXkqWLK5g.jpeg)