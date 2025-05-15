#async-processing 
https://blog.twitter.com/engineering/en_us/topics/infrastructure/2020/deleting-data-distributed-throughout-your-microservices-architecture

The erasure pipeline we’ve described thus far has a few key requirements. It must:

- Accept incoming erasure requests
- Track and persist which pieces of data have been deleted
- Call synchronous APIs to delete data
- Publish erasure events for asynchronous erasure
- Generate an offline dataset of erasure events

An example erasure pipeline might look like this:

![[Pasted image 20250309005025.png]]

Light green components are built by you. Dark green are built by partner teams. 
**Common Problems**

The first issue is service outages and [network partitions](https://en.wikipedia.org/wiki/Network_partition "Wikipedia article: Network Partition"). An erasure pipeline needs to be resilient to outages. Its goal is to succeed at erasure, so it can retry its tasks when service has been restored. A simple way to accomplish this is to ensure that all erasure tasks are replay-able. When there’s an outage, we simply replay any erasure events that were dropped. The erasure tracking system knows which erasure events have yet to fully be processed and can re-publish those..

**Maintenance**

This delegation can be achieved by putting each data-owning team on call for their erasure tasks. Maintenance of a pipeline like this, which combines disparate tasks into a pipeline with one [SLA](https://en.wikipedia.org/wiki/Service-level_agreement "Wikipedia article: Service Level Agreement"), can only scale if each team takes responsibility for their part in erasure.

At Twitter, we expect each team that owns an erasure task to place [alerts](https://blog.twitter.com/engineering/en_us/a/2016/observability-at-twitter-technical-overview-part-ii.html "Twitter Engineering Blog: Observability at Twitter: technical overview, part II") on the success of that task. We supplement these with an alert on the overall success of erasure event processing with an SLA of days or weeks. This lets us promptly catch erasure pipeline issues while directing issues with individual erasure tasks to the responsible team.

**Testing**

Testing a distributed pipeline like this one follows the same principles we’ve been discussing: each data-owning team is responsible for testing their erasure tasks. All you need to do as the erasure pipeline owner is generate test events that they can respond to.

The challenge is coordinating test data creation in the systems owned by your partner teams. In order to integration test their own erasure tasks, these partners need test data to exist before you trigger an erasure event. One solution is a testing framework that pairs test data generation with a cron job that publishes erasure events some time after test data has been created.

**Future Direction**

The complexity of an erasure pipeline can be greatly reduced by [implementing an abstraction](https://dl.acm.org/doi/10.1145/3241653.3241654 "ACM publication: A domain-specific language for microservices") like a [data access layer](https://en.wikipedia.org/wiki/Data_access_layer "Wikipedia article: Data Access Layer") or data catalog for the data living in your online microservices and offline warehouses. Twitter is [moving in this direction](https://www.youtube.com/watch?v=E1gDNHZr1NA) to simplify the architecture necessary for complex processing tasks like data deletion. Data access layers or data catalogs index the data needed to satisfy an erasure request and enable processing of that data. This unifies data deletion outcomes with data ownership responsibilities.