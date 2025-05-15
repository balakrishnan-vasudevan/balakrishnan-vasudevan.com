
## Clarification Questions:
 #  What To Monitor
	1. Application layer metrics:
		1. # of post requsts
		2. Concurrent requests
		3. Latency distribution of methods
		4. Length of unprocessed message queue
		5. Cache hit rate
		2.Language/Execution specific metrics:
			1. Version
			2. # of concurrent routines
			3. Last garbage collection
			4. # of bytes of memory allocated/freed
			5. Heap size
		3.Host/System metics 
			1. CPU/Memory/Disk Usage
			2. # of processes running on the host
			3. Status of file system, network , system timer
2. How to get the metrics out
		Push vs Pull - we should confirm with the interviewer: Do we need to get the metrics out of the server? Maybe we don’t. In that case, the server may expose an endpoint service with the metrics or it may just save the metrics to local disks and we can SSH onto it to inspect. The response from the interviewer is, however, very likely to be yes. We do want to get the metrics out. Otherwise, we’ll lose access to the metrics when the server is slow or down — just when we need them the most. We’d also want to put the metrics in a centralized place for better global monitoring and alerting.
		Promethus pulls - https://prometheus.io/blog/2016/07/23/pull-does-not-scale-or-does-it/
		Pushing is useful when firewall prevents monitoring system from accessing servers.
		With pull, challenging to offer high availability and scalability with a pull-only model
		If we’re using push, we can put a load balancer in front of a set of monitoring system replicas and have the servers being monitored send metrics through the load balancer. But with a pull-only model, the metrics are collected directly by a monitoring system instance. We’ll have to shard the metrics deliberately when pulling and deploy backup instances explicitly to support replication and failover. Depending on the environment, this may or may not be a big problem.
3. Persisting metrics
		Time series db
		Our first intuition should be that we absolutely cannot just write individual data samples to files as they arrive. That’ll be prohibitively inefficient because the monitoring system may end up collecting a million data samples or more every minute. So some form of batching is crucial. With batching in memory, there comes the risk of losing data. It may not be a big deal if we’re only batching for a short period of time, as typical time series use cases can tolerate the loss of a few data samples. But if we want to batch for a longer period of time, a durability safeguard should be put in place. After all, the most recent data samples are usually the most valuable. We don’t want to be in a position where we lose the last 30 minutes of metrics.
		==Write-ahead-log (WAL) is the canonical solution to complement in-memory batching for durability==. For more details, you can check out [the detailed article](https://eileen-code4fun.medium.com/building-an-append-only-log-from-scratch-e8712b49c924) I wrote on the topic. On a high level, WAL pipes the changes to a log file on disk that can be used to restore the system state after crashing. WAL doesn’t incur a big IO penalty because sequential file access is relatively fast.
		Now we can buffer the data samples in memory for a while, which opens doors for better write efficiency. The next thing we should decide is how we structure the data in files. One time series per file sounds like a simple solution, but unfortunately, it won’t scale. There are just too many time series to create individual files for. We have to store multiple time series in a file. On the other hand, we can’t just put everything in a monolithic file. That file will be too big to operate. We need to cut the file in some way. The natural choice here is to cut the file by the time dimension. We can create one file per day or other configurable time window. Let’s call the data in a time window a block. If the data volume in a block is too big for one file, we can shard it across a few files. We also need an index file in each block to tell us which file and what file position to look for in a particular time series. See figure 1 for an illustration.

![Sharding data across files](https://miro.medium.com/v2/resize:fit:700/1*Ob9a5IOtcHVkl574jAEnCQ.png)

	As data samples arrive in memory, we buffer them until we need to flush them to disk. When we flush them to disk, we organize them in blocks. The block for the most recent data samples typically represents a small time window. As the blocks grow older, we compact them to form longer time windows. This keeps the overall block number in check. What’s more, the old data samples are queried less frequently so we can put them in larger files for easy management. We can also down-sample the data as part of the compaction to reduce overall data volume. The idea of compacting young files into bigger old files is not new. It’s called a [log-structured merge tree](https://eileen-code4fun.medium.com/log-structured-merge-tree-lsm-tree-implementations-a-demo-and-leveldb-d5e028257330). LevelDB is probably the most famous implementation of it.

Compression should be employed to reduce the overall data volume. Time series data is an excellent candidate for compression. All the data samples can be expressed as delta from the preceding data samples. Facebook [published a paper](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf) that describes two particular tricks in time series data compression that led to 10x saving, taking advantage of the fact that adjacent data points are close. In their paper, a timestamp is encoded as delta of delta. The second-order derivative tends to have more zeroes. The floating-point value is encoded as an XOR result and can be restored by `(a XOR b) XOR a = b`. When two floating-point values are close, their XOR result has a lot of zeroes.
To grow beyond a single node, we need to scale the storage out. We can either back the data by using a distributed file system (such as HDFS) or redesign the storage logic to adapt to a more natively distributed infrastructure.
3. Supporting querying and alerting
		Time is a universal filtering criterion in all metrics searches. We use a time range to narrow the search down to a set of continuous blocks. If we know the time series ID, we can retrieve it from the files in those blocks. Otherwise, we’d need to add a reversed index to go from the search criteria to time series IDs and then follow the index files in blocks to locate the time series files. Once we retrieve the time series data, we can graph them for display.

		Alerts can be registered inside the monitoring server. While it sniffs through the incoming data samples, it can alert for any abnormal pattern. We can also decouple them from the monitoring server and deploy them as downstream monitoring servers that only collect and inspect a more selected set of metrics.



[[Observability at Twitter]]
[[Netflix - Observability]]
[[Wide Events]]
[[Pinterest - Time Series]]
[[Distributed datastore for logs]]
[[Async Workflow Observability]]
[[Logging at Twitter]]