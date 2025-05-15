# SSTable database

Tags: databases
Company: general
Status: Not started

**T**he last time we looked precisely at the log database. Today we will look at another structure called SSTable and what benefits we can achieve compared to a log-based. Cassandra uses SSTable to store data, so obtained knowledge will help to understand a big range of databases in depth.

🔗: Read about the log table in my [previous article](https://medium.com/@d9nich/lets-implement-the-log-database-or-big-ideas-behind-the-scene-694d86bdc2a6)

Prepare a coffee☕ we’re ready to dive🤿.



[**Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra)** is the most famous example of an **SSTable**

# **Move from log table to SSTables**

As we know from our previous article the order of the key-value pair in the **log table** is **unordered**. Now let’s think about the structure, that keeps rows **sorted by key** on the disk. This structure is known in computer science as a Sorted String Table(**SSTable**).

One more requirement for SSTable is to **single key across segments**. Lucky for us compaction process already solves this problem.

## **Advantages✅**

- You can do merging even if the keys can’t fit in memory. The approach is similar to the [*merge sort algorithm*](https://en.wikipedia.org/wiki/Merge_sort). We start reading from each segment, look a the first key in each file and write to the output file **lowest**. When two or more segments contain the same key, you keep the value from the recent one and skip from the other.

[https://miro.medium.com/v2/resize:fit:1282/0*AN4eypzKUTdiua6T](https://miro.medium.com/v2/resize:fit:1282/0*AN4eypzKUTdiua6T)

**Merging** several SSTable segments

- No need to keep all **keys** in memory. For, an example we want to find the *orange* value. We don’t know the *orange* offset, but because the keys are sorted — the *orange* should be between the *onion* and the *pear*. We go to the *onion* and iterate till *pear* until we find the key/value pair (or find that it’s absent).

☝️: It’s best to keep the size of blocks to **one kilobyte** (the best balance). It will keep in memory index small and the search time on disk won’t be significant.

[https://miro.medium.com/v2/resize:fit:1400/0*W29GZdweNqZtD5cJ](https://miro.medium.com/v2/resize:fit:1400/0*W29GZdweNqZtD5cJ)

SSTable **in-memory** index

- **📦Compression**: We need to access blocks of key/values anyway so that we can compress blocks. It’ll reduce storage space plus save I/O bandwidth.

## **How to keep SSTable ordered?**

First of all, we can keep sorted information on the disk (in our next article we would talk about B-trees), but sorting in memory is much faster.

🌳We can use [AVL](https://en.wikipedia.org/wiki/AVL_tree) or [red-black](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree) trees to keep data ordered. You can insert data in any order (difficulty is **O(log(n))**) and get elements back in sorted order. (difficulty **O(n)**).

![https://miro.medium.com/v2/resize:fit:1400/0*4cLtX-O9oo5cTKW0.png](https://miro.medium.com/v2/resize:fit:1400/0*4cLtX-O9oo5cTKW0.png)

[A red-black tree is a **self-balancing** tree](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE-%D1%87%D1%91%D1%80%D0%BD%D0%BE%D0%B5_%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Red-black_tree_example.svg)

Now we need to use the following strategies in our storage:

- ✍Use **memtable**, when you need to write. *Memtable* — in memory balanced data structure(Example [AVL tree](https://en.wikipedia.org/wiki/AVL_tree))
- 💾When the *memtable* raises a certain threshold, write as an SSTable on disk. While you write out the *memtable* on disk, you **can** continue **accepting writes** to a **new** *memtable*.
- 👓To read, first try to find a key in the memtable, then in the most recent on-disk segment(using an index of course), then in older and so on.
- ⏰Regularly merge and compact segments

☝️: Common size for *memtable* is 1MB

💦The one drawback here is when an application crashes, we’ll **lose** **records** in the *memtable*. To fix this behaviour we need to write records on a **disk**(it can be unordered) and in a **memtable**. When an application crashes we just **reread** **records** from the file. After the compaction, we can **erase** the **memtable**(in RAM) and the **recovery file** from the disk.

## **Who uses SSTable?**

👁[LevelDB](https://github.com/google/leveldb/blob/main/doc/impl.md) and [RocksDB](http://rocksdb.blogspot.com/), key/value storage libraries, use the algorithm described above. You can use LevelDB in Riak instead of the default Bitcask storage engine. Similar engine storage is used in [HBase](https://blog.cloudera.com/apache-hbase-i-o-hfile/) and [Cassandra](https://cassandra.apache.org/_/index.html), which have been inspired by [Google Bigtable paper](https://research.google/pubs/pub27898/).

ℹ️: Google Bigtable paper has first introduced the terms *SSTable* and *memtable*

![https://miro.medium.com/v2/resize:fit:1400/0*nWBAgxrn4I6hHmjN.png](https://miro.medium.com/v2/resize:fit:1400/0*nWBAgxrn4I6hHmjN.png)

[**Lucene**](https://lucene.apache.org/) is an indexing engine for full-text search in [Elasticsearch](https://www.elastic.co/) and [Solr](https://solr.apache.org/)

[Lucene](https://lucene.apache.org/) uses a similar method for storing *terms dictionary*. The **key** here is a **word** you search and **value** — all document **indexes** where this word occurs.

# **How we can improve performance?**

## **Optimize search of keys that do not exist**

In the simple realization of SSTable, you need to check the *memtable*, and then scan all segments. To speed up this process by adding a [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter). *Bloom filter* can say if a key doesn’t exist in your database and save from many unnecessary I/O operations.

## **⌚When we should compact/merge our segments?**

There are two strategies to determine the order and timing of compaction/merging:

- [**size-tiered**](https://cassandra.apache.org/doc/latest/cassandra/operating/compaction/stcs.html)([HBase](https://hbase.apache.org/)) — newer and smaller segments are merged into older and bigger segments.
- [**levelled compaction**](https://cassandra.apache.org/doc/latest/cassandra/operating/compaction/lcs.html)([LevelDB](https://github.com/google/leveldb), [RocksDB](https://rocksdb.org/)) — the key range is split up into smaller segments and older data is moved in separate “levels”. This way you can process incrementally and use less space.

ℹ️: [Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra) supports both *size-tiered* and *levelled compaction*.