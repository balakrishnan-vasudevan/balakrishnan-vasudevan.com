https://medium.com/@hnasr/following-a-database-read-to-the-metal-a187541333c2


![[Pasted image 20250314141643.png]]


When you create a table in a database, a file is created on disk and the data are layout out into  ==[fixed-sized database pages](https://medium.com/@hnasr/database-pages-a-deep-dive-38cdb2c79eb5)====. How the data is laid out in the page depends on whether the engine is row-store or column-store. Think of a page as a structure which has a header and data, the data portion is where the rows live.

A database page can be 8KB (Postgres) or 16KB (e.g. MySQL innodb) or more. The table is stored as an array of pages in the file, where page index + size tells the database exactly which offset to seek to and how much to read. For example, assume database page size is 8KB to read page 7 on disk, you need to seek to the offset 7*8192 + 1 and you would read a length of 8192 bytes.

The row and all its column are stored in the page one after the other. If a row cannot fit in the remaining space in the page, a new page is allocated and that row is placed in the new page.

==When a page is read from disk and placed into the buffer pool, we get any rows (and columns) that are in that page essentially for free. Believe it or not this might be the single most important realization to database optimization and data modeling.==

With that out of the way, let us execute this query, table STUDENTS, with an ID field of type serial (monotonically increasing). The table has 20k rows, spread across 20 pages. The row we want 1008 lives in page 1 (second page). Nothing in the caches. I don’t want to include indexes here just to keep things simple, slow but simple. I’ll be only drawing the first three pages for simplicity.

SELECT NAME FROM STUDENTS WHERE ID = 1008;

> Whether we are using clustered indexes where the primary index is the table or using a heap table without a primary index such in postgres, I think the model here is similar. Regardless the ID field is not indexed, in case of InnoDB you can think of another field as the primary key which forces us to do a full index scan where we read the leaf pages of the primary index, and in postgres a sequential scan on the table. We assume a 8KB page.

## Database

The database parses and understand the query and because the ID field is not indexed it goes into a full table scan mode to fetch row with value 1008.

The database starts at page 0 and checks if page 0 is in the buffer pool cached. Buffer pool is a shared memory space between all the database processes where the pages are kept, the pages can also receives writes there too. The database doesn’t find it to so issues a read to the table file to read page 0.

The seek position on the file is 0*8192 and we are reading 8192 bytes. The page is read and placed in the shared buffers memory. The page includes rows 1–1000, the databases parses the page, deserialize the look up the ID value for each row in memory and doesn’t find it. So we move to read page 1.

Reading page 1 will set the seek position on the file is 1*8192 and we are reading 8192 bytes. Page 1 is placed in memory in the shared buffers along side Page 0, the database looks up the row 1008 in the page, it finds it and returns to the user.

![[Pasted image 20250512075416.png]]

Let us now break that further and see what happens when the database issues the read to the OS.

## File System

The File system reads and writes data from disk in units called blocks or logical blocks. These units could range from 512 bytes to 4KB being the most common.

The operating system receives the request to issue a read for the file on offset 0 reading 8192 bytes and maps the requested bytes to file system blocks using the file system index node or _inode_ which contains metadata about the file. Each logical file system block address (LBA) maps to specific physical block in storage device as we will learn later. If you read a single byte you actually reading an entire block from disk.

![[Pasted image 20250512075431.png]]
When the request to read from offset 0 — 8192 bytes, the OS does checks the following things:

1. What are the blocks between offset 0 and byte 8192 on the file?
2. Assume 4KB file system block size, that give us two blocks.
3. The file system looks up the file’s inode (index node) to look up the logical block addresses (LBAs). Let us say the blocks are 100 and 101.
4. The OS then looks up blocks 100 and 101 in the file system page cache to see if a previous read has fetched them and put them in memory.
5. The file system page cache is in memory storing the block addresses and the address of virtual memory page on main memory.
6. The virtual memory page in the OS is often 4KB matching the block size. So you can fit one block in a memory page.
7. Say the OS doesn’t find blocks 100 and 101 in the page cache, so it prepares to read from disk.

Note the index node contain other metadata about the file such as permissions.

![[Pasted image 20250512075448.png]]

## Storage

We learned that reading the page 0 translates to offset 0 and length 8192 which got translated to file system blocks 100 and 101 each of size 4KB. The OS checked its cache and couldn’t find those blocks so it reads from disk.

Assume an NVMe SSD, the OS through the NVMe driver issues a read command to the storage device. The read command takes many parameters but what he most important is the starting LBA (logical block address) and the second parameter is the number of blocks to read. This means the drive issues a read command passing (100, 0) 0 in the length means read 1 block in NVM command set.

> Now here is where it gets interesting. The “block” size in NVMe can be different in size than the file system block size. For example here we assumed the NVMe block is identical to file system and equal to 4KB. If those were different the OS need to change the read parameters. For example if the NVMe block size is 2KB, the file system block size will contain 2 NVMe blocks. So read command will be 101, 3.

The SSD is broken into pages, that is the minimum read and write unit. The SSD NAND Page is [16KB in size these days](https://keefmck.blogspot.com/2023/04/why-ssds-lie-about-flush.html). The pages are grouped in larger units called erase unit confusingly often also called block. To write to an SSD page, the page must be in an erased state and you can’t erase a page by itself you have to erase the entire erase unit.

Now our NVMe logical block address maps to an offset within this page we speak off. So in this case since our NVMe logical block size is 4KB, 4 blocks fits in an SSD NAND page.

The SSD doesn’t really work with logical block addresses, it only knows the physical location of pages. So there must be a translation that needs to happen from logical block address to the offset in physical page. Because SSD page can be larger than block multiple blocks can map to the same page in different offsets.

![[Pasted image 20250512075506.png]]

The NVMe controller receives the command to read LBA 100 and LBA 101, the thing about NVMe drives are those logical block addresses, those two blocks are translated to physical page and offset say page 99 and offset 0x0001 and 0x1002 repsectively. Next the NVMe controller checks the local SSD DRAM cache to see if page 99 is in the cache. And yes there is an SSD cache. If page 99 isn’t in the cache, it is fetched entirely to the cache (the whole 16KB) and placed in the cache.

Once the page is in the cache the respective blocks are extracted from the page and returned to the OS host. In this case only the first 8KB is returned.

> You might say why not have the OS access the physical address of the pages directly? why this translation? The reason is because the disk sometimes need to move data around and it is hard to move data around when the OS points to the physical location.
> 
> Ironically, the moving data around can be offloaded to the host but without a cost at application complexity. Nothing is free. This is a deep researched topic that you may decide to dive into.

## Back to the File System

The OS gets the 8KB representing the two blocks 100, 101 and place it in two memory pages, It then updates the file system page cache so that next request to pull 100 or 101 can hit the host memory.

## Back to the database

The OS then returns the control to the database application which if you remember issued the read offset 0, length 8192 corresponding to page 0. The database puts the raw bytes into the shared buffer pool memory (different from file system cache). Page 0 is now “hot” for any other query to pull from it, page 0 can receive writes before it is flushed to disk.

Of course the next page is page 1 goes through the same story until the row ID 1008 is found.

## Summary

To read a single row from a database you have to read the page in which the row lives in. To read the database page, the DB issues a read with correct offset and length that corresponds to the page to the file. The OS maps those bytes to file system blocks address (or LBAs), the LBAs are checked against the file system page cache to see if there is a memory page with those blocks, Otherwise a read command is sent to the storage controller. The device converts the logical blocks to physical addresses, and pulls the page in cache and returns the requested bytes to the OS host. The host puts the blocks in the file system page cache and returns to the database, the database puts the page in shared buffer pool and starts processing and return the requested single row to the user.

You might say what if I have indexes? Similar story, the index is a b+tree structure that also stored on disk and has pages. When traversing the tree you will be fetching pages so the concept is identical.




[[LSM Trees and SSTables]]
[[B-Trees]]
[[RocksDB]]
![[Pasted image 20250331111547.png]]
