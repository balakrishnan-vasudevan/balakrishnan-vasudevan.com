# How a SQL database works

Status: Not started
URL: https://calpaterson.com/how-a-sql-database-works.html

The details on how tables and indexes work. Rows, pages, the heap and indexes are all covered, both on-disk layout and querying.

SQL (or relational) databases are some of oldest and probably still are the single most commonly used database technology - both in database server form (such as postgresql) or in library form (sqlite).

Despite this, SQL databases' internal operations can be mysterious to a surprisingly large number of people - even those who work with them daily.

Unlike other database technologies, such key-value stores or graph databases, relational databases are not based on a single data structure but a combination of several different data structures. Understanding this combination is not difficult and can help a lot when working with a SQL database.

## The relation

Programmers most often work with just two primary data types: arrays and associative arrays.

**Arrays** allow for lists of objects, providing a way of grouping multiple objects together.

![array.svg](array.svg)

Example array holding cats in an imaginary animal shelter

Array implementation details vary widely but in general: an item can be added to an array at the end in a constant amount of time no matter the size of the array already. Searching for an given item is different: each entry in the array must be checked and this takes a length of time proportional to the size of the array at present (deletion has similar performance characteristics).

| Operation | Time (worst-case) |
| --- | --- |
| Insert | Constant / O(1) |
| Search/Delete | Linear / O(n) |

**Associative arrays** (often called "hash-tables" after the most common implementation) allow for reference to items via a "key".

![assoc-array.svg](assoc-array.svg)

Example hash table holding the same cats, "keyed" by their registration number.

This key must be unique for each item but associate arrays typically allow for fast insert, search and delete *so long as the key is being used*. If the key isn't being used for the operation, the entire data structure must be traversed, just as with arrays.

| Operation | Time (worst-case) |
| --- | --- |
| Insert | Constant / O(1) |
| Search/Delete (by key) | Constant / O(1) |
| Search/Delete (otherwise) | **Linear / O(n)** |

SQL databases use a different type: the **relation**.

A relation is a generalisation of both of these data types. A relation is a set of tuples. Each tuple can hold the details of a single item but the individual fields are split out and accessible on the relation level. Within a relation, the tuple form is exactly the same for each tuple.

![relation.svg](relation.svg)

Example relation holding the same cats.

Relations are useful because they expose the internal fields of what was previously an opaque object. Fields like age and breed are now open to operations on the relation level itself. This means that more complicated operations are possible on the relation without having to write specific functions to ask questions of objects.

Being able to operate on fields directly also allows for easy definition of "indexes", which speed up access and search within the database.

SQL databases' implementation of relations varies a little but are mostly a combination of two different underlying data structures: the **heap file** and **b-trees**. Consequently the operation times are generally logarithmic - meaning that they grow slowly as the size of the data-set grows.

| Operation | Time (worst-case) |
| --- | --- |
| Insert | Logarithmic / O(log n) |
| Search/Delete | Logarithmic / O(log n) |

The rest of this discussion will be about how these two underlying data structures work.

## The row

SQL databases aren't a perfect representation of relations. Instead of relations and tuples they represent "tables" and "rows". Rows are functionally the same as tuples but tables have a quirk - duplicate rows are allowed. This does matter for writing queries but doesn't change the fundamentals of how things work so I'll treat them as the same and will use SQL terminology from now on.

Rows are typically represented, both on-disk and in memory, as a short header followed a concatenation of row values.

![row.svg](row.svg)

Example row holding data on Alfred.

The header will often contain information about the total length of the row. Depending on the specific implementation it might also contain other information, especially information about concurrency (ie: which transactions a given row is visible in).

The rest of the row is just the values, one after another.

There are two kinds of row values: those that are fixed length and those that are variable length. A 32-bit integer or a 64 bit float is an example of a fixed length value those can be represented directly. Strings, binary blobs, JSON, XML and other types can vary in length can be handled in one of two ways.

One common method is to use a special "terminator" character (often NULL or `\0`). This method means that null either cannot be allowed to appear in the string or that NULLs have some special handling to avoid ambiguity. The other alternative is to have a a leading length indicator to specify how many bytes long the string is.

The order that the values of the row appear in could be included in the header but usually is table level metadata to avoid having to waste space repeatedly including information about what the order of the row values is.

## The heap

Rows are stored in what is commonly called "the heap". This is where the main body of table data is held. The heap is broken down further into pages. Pages are short (often 4 or 8 kilobyte) collections of rows, again with a small header to indicate how many rows are present.

![page.svg](page.svg)

Example page. Note that the page has a fixed size and that free space is at the end.

Pages are a common pattern in systems which manage data that is moved frequently between disk and main memory. For exmaple, operating systems use pages in their virtual memory implementations.

![heap.svg](heap.svg)

