#observability , #logging-infra , #apache-spark, #apache-flume
**

Points to consider:

- Avoid logging personally identifiable information (PII), such as names, addresses, emails, and so on.
    
- Avoid logging sensitive information like credit card numbers, passwords, and so on.
    
- Avoid excessive information. Logging all information is unnecessary. It only takes up more space and affects performance. Logging, being an I/O-heavy operation, has its performance penalties.
    
- The logging mechanism should be secure and not vulnerable because logs contain the application’s flow, and an insecure logging mechanism is vulnerable to hackers.
    

  

Functional Requirements:

- Writing logs: The services of the distributed system must be able to write into the logging system.
    
- Searchable logs: It should be effortless for a system to find logs. Similarly, the application’s flow from end-to-end should also be effortless.
    
- Storing logging: The logs should reside in distributed storage for easy access.
    
- Centralized logging visualizer: The system should provide a unified view of globally separated services.
    

  

To fulfill another requirement of low latency, we don’t want the logging to affect the performance of other processes, so we send the logs asynchronously via a low-priority thread. By doing this, our system does not interfere with the performance of others and ensures availability.

Each service —> log data —> Accumulator —> Pub/Sub —> Blob storage

  

The following services will work on the pub-sub data:

- Filterer: It identifies the application and stores the logs in the blob storage reserved for that application since we do not want to mix logs of two different applications.
    
- Error aggregator: It is critical to identify an error as quickly as possible. We use a service that picks up the error messages from the pub-sub system and informs the respective client. It saves us the trouble of searching the logs.
    
- Alert aggregator: Alerts are also crucial. So, it is important to be aware of them early. This service identifies the alerts and notifies the appropriate stakeholders if a fatal error is encountered, or sends a message to a monitoring tool.
    

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXcYBjyH4R215oZz1naDIlpHet_Lc3Us1l3wKzx6vUzyBcxDox_2S39feAK15Qb8FzPK3cOxu20r1vMr0-_R36vtb_8FjU6z_PeWUlqMMNv9f_Qz7vmgMx-YPv--jVbRnDBm6KjFArVg34k5kO4SKkIT3DM?key=j4FcJWeNiYnhIt4RY32tSQ)

  

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXeqjMMwtKIimph7gqhLI5suI5AK4Fe6DJO6u9mFDQBmgrrY45KWOrA7kF0RUgQLB6X1UaH9LwXc3vJ8hUxiuuKTQwogfluIsS6HUfjcVVlXcqmgLJeIPklTd1xU9OMp30Y2mU-fW7hUkoxQ30P4OkiNyW8?key=j4FcJWeNiYnhIt4RY32tSQ)

  

[Apache Flume](https://flume.apache.org/) was the leading Hadoop based log aggregation tool. Once data was ingested on Hadoop, it was then analyzed using tools like [Apache Hive](https://hive.apache.org/), [Apache Pig](https://pig.apache.org/) and [Apache Spark](https://spark.apache.org/).

  

![](https://lh7-us.googleusercontent.com/docsz/AD_4nXc2HSqmagre7kLaFCRhIwARwsHm9cySraS9LyXlcf8knagBizcOYI6UKq4tTF1fj7O7ifAaDe8dUmHoZvB3MEHjrxIXinXa8R7nUJ5eSG-Y58PXok503oN-idcZpACpnpFo6O1D68c4tEtT4Jkjg9Ylmg?key=j4FcJWeNiYnhIt4RY32tSQ)

  
  

|   |   |   |
|---|---|---|
|Stage|Task|Tools|
|Logging libraries|These libraries can emit logs in a predefined format. So, the next step is to define an initial format that developers across the team agree on. This format does evolve as the project matures, but an agreed upon initial format is a great starting point.|log, glog, log4j|
|Forwarders and Agents|Both agents and forwarders collect logs from application output (e.g. log file or console) and forward them to a central location - hence these terms are used interchangeably, but there are subtle differences.<br><br>Forwarders are typically very lightweight, run on each host and forward logs to a central location with little to no post collection processing.  Run on the same host as the application. That’s why they are lightweight.  <br>Agents on the other hand are more sophisticated. They are typically deployed as a service on a dedicated host and can perform additional processing on the logs before forwarding them to a central location. This additional processing can include parsing, enrichment, filtering, sampling and more.   <br>Typically deployed as clustered service on dedicated hosts.|Forwarders - Examples are FluentBit, Filebeat, Logstash Forwarder, Vector etc.<br><br>  <br><br>Agents - Examples are FluentD, Logstash, Vector Aggregator etc. Many teams also use Kafka as an agent and processor before sending logs to a central location.|
|Logging Platforms|These platforms are responsible for ingesting logs from forwarders and/or agents, storing them in a reliable and scalable manner and providing a powerful interface for text search or analytics as relevant.||
|Search engines|Search engines are great at quickly returning a text snippet or a pattern from humongous volumes of text data. The problem lies in the ingestion. Indexing is a resource intensive process. As log volumes grow and grow, indexing all of the log data before ingesting it is highly compute intensive and this in turn slows down the ingestion process itself.<br><br>Another common issue is that indexing generates index metadata - and at high enough log volume, metadata can outgrow the actual data. Now, the way these systems work is that all this data and the index metadata has to be replicated across servers to ensure data availability and redundancy. This adds to the overall storage and network requirements - eventually making the system difficult and costly to scale.|Elasticsearch, Splunk, Mellisearch|
|Analytics Databases|OLAP -Online analytical processing (OLAP) is software technology you can use to analyze business data from different points of view.  <br>Analytics databases are designed to get you answers around your log data. For example, the rate of status 500 returned over last 10 minutes, average response time for a particular endpoint over last 24 hours, and so on.|Clickhouse|

  
**