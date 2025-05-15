# Internal Working of ElasticSearch

Tags: databases, elasticsearch
Category: Articles
Company: general
Status: Not started
URL: https://medium.com/@ByteCodeBlogger/internal-working-of-elasticsearch-deep-dive-34a87bbf0404

Elasticsearch is written in Java. Let’s see what data structure it uses internally? Best way to understand is through storing an example, shown in last section of this article.

![https://miro.medium.com/v2/resize:fit:1372/1*myxfDjOcFa20brPOVPEJqw.png](https://miro.medium.com/v2/resize:fit:1372/1*myxfDjOcFa20brPOVPEJqw.png)

I recently worked on Elasticsearch for a project, which got me curious about it. Let’s dive into the internal workings of Elasticsearch to understand how it efficiently handles data indexing and searching. But first a link below if you want to know what Elasticsearch is —

[**ElasticSearch: Finding Needle in the Haystack Made Easy-peasy!Searching smarter, not harder ;)**
medium.com](https://medium.com/@kulkarnishruti/elasticsearch-finding-needle-in-the-haystack-made-easy-peasy-371a67fec976?source=post_page-----34a87bbf0404--------------------------------)

# **Internal Components of Elasticsearch**

1. **Cluster**:
- A cluster is a collection of one or more nodes (servers) that together hold the entire data and provide indexing and search capabilities across all nodes.
- Each cluster has a unique identifier, known as the cluster name.

**2. Node**:

- A node is a single server that is part of the cluster. It stores data and participates in the cluster’s indexing and search capabilities.
- Each node has a unique identifier, and nodes are distinguished by their roles (master, data, ingest, etc.).

**3. Index**:

- An index is a collection of documents that have somewhat similar characteristics.
- For instance, you could have an index for customer data, another for product data, and another for order data.

**4. Document**:

- A document is a basic unit of information that can be indexed. It is expressed in JSON (JavaScript Object Notation) format.
- Each document resides in an index and has a unique identifier.

**5. Shard**:

- An index can be divided into multiple pieces called shards. This allows Elasticsearch to distribute and parallelize operations across a cluster.
- Each shard is a fully functional and independent “index” that can be hosted on any node in the cluster.

**6. Replica**:

- A replica is a copy of a shard. Replicas provide redundancy and high availability. If a node fails, the data can still be served from its replica.

# **Data Flow in Elasticsearch**

1. **Indexing**:
- When you index (add) a document to Elasticsearch, the document is assigned to a specific index.
- Elasticsearch routes the document to a specific shard based on a hashing mechanism.
- The shard processes the document and stores it on disk. This involves analyzing the document, creating an inverted index, and storing both the original document and its searchable representation.

**2. Searching**:

- When a search query is received, Elasticsearch determines which indices and shards to query.
- The search request is broadcast to all relevant shards in the cluster.
- Each shard performs a local search and returns its results.
- Elasticsearch aggregates these local results into a final set of results and returns them to the client.

# **Example Workflow**

Let’s illustrate this with a simplified example:

1. **Indexing a Document**:
- You send a JSON document (e.g., `{ "name": "John Doe", "age": 30 }`) to the `people` index.
- Elasticsearch routes the document to a specific shard (say, Shard 1) based on a hash of the document’s ID.
- Shard 1 analyzes the document, creates an for fast searching, and stores the document.
    
    inverted index
    

**2. Searching for a Document**:

- You send a search query (e.g., find documents where `name` is "John Doe").
- Elasticsearch identifies that the query should target the `people` index and determines which shards hold the relevant data.
- The search request is sent to all relevant shards.
- Each shard performs a local search and returns matching documents.
- Elasticsearch aggregates the results and sends them back to you.

# **Data Structure used internally by Elasticsearch :**

Elasticsearch uses several key data structures internally to provide its fast and efficient search capabilities. The most important ones are:

## **1. Inverted Index**

The inverted index is the core data structure behind Elasticsearch’s fast full-text search capabilities. An inverted index maps terms (words or tokens) to the documents that contain them, allowing quick lookups of documents based on the terms they include.

**Example**: For documents containing the following texts:

- Document 1: “Elasticsearch is powerful”
- Document 2: “Elasticsearch is scalable”

The inverted index might look like:

- “Elasticsearch”: [Document 1, Document 2]
- “is”: [Document 1, Document 2]
- “powerful”: [Document 1]
- “scalable”: [Document 2]

## **2. Document Store**

Documents in Elasticsearch are stored in a document-oriented database. Each document is a JSON object, and Elasticsearch stores and retrieves these documents efficiently.

## **3. BKD Tree**

Elasticsearch uses a specialized tree structure called a BKD (block k-d) tree for efficient indexing and searching of numeric and geo-point data. This tree structure helps in handling high-dimensional numeric data and provides efficient range queries and geo-distance searches.

## **4. Doc Values**

Doc values are a columnar storage format used by Elasticsearch to handle sorting, aggregations, and access to field values in documents efficiently. They allow Elasticsearch to access field values quickly without having to load entire documents.

## **5. Finite State Transducers (FSTs)**

FSTs are used to efficiently store and query prefix and exact match queries. They are particularly useful for handling autocomplete and suggestive search features.

## **6. Priority Queues and Heaps**

Elasticsearch uses priority queues and heaps internally for managing tasks like merging search results and handling top-k queries (e.g., fetching the top N search results).

## **7. Segment Files**

Elasticsearch indexes are divided into segments, and each segment is an inverted index. Segment files contain the actual data and metadata for the documents within that segment. When documents are added, deleted, or updated, Elasticsearch creates new segments and periodically merges them to optimize performance.

# **Let’s do one real-life example and store data like Elasticsearch would :**

Imagine we have a collection of three documents with the following content:

- **Document 1**: “Elasticsearch is a search engine”
- **Document 2**: “Elasticsearch can index documents quickly”
- **Document 3**: “A search engine can be powerful”

## **Tokenization**

First, Elasticsearch tokenizes each document into terms:

- **Document 1**: [“Elasticsearch”, “is”, “a”, “search”, “engine”]
- **Document 2**: [“Elasticsearch”, “can”, “index”, “documents”, “quickly”]
- **Document 3**: [“A”, “search”, “engine”, “can”, “be”, “powerful”]

## **Building the Inverted Index**

Elasticsearch then builds an inverted index mapping each term to the documents that contain it.

**Inverted Index:**

TermDocument IDsa[1]be[3]can[2, 3]documents[2]elasticsearch[1, 2]engine[1, 3]index[2]is[1]powerful[3]quickly[2]search[1, 3]

## **Using the Inverted Index**

When a search query is issued, such as “search engine,” Elasticsearch looks up the terms in the inverted index:

- **“search”**: [1, 3]
- **“engine”**: [1, 3]

Elasticsearch then combines the results to find documents containing both terms, which are Documents 1 and 3.

# **Adding and Retrieving Documents**

## **Indexing a Document**

To index a new document:

**Document 4**: “Quickly searching documents with Elasticsearch”

Tokenized terms:

- [“Quickly”, “searching”, “documents”, “with”, “Elasticsearch”]

The inverted index is updated to include Document 4:

**Updated Inverted Index:**

TermDocument IDsa[1]be[3]can[2, 3]documents[2, 4]elasticsearch[1, 2, 4]engine[1, 3]index[2]is[1]powerful[3]quickly[2, 4]search[1, 3]searching[4]with[4]

## **Searching for a Term**

If a user searches for “documents,” Elasticsearch finds it in the inverted index and retrieves Document IDs [2, 4].

# **Internal Data Structure Representation**

**Visual Representation of the Inverted Index:**

```
+--------------+---------------------+
| Term         | Document IDs        |
+--------------+---------------------+
| a            | [1]                 |
| be           | [3]                 |
| can          | [2, 3]              |
| documents    | [2, 4]              |
| elasticsearch| [1, 2, 4]           |
| engine       | [1, 3]              |
| index        | [2]                 |
| is           | [1]                 |
| powerful     | [3]                 |
| quickly      | [2, 4]              |
| search       | [1, 3]              |
| searching    | [4]                 |
| with         | [4]                 |
+--------------+---------------------+
```

# **Summary**

The inverted index is a core component that enables Elasticsearch to quickly search and retrieve relevant documents based on terms. By mapping terms to document IDs, Elasticsearch can efficiently handle search queries even across large datasets. This powerful data structure, along with others like BKD trees for numeric and geo-data, doc values for aggregations, and more, allows Elasticsearch to provide robust search and analytics capabilities.