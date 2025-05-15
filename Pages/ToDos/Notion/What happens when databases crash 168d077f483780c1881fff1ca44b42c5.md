# What happens when databases crash?

Tags: databases
Category: Articles
Company: general
Status: Not started

This can make an interesting interview question.

Databases have tables and indexes stored in files and cached in memory aka as buffer pool. As you create rows, the database system writes the rows to data pages on memory first which is then eventually written to data files on disk.

Reading a page always checks the memory buffer pool. If it is not there it pulls the page from disk and place it in the buffer pool.

There is a problem though, what happens if you lose power half-way through writing to the data files? Some pages would have been written while others didn’t. When the database starts back up, we end up with data loss, or worse corruption.

# **Meet the WAL**

Database folks quickly realized that they need something that would help with crashes and power loss, and that is the WAL (Write-ahead log) or Redo log.

What if as we write to tables and indexes data pages we create a log entry in the WAL of those changes. We write the WAL to its own files and also write to the data pages in memory. It is OK not write to the actual table and index data files on disk, those can stay in memory, as long as we have a log we can always construct the table.

The WAL is much smaller than the actual data files, and so we can flush them relatively faster. They are also sequential unlike data pages which are random. Disks love sequential writes, which is another benefit of WAL.

The WAL can also be used for all sort of things like replications and backup and yes crash recovery.

# **What if we crashed while writing the WAL?**

WAL entries are also written to memory first and then flushed later based on the transactions commit. That is why the transaction state is critical.

The database can crash after writing WAL entries, that is fine, as long we know the transaction state belonging to each WAL entry we can discard or omit uncommitted WAL entries upon recovery.

For example if you are in the middle of a transaction and the database crashed, we consider the transaction rolled-back by default. WAL entries flushed by this uncommitted transaction will be discarded upon recovery.

But if you were able to issue a COMMIT and the WAL entry for a transaction commit makes it to disk and the client gets a success, that transaction is considered committed even if we crashed right after. The database remain consistent in that case.

# **Redoing the WAL**

So we have established that WAL is the source of truth, we write the changes to data pages in memory of course (for on going transactions to use the latest and greatest) but we delay flushing the data pages to disk because the WAL made it to disk. The WAL is ahead of the data pages, thus the name, write ahead log.

Now we have data files on disk that are out of sync with what is in memory which is absolutely fine. As long as the database is running, we will only read from memory which has the latest. The problem is if the database crashes.

As the database starts back up, the file is out of date we can’t just pull it to memory and have clients read them, the WAL is the source of truth, we need to REDO the changes in the WAL back on the data files, and during that process nothing is allowed to read (otherwise we get corruption). The database startup time slows down the more out of sync the data files are from the WAL (many writes has happened but the data files were not updated for a long time).

# **Checkpointing**

The question here can I control how often data pages are flushed to disk? And the answer is yes, this is called as [checkpointing](https://www.postgresql.org/docs/current/sql-checkpoint.html), where a new WAL record is created called checkpoint record right after the entire data pages in memory are flushed to disk.

Checkpointing however is an IO heavy operation, the data pages can be very large and very random.

Too much checkpointing sure makes start up faster, but it indeeds takes a toll on your I/O disk bandwidth which may take precious time from critical point reads or writes.

Some database systems have also undo logs, but that is for another post.

# **How often should we flush the WAL?**

WAL contains changes from several transactions. If one of the transactions commit, we have to flush WAL to disk if we want to maintain durability. Of course this will flush other transactions data that may have not been committed which as we discussed is also fine, the transaction state saves us here.

But some databases expose certain configurations to relax how often the WAL is flushed. One of them being [fsync](https://x.com/hnasr/status/1661701014700048385), which ensures the contents of the WAL file is flushed to disk out of the OS page cache. Another is a transaction sibling commit delay, which waits for more transactions to commit so we incur fewer flushes.