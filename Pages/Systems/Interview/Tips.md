Sharing the System Design framework I’ve used that has served me well

I recently got back to interviewing, and thought I’d share the framework I’ve been using for system design interviews that has netted me offers at places like Google, Facebook, Uber, Microsoft, etc. Previously, I’ve also conducted numerous interviews and also been in hiring committees from the inside of these tech companies, so I felt sharing the angle from the interviewer’s point-of-view could be helpful.

Side note, this is not a replacement for studying your stuff. There are numerous resources I’ve used to prep and brush up on my fundamentals (there are a bunch shared in this subreddit alone). This is primarily a tactical framework I use to get that additional bump, which is often helpful when your hire/no-hire decision is on the boundary.

First, I think about these 3 points throughout the whole interview. Unlike the coding section, there is no formal answer on design interviews. It’s often not about the answer you produce, but how you get there.

1. **Speak out your logic**
2. 1. Remember, everything is a tradeoff. Everything. Even expanding that field in your DB that will enable a critical user feature, or adding a test that will prevent that recurring bug comes at a cost. Don’t even think about adding a load balancer or async task queue until you understand why that is the most effective use of your company’s engineering resources at that time. So talk about this. Speak it out. Say that you would start by monitoring where the bottleneck will happen with the increased traffic, and give your reasoning on why you believe service “x” is where you would start increasing instances, and what would be the cost of such. Don’t always have to go into depth, but try to formulate your design decisions around “given (because of) A, I would do B”
3. 2. One added benefit is that it gives you a fast way out should your decision be wrong. You might find that your logic is incorrect midway while you’re speaking out your logic. It might also expose a logic that comes from a misinterpretation of the requirements in which case you give a chance for your interviewer to correct your assumptions. The worst thing is when you have seemingly made up your (incorrect) decision, and the interviewer is not sure why you made that decision and is waiting for it to possibly make sense, but it never does and has to correct you 10 minutes later. By speaking out your logic you fail early and also have given a reasonable reason on what you took that path.
4. **Read the room**
5. 1. So I lied above that “it’s not about the answer you produce, but how you get there”. Although it shouldn’t be, in practice your interviewer has already used this question a few times and knows the parts a good candidate should be covering. If you do your homework well you should be able to get 2/3 of your way to what the interviewer wants, but how on earth are you going to cover designing an Instagram feed in 45 minutes comprehensively? So if the interviewer starts talking about data failover, make sure you immediately pivot over to that topic even though you really want to continue discussing that security issue. If the interviewer is uneasy with what you’re giving, keep trying out different angles to your approach instead of doubling-down on your first answer. Try to get as much coverage on the components the interviewer is “expecting” you to cover.
6. **Get your \[++\] marks**
7. 1. Remember, this is still an interview, not a tech discussion with your peers (unlike what some folks try to frame it as being). At the end of the day, the interviewer (at least a good one) is taking notes on the \[+\] and \[-\] parts of your interview session. If the previous part (“read the room”) was about minimizing the number of \[-\] marks, this section is about maximizing your \[+\] marks. If you’re targeting a senior role, you have to get some \[+\] and \[++\] marks. This is important for senior levels, and even for mid-levels (L4, L5), being able to “impress” the interviewer a couple of times during the interview goes a long way. So how do you impress?
8. 2. One approach is to go one level deeper. Best to use your past knowledge/experience if possible, as that makes your points the most unique. Don’t dwell too long, unless the interviewer follows up as it could prevent you from covering other topics the interviewer wants to discuss. The point is that you want to show that you can talk about parts of a system in a bit more detail than the average interviewee. Talk about a feature in a service you’ve used in the past (e.g. using sets/lists in Redis for structured data cache), how you’d implement a service logic (e.g. rough verbal or written algorithm description), alternative approaches and discuss tradeoffs (e.g. numerate 3-4 ways of caching the request and which option you would choose). Best way to prepare for this is as you’re studying, write down a few “show-off” points. Read through company engineering blogs in your field, look into the feature sets and technical docs of a few popular services that you can mention universally for different types of interviews.
9. 3. If you’re afraid to go too deep, simply touching in a different angle that is not commonly talked about will also add that “unique factor”. For example here are a wide variety of topics that you could be talking about. I’ve roughly ordered them by having the common topics at the top for generic interviews, but would obviously differ depending on your field.
      1. Scalability, availability, latency, throughput
      2. Usability (product-level), extensibility, testability, operational (monitoring, debugging, logging), resource capacity (CPU, memory, network bandwidth), async/offline jobs, analytics
      3. Security, portability (different surfaces), privacy (data retention, encryption)

