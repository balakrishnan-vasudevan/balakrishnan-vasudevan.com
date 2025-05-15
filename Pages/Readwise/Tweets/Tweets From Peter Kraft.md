# Tweets From Peter Kraft

![rw-book-cover](https://pbs.twimg.com/profile_images/1803927746034434048/qN_tlL_7.jpg)

## Metadata
- Author: [[@petereliaskraft on Twitter]]
- Full Title: Tweets From Peter Kraft
- Category: #tweets
- URL: https://twitter.com/petereliaskraft

## Highlights
- What if you could **prove **your program is correct? Not just "looks good to me", but a **formal mathematical guarantee** that it does what you want?
  This **formal verification **is far too difficult for most programs we write, but for the most critical software in the world, it may be worth it. There's not much software more critical than **AWS S3**, which is why this paper on how they formally verify part of its internals is so interesting.
  This paper focuses on one of the lowest-level, most complex, and most critical parts of S3-the storage node servers that persist object data on hard disks. When this paper was written, AWS was in the process of migrating to a new, higher-performance storage server implementation written in Rust, called ShardStore. Before moving critical customer data to ShardStore, they set out to **formally prove** its correctness.
  The main goal of the verification effort is to prove the storage servers **don't lose or corrupt data**: they're durable in the absence of crashes and consistent in the presence of crashes or concurrency. 
  The AWS team implemented verification in two main steps. First, they built **reference models** of their system that define its expected semantics. These are small executable specifications (1% of the size of the original) that are embedded in the code base and continuously updated alongside it. 
  Then, they verify that the actual system has equivalent observable behaviors to the reference model. Generally, the way they did this was through highly sophisticated fuzzing, running tens of millions of automated tests on the real system with cleverly chosen inputs and quickly validating that the observable semantics of the real system were equivalent to that of the reference model. This is far more effective than regular fuzzing because the reference models allow rapidly checking if **all** the system's observable behaviors are correct.
  This kind of verification work isn't easy to do (and it depends on correct reference models) and isn't suited for every application. But if half the world's infrastructure depends on what you're building, then it's good to have stronger guarantees your code is correct!
  ![](https://pbs.twimg.com/media/GbeunHFbMAAjACx.png) ([View Tweet](https://twitter.com/petereliaskraft/status/1853149845349150745))
