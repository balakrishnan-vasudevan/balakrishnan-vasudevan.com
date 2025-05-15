# MongoDB Internal Architecture

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article3.5c705a01b476.png)

## Metadata
- Author: [[Hussein Nasser]]
- Full Title: MongoDB Internal Architecture
- Category: #articles
- URL: https://medium.com/p/9a32f1403d6f

## Highlights
- Users submit JSON documents to Mongo where they are stored internally as BSON (Binary JSON) format for faster and efficient storage. Mongo retrives BSON and cover them back to JSON for user consultation.
- Users create collections (think of them as tables in RDBMS) which hold multiple documents. Because MongoDB is schema-less database, collections can store documents with different fields and that is fine. Users can submit document with a field that never existed any document in the collection.
- The _id primary index is used to map the _id to the BSON document through a B+Tree structure.
- Users can create secondary B+Tree indexes on any field on the collection which then points back to BSON documents satisfying the index. This is very useful to allow fast traversal using different fields on the document not just the default _id field. Without secondary indexes, Mongo has to do a full collection scan looking for the document fields one by one.
- WiredTiger has many features such as document level locking and compression. This allowed two concurrent writes to update different documents in the same collection without being serialized, something that wasn’t possible in the MMAPV1 engine. BSON documents in WiredTiger are compressed and stored in a hidden index where the leaf pages are recordId, BSON pairs. This means more BSON documents can be fetched with fewer I/Os making I/O in WiredTiger more effective increasing the overall performance.
- Primary index _id and secondary indexes have been changed to point to recordId (a 64 bit integer) instead of the Diskloc. This is a similar model to PostgreSQL where all indexes are secondary and point directly to the tupleid on the heap.
- The double lookup cost consumes CPU, memory, time and disk space to store both primary index and the hidden clustered index. This is also true for secondary indexes.
- A Clustered Index is an index where a lookup gives you all what you need, all fields are stored in the the leaf page resulting in what is commonly known in database systems as Index-only scans. Clustered collections were introduced in Mongo 5.3 making the primary _id index a clustered index where leaf pages contain the BSON documents and no more hidden WT index.
- This way a lookup on the _id returns the BSON document directly, improving performance for workloads using the _id field. No more second lookup.
- Because the data has technically moved, secondary indexes need to point to _id field instead of the recordId. This means secondary indexes will still need to do two lookups one on the secondary index to find the _id and another lookup on the primary index _id to find the BSON document. Nothing new here as this is what they used to do in non-clustered collections, except we find recordid instead of _id.
- However this creates a problem, the secondary index now stores 12 bytes (yes bytes not bits) as value to their key which significantly bloats all secondary indexes on clustered collection. What makes this worse is some users might define their own _id which can go beyond 12 bytes further exacerbating the size of secondary indexes. So watch out of this during data modeling.
- This changes Mongo architecture to be similar to MySQL InnoDB, where secondary indexes point to the primary key. But unlike MySQL where tables MUST be clusetered, in Mongo at least get a choice to cluster your collection or not. This is actually pretty good tradeoff.
- However, one must use it with caution as the more secondary indexes the larger the size of these indexes get the harder it is to put them in memory for faster traversal. The MongoDB docs on clustered collection.
- MMAPV1 comes with some of limitations. While Diskloc is an amazing O(1) way to find the document from disk using the file and offset, maintaining it is difficult as documents are inserted and updated. When you update a document, the size increases changing the offset values, which means now all Diskloc offsets after that document are now off and need to be updated. Another major limitation with MMapv1 is the single global databse lock for writes, which means only 1 writer per database can write at at time, signfically slowing down concurrent writes.
