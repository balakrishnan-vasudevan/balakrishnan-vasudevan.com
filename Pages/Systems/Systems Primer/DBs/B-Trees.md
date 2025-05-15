A binary tree using pointers on disk 
Writes iterate through the binary tree and either overwrite the existing key value or create a new page on disk and modify the parent pointer to the new page

Pro: Faster reads, know exactly where key is located! 
Con: Slow writes to disk instead of memory.


![[Screenshot 2025-03-31 at 11.04.07 AM.png]]
**Introduction to B-Trees**

B-Trees are a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. They are widely used in relational databases like MySQL, PostgreSQL, and Oracle.

**Architectural Advantages of B-Trees**

**1. Balanced Read and Write Performance:** B-Trees are designed to provide a good balance between read and write operations. The tree structure allows for efficient searching, insertion, and deletion operations, typically with O(log n) complexity.

**2. Disk Storage Optimization:** B-Trees are optimized to minimize disk access, which is crucial for database performance. They ensure that nodes are loaded into memory as infrequently as possible, making them suitable for systems where disk I/O is a significant bottleneck.

**3. Efficient Range Queries:** Since B-Trees maintain data in a sorted order, they are particularly efficient for range queries. For example, querying all records between two dates can be performed by traversing the tree from the starting date to the ending date without needing to scan the entire dataset.

**B-Trees in Relational Databases**

In relational databases, B-Trees are used as the primary index structure. They help maintain the order of records and ensure efficient access. For example, an SQL query that selects data based on a range of dates can efficiently retrieve the required records using a B-Tree index.

However, while B-Trees offer balanced read and write capabilities, they are not always the best choice for applications with extremely high write loads, such as those encountered in time-series data ingestion. The need for rebalancing and maintaining order can introduce overhead, particularly in write-heavy scenarios.

![[Pasted image 20250331111323.png]]

- **Root Node:** The top-level node containing keys that partition the dataset.
- **Internal Nodes:** Intermediate nodes that help in navigating the tree.
- **Leaf Nodes:** The bottom-level nodes that store the actual data entries.

The arrows represent the branches connecting the nodes, guiding the search, insertion, and deletion operations within the B-tree.


[[pages/Systems/Systems Primer/DBs/Postgres]]
[[Pages/General/Readwise/Articles/MongoDB Internal Architecture]]
