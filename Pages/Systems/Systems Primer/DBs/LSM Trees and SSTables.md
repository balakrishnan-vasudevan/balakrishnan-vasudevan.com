Writes first go to a balanced binary search tree in memory 
Tree flushed to a sorted table on disk when it gets too big 
Can binary search SSTables for the value of a key 
If there are too many SSTables they can be merged together (old values of keys will be discarded)

![[Screenshot 2025-03-31 at 11.04.42 AM.png]]

Pro: Fast writes to memory! 
Con: May have to search many SSTables for value of key.

Sorted Strings Table (SSTable) is a **persistent file format** used to take the in-memory data stored in memtables, and store it on disk in a persistent, **ordered, immutable set of files.**

- Immutable means SSTables are never modified. They are later merged into new SSTables or deleted as data is updated.
The purpose of a database is to persistently and efficiently store data. That storage needs to be durable, so that the data isn’t lost when the system is shut down .

# How write works in LSM Tree?

Let’s dive deeper into how writing works in an LSM Tree.

When you want to write data to the LSM Tree the first stop is the in-memory layer of the LSM Tree, which is like the top part of the tree and is super fast as well, because it’s stored in memory!

However, keeping all the data in memory indefinitely is not practical, so the LSM tree ==periodically flushes the data from the in-memory layer to disk.==

But here’s the clever part: _before the data is flushed to disk and organized into SSTables, it is also written to the Write-Ahead Log (WAL)_.

> The Write-Ahead Log acts as a backup, ensuring the durability of the data. It serves as a log of all the changes made to the database, acting as a safety net in case of system failures or crashes.

![[Pasted image 20250331111142.png]]

So, when a write operation occurs,

- The data is first written to the in-memory layer for speedy performance.
- Simultaneously, _the changes are recorded in the Write-Ahead Log to ensure data integrity_.
- Then, at regular intervals or when the in-memory layer reaches a certain threshold, the data is flushed to disk and organized into SSTables.

_SSTables, or Sorted String Tables, are essentially just sorted key-value pairs that are written to disk._

One of the best things about SSTables is that they’re incredibly efficient for searching and reading data. As you accumulate more data, more levels of SSTables are created, with each layer being more compressed than the previous one. The number of levels and amount of compression can vary depending on the use case, but the general idea is to keep compressing the data as you go down the layers.

Now, you might be wondering **_why the LSM Tree uses this approach_.**

The answer is simple: it’s great at minimizing disk I/O operations. By writing to disk periodically and in larger batches, you’re reducing the number of times the disk has to spin up and down to access data.

# How is data read from LSM tree?

When you want to read data from an LSM tree, the process begins with a user query. You’re searching for a specific piece of information, and the LSM tree jumps into action to find it for you.

The first place the LSM tree checks is the in-memory layer. Remember, this layer is super fast to access because it’s stored in memory. So, if the data you’re looking for happens to be in this layer, hooray! The LSM tree quickly retrieves it, and you get your desired information without any delay.

But, what if the data you’re searching for is not in the in-memory layer? Well, don’t worry, the LSM tree has a plan for that too! It moves on to the next step, which involves searching the on-disk layer, where the data is stored in what we call SSTables.

Now, this is where the bloom filter comes into play. Picture the bloom filter as a clever little assistant that helps the LSM tree narrow down its search. Before diving into each SSTable, the LSM tree consults the bloom filter to see if the data you’re looking for might exist in a particular SSTable. ==_The bloom filter gives a probabilistic answer — it either says “the data might exist” or “the data definitely doesn’t exist.”_==

![[Pasted image 20250331111201.png]]

If the bloom filter indicates that the data might exist in a specific SSTable, the LSM tree jumps into action again and starts searching that SSTable. It scans the sorted key-value pairs within the SSTable until it either finds the data you’re looking for (yay!) or realizes it’s not there.

