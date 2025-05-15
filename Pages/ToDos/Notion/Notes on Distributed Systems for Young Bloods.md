Source: https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/

**Distributed systems are different because they fail often.** When asked what separates distributed systems from other fields of software engineering, the new engineer often cites latency, believing that’s what makes distributed computation hard.

Design for failure

**Writing robust distributed systems costs more than writing robust single-machine systems, because there are failures that only occur with many machines.**

**Robust, open source distributed systems are much less common than robust, single-machine systems.**  The cost of running many machines for long periods of time is a burden on open source communities.

**Coordination is very hard.**  Avoid coordinating machines wherever possible. This is often described as “horizontal scalability”. The real trick of horizontal scalability is independence – being able to get data to machines such that communication and consensus between those machines is kept to a minimum. Every time two machines have to agree on something, the service becomes harder to implement.

Learning about the [Two Generals](http://en.wikipedia.org/wiki/Two_Generals%27_Problem)  and [Byzantine Generals](http://en.wikipedia.org/wiki/Byzantine_Generals%27_Problem) problems is useful here. (Oh, and Paxos really is [very hard to implement](http://research.google.com/pubs/pub33002.html) ; that’s not grumpy old engineers thinking they know better than you.)

**If you can fit your problem in memory, it’s probably trivial.**  To a distributed systems engineer, problems that are local to one machine are easy. Figuring out how to process data quickly is harder when the data is a few switches away instead of a few pointer dereferences away.

**It’s slow” is the hardest problem you’ll ever debug.**  “It’s slow” might mean one or more of the number of systems involved in performing a user request is slow. It might mean one or more of the parts of a pipeline of transformations across many machines is slow. “It’s slow” is hard, in part, because the problem statement doesn’t provide many clues to the location of the flaw. [Dapper](http://research.google.com/pubs/pub36356.html)  and [Zipkin](http://engineering.twitter.com/2012/06/distributed-systems-tracing-with-zipkin.html)  were built for a reason.

**Implement backpressure throughout your system.**  Backpressure is the signaling of failure from a serving system to the requesting system and how the requesting system handles those failures to prevent overloading itself and the serving system. Designing for backpressure means bounding resource use during times of overload and times of system failure. This is one of the basic building blocks of creating a robust distributed system.

Implementations of backpressure usually involve either dropping new messages on the floor, or shipping errors back to users (and incrementing a metric in both cases) when a resource becomes limited or failures occur. Timeouts and exponential back-offs on connections and requests to other systems are also essential.

Without backpressure mechanisms in place, cascading failure or unintentional message loss become likely.

**Find ways to be partially available.** Partial availability is being able to return some results even when parts of your system is failing.

A typical search system sets a time limit on how long it will search its documents, and, if that time limit expires before all of its documents are searched, it will return whatever results it has gathered. This makes search easier to scale in the face of intermittent slowdowns, and errors because those failures are treated the same as not being able to search all of their documents. The system allows for partial results to be returned to the user and its resilience is increased.

**Metrics are the only way to get your job done.**  Exposing metrics (such as latency percentiles, increasing counters on certain actions, rates of change) is the only way to cross the gap from what you believe your system does in production and what it actually is doing

Log files are good to have, but they tend to lie. For example, it’s very common for the logging of a few error classes to take up a large proportion of a space in a log file but, in actuality, occur in a very low proportion of requests. Because logging successes is redundant in most cases (and would blow out the disk in most cases) and because engineers often guess wrong on which kinds of error classes are useful to see, log files get filled up with all sorts of odd bits and bobs. Prefer logging as if someone who has not seen the code will be reading the logs.

**Use percentiles, not averages.** Percentiles (50th, 99th, 99.9th, 99.99th) are more accurate and informative than averages in the vast majority of distributed systems. Using a mean assumes that the metric under evaluation follows a bell curve but, in practice, this describes very few metrics an engineer cares about

**Learn to estimate your capacity.** You’ll learn how many seconds are in a day because of this. Knowing how many machines you need to perform a task is the difference between a long-lasting system, and one that needs to be replaced 3 months into its job. Or, worse, needs to be replaced before you finish productionizing it.

**Feature flags are how infrastructure is rolled out.**  “Feature flags” are a common way product engineers roll out new features in a system. Feature flags are typically associated with frontend A/B testing where they are used to show a new design or feature to only some of the userbase. But they are a powerful way of replacing infrastructure as well.

**Choose id spaces wisely.** The space of ids you choose for your system will shape your system.

The more ids required to get to a piece of data, the more options you have in partitioning the data. The fewer ids required to get a piece of data, the easier it is to consume your system’s output.

Watch out for what kind of information you encode in your ids, explicitly and implicitly. Clients may use the structure of your ids to de-anonymize private data, crawl your system in unexpected ways (auto-incrementing ids are a typical sore point), or perform a [host of other attacks](https://www.owasp.org/index.php/Top_10_2010-A4-Insecure_Direct_Object_References)

**Exploit data-locality.**  The closer the processing and caching of your data is kept to its persistent storage, the more efficient your processing, and the easier it will be to keep your caching consistent and fast. Networks have more failures and more latency than pointer dereferences and `fread(3)` .

**Writing cached data back to persistent storage is bad.**

If the implementers talk about “Russian-doll caching”, you have a large chance of hitting highly visible bugs. This entry could have been left out of the list, but I have a special hate in my heart for it. A common presentation of this flaw is user information (e.g. screennames, emails, and hashed passwords) mysteriously reverting to a previous value.

For homework, apply the CAP theorem’s constraints to a real world implementation of Russian-doll caching.

**Computers can do more than you think they can.**  In the field today, there’s plenty of misinformation about what a machine is capable of from practitioners that do not have a great deal of experience.

**Use the CAP theorem to critique systems.** The CAP theorem isn’t something you can build a system out of. It’s not a theorem you can take as a first principle and derive a working system from. It’s much too general in its purview, and the space of possible solutions too broad.

However, it is well-suited for critiquing a distributed system design, and understanding what trade-offs need to be made. Taking a system design and iterating through the constraints CAP puts on its subsystems will leave you with a better design at the end. One last note: Out of C, A, and P, you [can’t choose CA](http://codahale.com/you-cant-sacrifice-partition-tolerance/). [#](https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/#cap)

**Extract services.**  “Service” here means “a distributed system that incorporates higher-level logic than a storage system and typically has a request-response style API”. Be on the lookout for code changes that would be easier to do if the code existed in a separate service instead of in your system.