So with these high-level points in mind, throughout the interview I try to take a simple 3 phase approach unless guided differently by the interviewer.

1. **Assumptions**
2. 1. Clarify: From the interviewer’s perspective, this is the part where I see if the interviewee can narrow down an ambiguous scoped problem by asking relevant questions. From the interviewee’s perspective, all you need to think about is whether I can draw the right “building blocks” in part 2 below (high level design) with the information given. Don’t leave this step without 100% understanding the problem. Try to draw the building blocks in your head and if you’re stuck, ask.
3. 2. Scope: After you’ve clarified and understood the problem, rule out blocks you won’t be drawing. Clarify the scope of the problem. e.g. do I have to think about the user login/authorization for this web app? What about the expiry on this URL short link?
4. 3. Ballpark estimate: I feel this part is a bit overblown in design discussions. Showing off that you can crunch numbers well doesn’t impress interviewers. What does is how you connect those numbers to your design decisions. Here are a few points I try to touch on in this part
      1. Data schema, size → Guides database choice, replication
      2. Traffic: Bandwidth, patterns (cyclical, bursty) → Determines whether you need to touch on scalability and how.
      3. Read:write ratio → Storage (availability for high read), scaling (cache), API decisions
5. **High level design**
6. 1. The part where you draw the rough building blocks. Try to “read the room” and make sure you get good coverage in this section. I make it a point that I will talk about scaling and other details after I have a rough drawing of the high level design.
7. 2. In this section, I try to make sure I have good coverage on these two parts
      4. Component/API: Discuss the various components (service, storage, cache, queue, client, extensions) and also the interface between each component (API, communication protocol).
      5. Data: Details on data schema, flow between services, how it would be stored, cached, modified.
8. **Detailed discussion**
9. 1. This part is extremely specific to the problem at hand and it’s important to also follow the flow you are having with your interviewer in your session. Aim to get a few \[+\], \[++\] points here to show your knowledge and reasoning.
10. 2. Scalability: A frequent extension to the basic discussions. There should be a lot of material discussing this, but it’s important to note the following
      6. Mention the tradeoffs of scaling your system and that you would only add a solution for this when/if needed (e.g. live traffic monitoring suggests we need to scale, we have strong product indication that we will require a large amount of traffic from day 0, Golang is beneficial for our scaling purposes despite the tradeoffs around generics, dependency management and even just experienced dev hiring)
11. 3. In general, here are some common topics to be aware about so that you can discuss should you go over them in this section: Load balancing, reverse proxy, Caching (server-side, client side, database-level, eviction policies), CDN, DNS,  Async (task queues, message queues, backpressure routing), Batch (map-reduce), Database (RDBMS, No-SQL, Federation, Sharding, Denormalization, CAP theorem), Communication (REST, UDP, TCP, RPC)
12. 4. Different angle of discussions, mentioned in “3. Get your \[++\] marks” above, are also good points to touch in this section should you have time.

Hoping this helps for some folks out there prepping for their interviews.

I also have a few mock interviews that I’ve been doing that follows this template. I’m planning to spend some time cleaning them up a bit and adding more details around the \[++\] part for each mock interview. Leave me a note if you’re interested, and I’ll let you know when they’re ready.

