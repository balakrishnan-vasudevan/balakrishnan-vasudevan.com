# Let’s implement the log database or Big ideas behind the scene

Tags: databases
Category: Articles
Company: general
Status: Not started
URL: https://d9nich.medium.com/lets-implement-the-log-database-or-big-ideas-behind-the-scene-694d86bdc2a6

**In** most situations, you wouldn’t create your own storage, but you should **select** a storage engine, that matches your application needs. To **tune** a database to your data flow you need to know *how the storage engine works*. In this chapter, we will explore **log** database engines by **building** our own from scratch. Prepare a coffee☕ we’re ready to dive🤿.

[https://miro.medium.com/v2/resize:fit:1400/0*qlLZXotK8lP65LqO](https://miro.medium.com/v2/resize:fit:1400/0*qlLZXotK8lP65LqO)

Photo by [Jandira Sonnendeck](https://unsplash.com/@jandira_sonnendeck?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=medium&utm_medium=referral)

> “Cleaning and organizing is a practice, not a project.” — proverb
> 

# **What database should do?**

The database should do two things:

1. When you give data, the database should **save** data.
2. When you ask for stored data, the database **gives it back** to you.

The world’s simplest database implemented in Python is provided below👇:

Simple database solution

You can call **`db_upsert`** to store a value in the database. It can be anything from a simple string to JSON. Then you can call **`db_get`** to retrieve the most recent value by **key**.

Example of program usage:

![https://miro.medium.com/v2/resize:fit:1400/1*dVUvrkVYxZPVHRuKXV5IXA.png](https://miro.medium.com/v2/resize:fit:1400/1*dVUvrkVYxZPVHRuKXV5IXA.png)

execution **example**

Every time we need to **add** a new key/value pair we put it at the end of the file. This file is also well known as a **log** or **append-only** data file. **Logs** are incredibly fast because appending to a file is generally very efficient. The modern database has more issues to deal with (*concurrency* access, *errors* in runtime), but the basic principle remains the same.

To **get** a value by key, we need to search for the latest occurrence in a file. This operation in our case has awful performance — **O(n)**. You have to search through all the files to find the newest value. It means that a 2 times bigger file, will take 2 times more time to find a value.

The solution to the “**get**” problem in our situation is to add an **index**. However, adding an index will slow down the database on write. This is an important **trade-off** in storage systems: every index **slows down** writes, but well-chosen indexes **speed up** reads.

# **Indexes**

We will start with the **hash** index for the **key-value** store. It’ll be a good point to understand how we can implement a more complicated one.

Key-value databases are very similar to a **dictionary** that is implemented in all widespread programming languages. We will use this structure for implementing our index of data on disk.

In our example application, we use an append-only strategy. We can store the position of the newest data in the file(**offset**) in our dictionary.

![https://miro.medium.com/v2/resize:fit:1400/1*8_BAG7TKJwubyHaYouLB7A.png](https://miro.medium.com/v2/resize:fit:1400/1*8_BAG7TKJwubyHaYouLB7A.png)

In memory **index** representation

ℹ️: In the picture, the file is presented and divided by 30 bytes in each row, however in reality this is just one big unbreakable row.

Whenever you **append** a new key value, you also **update** the offset in your index. (Keep it **up to date**). If you want to read data, you just look in your index and seek this position.

ℹ️: Seek of position is very efficient and is equal to **O**(1)

An example of my simple DB application with an index is shown below👇:

DB with an **index** on python

![https://miro.medium.com/v2/resize:fit:806/1*5W8qqBVoljQaj9PFD1YSZQ.png](https://miro.medium.com/v2/resize:fit:806/1*5W8qqBVoljQaj9PFD1YSZQ.png)

Execution **index application**

For you, as a reader, this way to create an index may sound naive, but this approach is used in the real database — [Bitcask](https://en.wikipedia.org/wiki/Bitcask) ([Riak](https://en.wikipedia.org/wiki/Riak) storage engine). Bitcask requires that all of the available **keys** can fit in the memory. However, **values** can be larger than **keys**, because you can retrieve “value” from the disk using **single seek**. Moreover, if the information has been **cached** by the filesystem, an application doesn’t require any I/O operations at all.

## **Use cases for such storage**

The best example is **counting** how many people have visited our certain page on the website. We have a **limited** amount of pages (**keys**) and the value of our storage is **frequently updated**.

## **Compaction 📦**

Our tactic is to append changes to a single file, but in this scenario, we can easily at some point of time run **out of disk space**. To avoid this we should:

1. Break the log into segments of a certain size
2. Regularly do **compaction**

☝️: Each segment has a **separate** in-memory hash table (index matching keys with values offset). In order to find the value of a key, we first search for a key in the **latest** dictionary and return the value if we found. If the key is absent in the dictionary we move to the **older** one.

**Compaction** — throw away outdated values, keeping only the recent one

Compaction advises:

- 🔒Segments are never modified, so the compacted content is written to a new file
- 🏪Compaction can be performed in the **background** (in a separate thread), during serving read requests
- 🧹After compaction, we can delete **old** files

![https://miro.medium.com/v2/resize:fit:1400/1*VkYmnRFi8ZzmaBOxrluv4A.png](https://miro.medium.com/v2/resize:fit:1400/1*VkYmnRFi8ZzmaBOxrluv4A.png)

**Compaction** process

One more optimization is to **merge** several data file segments during **compaction** because compaction often makes segments smaller (the key appears several times in the log).

![https://miro.medium.com/v2/resize:fit:1400/1*DvHXZPneMhe8SzpOBsjRRQ.png](https://miro.medium.com/v2/resize:fit:1400/1*DvHXZPneMhe8SzpOBsjRRQ.png)

**Compaction** and **merging** process

ℹ️: In the merge process we keep the number of segments small, so we check only several dictionaries, keeping the merge & compaction algorithm efficient.

## **Compaction common issues**

In theory, compaction is easy to achieve, however, there are some key moments that can slow down us:

- **❌Deleting** records — if you want to delete a record you need to push a special record (*tombstone*). When compaction occurs and the latest value is a *tombstone*, we will **omit the** key in the compacted file.
- 🔃 Crash **recovery** — if the database is restarted we need to load our *in-memory hashes*. Of course, we can restore it by reading **all** database files. However, [Bitcask](https://en.wikipedia.org/wiki/Bitcask) comes with an approach of storing snapshots of a *hash map*, to speed up this process.
- ⚡ **Partially** written records — The database can **crash** halfway through writing a key/value pair to a file. Bitcask stores a checksum with a row and skips rows if the checksum doesn't match.
- 🔀 **Concurrency** — It’s common practice to keep one thread for writing and multiple threads for reading.
- 🔢**Format** — **CSV** in our implementation is presented only for **learning purposes**. For a real system, it’s better to use **binary formats**. Binary formats give you an opportunity to omit the delimiter of rows: first, you encode *string length* and then provide a *string by itself*. This way it’s much faster and simpler.

🔗: More about formats you can read in [my article](https://medium.com/@d9nich/json-xml-protobuf-thrift-avro-or-everything-you-need-to-know-about-encoding-data-6077a7e769e2).

## **Drawbacks and cons of an append-only log**

The attentive reader should ask a question: “Why not update a record value in place?”. Well, this opens the main advantages of LSM trees (Log-structured merge-tree)

Advantages👍:

- 💿Appending and compaction/merging is **faster** than the random write operation, especially if we’re using HDD.
- ⏪It’s easier to implement **concurrent** access and **recovery**. You don’t need to worry about the situation when you write half of the new data, the application crashes and you get **half new** and **half old** data.

Limitations👎:

- 🧠All keys should **fit** in **memory**. Of course, you can keep the dictionary on disk, but it requires expensive I/O operations and hash collision complicated logic.
- 🅰↔🅱 **Range** queries are **not efficient**. To scan from **`foo001`** to **`foo999`** you **need to scan** each key individually.