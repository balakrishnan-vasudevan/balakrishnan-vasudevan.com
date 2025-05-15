
Here are some commonly used database terms along with brief descriptions:

  

1. General Database Terms

• Database: A structured collection of data stored and managed electronically.

• Schema: The structure of a database, defining tables, columns, data types, and relationships.

• Table: A collection of rows and columns that stores related data in a relational database.

• Record (Row/Tuple): A single entry in a table, representing a set of related values.

• Column (Field/Attribute): A vertical data structure in a table that defines a specific type of data.

  

2. Keys and Indexing

• Primary Key: A unique identifier for a row in a table (e.g., id column).

• Foreign Key: A column that references a primary key in another table to establish relationships.

• [[Indexing]]: A data structure that improves query performance by allowing faster lookups.

• Composite Key: A primary key made up of multiple columns.

• Unique Constraint: Ensures that all values in a column or combination of columns are unique.

  

3. Transactions and Concurrency

• Transaction: A sequence of database operations that must be completed fully or not at all (Atomicity).

• ACID: Properties that ensure reliable transactions:

• Atomicity: All operations in a transaction succeed or none do.

• Consistency: The database remains valid before and after a transaction.

• Isolation: Transactions do not interfere with each other.

• Durability: Changes from committed transactions persist even after system failures.

• Deadlock: A situation where multiple transactions block each other from accessing resources.

• Locking: Mechanism to control concurrent access to data.

  

4. Querying and Optimization

• SQL (Structured Query Language): The language used to interact with relational databases.

• JOIN: A SQL operation used to combine rows from multiple tables based on a related column.

• Normalization: Organizing a database to reduce redundancy and improve efficiency.

• Denormalization: Combining tables to optimize read performance at the cost of some redundancy.

• Stored Procedure: A precompiled set of SQL statements stored in the database for reuse.

• View: A virtual table based on a query that provides a subset of data.

  

5. Storage and Performance

• [[Sharding]]: Splitting a large database into smaller, distributed databases for scalability.

• [[Replication]]: Copying data across multiple servers for redundancy and availability.

•[[Partitioning]]: Dividing a table into smaller pieces for better query performance.

• Caching: Storing frequently accessed data in memory for faster retrieval.

  

6. NoSQL and Modern Databases

• NoSQL: A type of database that does not use the traditional relational model (e.g., MongoDB, Redis).

• Document Store: A NoSQL database that stores data in JSON or BSON format (e.g., MongoDB).

• Key-Value Store: A database where data is stored as key-value pairs (e.g., Redis).

• Column-Family Store: A database that organizes data into column families (e.g., Cassandra).

• Graph Database: A database optimized for relationships between entities (e.g., Neo4j).

[[pages/Systems/Systems Primer/DBs/Following a database read to the metal|Following a database read to the metal]]
   [[CQRS]]