## Cheat Sheet:
- ## Interview Framework:
  
  This section is designed to give you a set of steps to follow during the interview. You might be nervous. Remember that if you follow the process below in order, you will end up with a well-structured problem solving approach to tackle any difficult design problem. You got this.
- Unsolicited advice
  
  > During the interview, try not to explain anything that you haven’t read up on. If you mention “RabbitMQ” but have no idea what it is, you open yourself to being asked “What does it do?”. This is detrimental to your performance.
  
  Instead, make the interview collaborative at the mid level. Suggest strategies and ask for confirmation to ensure that you are getting to a good solution. Remember: breadth is greater than depth (**at the mid level**)*
  
  >
- Establish Functional Requirements
	- What does the system actually DO?
	- Keep it user centric - “Users should be able to….”
	- It can be easily tested and verified
		- You’ve gotta be able to prove it works
	- The requirements are specific (If you can quantify, go for it!)
		- If it’s vague it’s not a requirement, it’s a wish
		- Search Engine Example: “Users should be access results in pages up to 100”
- Establish Non-Functional Requirements
	- HOW will your system do the thing?
	- Everyone wants Security + Scalability + Performance (Duh)
	- Use this as a place to discuss tradeoffs… Like if you want Consistency over availability
	- Is your system read heavy or write heavy?
	- Tell your interviewer you’ll do calculations as you go through the design in places you need. Usually both of you know that it will be a distributed system in the ball park of “a lot” of requests. Spending too much time on calculations is not worth it.
- Articulate functional objects
- Write API
  
  Remember that private (user) info should be transported through a JWT or a session token. Your interviewer will be impressed.
	- POST
	- PATCH
	- GET
	- PUT
	- *When to use post vs put:*
	  
	  Post is used when creating a new object but you don’t care about editing a specific object. Multiple posts will create multiple objects.
	  
	  If you wanted to create a social media post, you would call `POST /v1/createPost`
	  
	  Calling this endpoint multiple times would create multiple posts.
	  
	  Put is more like a getOrDefault() on a dictionary, where if the object doesn’t exist it will create one and if it does, it will edit it. That means it is idempotent, since multiple PUT’s will leave the database in the same state
	  
	  For example: If you wanted to create a flight AS297 with onTime = true, you’d say  `PUT/v1/flight/AS297?ontime=true`
- Design the system
	- Design the system
	  
	  **Start Simple:**
		- Picking a DB
			- SQL
			  
			  SQL databases are structured tables that support relations. Most SQL databases have mature support of ACID properties (explained below)
			- NoSQL
			  
			  Most of the time, you will be dealing with document-store NoSQL databases. Basically they store a primary key of your choice to a JSON document.
			- What the f*ck is the difference?
			  
			  A bunch of great database technology exists for both SQL and NoSQL that makes the lines very blurry in industry. Basically, if you want a ton of writes and don’t have that many relations, use NoSQL (MongoDB is great). If you have a lot of relations (joins) and want consistency and ACID properties then use SQL. It really doesn’t matter for most things.
			  
			  If you’re doing anything financial, just use SQL
			- Okay but what the f*ck is ACID
			  
			  Not the kind you trip on.
				- Atomicity - Operations either complete completely or roll back. No partial writes.
				- Consistency - Database rules are enforced before and after the transaction
				- Isolation - A DB transaction will not be impacted by other transactions (reads or writes). The intermediate state of a transaction is invisible to other transactions, preventing issues like dirty reads, non-repeatable reads, and phantom reads.
				- Durability - Successful transactions survive forever. They cannot be undone, even in the event of a crash, power loss, or error
		- You can abstract the first part into client → API Gateway
			- Remember to explain that the API Gateway handles
				- Request Routing
				- Rate Limiting
				- Load Balancing
				- Auth
		- Begin with the simplest form of the system to meet the functional requirements.
			- This typically involves designing a solution for a single client, focusing on core functionalities without worrying about scale or redundancy at first.
		- Consider a monolithic architecture or a basic client-server model, depending on the problem's requirements.
			- Identify the core components needed, such as the application server, database, and any external services.
			  
			  ```
			  Perbhat's tips:
			  * Don’t forget to bring up pagination if fetching lots of data
			  * Whenever you need to sort something or handle complex logic,
			  you can draw a box and say "<functionality> service". Figure
			  out the rest of the design and get back to this later.
			  * Whenever you make a service, cache the results
			  Client request -> API Gateway -> Cache (for service)
			  -> Service -> Cache -> DB <- things that write to the db
			  ```
	- Scaling and Redundancy
	  
	  **Address Scalability:**
		- Once the basic solution is established, think about scaling the system. This usually involves adding more instances of key components, such as application servers or databases, and implementing sharding or partitioning strategies.
		- Introduce a load balancer to distribute traffic across multiple instances, ensuring that the system can handle increased load and provide high availability.
	- **Mitigate Single Points of Failure:**
	  
	  Identify potential single points of failure in your design, such as a single database or server. For each, introduce mechanisms to mitigate these risks:
		- **Sharding:** For databases, shard data across multiple nodes to distribute load and provide fault tolerance.
			- *hint: most of the time you either want hash (using consistent hash), geographic (for video use cases and CDN’s etc.), and range (think when you know the entire ID range have about equal traffic throughout)*
		- **Replication and Failover:** Use replication for critical components, such as databases, to ensure data availability. Implement failover strategies to switch to a replica in case of failure.
		- **Snapshots and Backups:** For systems like Redis (an in-memory database), use regular snapshots and backups to prevent data loss in case of failure. Consider using persistent storage if data durability is crucial.
