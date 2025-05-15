#async-processing , #task-scheduler 

asynchronous jobs include indexing a file to enable **search** over its contents, generating **previews** of files to be displayed when the files are viewed on the Dropbox website, and delivering notifications of file changes to third-party apps using the [Dropbox developer API](https://www.dropbox.com/developers). This is where Cape comes in — it’s a framework that enables real-time asynchronous processing of billions of events a day, powering many Dropbox features.


Requirements:
Low latency
Multiple event types
Scale
Variable workloads
Isolation
At-least-once gurantee

[SFJ](https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/) (Server File Journal), which is the metadata database for files in Dropbox. Every change to a file in a user’s Dropbox is associated with a [Namespace ID](https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/) (NSID) and a [Journal ID](https://blogs.dropbox.com/tech/2014/07/streaming-file-synchronization/) (JID), which together uniquely identify each event in SFJ. The second supported source is [Edgestore](https://blogs.dropbox.com/tech/2016/08/reintroducing-edgestore/), which is a metadata store for non-file metadata powering many Dropbox services and products. All changes to a particular Edgestore [Entity](https://blogs.dropbox.com/tech/2016/08/reintroducing-edgestore/) or [Association](https://blogs.dropbox.com/tech/2016/08/reintroducing-edgestore/) type can be uniquely identified by a combination of a [GID](https://blogs.dropbox.com/tech/2016/08/reintroducing-edgestore/) (global id) and a Revision ID
For example, events flowing into a [Kafka](https://kafka.apache.org/) cluster could fit into Cape’s event stream abstraction as follows:

Shown below is an overview of what Cape looks like:

![](https://dropbox.tech/cms/content/dam/dropbox/tech-blog/en-us/2017/05/00-cape-system-architecture.png)

SFJ and Edgestore services send _pings_ to a **Cape Frontend** via RPCs containing metadata from relevant events as they happen. These pings are not in the critical path for SFJ and Edgestore, and so are sent asynchronously instead. This setup minimizes the availability impact on critical Dropbox services as a whole (when Cape or a service it depends on is experiencing an issue) while enabling real-time processing of events in the normal case. The Cape Frontend publishes these pings to [Kafka](https://kafka.apache.org/) queues where they are persisted until they are picked up for processing.

The **Cape Dispatcher** subscribes to the aforementioned Kafka queues to receive event pings and kick off the necessary processing. The Dispatcher contains all the intelligent business logic in Cape and dispatches particular events to the appropriate lambda workers based on how users have configured Cape. In addition, it’s responsible for ensuring other guarantees that Cape provides, notably around ordering between events and dependencies between lambdas.

The **Lambda Workers** receive events from the Dispatcher via [Redis](https://redis.io/), carry out the users’ business logic, and respond to the Cape Dispatcher with the status of this processing — if the processing is successful, this is the end of the processing for that particular event.

pings from SFJ and Edgestore are sent asynchronously and outside the critical path to the Cape Frontend, which of course means they are not guaranteed to be sent for every event. You may have realized that this makes it seemingly impossible for Cape to provide the guarantee that every event is processed at least once, e.g. it would be possible for a file to be synced to Dropbox but for us to miss all the asynchronous processing that should happen as a result. This is where **Cape Refresh** comes in — these workers continually scan the SFJ and Edgestore databases for recent events that may have been missed and send the necessary pings to the Cape Frontend to ensure they are processed. Additionally, this serves as a mechanism to detect permanent failures in users’ application code on any of the billions of Subjects processed by Cape.

Uses:
1. **Audit Logs:** Cape enables real-time indexing of Dropbox events relevant to [audit logs](https://www.dropbox.com/en/help/505), enabling Dropbox Business admins to search over these logs
2. **Search:** Cape is used for real-time indexing when a file in Dropbox changes, enabling search over a file’s contents
3. **Developer API:** Cape is used to deliver real-time notifications of file changes to third party apps using the [Dropbox developer API](https://www.dropbox.com/developers)
4. **Sharing permissions:** Cape is used to perform expensive operations asynchronously, e.g. propagating permissions changes across a large or deep hierarchy of shared folders


[[Dropbox ATF]]