On the other hand, if the bloom filter confidently declares that the data definitely doesn’t exist in a particular SSTable, the LSM tree skips that SSTable and moves on to the next one. It’s like the bloom filter acts as a reliable guide, showing the LSM tree which SSTables are worth exploring and which can be skipped, saving time and effort.

And that’s how reading works in an LSM tree! The combination of checking the in-memory layer, leveraging the bloom filter, and searching the on-disk SSTables allows for efficient and speedy retrieval of data.

1. **NoSQL databases** One of the primary use cases of LSM trees is in NoSQL databases. These databases are designed to handle large amounts of unstructured or semi-structured data, and the LSM tree architecture aligns perfectly with their requirements. LSM trees offer excellent write performance, which is crucial for managing the high data ingestion rates typically encountered in NoSQL databases. The ability to efficiently handle write-intensive workloads makes LSM trees an ideal choice for storing and managing the vast amounts of data these databases handle.
2. **Time series databases** are another area where LSM trees shine. Time series data is characterized by its timestamped nature, where data points are associated with specific time intervals. LSM trees provide efficient storage and retrieval of time series data, thanks to their sorted structure. This allows for quick access to data points based on timestamps, enabling efficient analysis and querying of time-based data.
3. **Search engines**, LSM trees play a vital role in facilitating fast and accurate search operations. Search engines need to index and retrieve vast amounts of data quickly to provide relevant search results. LSM trees, with their ability to handle large datasets and provide efficient read operations, are a natural fit for search engine architectures. They allow for speedy retrieval of indexed data, making search queries lightning-fast and providing a seamless user experience.
4. **Log systems** LSM trees also find their place in log systems, such as those used for real-time event streaming or log processing. In log systems, data needs to be written in an append-only manner, preserving the order of events. LSM trees excel in this scenario, as they offer efficient write operations by sequentially appending new data to the in-memory layer. The write-ahead log (WAL) ensures durability and recovery in case of system failures, further enhancing the reliability of log systems.

**Options:**

- **In Memory:** Keeping all the data only in memory would be fast, but not durable.
- **Normal Disk** : Writing every update to storage immediately would be very slow and inefficient at scale.
- **B tree** : B-tree-based databases use balanced tree structures which provide efficient read and write operations (Used in _:_ **_PostgreSQL, MySQL.)._** It provides more balanced performance for sequential and random access.
- **SSTable**

## Benefits of SSTable