- ## Key Technologies (WIP):
  
  I am still organizing this section. Below you will find various tools you can use to handle data, as well as their most popular commercial applications. Be sure to read up on these. I will rank them in order of importance soon. If nothing else, know SQL vs NoSQL, blob storage, caching, streams, and queues.
- **Streams**
	- **Purpose**: Real-time data processing and analytics.
	- **Commercial Counterparts**:
		- **Apache Kafka**: Confluent
		- **Amazon Kinesis**: AWS
		- **Azure Event Hubs**: Microsoft Azure
- **Caches**
	- **Purpose**: Improve data retrieval speed by storing frequently accessed data in memory.
	- **Commercial Counterparts**:
		- **Redis**: Redis Enterprise
		- **Memcached**: AWS ElastiCache for Memcached
		- **Varnish**: Varnish Plus
- **Queues**
	- **Purpose**: Asynchronous message passing, decoupling systems.
	- **Commercial Counterparts**:
		- **RabbitMQ**: Pivotal RabbitMQ
		- **Apache ActiveMQ**: AWS MQ
		- **Amazon SQS**: AWS
		- **Google Cloud Pub/Sub**: Google Cloud
- **Time Series Databases**
	- **Purpose**: Optimized for time-stamped or time-series data.
	- **Commercial Counterparts**:
		- **InfluxDB**: InfluxData
		- **Prometheus**: Managed Prometheus (Google Cloud, AWS)
		- **TimescaleDB**: Timescale
		- **OpenTSDB**: Commercial support via various providers
- **Search Engines**
	- **Purpose**: Full-text search and analytics.
	- **Commercial Counterparts**:
		- **Elasticsearch**: Elastic NV
		- **OpenSearch**: AWS OpenSearch Service
		- **Solr**: Lucidworks Fusion
- **Columnar Databases**
	- **Purpose**: Efficient storage and retrieval of data, particularly for analytics.
	- **Commercial Counterparts**:
		- **Apache Cassandra**: DataStax
		- **Amazon Redshift**: AWS
- **Graph Databases**
	- **Purpose**: Optimized for managing and querying graph-based data.
	- **Commercial Counterparts**:
		- **Neo4j**: Neo4j Enterprise
		- **Amazon Neptune**: AWS
		- **Azure Cosmos DB (Gremlin API)**: Microsoft Azure
- **Key-Value Stores**
	- **Purpose**: Simple storage for key-value pairs.
	- **Commercial Counterparts**:
		- **DynamoDB**: AWS
		- **Riak KV**: Basho
		- **Aerospike**: Aerospike
- **Document Stores**
	- **Purpose**: Store, retrieve, and manage document-oriented information.
	- **Commercial Counterparts**:
		- **MongoDB**: MongoDB Atlas
		- **Couchbase**: Couchbase Server
		- **RavenDB**: RavenDB Cloud
- **Object Storage**
	- **Purpose**: Store unstructured data as objects.
	- **Commercial Counterparts**:
		- **Amazon S3**: AWS
		- **Google Cloud Storage**: Google Cloud
		- **Azure Blob Storage**: Microsoft Azure
- **Relational Databases**
	- **Purpose**: Structured data storage, supporting SQL queries.
	- **Commercial Counterparts**:
		- **MySQL**: Oracle MySQL
		- **PostgreSQL**: EnterpriseDB
		- **Oracle Database**: Oracle
		- **Microsoft SQL Server**: Microsoft
- **In-Memory Databases**
	- **Purpose**: Store data in-memory for fast access and low latency.
	- **Commercial Counterparts**:
		- **Redis**: Redis Enterprise
		- **Memcached**: AWS ElastiCache for Memcached
		- **SAP HANA**: SAP
- **Distributed File Systems**
  
  **Purpose**: Distributed storage and access of files across multiple servers.
  
  **Commercial Counterparts**:
	- **Hadoop HDFS**: Cloudera, Hortonworks
	- **Google Cloud Storage**: Google Cloud
	- **Amazon S3**: AWS
- **Data Warehouses**
	- **Purpose**: Central repository for large amounts of structured data.
	- **Commercial Counterparts**:
		- **Snowflake**: Snowflake Inc.
		- **Amazon Redshift**: AWS
		- **Google BigQuery**: Google Cloud
- **Object Relational Mappers (ORMs)**
	- **Purpose**: Map objects in application code to database tables.
	- **Commercial Counterparts**:
		- **Hibernate**: Red Hat
		- **Entity Framework**: Microsoft
		- **SQLAlchemy**: Community supported



https://newsletter.systemdesigncodex.com/p/15-must-know-elements-of-system-design?utm_source=%2Finbox%2Fsaved&utm_medium=reader2
https://newsletter.systemdesigncodex.com/p/8-must-know-strategies-to-build-scalable
