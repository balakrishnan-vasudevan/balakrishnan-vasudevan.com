# Goku TSDB Pinterest

Tags: time-series-db
Category: Articles
Company: Pintrest
Status: Not started
URL: https://medium.com/pinterest-engineering/improving-efficiency-of-goku-time-series-database-at-pinterest-part-2-08130f25b874

# Improving Efficiency Of Goku Time Series Database at Pinterest (Part 2)

![https://miro.medium.com/v2/resize:fill:88:88/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg](https://miro.medium.com/v2/resize:fill:88:88/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)

![https://miro.medium.com/v2/resize:fill:48:48/1*XiUFDZgSFl6n-MM2yXFifQ.png](https://miro.medium.com/v2/resize:fill:48:48/1*XiUFDZgSFl6n-MM2yXFifQ.png)

[Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----08130f25b874--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2Fef81ef829bcb&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fimproving-efficiency-of-goku-time-series-database-at-pinterest-part-2-08130f25b874&user=Pinterest+Engineering&userId=ef81ef829bcb&source=post_page-ef81ef829bcb----08130f25b874---------------------post_header-----------)

Published in

[Pinterest Engineering Blog](https://medium.com/pinterest-engineering?source=post_page-----08130f25b874--------------------------------)

·

11 min read

·

Mar 12, 2024

Monil Mukesh Sanghavi | Software Engineer, Real Time Analytics Team; Xiao Li | Software Engineer, Real Time Analytics Team; Ming-May Hu | Software Engineer, Real Time Analytics Team; Zhenxiao Luo | Software Engineer, Real Time Analytics Team; Kapil Bajaj | Manager, Real Time Analytics Team

![https://miro.medium.com/v2/resize:fit:700/1*Hujnqp_ULTXGaPrm1-P7hg.jpeg](https://miro.medium.com/v2/resize:fit:700/1*Hujnqp_ULTXGaPrm1-P7hg.jpeg)

At Pinterest, one of the pillars of the observability stack provides internal engineering teams (our users) the opportunity to monitor their services using metrics data and set up alerting on it. Goku is our in-house time series database providing cost efficient and low latency storage for metrics data. Underneath, Goku is not a single cluster but a collection of sub-service components including:

- Goku Short Term (in-memory storage for the last 24 hours of data, referred to as GokuS)
- Goku Long Term (ssd and hdd based storage for older data, referred to as GokuL)
- Goku Compactor (time series data aggregation and conversion engine)
- Goku Root (smart query routing)

You can read more about these components in the blog posts on [GokuS Storage](https://medium.com/pinterest-engineering/goku-building-a-scalable-and-high-performant-time-series-database-system-a8ff5758a181), [GokuL (long term) storage](https://medium.com/pinterest-engineering/gokul-extending-time-series-data-storage-to-serve-beyond-one-day-52264307364d), and [Cost Savings on Goku](https://medium.com/pinterest-engineering/cost-reduction-in-goku-9bf09696e99e), but a lot has changed in Goku since those were written. We have implemented multiple features that increased the efficiency of Goku and improved the user experience. In this 3 part blog post series, we will cover the efficiency improvements in 3 major aspects:

1. [Improving recovery time of both GokuS and GokuL (this is the total time a single host or cluster in Goku takes to come up and start serving time series queries)](https://medium.com/pinterest-engineering/improving-efficiency-of-goku-time-series-database-at-pinterest-part-1-7659b94796f4)
2. Improving query experience in Goku by lowering latencies of expensive and high cardinality queries
3. Reducing the overall cost of Goku at Pinterest

We’ll also share some learnings and takeaways from using Goku for storing metrics at Pinterest.

This 2nd blog post focuses on how Goku time series queries were improved. We will provide a brief overview of Goku’s time series data model, query model, and architecture. We will follow up with the improvement features we added including rollup, pre-aggregation, and pagination.

# Brief overview of the time series data model of Goku

The data model of a time series in Goku is very similar to OpenTSDB’s (which Goku replaced) data model. You can find more details [here](http://opentsdb.net/docs/build/html/user_guide/writing/index.html#data-specification). Here’s a quick overview of the Goku TimeSeries data model.

**A time series metadata or key** consists of the following:

![https://miro.medium.com/v2/resize:fit:700/1*zaUDdaOJ43FlSJtp8dFq3w.png](https://miro.medium.com/v2/resize:fit:700/1*zaUDdaOJ43FlSJtp8dFq3w.png)

**The data part of a time series, which we refer to as time series stream,** consists of **data points** that are time value pairs, where time is in unix time and value is a numerical value.

![https://miro.medium.com/v2/resize:fit:700/1*3qS2NbqvZXMBXb78o1J9oQ.png](https://miro.medium.com/v2/resize:fit:700/1*3qS2NbqvZXMBXb78o1J9oQ.png)

Multiple hosts can emit time series for a unique metric name. For example: cpu,memory,disk usage or some application metric. The host-specific information is part of one of the tags mentioned above. For example: tag- key == host and value == host name.

![https://miro.medium.com/v2/resize:fit:700/1*4wohgdvmu0s--TNSFcCdoA.png](https://miro.medium.com/v2/resize:fit:700/1*4wohgdvmu0s--TNSFcCdoA.png)

A cardinality of a metric (i.e. metric name) is defined as the total number of unique timeseries for that metric name. A unique time series has a unique combination of tag keys and values. You can understand more about cardinality [here](http://opentsdb.net/docs/build/html/user_guide/writing/index.html#time-series-cardinality).

For example, the cardinality of the metric name “proc.stat.cpu” in the above table is 5, because the combination of tag value pairs along with the metric name of each of these 5 timeseries do not repeat. Similarly, the cardinality of the metric name “proc.stat.mem” is 3. Note how we represent a particular string (be it metric name or tag value) as a unique color. This is to show that a certain tag value pair can be present in multiple time series, but the combination of such strings is what makes a time series unique.

# Brief overview of the time series query model of Goku

Goku uses [apache thrift](https://thrift.apache.org/) for Query RPC. The query model of Goku is very similar to OpenTSDB’s query model specified [here](http://opentsdb.net/docs/build/html/user_guide/query/index.html#). To summarize, a query to Goku Root is similar to the request specified below:

[https://miro.medium.com/v2/resize:fit:648/0*4iFa_B4mid8V0gth](https://miro.medium.com/v2/resize:fit:648/0*4iFa_B4mid8V0gth)

Let’s go over the important options in the request structure above:

- **metricName** — metric name without the tag combinations
- **list<Filter>** — filters on tag values like pattern match, wildcard, include/ exclude tag value (can be multiple), etc.
- **Aggregator** — sum/ max/ min/ p99/ count/ mean/ median etc. on the group of timeseries
- **Downsample** — user specified granularity in time returned in results
- **Rollup aggregation/ interval** — downsampling at a time series level. This option becomes mandatory in long range queries (you will see the reason below in Rollup).
- **startTime, endTime** — range of query

The query response looks as follows:

[https://miro.medium.com/v2/resize:fit:556/0*96RiOmdWiXvrWkmk](https://miro.medium.com/v2/resize:fit:556/0*96RiOmdWiXvrWkmk)

# Brief overview of the time series query path of Goku

[https://miro.medium.com/v2/resize:fit:700/0*EQMZvHDZLYIEolLK](https://miro.medium.com/v2/resize:fit:700/0*EQMZvHDZLYIEolLK)

The monitoring and alerting framework at Pinterest (internally called statsboard) query client sends QueryRequest to Goku Root, which forwards it to the leaf clusters (GokuS and/ or GokuL) based on the query time range and the shards they host. The leaf clusters do the necessary grouping (filtering), interpolation, aggregation, and downsampling as needed and respond to the Goku Root with QueryResponse. The Root will again do the aggregation if necessary and respond to the statsboard query client with QueryResponse.

Let’s now look at how we improved the query experience.

# Rollup

Goku supports the lowest time granularity of 1 second in the time series stream. However, having such fine granularity can impact the query performance due to the following reasons:

- Too much data (too many data points) over the network for a non downsample raw query
- Expensive computation and hence cpu cost while aggregating because of too many data points
- Time consuming data fetch, especially for GokuL (which uses SSD, HDD for data storage)

For old metric data residing in GokuL, we decided to also store rolled up data to boost query latency. Rolling up means reducing the granularity of the time series data points by storing aggregated values for the decided interval. For example: A raw time series stream

![https://miro.medium.com/v2/resize:fit:700/1*AM6PqF7pXwX_Y6PVjEkZgA.png](https://miro.medium.com/v2/resize:fit:700/1*AM6PqF7pXwX_Y6PVjEkZgA.png)

when aggregated using rollup interval of 5 and rollup aggregators of sum, min, max, count, average will have 5 shorter time series streams as follows:

![https://miro.medium.com/v2/resize:fit:700/1*Khtr3YVGS4hEqpQiw--D_w.png](https://miro.medium.com/v2/resize:fit:700/1*Khtr3YVGS4hEqpQiw--D_w.png)

The following table explains the tiering and rollup strategy:

![https://miro.medium.com/v2/resize:fit:700/1*W1VLpVZt_Djir41KIOzQIA.png](https://miro.medium.com/v2/resize:fit:700/1*W1VLpVZt_Djir41KIOzQIA.png)

Rollup benefitted the GokuL service in 3 ways:

- Reduced the storage cost of abundant raw data
- Decreased the data fetch cost from ssd, reduced the cpu aggregation cost, and thus reduced the query latency
- Some queries that would time out from the OpenTSDB supporting HBase clusters would return successful query results from GokuL.

The rollup aggregation is done in the Goku compactor (explained [here](https://medium.com/pinterest-engineering/gokul-extending-time-series-data-storage-to-serve-beyond-one-day-52264307364d)) before it creates the sst files containing the time series data to be stored in the rocksDB based GokuL instances.

In production, we observe that p99 latency of queries using rolled up data is almost 1000x less than queries using raw data.

P99 latency for GokuL query using raw data is almost a few seconds

[https://miro.medium.com/v2/resize:fit:700/0*sq0TcBphxc0ms_Gi](https://miro.medium.com/v2/resize:fit:700/0*sq0TcBphxc0ms_Gi)

GokuL query using rollup data has p99 in milliseconds.

[https://miro.medium.com/v2/resize:fit:700/0*zZlAfze2XYE7LLCb](https://miro.medium.com/v2/resize:fit:700/0*zZlAfze2XYE7LLCb)

# Pre-aggregation

At query time, Goku responds with an exception stating “cardinality limit exceeded” if the number of time series the query would select/ read from post filtering exceeds the pre-configured limit. This is to protect the Goku system resources due to noisy expensive queries. We observed queries for high cardinality metrics hitting timeouts, chewing up the system resources, and affecting the otherwise low latency queries. Often, after analyzing the high cardinality or timing out queries, we found that the tag(s) that contributed to the high cardinality of the metric were not even needed by the user in the final query result.

The pre-aggregation feature was introduced with the aim of removing these unwanted tags in the pre-aggregated metrics, thus, reducing the original cardinality, reducing the query latency, and successfully serving the query results to the user without timing out or consuming a lot of system resources. The feature creates and stores aggregated time series by removing unnecessary tags that the user mentions. The aggregated time series has tags that the user has specifically asked to preserve. For example:

![https://miro.medium.com/v2/resize:fit:700/1*CctPVwWKwHteyPI1Jex_GA.png](https://miro.medium.com/v2/resize:fit:700/1*CctPVwWKwHteyPI1Jex_GA.png)

If the user asks to enable pre-aggregation for the metric “app.some_stat” and wants to preserve only the cluster and az information, the pre-aggregated time series will look like this:

![https://miro.medium.com/v2/resize:fit:700/1*HX_PdwkHMn_6zV5YkbXoHA.png](https://miro.medium.com/v2/resize:fit:700/1*HX_PdwkHMn_6zV5YkbXoHA.png)

Note how the cardinality of the pre-aggregated metric is reduced from 5 to 3.

The pre-aggregated metrics are new time series created within Goku that do not replace the original raw time series. Also for the sake of simplicity, we decided to not introduce these metrics back into the typical ingestion pipeline that we emit to Kafka.

Here is a flow of how enabling pre-aggregation works:

1. Users experiencing high latency queries or queries hitting cardinality limit exceeded timeout decide to enable pre-aggregation for the metric.
2. The Goku team provides the tag combination distribution of the metric to the user. For example:

[https://miro.medium.com/v2/resize:fit:700/0*oJ_pmvhmJfGIPz6H](https://miro.medium.com/v2/resize:fit:700/0*oJ_pmvhmJfGIPz6H)

3. Users decide on the tags they want to preserve in the pre-aggregated time series. The “to be preserved” tags are called grouping tags. There is also an optional provision provided to select a particular tag key == tag value combination to be preserved and discard all other tag value combinations for that tag key. These provisions are referred to as conditional tags.

4. User is notified of the reduced cardinality and pre-aggregation is enabled for the metric which the user finalizes.

[https://miro.medium.com/v2/resize:fit:700/0*LR-hyIp5LSsnF6CP](https://miro.medium.com/v2/resize:fit:700/0*LR-hyIp5LSsnF6CP)

**Write path change:**

After consuming a data point for a metric from Kafka, the Goku Short Term host checks if the time series qualifies to be pre-aggregated. If the time series qualifies, the value of the datapoint is entered in an in memory data structure, which records the sum, max, min, count, and mean of the data seen so far. The data structure also emits 5 aggregated data points (aggregations mentioned above) for the time series with an internally modified Goku metric name every minute.

**Read Path change:**

In the query request to Goku Root, the observability statsboard client sends a boolean, which determines if the pre-aggregated version of the metric needs to be queried. Goku Root does the corresponding metric name change to query the right time series.

Success story: One production metric (in the example provided above) stored in Goku on which alerts were set was seeing high cardinality exceptions (cardinality ~32M during peak hours).

[https://miro.medium.com/v2/resize:fit:700/0*LMkJfweToOHdcgKY](https://miro.medium.com/v2/resize:fit:700/0*LMkJfweToOHdcgKY)

We reached out to the user to help understand the use case and suggested enabling pre-aggregation for their metric. Once we enabled pre-aggregation, the queries successfully completed with latencies below 100ms.

[https://miro.medium.com/v2/resize:fit:700/0*4kXCvgcaHfutOmAq](https://miro.medium.com/v2/resize:fit:700/0*4kXCvgcaHfutOmAq)

We have onboarded more than 50 use cases for pre-aggregation.

# Pagination

During launch to production, a query timeout feature had to be implemented in Goku Long Term to avoid an expensive query consuming the server resources for a long time. This, however, resulted in users of expensive queries seeing timeouts and wastage of server resources even if it was for a short period of time (i.e. configured query timeout). To confront this issue, the pagination feature was introduced, which would promise a non timed out result to the end user of an expensive query, even though it may take longer than usual. It would also break/ plan the query in such a way that resource usage at the server is controlled.

The workflow of the pagination feature is:

1. Query client sends a PagedQueryRequest to Goku Root if the metric is in the list of pagination supported metrics.
2. Goku Root plans the query based on time slicing.
3. Goku Root and Query client have a series of request-response exchanges with the root server. This provides the query client with a hint of what should be the next start and end time range of the query and its own IP address so that the traffic managing envoy can route the query to the right server.

We have incorporated ~10 use cases in production.

# Future work

The following are ideas we have to further improve query experience in Goku:

## Tag-based aggregation in Goku

During compaction, generate pre-aggregated time series by aggregating on the high cardinality contributing tags like host, etc. Work with the client team to identify such tags. This will generate time series and increase the storage cost, but not by much. In the queries, if the high cardinality tags are not present, the leaf server will automatically serve using the pre-aggregated time series.

Currently, the client observability team already has a feature in place to remove the high cardinality contributing host tag from a set of long term metrics. In the future, this can make use of the tag-based aggregation support in Goku, or Goku can provide the pointers to the observability team based on the query analysis above to include more long term metrics in their list.

## Post-query processing support in Goku

Many users of statsboard use the tscript post query processing to further process their results. The pushing of this processing layer into Goku can provide the following benefits:

1. Leverages extra compute resources available at Goku Root and Goku Leaf (GokuS and GokuL) clusters
2. Less data over the network leading to possible lower query latencies

Some examples of post query processing support include finding the top N time series, summing of the time series, etc.

## Backfilling support in pre-aggregation

We currently do not support pre-aggregated queries for a metric for a time range that falls before the time the metric was configured for pre-aggregation. For example: if a metric was enabled for pre-aggregation on 1st Jan 2022 00:00:00, users won’t be able to query pre-aggregated data for time before 31st Dec 2021 23:59:59. By supporting pre-aggregation during compaction, we can remove this limit and slowly but steadily (as larger tier buckets start forming), users will start seeing pre-aggregated data for older time ranges.

## SQL support

Currently, Goku is queryable only by using a thrift interface for RPC. SQL is widely used worldwide as a querying framework for data, and having SQL support in Goku would significantly help analytical use cases. We are starting to see an increasing demand for this and are exploring solutions.

## Read from S3

An ability to store and read from S3 would help Goku extend the ttl of raw data, and even extend the ttl of queryable metrics data. This could also prove cost beneficial to store metrics that are infrequently used.

# Special acknowledgement

Special thanks to Rui Zhang, Hao Jiang, and Miao Wang for their efforts in supporting the above features. A huge thanks to the Observability team for their help and support for these features at the user facing side.

# Next blog

In the next blog, we will focus on how we brought down the cost of the Goku service(s).

*To learn more about engineering at Pinterest, check out the rest of our [Engineering Blog](https://medium.com/pinterest-engineering) and visit our [Pinterest Labs](https://www.pinterestlabs.com/?utm_source=Medium&utm_campaign=engineering-Q12024&utm_medium=blogarticle&utm_content=Mukesh) site. To explore and apply to open roles, visit our [Careers](https://www.pinterestcareers.com/?utm_source=Medium&utm_campaign=engineering-Q12024&utm_medium=blogarticle&utm_content=Mukesh) page.*