- [SSTables](https://www.scylladb.com/glossary/sstable/) are **quick and efficient to read and write since they are append only and do not overwrite existing data** to disk.
- They use binary search and index files to locate blocks and keys within blocks.
- Merging SSTables is similar to doing a merge sort

![[Pasted image 20250331110917.png]]

## **Indexing in SS table :**

- To find if a key exists we don’t need an index of all the keys in memory, instead we can keep an index for every few kilobytes and then perform a scan (sparse index). So rather than store keys individually, they gain speed by maintaining a selective or sparse index, keeping index entries for only a subset of the data rather than every individual record.

![[Pasted image 20250331110935.png]]

**Real World Use Case:**

- LSM databases are commonly used in various applications, including time-series databases, distributed systems, and Big Data analytics platforms.
- The append-only nature of write operations and the ability to batch writes and merge data efficiently make LSM databases well-suited for high-throughput environments.

## Drawbacks of LSM Databases:

1. **Relatively higher read latency:** LSM databases may suffer from performance during read-heavy workloads. This is because data may be spread across multiple SSTables, requiring additional disk seeks to locate and retrieve the desired data.
2. **Write process overhead:** Although LSM databases offer high write throughput, individual write operations may experience higher latency compared to traditional B-tree-based databases. This is due to the additional overhead of write-ahead logging, memtable flushes, and compaction processes.

**Architectural Advantages of LSM Trees**

1. **High Write Throughput:** LSM trees handle writes by first buffering them in memory (in a structure called a MemTable). Once the MemTable reaches a certain size, it is flushed to disk in a sorted manner, creating immutable files called SSTables (Sorted String Tables). This process minimizes random writes and maximizes sequential writes, which are much faster on disk-based storage systems.  
    **2. Efficient Data Compaction:** To maintain data order and minimize the number of files, LSM trees periodically merge SSTables in a process called compaction. Compaction helps to remove deleted data, consolidate records, and ensure that the most recent data is quickly accessible.  
    **3. Optimized for Append-Only Workloads:** LSM trees are particularly well-suited for append-only workloads, where data is written sequentially and not frequently updated. This makes them ideal for time-series data, where new records are continually added.

**LSM Trees in NoSQL Databases**

NoSQL databases, such as Apache Cassandra, HBase, and LevelDB, use LSM trees to manage their storage. The primary reasons for this choice include:

**- Scalability:** LSM trees allow databases to scale horizontally, handling large volumes of writes across distributed systems.  
**- Flexibility:** NoSQL databases often need to accommodate varying data models and workloads. LSM trees provide the necessary flexibility to handle diverse use cases, from high-throughput data ingestion to real-time analytics.

However, the advantages of LSM trees come with trade-offs. The reliance on compaction can lead to temporary performance degradation, and read operations can be slower compared to B-Trees, especially when data is spread across multiple SSTables. This is known as read amplification, where a single read request might require accessing multiple SSTables.
![[Pasted image 20250331111426.png]]

1. **In-Memory Buffer**: This is the initial stage where incoming data is first collected.
2. **Memtable**: The data from the in-memory buffer is sorted and stored in the memtable.The Memtable is essentially an ordered map, allowing fast write and read access.Memtables are not durable by themselves, meaning that if the system crashes, data in the Memtable may be lost. This is mitigated by also writing updates to a write-ahead log (WAL) for durability.
3. **Immutable Memtable**: Once the memtable reaches a certain size, it becomes immutable and is ready to be flushed to disk.
4. **Flush to Disk (SSTables)**: The immutable memtable is written to disk as SSTables (Sorted String Tables). SSTables, once written, are immutable. This means that they cannot be altered, which simplifies concurrency control and ensures data consistency.Like Memtables, SSTables store data in a sorted order. This characteristic is crucial for efficient range queries and merges during compaction.The sorted nature of SSTables allows for efficient binary search operations, making read queries fast. SSTables are often accompanied by additional metadata, such as Bloom filters, which help quickly determine whether a key is present in the table without reading the entire data structure.
5. **Merge Compaction**: Over time, multiple SSTables are merged and compacted to maintain efficiency and reduce storage space.

This process ensures efficient writes and optimizes read performance in a database system. The “Flush” and “Compact” steps are critical in maintaining the balance between memory and disk usage, ensuring data is organized and easily retrievable.

**LSM Trees in Timeseries Databases**

Time-series data consists of data points collected or recorded at specific time intervals. Examples include stock prices, temperature readings, heart rate monitoring, and server performance metrics. This data is characterized by its high volume, frequent updates, and the need for quick retrieval and analysis over time intervals.

The nature of time-series data presents several challenges:

**1. High Ingestion Rate**: Time-series data systems often require the ingestion of large volumes of data at high frequencies, necessitating efficient write operations.  
**2. Efficient Storage and Retrieval:** Due to the sheer volume of data, storage efficiency and fast retrieval are critical. Indexing mechanisms and data structures play a significant role in achieving this balance.  
**3. Complex Querying and Aggregation:** Time-series analysis often involves complex queries, such as aggregating data over specific time periods or drilling down into detailed dimensions.

TSDBs leverage LSM trees due to their ability to handle high write loads and their efficiency in managing large volumes of data. However, TSDBs go a step further by incorporating additional optimizations tailored to the unique requirements of time-series data.

**1. Time-Partitioned Data**: TSDBs often partition data based on time intervals, such as hourly, daily, or monthly partitions. This partitioning helps to isolate data segments, making it easier to manage retention policies, perform backups, and optimize query performance. By partitioning data, TSDBs can quickly locate the relevant time segments during a query, reducing the amount of data scanned.

**2. Downsampling and Aggregation:** To manage storage costs and improve query performance, TSDBs often downsample data, storing less granular data as it ages. For example, high-resolution data may be retained for a short period, while downsampled (averaged or aggregated) data is stored for longer durations. This approach reduces storage requirements and speeds up queries by limiting the amount of data that needs to be processed.

**3. Efficient Compression:** Time-series data often contains patterns or repetitions, making it suitable for compression. TSDBs utilize advanced compression algorithms to reduce the storage footprint. This not only saves disk space but also improves query performance by reducing the amount of data that needs to be read from disk.

**4. Optimized Query Execution:** TSDBs optimize query execution by supporting specialized query languages or extensions that allow for efficient time-based filtering, aggregation, and interpolation. For example, Prometheus uses PromQL, a query language designed for time-series data, allowing users to define complex queries that efficiently retrieve and aggregate data over time.

**Challenges with LSM Trees in TSDBs**

While LSM trees provide excellent write performance, they can struggle with read-heavy workloads, especially when complex queries require accessing data spread across multiple SSTables. This issue, known as read amplification, can lead to slower query response times and increased resource consumption.

**Apache Druid’s Solution: Fast Query Analysis**

Apache Druid is a real-time analytics database designed to provide fast query analysis over large datasets. It combines features of both TSDBs and data warehouses, making it suitable for a wide range of analytical use cases, including time-series data.

**Key Innovations in Apache Druid**

**1. Segment-Based Storage:** Druid stores data in segments, which are time-partitioned chunks of data. Each segment is optimized for fast querying and can be processed independently, allowing Druid to scale horizontally and handle large datasets efficiently.

**2. Column-Oriented Storage:** Druid uses a columnar storage format, which stores each column of data separately. This format is highly efficient for analytical queries, as it allows Druid to read only the relevant columns needed for a query, reducing I/O and improving performance.

**3. Pre-Aggregation:** Druid supports pre-aggregation, where data is aggregated during ingestion, reducing the amount of work required during query time. This pre-aggregation can include operations like summing, averaging, and counting, which are common in time-series analysis.

**4. Real-Time Ingestion and Querying:** Druid is designed for real-time analytics, allowing for the ingestion and querying of data with minimal latency. This makes it ideal for applications that require immediate insights from streaming data, such as monitoring and alerting systems.

**5. Advanced Indexing:** Druid uses advanced indexing techniques, including bitmap and inverted indexes, to accelerate query performance. These indexes allow Druid to quickly filter and aggregate data based on various dimensions, such as time, geographic location, or user attributes.

**6. Drill-Down and Exploration:** Druid provides powerful capabilities for drilling down into data. Users can start with high-level aggregates and then explore finer details by drilling down into specific dimensions or time intervals. This feature is particularly valuable for exploratory data analysis and investigative use cases.

**Benefits of Apache Druid’s Architecture**

**1. Fast Query Performance:** By leveraging columnar storage, pre-aggregation, and advanced indexing, Druid can deliver fast query response times, even for complex analytical queries. This makes it suitable for interactive dashboards and real-time data exploration.

**2. Scalability and Fault Tolerance:** Druid’s architecture allows for horizontal scaling, making it capable of handling large datasets and high query loads. It also provides built-in fault tolerance, ensuring data availability and reliability.

**3. Versatility:** While Druid is optimized for time-series data, it can also handle a wide range of other data types and analytical use cases. This versatility makes it a valuable tool for organizations that require both real-time and historical data analysis.


**tldr:**

SSTable (Sorted Strings Table) is a file of key/value string pairs, sorted by keys

- It provides a persistent,ordered immutable store for keys,values pair.  
- Internally, each SSTable contains a sequence of blocks .  
- A index block (stored at the end of the SSTable) is used to locate blocks  
- The index is loaded into memory when the SSTable is opened.  
- A lookup can be performed with a single disk seek: we first find the appropriate block by performing a binary search in the in-memory index, and then reading the appropriate block from disk.

[[pages/Systems/Systems Primer/DBs/Cassandra|Cassandra]]