Edit: I ended up making [a list of 1-pagers on core system design topics](https://www.reddit.com/r/cscareerquestions/comments/knsoo0/part_2_system_design_core_topic_1_pagers/). Sharing it here for folks that are interested.
Good guide, quite comprehensive.

Would add these to the common topics to know:

consistent hashing, websockets/long polling/etc, Cassandra + KV DBs (why use this instead of relational), Key Generation Service, PostgresDB/SQL table designs, indexing, leader and follower via Zookeeper, config files via Chef... etc, SQS/SNS, Kafka, in-memory caching

Source: Received 5 200-300k TC offers this year with < 6 years of experience, 4 of them were liquid.

--

Edit: read some replies and wanted to add for reference, it's more important to learn the type of technology than the tech itself.

SQS/SNS are message queue + topic implementation in AWS, Cassandra and BigTable are wide-column DBs... so learn for example that message queues can be used for fault tolerance and wide-column DBs remove the need for association tables (don't quote me on this, I'm braindead from the holidays), Zookeeper can be used for majority etc.

Edit 2: I forgot to put monitoring/distributed tracing in the topics list


Part 2: System design core topic 1 pagers

After I shared the [system design interview framework](https://www.reddit.com/r/cscareerquestions/comments/kd13sx/sharing_the_system_design_framework_ive_used_that/) earlier this month, I was surprised to see this [top comment](https://www.reddit.com/r/cscareerquestions/comments/kd13sx/sharing_the_system_design_framework_ive_used_that/gfv4zqv?utm_source=share&utm_medium=web2x&context=3) about the struggle of learning all the topics relevant for system design interviews. I also recall the amount of topics feeling overwhelming at first, and difficult to compress into simple language that would be useful in actual interviews.

So I spent some time over the past few weeks compressing my notes to make a list of core topics that were useful for me into a list of 1 pagers on each topic. The idea was to make it as simple as possible to digest. For beginners and also for folks who’ve already studied their material and want a simple cheat sheet to go over before their interviews.

As mentioned in the previous post, I felt discussing trade-offs and adding that extra depth (++ points) were important, so I tried to cover those aspects into each topic. Basically each topic has a subsection on

* trade-offs
* where and how to use the topic in an actual system design interview
* \[++\] deep dive touch points. Obviously I can’t fit all deep discussions into a 1-pager so I linked resources I felt were useful for each topic.

I put up the pdf summarizing the core topics [here](http://gum.co/sysdesign). Personally, it would be a great consolation prize for the hours I spent over the holidays if folks could tip in a dollar, but if for any reason that doesn’t work for you, leave me a note and I’ll shave off that dollar so that you can access the material.

There is basically a 1 pager across each of these topics

* CAP Theorem
* Domain Name Service (DNS)
* Consistent Hashing
* Scaling
   * Load Balancing
   * Reverse Proxy
   * CDN
   * Caching
* Database
   * RDBMS
   * NoSQL
* Event-based architecture
   * Messaging
   * Streaming & Batch processing
* Communication Protocols

and sharing here one of those 1-pagers on the topic of messaging using queues.

==========

**Messaging**

*What is it?*

Messaging is a form of [event-driven architecture](https://www.redhat.com/en/topics/integration/what-is-event-driven-architecture) where messages are passed across services asynchronously using queues. This provides a flexible interface for services to communicate without forcing explicit contracts across services. The asynchronous nature also allows for services to respond back without waiting for subsequent services to finish (e.g. email delivery). Separating the business logic that requires offline processing also modularizes the system so that it’s easier to scale each component independently. There are two forms of messaging:

* Point-to-point: There is one explicit connection between services where a middle layer queue acts as an intermediary buffer while events get processed.
* Publish-subscribe: There are multiple consumers of the message, and each subscriber “subscribes” to a topic. Once an event of that topic is produced the subscribers are notified and messages are pushed.

*Trade-offs, caveats and alternatives*

* Queues can be overloaded with events if not processed in time (consumer machines are overloaded or down). [Backpressure](https://www.tedinski.com/2019/03/05/backpressure.html) techniques are applied to prevent the queue from being overloaded and the overall throughput remains consistent.
* Messaging requires additional services that act as brokers with additional logic to acknowledge the acceptance of a message. It also adds delay for the final job (on the consumer) to finish. Simple tasks can be better off using synchronous communication protocols (REST, RPC, etc.)
* There are other methods that facilitate asynchronous communication across services without involving an explicit message broker such as [webhooks](https://zapier.com/blog/what-are-webhooks/), [websockets](https://www.html5rocks.com/en/tutorials/websockets/basics/) (if an explicit open communication channel is possible), [SSE](https://en.wikipedia.org/wiki/Server-sent_events).

*Use it for…*

* Whenever there is a process that requires time that you don’t want to incur to your client (e.g. respond back immediately), leveraging a queue to handle the request asynchronously can be beneficial.
* Depending on the application, it can be helpful to discuss how you would return a response back to the user after the consumer has worked on the task. (e.g. a confirmation email for a bug report). Essentially the response back to the user can be split into tiers (immediate response followed by final response).

*++*

* Protocols such as [AMQP](https://www.amqp.org/about/what), [STOMP](https://stomp.github.io/), [MQTT](https://mqtt.org/) exist to define contracts between services and are available on popular messaging services such as [RabbitMQ](https://www.rabbitmq.com/protocols.html), while other services such as [Kafka](https://kafka.apache.org/protocol.html#protocol_details), [AmazonSQS](https://aws.amazon.com/sqs/) are not restricted by such protocols.
* Depending on your need, a simple Redis [List](https://redis.io/topics/data-types) might suffice as a highly available message broker without incurring complexity. If you need more complex features (e.g. message receipt, flexible routing) a proper message broker would be needed.
* Further reading: [1](https://nordicapis.com/5-protocols-for-event-driven-api-architectures/), [2](https://www.tutorialspoint.com/apache_storm/apache_storm_distributed_messaging_system.htm), [3](https://www.upsolver.com/blog/kafka-versus-rabbitmq-architecture-performance-use-case)

\--------

Again, hope this helps for everyone preparing their interviews! Happy to incorporate feedback as well to make the resource more useful, so if folks have any please let me know.

https://www.reddit.com/r/cscareerquestions/s/fa0aba6KkT

Hey, thanks so much for the kind words. I put the link to the resources I used at the end of my pdf file, but I'll put them down here too.

•	⁠https://tianpan.co/notes/2016-02-13-crack-the-system-design-interview/
•	⁠https://github.com/donnemartin/system-design-primer
•	⁠https://github.com/checkcheckzz/system-design-interview

These links were great for me prepping my interview and getting an overall sense of doing system design.

from my exp working with senior/staff engineers, the key to system design prep isnt just absorbing content - its about building a mental framework u can apply anywhere!

here's what worked for lot of folks i know:

active learning vs passive watching

•	⁠take notes while watching/reading
•	⁠try to predict next steps b4 theyre shown
•	⁠pause n think "what would i do here?"

practice breaking down problems

•	⁠pick random products u use daily
•	⁠sketch out high lvl design in 5 mins
•	⁠identify bottlenecks n tradeoffs
•	⁠compare ur solution w/ videos later

focus on patterns not specific solutions

•	⁠scalability patterns
•	⁠data consistency approaches
•	⁠common failure modes
•	⁠caching strategies etc

find someone whos recently interviewed at ur target companies n do mock interviews! getting real feedback on ur approach is way more valuable than memorizing solutions. lots of great coaches out there who can point out blind spots u might miss. wat company ur interviewing? check prepfully - has some reallllly good coaches

also dont forget - sys design isnt just about technical stuff. at staff level they rly care about:

•	⁠how u communicate tradeoffs
•	⁠how u handle ambiguity
•	⁠whether u consider business impact
•	⁠how u break down complex probs

good luck w/ the prep!


As an interviewer for those, let me give you one advice: tradeoffs, tradeoffs, tradeoffs.

Everything about L6+ interview rubrics is about you thinking about, understanding and explaining tradeoffs. When you're explaining, explain WHY you're making a decision like you are, what is the tradeoff you're making and what is the downside of the thing you're making.

The biggest issue all "high level" candidates do on my interviews is failing to explain that - "I'll just take Spark, Kafka and S3 and then upload/stream, blah blah" is an answer for senior/mid level devs. Those are the ones that execute.

For L6+ we need to hear WHY do you think those technologies you chose on the spot are better than any other approach and in which cases will they fail. Because as L6+ you're the one deciding which approach to use and we need to be sure you're not just defaulting to first thing you accidentally learned 3 years ago from a blog post.

In many ways, you need experience to answer those questions well - but checking for experience is the point of the interview. Too many candidates just jump into solutions without explaining tradeoffs, which makes them look less experienced than they are.

To paraphrase the late co-creator of erlang “If you design for 100 billion users then scale down, your system will gracefully scale upwards as demand increases. If you design for 100 users, then 10000, then 1 million, you will have to rewrite the thing multiple times.”

I'm going to strongly disagree with the primary thrust of this as it applies to interviews and as it applies to building stuff in the real world.

If the interview question is "design for massive amounts of load, 1 billion rps", then it makes sense to do this. But for a general "design a hotel booking system" or "design a batch processing system", this is a terrible approach. When I'm asking a design question, I'm not looking for flights of fancy beyond the question, I'm looking to see if the person can come up and communicate an effective and simple approach. Then we'll add on complexities; they might be scale, but they also might be transactional complexity, or contention, or bursts of requests, or transactional dependencies. For example designing a system for 1million requests per minute continuous is very different from designing a system for 1 million requests per minute for 10 minutes. Very very different.

If someone I'm interviewing starts off with this philosophy of "Design for 100 billion users [which, btw is more than 11x the number of human beings on earth, never mind those with internet access] first" I'm going to push back firmly. And if they persist in insisting that their approach is right, I'm writing them off then and there.

And for the real world, I haven't worked on systems which approach 1billion rps, but I have worked on systems which got close to 1billion / minute. And we didn't get there by starting with "how do we scale for 1 billion rps". We got there through iteration. Build the best, simplest solution for the scale we had at the time. Then we saw what started to break when its limits were met. And we iterated. Your approach of "you should never have to rewrite anything multiple times as you scale up" is completely the opposite of my experience. You should expect to rewrite things as you grow, and your growth could be in any number of dimensions: straightforward scale, requirement complexity, dependency complexity, etc.

Being able to understand the current challenges, and envision and communicate an effective and simple solution for the current challenges and any next ones you can reasonably describe are what's needed. If I ask you for a monitoring solution for a 10 node cluster and you start designing monitoring for Meta's datacenters, you gonna fail my interview.

I actually really like Hello Interview: https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction

Follow/read/watch all the examples and use ChatGPT as a sounding board to bounce ideas off of.

Deep dives almost always have to do with how to scale, how to eliminate a bottleneck, and you can almost always use the same set of technologies for those solutions. Pick a few solutions (database, cache, queue) and use ChatGPT to learn those technologies really well. The website I linked also goes through some core technologies really well - I highly recommend going through those.

For mock interviews, just use Excalidraw, set a timer, and see how close you get to an actual solution. Your solution doesn't need to match exactly. Remember to talk out loud while doing this.


Was asked this system design question during an interview. Was my approach acceptable?

So I recently had a technical interview where the interviewer asked me how I’d design a scalable credit-based system. It was a pretty interesting challenge, so I thought I’d break down my approach here so that you guys can let me know if I did anything wrong or if this approach would fail in any way.

  
Here are the requirements given during the interview

* **Track user credits** (adding/subtracting credits based on transactions)
* **Handle high concurrency** (multiple users accessing/updating their balances simultaneously)
* **Be traceable and auditable** (every transaction should be recorded for accuracy)
* **Scale well** for high read and write demands
* **Allow users to purchase more credits**

  
**My Approach**

So first of all, I have 3 schemas for Users, Credits, and Transactions table. You can view the snippets here [https://pastebin.com/AuBBx517](https://pastebin.com/AuBBx517)

  
To make sure updates were atomic (especially with concurrent users), I proposed using PostgreSQL transactions with `FOR UPDATE` row-level locking. This ensures that only one update on a user’s balance can happen at a time. I've also proposed to use Redis for caching data to ensure that we can support high reads. As for cache invalidation, I ensure that the value in the cache is updated every time there's a new transaction being sent to the database. 

To support auditing and monitoring, I proposed to use either Prometheus or Grafana to track any metrics such as number of failed transactions, high frequency transactions, and for traceability. 

However, this seems too simple and was wondering if I should change my approach for this question? The interview did mentioned scalability, so should I have just introduced Kubernetes for database scalability and using kafka streams to approach this problem?


My take?

Designs should be as simple as needed for the use case, and no more.

I see system design interviews as a conversation. Your starting point is valid. Often interviewers will drill down in particulars to test your knowledge, or give you hints or explicitly say you're off track if you go completely wrong.

I think it's also best to avoid prescribing specific tools. I like choices eg Prometheus or grafana, but as an interviewer I might ask you to describe the difference and which would you recommend for the app and why.

Scalability is always (?) important. The interviewer might say ok, the system is now breaking here, how would you improve the design. You might then say something like database sharding or replication, or streaming event based queues, or improved caching optimization, etc. 

System design is about tradeoffs. There is no perfect answer, there are many reasonable ones. The value of system design interviews is to understand how you approach problems, and the level of technical breadth and depth.

I really enjoyed the content on this site (not affiliated) https://interviewing.io/guides/system-design-interview which has a lot more detail.

Good luck!

System design : intuitions of numbers for operations (read, write, etc)

EDIT 2: Added TL;DR summary of comments at the bottom for future readers.

\------

Hello there, 7yo software engineer, been in the same company since the begining of my career and we have a lot of proprietary technology.

As I am preparing system design interview, I realised that I had a hard time knowing rough number of what is possible with a given tech used outside.eg : usual sql database, how much can they read  before exploding ? 1000req/sec? 10000req/sec ? more ? How much can they write ? same with no-sql db, queues, services, vms and various other tech.

I am not looking for a concrete answer with much optimization but more like this is baseline to expect of this type of technology.

**Do you have a ressource for where I can find this kind of information ?**

The ideal would be some kind of table with various tech and different operation on it and their usual performance.

eg (non exhaustif list of operations ):

|Database|read|write|
|:-|:-|:-|
|mysql|xxxx/s|xxxx/s   (but slow down reads)|
|postgres|xxxx/s|xxxx/s|
|cassandra|xxxx/s|xxxx/s|

&#x200B;

|Queues|ingestion rate|consumers max num|
|:-|:-|:-|
|Kafka|xxxx/s|xxx|

EDIT : Note I realised that I maybe haven't convey exactly what I wanted hence I  [Added more info as a reply](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1y3xw7/?utm_source=share&utm_medium=web2x&context=3)

EDIT2 :Thank you all for the discussion this was really useful !**Summary of comments**\- Most comments converge that we shouldn't care about the numbers.(see  [Added more info as a reply](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1y3xw7/?utm_source=share&utm_medium=web2x&context=3) for the links)Few other useful post to read [post1](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1ygsuz/?utm_source=share&utm_medium=web2x&context=3) , [post2](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1ygsuz/?utm_source=share&utm_medium=web2x&context=3)Some comments like : " The real data is going to come from your observability. "Few comments I read here and there as engineer we should \*\*"measure, observe, iterate" (or measure, find bottleneck, react)\*\*if you want numbers, load test as it's too specific to the size of your data, technology etc.

I still strongly believe that I should have an intuition of what is realistic vs fantasy. Maybe having a baseline with one node helps knowing what is realistic. Below you can find some comment that gives an actual answer to my question  :

\- if you want technology specific, these [post1](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1yapj0/?utm_source=share&utm_medium=web2x&context=3) and [post2](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1z5x26/?utm_source=share&utm_medium=web2x&context=3) help me figure out that what I was looking for were **benchmarks,** although personally I was looking for something higher level.

\-  There is the "every number that software engineer should know" Well I stumble upon them in my career and I know them roughly although I never used them to make any calculation of what is realistic. [Thanks to this post](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i1xnlb0/?utm_source=share&utm_medium=web2x&context=3)  and this post made me discover that. Eg :

Rule of thumb: 250usec to read 1MB of data from memory**Simple math: 1s / 250usec = 4GB/sec maximum <= I can use this a baselinez**

\- [This post](https://www.reddit.com/r/ExperiencedDevs/comments/tm5jvp/comment/i21jstg/?utm_source=share&utm_medium=web2x&context=3) about Simon Eskildsen’s talks and napkin-math repo is the closest I got to my answer. (only skimmed it but it seems like the content is what i was looking for)  
\- also this [https://computers-are-fast.github.io/](https://computers-are-fast.github.io/) 

Tradeoffs between batch processing and streaming?

Standard system design q: you’re building a service that gets you the top N songs or top N most popular news stories in some specified time interval. I understand you can have it done in a streaming way, aggregating event counts in real time using some min count sketch structure, or through batch processing if the time interval was longer (say 1 hour).

My question is, is one of these easier/better to build out? I’d think the streaming real time service would be more of use to clients, but what are the tradeoffs to building that out vs a batch system? 

Let me know if there’s a better place to ask this.

Streaming is a high-maintenance, complex bitch that offers real-time data and scalability, but it's costly and a pain to manage; batch processing is your reliable, easy-to-handle workhorse, less resource-intensive but slower and less sexy - choose based on whether you want a race car or a minivan.



** Netflix **
Netflix System Design

I have gotten sooooo many questions on what u had on my system design. Here is my two cents: 

Very driven by the interviewer. There were times where he didn't agree with me, but I took em through the process of how I understand the problems, why I am doing such things, and tradeoffs which in the end led them to agree with me. First 15 mins was resume review for me.

As mentioned above know these
1. Database (SQL vs NOSQL | Horizontal vs Vertical Scaling | Sharding vs Replicating)
2. API Design
3. Load Balancers + CDNs

To Add:
1. Make sure you know how does your application work whens sharding but the user travels to a new country 

For these start with single user in one country -> multiple users in multiple counties. Think about how user travels would change things. Think about where exactly will the binaries be stores of the files. How am I making sure things are fast? Can I shard? What database is the best to use and why? What are the schemes of this? Do I need a CDN? Why and how does it help me?  

Please don’t DM won’t be responding this is the only info I will be giving out. Good luck!


Staff+ interviewers, what are the reasons you reject someone in a system design interview?

Currently a senior EM looking out for a job change.

I'm gonna have a system design round with a company that boasts that they expect their EMs+ to be technically as good as a Staff+ Engineers (only from system design ability POV). I know this might seem weird but please kindly ignore this. I'm not worried.

Now that brings me to the title. 

If you're someone who does system design interviews for Staff+ positions, what are the reasons you reject them? 

Assume the scenario where the candidate thinks it went well. Yet you looked for some important things and you reject them. Why? 
They’re still general, but lack of trade off analysis, not understanding or digging for the actual problem, the big thing for me is pushing for a silver bullet. There is always a trade off and if you can’t tell me the cons and the pros, you are not being objective.
When they are unable to discuss the pro/cons of different techniques.  Honestly, most systems can be designed in different ways and still work.  What I want to know is WHY they are choosing what they chose, and what alternatives did the consider and why those were eliminated.

How they got there is much more important than what they ended up with.  Did they ask the right questions to design a system that would fulfill immediate, short-term, and long-term needs?  Did they give themselves an out in case something turns out to be less efficient than they anticipated?

Last thing I want is someone coming in thinking that there is one and only one "right way".  Every design weighs the pros and cons, and sometimes they aren't technical concerns, but culture, experience, and team familiarity.  Or perhaps being able to leverage old systems or designs at least partially as a gradual shift from an aging system to a new one.  Take into consideration the long time maintenance costs, availability of required technical personnel, infrastructure costs, and flexibility of the end system (scale up, scale out, scale down, cloud, on premise, or mix).  And for the love of god, right size it.  Don't design me a platform that can run google when all we needed one a to-do list application that 3 people will use.
Communication is going to be huge at that level for me. Asking the right questions, talking about the types of systems they've designed in the past, being able to justify and explain design choices, being able to identify the tradeoffs and weaknesses of their design, etc.

Honestly, I feel like this is a hard question to give meaningful answers for. At Staff+ level you are being judged on the knowledge and skills gained over 10+ years. At that point it's less about what you know and more about who you are. Your career has really had time to shape and mold you to the point where it, to an extent, defines how you think and react. It's certainly not something anyone can cram for or fake.

So the best advice I have would be to just practice basic interview communication skills and go through your work history and refresh on all you've done, the successes, the failures, and what you learned from each. As you solve problems use the opportunity to share a bit about where you learned the lessons you're implementing.

At Staff+ level you're no longer trying to demonstrate your potential to become a good dev. You're trying to demonstrate you're already a great dev with a track record of success that is going to have immediate impact when hired.

