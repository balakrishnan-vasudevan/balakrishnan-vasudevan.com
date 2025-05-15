# System Design Interview – An Insider's Guide

![rw-book-cover](https://m.media-amazon.com/images/I/713EB+DpiQL._SY160.jpg)

## Metadata
- Author: [[Alex Xu]]
- Full Title: System Design Interview – An Insider's Guide
- Category: #books

## Highlights
- web app, database, cache, etc. ([Location 79](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=79))
- web application and mobile application. ([Location 90](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=90))
- •Web application: it uses a combination of server-side languages (Java, Python, etc.) to handle business logic, storage, etc., and client-side languages (HTML and JavaScript) for presentation. •Mobile application: HTTP protocol is the communication protocol between the mobile app and the web server. JavaScript Object Notation (JSON) is commonly used API response format to transfer data due to its simplicity. An example of the API response in JSON format is shown below: ([Location 91](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=91))
- Separating web/mobile traffic (web tier) and database (data tier) servers allows them to be scaled independently. ([Location 100](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=100))
- key-value stores, graph stores, column ([Location 109](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=109))
- stores, and document stores. ([Location 109](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=109))
- Non-relational databases might be the right choice if: •Your application requires super-low latency. •Your data are unstructured, or you do not have any relational data. •You only need to serialize and deserialize data (JSON, XML, YAML, etc.). •You need to store a massive amount of data. ([Location 113](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=113))
    - Note: What sort of databases would you need for operations tasks like,say configuration mgmt, monitoring, log data from servers etc.
- Vertical scaling, referred to as “scale up”, means the process of adding more power (CPU, RAM, etc.) to your servers. Horizontal scaling, referred to as “scale-out”, allows you to scale by adding more servers into your pool of resources. ([Location 120](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=120))
- After receiving a request, a web server first checks if the cache has the available response. If it has, it sends data back to the client. If not, it queries the database, stores the response in cache, and sends it back to the client. This caching strategy is called a read-through cache. ([Location 199](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=199))
- Consider using cache when data is read frequently but modified infrequently. ([Location 208](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=208))
- Since cached data is stored in volatile memory, a cache server is not ideal for persisting data. ([Location 208](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=208))
- A good practice is to store session data in the persistent storage such as relational database or NoSQL. Each web server in the cluster can access state data from databases. This is called stateless web tier. ([Location 276](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=276))
- sticky sessions ([Location 287](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=287))
- The shared data store could be a relational database, Memcached/Redis, NoSQL, etc. The NoSQL data store is chosen as it is easy to scale. ([Location 297](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=297))
- geo-routed, ([Location 304](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=304))
    - Note: How is this carried out? Does it use - anycasting?
- geoDNS is a DNS service that allows domain names to be resolved to IP addresses based on the location of a user. ([Location 305](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=305))
- To further scale our system, we need to decouple different components of the system so they can be scaled independently. Messaging queue is a key strategy employed by many real-world distributed systems to solve this problem. ([Location 320](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=320))
- A message queue is a durable component, stored in memory, that supports asynchronous communication. It serves as a buffer and distributes asynchronous requests. ([Location 323](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=323))
- When choosing a sharding key, one of the most important criteria is to choose a key that can evenly distributed data. ([Location 387](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=387))
- •Keep web tier stateless •Build redundancy at every tier •Cache data as much as you can •Support multiple data centers •Host static assets in CDN •Scale your data tier by sharding •Split tiers into individual services •Monitor your system and use automation tools ([Location 408](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=408))
- Step 1 - Understand the problem and establish design scope ([Location 583](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=583))
    - Tags: [[blue]] 
- •What specific features are we going to build? •How many users does the product have? •How fast does the company anticipate to scale up? What are the anticipated scales in 3 months, 6 months, and a year? •What is the company’s technology stack? What existing services you might leverage to simplify the design? ([Location 604](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=604))
    - Tags: [[blue]] 
- Step 2 - Propose high-level design and get buy-in ([Location 630](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=630))
    - Tags: [[blue]] 
- Step 3 - Design deep dive ([Location 657](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=657))
    - Tags: [[blue]] 
- Sometimes, for a senior candidate interview, the discussion could be on the system performance characteristics, likely focusing on the bottlenecks and resource estimations. ([Location 666](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=666))
- For URL shortener, it is interesting to dive into the hash function design that converts a long URL to a short one. For a chat system, how to reduce latency and how to support online/offline status are two interesting topics. ([Location 668](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=668))
    - Tags: [[blue]] 
- Step 4 - Wrap up ([Location 682](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=682))
    - Tags: [[blue]] 
- •The interviewer might want you to identify the system bottlenecks and discuss potential improvements. Never say your design is perfect and nothing can be improved. There is always something to improve upon. This is a great opportunity to show your critical thinking and leave a good final impression. •It could be useful to give the interviewer a recap of your design. This is particularly important if you suggested a few solutions. Refreshing your interviewer’s memory can be helpful after a long session. •Error cases (server failure, network loss, etc.) are interesting to talk about. ([Location 684](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=684))
- •Operation issues are worth mentioning. How do you monitor metrics and error logs? How to roll out the system? •How to handle the next scale curve is also an interesting topic. For example, if your current design supports 1 million users, what changes do you need to make to support 10 million users? •Propose other refinements you need if you had more time. ([Location 691](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=691))
- Dos •Always ask for clarification. Do not assume your assumption is correct. •Understand the requirements of the problem. •There is neither the right answer nor the best answer. A solution designed to solve the problems of a young startup is different from that of an established company with millions of users. Make sure you understand the requirements. •Let the interviewer know what you are thinking. Communicate with your interview. •Suggest multiple approaches if possible. •Once you agree with your interviewer on the blueprint, go into details on each component. Design the most critical components first. ([Location 698](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=698))
    - Tags: [[blue]] 
- •Bounce ideas off the interviewer. A good interviewer works with you as a teammate. •Never give up. ([Location 709](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=709))
    - Tags: [[blue]] 
- Don’ts •Don't be unprepared for typical interview questions. •Don’t jump into a solution without clarifying the requirements and assumptions. •Don’t go into too much detail on a single component in the beginning. Give the high-level design first then drills down. •If you get stuck, don't hesitate to ask for hints. •Again, communicate. Don't think in silence. •Don’t think your interview is done once you give the design. You are not done until your interviewer says you are done. Ask for feedback early and often. ([Location 711](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=711))
    - Tags: [[pink]] 
- Step 1 Understand the problem and establish design scope: 3 - 10 minutes Step 2 Propose high-level design and get buy-in: 10 - 15 minutes Step 3 Design deep dive: 10 - 25 minutes Step 4 Wrap: 3 - 5 minutes ([Location 726](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=726))
    - Tags: [[blue]] 
- API gateway is a fully managed service that supports rate limiting, SSL termination, authentication, IP whitelisting, servicing static content, etc. ([Location 802](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=802))
- we need a counter to keep track of how many requests are sent from the same user, IP address, etc. If the counter is larger than the limit, the request is disallowed. ([Location 964](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=964))
- Using the database is not a good idea due to slowness of disk access. ([Location 965](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=965))
- •INCR: It increases the stored counter by 1. •EXPIRE: It sets a timeout for the counter. If the timeout expires, the counter is automatically deleted. ([Location 968](https://readwise.io/to_kindle?action=open&asin=B08B3FWYBX&location=968))
    - Tags: [[orange]] 