Example heap. Just a header and then page after page. The heap can grow to an unlimited size. Note that there is a gap where Page 3 has been deleted.

Working through pages, operations on the heap are simple. To perform a write, the relevant page is read from disk into memory if necessary, then edited and then written back to disk. Updates are similar. Pages can be appended to until there is no more space for any additional rows. Deletion is similarly simple: the page is rewritten without the unwanted row.

Use of pages instead of storing rows directly in a file has a few advantages. The first is that pages are highly amenable to IO buffering, which helps performance. In many IO systems reading a whole page from disk takes the same amount of time as would reading a 40 byte row directly. Once a page has been read into memory it can be kept there as a cache until there is a shortage of memory and it has to be evicted from memory.

The second reason is that access to pages by number is fast - the database system seeks to the start of the page ((page size * page number) + 1) and then reads forward as many bytes as the page size. This makes the heap and page system very efficient if there is an external reference to the page number.

The third benefit is that pages allow fragmentation to be dealt with piecewise. Fragmentation happens when rows are deleted, creating gaps. If rows were written directly, these gaps would be difficult to fill - only a row of the same or equal size as the deleted row could be placed in the gap. With pages, fragmentation is limited as pages are written whole with the gaps moved to the end of the page. Perhaps when a page is completely empty a page from the end of the heap can be moved and written in this location instead.

Heaps overall have great performance for insertion. A free space has to be found and then the row written into it. Depending on the method for finding this can be as simple as writing to the last page and calling it a day.

The problem heaps don't solve is search. When you want to find all rows where a=1, you need to work through every page to find it. That's often called a "full table scan" and performs very poorly. Narrowing the number of pages that must be consulted improves performance hugely. What is required for this is an **index**.

## The index

The crucial addition on top of the heap is the index. SQL databases overwhelmingly use B-trees (or minor variations) as indexes.

B-trees were invented at Boeing in the 1970s. Despite allusions in the name, they aren't binary trees - though they are balanced. B-trees work in the following way: each node holds an ordered list. Each element in that list is either a value itself or a reference to another node that holds the value in question (or which holds yet another reference to that value).

A node will usually fill a database page - so the ordered list will contain hundreds or thousands of elements. This makes b-trees very dense per-page and hopefully very shallow - ideal for looking up a key with the minimum of dereferences (each dereference could cause a page load). Some database systems use the same heap structure for heap pages and index pages.

![b-tree.svg](b-tree.svg)

Example b-tree. In reality they are likely to be thousands of entries wide - however they will usually be similarly shallow - often just 2 or 3 levels.

All operations on B-trees have logarithmic complexity: execution time grows slowly as the number of items in the index increases. This means that they remain fast even with large database sizes.

For many it can be surpising the indices aren't hash tables. After all, don't hash tables have faster access and insert times (constant) than b-trees? There are a few reasons for this.

Firstly, a hash table has a fixed size: if you have a hash function that outputs a two byte hash your hash table is limited to 65535 distinct locations[1](https://calpaterson.com/how-a-sql-database-works.html#fn:distinct-hashes). To deal with rising occupancy in your hashtable you have to "rebalance" - that is, increase the hash size and recalculate for all entries. Unfortunately rebalancing means having to recalculate every hash and hold both the new and old table in memory for a period.

Second is that hash tables are relatively sparse in memory. A 32-bit hash table requires 2GB of ram. Assuming that a rebalance occurs once occupancy is greater than 75% that means that *at least* 500mb of memory is wasted - likely more. This sparseness means they compete with the heap for memory.

The third reason is that hashing can't really help with operations where you want all values between two numbers - say, all cats adopted last week - as hash tables don't maintain order. This also causes hassle for the query optimiser as an estimate of rows returned cannot be provided until the query is under way.

## The combination in practice

A single table will have a single heap and *multiple* indexes. Each index will document, for each entry, in which page (or pages) a the relevant row can be found. This allows for general logarithmic access by any key if the relevant index exists.

## Contact/etc

Please do [send me an email](mailto:cal@calpaterson.com) about this article, especially if you disagreed with it.

If you liked it, you might like [other things I've written](https://calpaterson.com/).

If you enjoyed this article and as a result are feeling charitable towards me: **please try out my side-project, [csvbase](https://csvbase.com/meripaterson/stock-exchanges)**, or "Github, but for data tables".

## Further reading

1. 
    
    [Chapter 12 of the Postgres manual](https://www.postgresql.org/docs/12/internals.html) gives a good overview of the disk layout of their page and heap system.
    
2. 
    
    [SQL performance explained](https://www.librarything.com/work/12949629) gives a great overview of how querying works in detail and what you can do to improve your queries.
    
3. 
    
    [Transaction Processing: Concepts and Techniques](https://www.librarything.com/work/143113) covers the same material but in a lot more detail (and much more besides).