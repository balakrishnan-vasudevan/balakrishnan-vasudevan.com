# Search System: Design That Scales

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article2.74d541386bbf.png)

## Metadata
- Author: [[Manav Garg]]
- Full Title: Search System: Design That Scales
- Category: #articles
- URL: https://medium.com/p/2fdf407a2d34

## Highlights
- a) Availability: Users should have high levels of access to the system.
  b) Scalability: The system must be scalable in order to handle the growing volume of data. To put it another way, it should be able to index a lot of data.
  c) Quick large data searches: Regardless of how much material is being searched, the user should receive the results fast.
  d) Lower overall cost: Constructing a search system should be less expensive.
- Three main components do this: 
  a) A crawler that fetches content and creates documents.
  b) An indexer, which builds a searchable index.
  c) A searcher responds to search queries by running the search query on the index created by the indexer.
- The crawler gathers information from the targeted resource.
- The indexer retrieves the documents from a distributed storage and uses MapReduce, which is executed on a distributed cluster of commodity machines, to index these documents. For distributed and parallel index building, the indexer takes advantage of a distributed data processing technology like MapReduce. The distributed storage contains the created index table.
- The index and the documents are stored on distributed storage.
- The user types a search string with many words into the search area.
- The searcher parses the search string, searches for the mappings from the index that are stored in the distributed storage, and returns the most matched results to the user. The searcher intelligently maps the incorrectly spelled words in the search string to the closest vocabulary words. It also looks for the documents that include all the words and ranks them.
- The next thing which can affect our elastic search is ingestion. For example, let’s talk in the case of a social media website; there will be content posted every minute, right? Whenever content is posted, it needs to be indexed in the elastic search to make it searchable. If something goes viral and everybody starts posting regarding the event, then a sudden surge in traffic can affect our elastic search. Elasticsearch becomes a little tricky when there is a such increase in traffic because whenever the load increases suddenly, we do not get time to spin up new nodes because it takes time to distribute data. Hence, two things happen due to this:
  a) Increased Indexing latency: Latency for indexing the new data in the elastic search shoots up.
  b) Increased Query latency: Latency to search the data shoots up.
- Instead of getting each post directly to the elastic search, the answer to this lies in doing it asynchronously. 
  Any write happening to the elastic search should go through some kind of a queuing mechanism, and the best way to achieve this, as you may have read in my previous blogs, is through a pub/sub system ( for example kafka).
- The proxy now takes the data and pushes it to the kafka; hence, no direct ingestion happens in the ES. This ensures that we put the data in a very streamlined way to the elastic search without increasing any significant load. This provides a number of advantages, as listed below:
  a) Batch write: We can have a batch write to the ES. As shown in the diagram, we can have one topic per elastic search cluster and make a bulk calls and make writes reducing the load.
  b) Queuing of the write requests: In case Elasticsearch is overloaded, the requests can be queued and consumed at a specified pace. 
  c) Retries: if the cluster is down, we can retry easily
  d) Read latency is not affected: The read latency is not affected in case of any increase in load.
- The main job of this service is too dump hundreds of terabytes of data into the ES. In ES, the indexing happens using a MapReduce job which is synchronous. ElasticSearch (ES) is not designed to handle that high ingestion in one shot. Now the indexing request is dumped to temporary storage and consumed asynchronously using similar workers as above. Twitter has implemented this very efficiently at scale. 
  So now, instead of directly dumping the data, the map-reduce job flushes it into a file system which can be any like S3 or HDFS, etc. Instead of writing this directly to the ES, now we have workers reading the data from the file system and pushing it to the ES. So here, massive ingestion occurs, solving the problem of ES, where is cannot take huge ingestion in one shot.
- The main learning which we get here is that writes are always asynchronous, and the reads still happen in a synchronous manner. This provides a very seamless system; this is how we built a scalable system such that writes can happen eventually but let the reads happen synchronously. This is a way of ensuring that, at a scale, our ES cluster does not go down.
- we need a standardized way for the end user can access the elastic search cluster. We add a proxy between a client and the server. So whichever microservice (assuming the elastic search cluster may be used across teams) needs to access the Elasticsearch needs to go through the proxy. Now because we have a proxy, we can stack a lot of parameters like throttling (rate limiter), router, monitoring, etc.
