#observability 
Source: https://blog.twitter.com/engineering/en_us/a/2013/observability-at-twitter
Visibility into the health and performance of our diverse service topology has become an important driver for quickly determining the root cause of issues, as well as increasing Twitter’s overall reliability and efficiency.

To understand the health and performance of our services, many things need to be considered together: operating systems, in-house and open-source JVM-based applications, core libraries such as [Finagle](http://twitter.github.io/finagle/) , storage dependencies such as caches and databases, and finally, application-level metrics.

![[Pasted image 20231110101450.png]]
Collection:

- implemented via in-memory counters and approximate histograms in a service or application memory space
- exported to Observability stack over a consistent interface
- An endpoint is generally an HTTP server that serves a consistent view of all metrics it exports
- applications commonly export anywhere from 50 to over 10,000 individual metrics per instance.
- For applications and metrics which do not use our core common libraries, data is made available via a host-agent over the same HTTP interface. This includes machine and operating system statistics, such as disk health, CPU, memory, and overall network traffic.
- All metrics are identified by multiple dimensions, including an underlying service name, and the origin of the data: such as a host, dynamically scheduled application instance identifier, or other identifiers specific to the service, and a metric name.
- Numerical metrics are written to a time series database.
- Batch processing and non-numeric values - data routed to HDFS using Scribe. (HDFS = Hadoop Distributed File System HDFS is a distributed file system that handles large data sets running on commodity hardware. It is used to scale a single Apache Hadoop cluster to hundreds (and even thousands) of nodes. HDFS is one of the major components of [Apache Hadoop](https://www.ibm.com/analytics/hadoop) , the others being [MapReduce](https://www.ibm.com/topics/mapreduce) and YARN.)
    - Scalding and Pig jobs can be run to produce reports that are not time sensitive.
- Determining the network location of applications running in a multi-tenant scheduled environment such as [Mesos](http://mesos.apache.org/)  adds additional complexity to metric collection when compared to ones deployed on statically allocated hosts. - Zookeeper helps with dynamic service discovery to see where an application is running.
- Data centralized for use in collector configurations, queried multiple times by users and automated systems.
- System also has a self-service feature to collect data at user-specified interval and serve it from an ephemeral store.
- Storage: In-house developed time series storage and query service which served as the abstraction layer for a multitude of Observability products.
- Separate clusters for different data sets.
- A typical production instance of the time series database is based on four distinct Cassandra clusters, each responsible for a different dimension (real-time, historical, aggregate, index) due to different performance constraints.
- Archival data is stored at a lower resolution for trending and long term analysis, whereas higher resolution data is periodically expired. Aggregation is generally performed at write-time to avoid extra storage operations for metrics that are expected to be immediately consumed.
- For Observability, query functionality is exposed as a service by our time series database over HTTP and Thrift.
- Engineers use the unified query language to retrieve and plot time series data on charts using a web application called Viz. A chart is the most basic visualization unit in Observability products
- Our monitoring system allows users to define alert conditions and notifications in the same query language they use for ad hoc queries and building dashboards.

Two other significant systems:

1. Zipkin - Distributed tracing system
2. In-house exception logging and reporting application