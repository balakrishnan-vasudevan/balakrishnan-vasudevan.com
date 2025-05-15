https://medium.com/systemdesign-us-blog/how-does-storage-work-in-distributed-systems-fde890e88a7f



### **Object storage**

Object storage stores and manages data as discrete units called _objects_. An object typically consists of the actual data—such as documents, images, or data values— and its associated metadata. Metadata is additional information about the object that you can use to retrieve it. The metadata can include attributes like the unique identifier, object's name, size, creation date, and custom-defined tags.

Object storage systems use a flat namespace, so objects are stored without the need for a hierarchical structure. Instead, the object’s unique identifier provides the address for the object within the storage system. A hashing algorithm generates the ID from the object's content, which ensures that objects with the same content have the same identifier.

### **Block storage**

Block storage works by dividing data into fixed-sized blocks and storing them as individual units. Blocks range from a few kilobytes to several megabytes in size. They can be predetermined during the configuration process.

The operating system gives each block a unique address or block number, logged inside a data lookup table. The addressing uses a logical block addressing (LBA) scheme that assigns a sequential number to each block.

Block storage allows direct access to individual data blocks. You can read or write data to specific blocks without having to retrieve or modify the entire dataset the block belongs to. 

### **Cloud file storage**

Cloud file storage is a hierarchical storage system that provides shared access to file data. It uses a remote infrastructure of servers to store data. The cloud provider maintains the servers and manages data on them. Files contain metadata like the file name, size, timestamps, and permissions.

You can create, modify, delete, and read files. You can also organize them logically in directory trees for intuitive access. Multiple users can simultaneously access the same files. Security for online file storage is managed with user and group permissions, so that administrators can control access to the shared file data.

## What are the key differences between object storage, block storage, and file storage?

Object storage, block storage, and cloud file storage have some key differences.

### **File management**

Object storage solutions support storage of files as objects. Accessing them with existing applications requires new code, the use of APIs, and direct knowledge of naming semantics. 

Similarly, block storage can be used as the underlying storage component of a self-managed file storage solution. However, the one-to-one relationship required between the host and volume makes it difficult to have the scalability, availability, and affordability of a fully managed file storage solution. You require additional budget and management resources to support files on block storage.

Only file-based storage supports common file-level protocols and permissions models. You don’t require new code to integrate with applications configured to work with shared file storage.

### **Metadata management**

Object storage metadata can hold any amount of information about an object. This includes its name, content type, creation date, size, or other custom-defined inputs. By using a flexible metadata schema, you can create additional fields that help you locate data. 

Block storage stores as little metadata as possible to maintain high efficiency. A very basic metadata structure ensures minimal overheads during a data transfer. Block storage mainly uses unique identifiers for each block when searching, finding, and retrieving data.

Cloud file storage uses metadata to describe the data that a file holds. You can access and change the metadata that’s attached to files. This function depends on your access. Cloud storage systems using access control lists (ACLs) as permission control of who can access and change metadata.

### **Performance**

Object storage systems prioritize storage quantity over availability. As highly scalable systems, you can store large volume of unstructured data in an object storage system. However, there’s more latency when you access these files. Object storage also has a lower throughput compared to block storage and cloud storage. 

Block storage offers high performance, low latency, and quick data transfer rates. As it operates on a block level, you can directly access data and achieve a high I/O performance. You use block storage for applications that need fast access to data you have stored, like a virtual machine or database. 

Cloud file storage can offer high performance, but this isn’t the main reason you would use it. Instead, cloud file storage is more about storing data in a manner intuitive for human access. File sharing, collaboration, and shared repositories are more common with cloud file storage than high performance.

### **Physical storage systems**

Object storage normally uses a distributed storage environment across multiple different storage nodes or servers.

On the other hand, block storage uses RAID, SSDs, and hard disk drives (HDDs) for storage.

Finally, cloud file storage uses network-attached storage (NAS) in an on-premises setup. In the cloud, file storage service may be set up over underlying physical block storage.

[Read a comparison of SDDs and HDDs »](https://aws.amazon.com/compare/the-difference-between-ssd-hard-drive/)

[Read about NAS »](https://aws.amazon.com/what-is/nas/)

### **Scalability**

Object storage offers near-infinite scaling, to petabytes and billions of objects.

Block storage offers scalability by adding more storage volumes or expanding existing volumes. Scalability depends on the block storage system's ability to handle increased I/O demands and capacity requirements.

Because of the inherent hierarchy and pathing, file storage hits scaling constraints and is the least scalable of the three.

## When should one use object storage, block storage, and file storage?

![[Pasted image 20250505091430.png]]

Object storage is best used for large amounts of unstructured data. This is especially true when durability, unlimited storage, scalability, and complex metadata management are relevant factors for overall performance.

Block storage offers high-speed data processing, low latency, and high-performance storage. Any service that requires fast access to data works well with block storage. For example, real-time analytics, high-performance computing, and systems with many rapid transactions all benefit from block storage.

Cloud file storage is best when users need concurrent access to a shared system of files. Additionally, file-level access control allows you to set up permissions and access control lists (ACLs) to increase security. For example, collaborative work environments that require sharing files between remote teams use file storage. 

## Summary of differences: object vs. block vs. file storage

|                     |                                                                                                                             |                                                                                                            |                                                                                                                                  |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
|                     | **Object storage**                                                                                                          | **Block storage**                                                                                          | **Cloud file storage**                                                                                                           |
| File management     | Store files as objects. Accessing files in object storage with existing applications requires new code and the use of APIs. | Can store files but requires additional budget and management resources to support files on block storage. | Supports common file-level protocols and permissions models. Usable by applications configured to work with shared file storage. |
| Metadata management | Can store unlimited metadata for any object. Define custom metadata fields.                                                 | Uses very little associated metadata.                                                                      | Stores limited metadata relevant to files only.                                                                                  |
| Performance         | Stores unlimited data with minimal latency.                                                                                 | High-performance, low latency, and rapid data transfer.                                                    | Offers high performance for shared file access.                                                                                  |
| Physical storage    | Distributed across multiple storage nodes.                                                                                  | Distributed across SSDs and HDDs.                                                                          | On-premises NAS servers or over underlying physical block storage.                                                               |
| Scalability         | Unlimited scale.                                                                                                            | Somewhat limited.                                                                                          | Somewhat limited.                                                                                                                |



