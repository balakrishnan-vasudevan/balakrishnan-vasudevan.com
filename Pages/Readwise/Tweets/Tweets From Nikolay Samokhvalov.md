# Tweets From Nikolay Samokhvalov

![rw-book-cover](https://pbs.twimg.com/profile_images/1527397132906270722/3YqidRm5.jpg)

## Metadata
- Author: [[@samokhvalov on Twitter]]
- Full Title: Tweets From Nikolay Samokhvalov
- Category: #tweets
- URL: https://twitter.com/samokhvalov

## Highlights
- When analyzing Postgres query execution plans, I always recommend using the BUFFERS option:
  explain (analyze, buffers) <query>;
  Example:
  test=# explain (analyze, buffers) select * from t1 where num > 10000 order by num limit 1000;
  QUERY PLAN
  ----------------------------------------------------------
  Limit (cost=312472.59..312589.27 rows=1000 width=16) (actual time=314.798..316.400 rows=1000 loops=1)
  Buffers: shared hit=54173
  ...
  Rows Removed by Filter: 333161
  Buffers: shared hit=54055
  Planning Time: 0.212 ms
  Execution Time: 316.461 ms
  (18 rows)
  If EXPLAIN ANALYZE used without BUFFERS, the analysis lacks the information about the buffer pool IO.
  Reasons to prefer using `EXPLAIN (ANALYZE, BUFFERS)` over just `EXPLAIN ANALYZE`
  1. IO operations with the buffer pool available for each node in the plan.
  2. It gives understanding about data volumes involved (note: the buffer hits numbers provided can involve "hitting" the same buffer multiple times).
  3. If analysis is focusing on the IO numbers, then it is possible to use weaker hardware (less RAM, slower disks) but still have reliable data for query optimization.
  For better understanding, it is recommended to convert buffer numbers to bytes. On most systems, 1 buffer is 8 KiB. So, 10 buffer reads is 80 KiB.
  However, beware of possible confusion: it is worth remembering that the numbers provided by EXPLAIN (ANALYZE, BUFFERS) are not data volumes but rather IO numbers – the amount of that IO work that has been done. For example, for just a single buffer in memory, there may be 10 hits – in this case, we don't have 80 KiB present in the buffer pool, we just processed 80 KiB, dealing with the same buffer 10 times. It is, actually, an imperfect naming: it is presented as "Buffers: shared hit=5", but this number is rather "buffer hits" than "buffers hit" – the number of operations, not the size of the data.
  Summary:
  Use EXPLAIN (ANALYZE, BUFFERS) always, not just EXPLAIN ANALYZE – so you can see the actual IO work done by Postgres when executing queries.
  This gives a better understanding of the data volumes involved. Even better if you start translating buffer numbers to bytes – just multiplying them by the block size (8 KiB in most cases).
  Don't think about the timing numbers when you're inside the optimization process – it may feel counter-intuitive, but this is what allows you to forget about differences in environments. And this is what allows working with thin clones – look at Database Lab Engine and what other companies do with it.
  Finally, when optimizing a query, if you managed to reduce the BUFFERS numbers, this means that to execute this query, Postgres will need fewer buffers in the buffer pool involved, reducing IO, minimizing risks of contention, and leaving more space in the buffer pool for something else. Following this approach may eventually provide a global positive effect for the general performance of your database.
  My old blog post on this topic: https://t.co/kME7opUAaF ([View Tweet](https://twitter.com/samokhvalov/status/1706689567355732052))
- I'm going to start a @PostgreSQL marathon: each day I'll be posting a new "howto" recipe. Today is the day zero, and the first post is here.
  My goal is to create at least 365 posts 😎
  Why am I doing it?
  1) Postgres docs are awesome but often lack practical pieces of advice (howtos)
  2) 20+ years of database experience, from small startups to giants like Chewy, GitLab, Miro - always have a feeling that I need to share
  3) eventually I aim to have a structured set of howtos, constantly improving it - and make the systems we develop at https://t.co/BHM0AWWGWC @Database_Lab better and more helpful.
  Subscribe, like, share, and wish me luck with this -- and let's go! 🏊‍♂️ ([View Tweet](https://twitter.com/samokhvalov/status/1706748070967624174))
