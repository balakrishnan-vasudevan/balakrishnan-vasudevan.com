# Tweets From Dominik Tornow

![rw-book-cover](https://pbs.twimg.com/profile_images/1298463326423277569/N2SAaljB.jpg)

## Metadata
- Author: [[@DominikTornow on Twitter]]
- Full Title: Tweets From Dominik Tornow
- Category: #tweets
- URL: https://twitter.com/DominikTornow

## Highlights
- How did you get into distributed systems?! 
  How did you level up?! ([View Tweet](https://twitter.com/DominikTornow/status/1523346998367248384))
- I talk a lot about application-level failure and platform-level failure.
  That begs the question: What is an application-level failure and what is a platform-level failure?!
  🧵 ([View Tweet](https://twitter.com/DominikTornow/status/1574679105538523138))
- Check out my new blog post Handling Failures from First Principle.
  The post presents a principled failure handling strategy that guarantees correctness & completeness while maximizing the chance of success in the presence of failure.
  Some weekend fun 🤓
  https://t.co/epRqWkNuKL ([View Tweet](https://twitter.com/DominikTornow/status/1583873317487857665))
- Thinking in Distributed Systems can be challenging and sometimes outright confusing.
  Short thread on my favorite thinking tool.
  #ThinkingInDistributedSystems #Goals2023
  🤓👇 ([View Tweet](https://twitter.com/DominikTornow/status/1610744164232355840))
- A side effect of working on Thinking in Distributed Systems that I did not anticipate:
  Writing this book makes me feel unexpectedly vulnerable
  #ThinkingInDistributedSystems #Goals2023
  🧵👇 ([View Tweet](https://twitter.com/DominikTornow/status/1612154897545441280))
- So we all agree that distributed systems can be complex and confusing, but do we agree why distributed systems can be complex and confusing?!
  🧵👇 ([View Tweet](https://twitter.com/DominikTornow/status/1611479068033286145))
- According to your mental model, what does "Consistency" actually mean?!
  E.g. "We have to trade off Consistency and Availability"
  Well, we can have Eventual Consistency & Availability, for some definition of Eventual Consistency
  How do *you* define Consistency (on its own)?! ([View Tweet](https://twitter.com/DominikTornow/status/1690075610054537216))
- Working on the final Chpt of Thinking in Distributed Systems, all about Cloud, Serverless, and (Micro)Services
  Writing hits different with a snowy background ❄️❤️
  #ThinkingInDistributedSystems https://t.co/hyCwRLYQD3
  ![](https://pbs.twimg.com/media/GA68IepaUAAt2D9.jpg) ([View Tweet](https://twitter.com/DominikTornow/status/1733539504772854192))
- A deep dive into 𝗟𝗲𝗮𝗱𝗲𝗿 𝗘𝗹𝗲𝗰𝘁𝗶𝗼𝗻 in Distributed Systems, 𝗣𝗮𝗿𝘁 𝟮
  We assume that allowing two or more processes to make concurrent decisions leads to a conflict
  Leader election is a nuanced topic. We have to make a distinction between
  🎖️ being the leader
  💭 believing to be the leader, and
  🛠️ acting as the leader
  𝗢𝘂𝗿 𝗳𝗼𝗰𝘂𝘀 𝗶𝘀 𝗻𝗼𝘁 𝗼𝗻𝗲 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘁𝗼 𝗯𝗲 𝘁𝗵𝗲 𝗹𝗲𝗮𝗱𝗲𝗿, 𝗯𝘂𝘁 𝗼𝗻𝗲 𝗽𝗿𝗼𝗰𝗲𝘀𝘀 𝘁𝗼 𝗮𝗰𝘁 𝗮𝘀 𝘁𝗵𝗲 𝗹𝗲𝗮𝗱𝗲𝗿
  How can we guarantee that only one process acts as the leader?!
  A widely used strategy involves the use of 𝗳𝗲𝗻𝗰𝗶𝗻𝗴 𝘁𝗼𝗸𝗲𝗻𝘀.
  Remember our example: Our system consists of two processes, a locking service, and a storage service
  Beyond providing a lock, the locking service issues a continuously increasing fencing token. This token is included in every request a process makes to the storage service.
  The storage service 
  👍 approves requests with current fencing token
  👎 rejects requests with outdated tokens
  current = same or higher than previously observed
  𝗥𝗲𝗱𝗲𝗳𝗶𝗻𝗶𝗻𝗴 𝗢𝘂𝗿 𝗨𝗻𝗱𝗲𝗿𝘀𝘁𝗮𝗻𝗱𝗶𝗻𝗴 𝗼𝗳 𝗖𝗼𝗿𝗿𝗲𝗰𝘁𝗻𝗲𝘀𝘀
  We now redefine a system's trace as correct not merely when the latest action is issued by the process holding the lock
  Instead, a system's trace is correct if the last action is tagged with a fencing token that is the same or higher than that of the preceding action.<img src='https://pbs.twimg.com/media/GEpNSWGbkAAHfST.jpg'/> ([View Tweet](https://twitter.com/DominikTornow/status/1750579431775834249))
