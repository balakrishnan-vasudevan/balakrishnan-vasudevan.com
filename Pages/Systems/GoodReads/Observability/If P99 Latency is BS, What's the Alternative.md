# If P99 Latency is BS, What's the Alternative?

Tags: latency, observability
Category: Articles
Company: general
Status: Not started
URL: https://www.p99conf.io/2023/09/14/if-p99-latency-is-bs-whats-the-alternative/

![gil-charity-alex-p99conf-speakers.jpg](gil-charity-alex-p99conf-speakers.jpg)

*P99 CONF 2023 is now a wrap! You can (re)watch all videos and access the decks now.*

[ACCESS ALL THE VIDEOS AND DECKS NOW](https://www.p99conf.io/on-demand/)

Speakers calling BS on the very essence of a conference’s name is typically *not* socially acceptable. But P99 CONF isn’t your usual conference. The community – and the hosts – loved it when three daring speakers openly challenged the value of P99 latencies at P99 CONF 2023.

The P99 shakedown started with Gil Tene (known for his [“oh sh*t” talk](https://www.youtube.com/watch?v=lJ8ydIuPFeU) on how NOT to measure latency) kicking off the conference with his take on “Misery Metrics & Consequences.” Alex Hidalgo picked up the baton with “Throw Away Your Nines.” Then, Charity Majors took it across the finish line with the conference’s most colorful (literally and figuratively) expression of “P99 is BS.”

So what’s the problem with P99s? And if they truly are BS, what should we look at instead?

*P99 CONF 2023 is a [free virtual conference](https://www.p99conf.io/) on low latency engineering strategies. Join the community in October for a no-holds-barred exploration of topics like Rust, observability, edge, performance tuning, AI/ML, Kubernetes, Linux kernel and more – with an all-star lineup of experts, including engineers from almost any impressive tech company you can imagine.*
- ## Gil Tene: How I Learned to Stop Worrying and Love Misery
  
  Gil Tene, CTO at [Azul](https://www.azul.com/), launched his takedown of P99 “percentlies” (his spelling, not a typo) with a seemingly pretty chart – filled with pretty little lies:
  
  This dashboard shows 25th, 50th, 90th and 95th percentiles over a period of two hours, and it seems to give us a pretty good idea of what’s going on. What stands out is the fact that the 95th percentile spikes up for some reason around 12:40, the 90th percentile spikes up a little bit under it, and the other percentiles seem to stay the same. You might read this to mean that there are some outliers you might want to explore, but the rest seems generally OK.
  
  But looking at this is a pure waste of time, according to Tene. “What is *not* shown on this chart is the 5% of things that are worse than the 95th percentile. This chart shows the good stuff; it only shows happy results. For this chart to show even this spike, it has to be so bad that more than 5% of the things that we see have reached this level. This is the chart you show if you want to hide from reality or to hide reality from other people. It’s a great chart to show if you are not doing your job well, but you want your bonus anyway.”
- ### From Bad to Worse
  
  So bring on the P99s and it’s all better? Well, it does provide more insight into how bad it really is. With P99s, something like this…
  
  turns into this…
  
  But, even as bad as it seems now, you’re still totally overlooking the 1% of things that are worse than everything shown here. As Tene emphasizes, “The act of showing percentiles – only to some depth, to a few numbers, usually nines – is the act of hiding from reality… If you care about service levels, if you care about the behavior of your systems as seen by end users, by customers, by businesses – you need to look even deeper than that.”
  
  When you measure the P99, what are the chances that your end user (a person or a client) would experience something worse than the 99th percentile? Pretty good, actually. P99 does NOT mean that 99% of things will be better than that. Tene takes the example of a super simple user session that involves just five page loads averaging 40 resources per page. How many users will NOT experience something worse than the 99th percentile of HTTP requests? Only about 13%. In other words, 87% of your end users experience something *worse* than your P99.
- ### So. Many. Nines.
  
  So, do you obsess over even more nines? Well, that’s problematic too: “There’s not enough data points in the period of time we’re measuring to classify them with enough nines. And we don’t tend to aggregate things across the data sets in order to actually extract a higher number of nines from larger data.” Tene came up with an [HdrHistogram](http://hdrhistogram.org/) to account for this, enabling people to record data and to accumulate intervals of data together to get an accurate number of nines. But he’s given up on that tool achieving broad adoption (“The chances of people actually using well-structured histograms for a larger number of nines is not very high”).
  
  And although it’s hard to measure all these nines, it’s even harder to do it well. That requires accounting for [coordinated omission](https://www.scylladb.com/2021/04/22/on-coordinated-omission/#:~:text=Coordinated%20omission%20is%20a%20term,way%20that%20avoids%20measuring%20outliers.), a much larger topic than we can adequately cover here. Quick summary: A slow operation gets measured only once and the ripple effect of all the other delays it causes don’t get measured at all. This skews results immensely.
- ### Misery Loves … Better User Experiences?
  
  At this trough of despair, Tene pauses to reflect: “So if things are so broken, and we just can’t seem to get anything right here, what do we do? Do we just give up?” Fortunately, no. Some things people are doing actually do help us provide better experiences. Case in point: misery metrics.
  
  Think about what failure looks like in your system and measure the corresponding “misery metrics.” You can reliably measure indicators like timeouts, retries, failed queries and even business-focused metrics like abandoned shopping carts. If those numbers are trending in a bad direction, who cares what your P99 is? There’s clearly a problem … go diagnose and fix it!
  
  Tene wraps up with his take on how to monitor these misery metrics. “Plot the bad thing, watch it, and see how it reacts to the world, see how it reacts to load. Your success rate is measured by the number of things that aren’t broken. In general, you will know when things aren’t good enough. If you don’t deliver a result within 50 milliseconds, users will move on. If you don’t let them check out of their shopping cart in 5 seconds, they’ll abandon. Usually, being better than needed is *not* a benefit. But being even a little bit worse than needed is enough to lose business.”
  
  This recap is really just scratching the surface. Be sure to catch all the details, straight from the mouth of the “how NOT to measure latency” master himself.
  
  [**WATCH GIL TENE’S KEYNOTE**](https://www.p99conf.io/session/misery-metrics-consequences/)
- ## Throw Away Some Nines
  
  For even more critical perspectives on measuring P99s, take a look at [Charity Major’s spirited P99 CONF keynote](https://www.p99conf.io/session/from-slo-to-goty/) as well as [Alex Hidalgo’s carefully crafted exploration](https://www.p99conf.io/session/throw-away-your-nines/) on all the nines. Also see this [great writeup by Jessica Wachtel](https://thenewstack.io/when-99-service-level-objectives-are-overrated-and-too-expensive/).
- ### Majors: You’re Careering Down the Freeway Without Your Glasses On
  
  Early on, Charity Majors, CTO at [Honeycomb](https://www.honeycomb.io/), flat out states that P99 is BS because every user interaction counts. Even if you’re hitting all your nines, “there can still be a whole bunch of pathologies. Everybody who logged in today might have had their state saved on an unresponsive shard, payments might be failing – there’s an infinitely long, thin tail of things that almost never happen that someday *will* happen – and whenever they do, they will inevitably bite you.”
  
  Rather than obsess over nines, Majors wants us to look inward and focus on gaining better and faster visibility into what’s really going on inside the system. “Observability lets you inspect cause and effect at a very granular level. It connects effort to output, it connects cause to effect and helps you to iterate and improve on what works using a magnifying glass. Without observability, you are really driving blind, you’re careening down the freeway without your glasses on.”
  
  She continues, “Only a very, very small fraction of system problems and bugs ever actually need to be closely understood. But, that tiny percentage has an outsized effect on the success of your business and the happiness of your users. And the tricky part is that you can never predict in advance what they’re going to be.”
  
  And here’s a summary of Majors’ colorful solution:
  
  She explains, “Really, it’s about empowering software engineers to own their own code, and the way that you do this is by instrumenting it as you go. Never accept a pull request unless you can explain how you can tell if it breaks and what the instrumentation is… If you can do this, shipping software reliably with fast feedback loops, you can probably catch upwards of 80% of all problems before your users do.”
  
  Note that in many respects, Majors is actually quite aligned with Gil’s emphasis on so-called misery metrics: “Instead of alerting on hundreds or thousands of symptom-based monitoring checks, alert only on a few precious SLOs that directly reflect user pain.”
  
  [**WATCH CHARITY’S KEYNOTE**](https://www.p99conf.io/session/from-slo-to-goty/)
- ### Hidalgo: Kill Rethink your darlings
  
  Spoiler alert: Alex Hidalgo, principal reliability advocate at [Nobl9](https://www.nobl9.com/), isn’t a total nine hater. A key takeaway from his P99 CONF session was to look *beyond* the nines if you want to improve experiences for real-world users working with real-world applications run by teams with real-world budgets.
  
  P99 latencies focus on standard long-tail distributions, but, as Hidalgo has experienced, that’s not always typical. As a former Google site reliability engineer, he’s seen quite a variety of distributions: bimodal, left-skewed, multimodel, to name a few. If you just look at P99s because that’s what you always do, then you could be missing a lot. “Nines aren’t terrible to use, but they’re not always the right choice,” he explained. “You need to be meaningful.”
  
  But what does it mean to be meaningful in this context? As Hidalgo wraps up: “Actually, using the number nine is just fine. There’s nothing wrong with aiming for 99.9% reliability. There’s absolutely nothing wrong with using the 99th percentile for your latency measurements. Because part of being meaningful about your choices, and meaningful about your decisions, is that you *should* be looking to the past. You just don’t want to copy the past. Sometimes what was done before was actually a very good idea. There’s a reason why some of these things are so common – because very often they *are* the right choices. You just need to make sure that they’re the right choices for you.”
  
  [**WATCH ALEX’S TALK**](https://www.p99conf.io/session/throw-away-your-nines/)
- ## Continue the Latency Conversation at P99 CONF 23
  
  So maybe we don’t need to throw away *all* of our nines – and we’re keeping the conference name as is, despite the snarky banter in the chat. 😉
  
  If you want to continue the conversation on measuring and optimizing latency, [join your peers at P99CONF](https://www.p99conf.io/?latest_sfdc_campaign=7016O000000rial&campaign_status&utm_campaign=mp%20newstack%202023-10-18%20p99%20conf&utm_medium=marketing%20partner&utm_source=marketing%20partner&lead_source_type=the%20new%20stack), where friendly debate is not only welcomed but encouraged. Topics up for discussion this year span across domains like:
- **Rust** – Optimizations, case studies, future use cases, Rust vs C++, Zig, Go
- **Kubernetes** – Database scaling, application optimization, edge, benchmarking
- **Databases and event streaming** – SQL, NoSQL, caching, data streaming
- **AI/M**L – feature stores, real-time model predictions
- **Edge** – Databases, unikernels, API gateways
- **Observability** – eBPF, tracing, OpenTelemetry
  
  ![sqlflame_8gkg9z11x29g4.png](sqlflame_8gkg9z11x29g4.png)
  
  *P99 CONF 2023 is now a wrap! You can (re)watch all videos and access the decks now.*
  
  [ACCESS ALL THE VIDEOS AND DECKS NOW](https://www.p99conf.io/on-demand/)
  
  > Editor’s note: The following is a post from Tanel Poder, “a long-time computer performance geek.” He spoke at P99 CONF 23 on “Always-on Profiling of All Linux Threads, On-CPU and Off-CPU, with eBPF & Context Enrichment.” Watch his talk to discover a new open source eBPF tool for efficiently sampling both on-CPU events and off-CPU events for every thread (task) in the OS. This article was originally published on Tanel’s blog.
  > 
  
  [Watch Tanel’s Talk](https://www.p99conf.io/session/always-on-profiling-of-all-linux-threads-on-cpu-and-off-cpu-with-ebpf-context-enrichment/)
- ## Introduction
  
  Brendan Gregg invented and popularized a way to profile & visualize program response time by sampling stack traces and using his [FlameGraph](http://www.brendangregg.com/flamegraphs.html) concept & tools. This technique is a great way for visualizing metrics in *nested hierarchies*, what stack-based program execution uses under the hood for invoking and tracking function calls. If you don’t know what FlameGraphs are, I suggest you read Brendan’s explanation first.
  
  In this blog post I won’t be doing traditional stack profiling, but will apply FlameGraphs in a new way for visualizing Oracle Database SQL execution plan metrics. This visualization is not limited to Oracle only, it can be used on any RDBMS engine, as long as the engine reports actual time taken at execution plan operator (plan line) level.
  
  Even though FlameCharts could be used for visualizing any cumulative metric (like amount of I/O generated in different stages of the plan), in this post I will measure what matters the most — the *response time* used by individual execution plan operators. I’m using Oracle’s DBMS_XPLAN with the *statistics_level=all* setting for the examples in this post.
- ## Current State of SQL Plan Visualization (Oracle & Postgres examples)
  
  It’s worth mentioning that the Oracle Database already has great instrumentation and pretty good visualization of its execution plans. Here’s an example plan of Query 72 of the TPC-DS benchmark (11-table join) visualized as a tree using the Oracle’s Real-Time SQL Monitoring tool:
  
  The tree gives a high level overview of the execution plan hierarchy, but doesn’t have a good way for visualizing which plan nodes or branches took the most time to run. The tabular view below has lots of additional performance metrics (and that’s where I spend most of my time when doing [Oracle SQL tuning](https://tanelpoder.com/seminar/advanced-oracle-sql-tuning-training/)). For example, the last, `Activity%` column tells you exactly on which plan line most of the time was spent. However, this layout has a shortcoming, your plan may be way too large to fit on one screen. Lots of scrolling back’n’forth is needed with large plans, trying to remember whatever was shown in some other section of the plan.
  
  Here are couple of current Postgres plan visualizer examples that provide useful details and emphasize where in the plan to focus:
  
  *^ Tabular layout and heatmap visualization of Postgres plans by [explain.depesz.com](http://explain.depesz.com/).*
  
  *^ Tree layout with Postgres plan node self-time usage by [tatiyants.com/postgres-query-plan-visualization](http://tatiyants.com/postgres-query-plan-visualization/)*.
  
  Both the tabular and tree layouts have their strengths and weaknesses, but in my experience both of them become troubleshooting bottlenecks with *very large plans* when trying to understand the plan structure *and* its resource usage at a glance. By very large plans I mean SQL execution plans that have hundreds, or thousands, of operators in them as you’d typically see in enterprise ERP databases and complex data warehouse systems.
  
  Also, you don’t get always lucky and find a single plan operator or a branch that uses 95% of your response time, sometimes the performance problem starts from a much higher level driving operation that causes many plan lines deep in distant locations to use a small amount of the resources each, totaling up to a bigger problem.
  
  So I’ve been thinking of additional ways for visualizing very large plans that would give a good high level plan overview at a glance, ability to understand parent-child-grandchild relationships through many plan layers *and* at the same time show the resource consumption of all plan operators too.
- ## Introducing FlameGraphs for SQL Performance Visualization
  
  Conceptually, at high level, you can compare Oracle or Postgres SQL plan execution to how a regular program makes function calls. A driver function `main()` calls `do_something()`, that function delegates work further, calling `get_item()` etc … once the `get_item()` function gets what it wants, it *returns control* back to the right location in its calling function `do_something()` (with the help of stack), who may then call some other function, return or just loop back and call the `get_item()` function again. This is how programs work.
  
  The Oracle RDBMS engine does the same at high level, when executing plans. A `SELECT STATEMENT` (data fetch) operator may call a `NESTED LOOPS` join operator under the hood, who then calls `INDEX RANGE SCAN` operator, who then calls some low level C functions to extract data from some buffers in the cache. The `INDEX RANGE SCAN` then returns control back to the parent `NESTED LOOPS` operator with the help of stack, who then may decide to access the other table involved in the join or loop back and invoke the same `INDEX RANGE SCAN` again (to fetch another batch of data).
  
  So, a regular application with C functions or Java methods invoking subroutines at low level is very similar how the Oracle RDBMS execution plan operators invoke “child rowsources”. Therefore you can use the existing FlameGraph toolset to visualize SQL execution plan performance without modifications.
  
  Oracle can report how much time was spent in each execution plan operator depending on the method, either the absolute “self-time” value or a cumulative value that includes all child operators in the execution plan tree. With some recursive calculation logic (easy to do in SQL) we can generate data that the FlameGraph.pl tool can use. I will explain the flow later, but here’s a FlameGraph of the same 11-table join execution plan previously visualized with Oracle’s tools above:
  
  ![sqlflame_1v329s9f8jhz3.svg](sqlflame_1v329s9f8jhz3.svg)
  
  > You can open the above image — and the flamegraphs below too — in a new tab to get into the interactive SVG mode and click/move your mouse over the plan lines, zoom in and see the cumulative response time values (in milliseconds) in the bottom of the chart.
  > 
  
  ## What’s the value of FlameGraphs for SQL?
  
  Your RDBMS engine may already have some visualization tools of execution plan *structure*. Fewer RDBMS engines have visualization of not only the structure of the plan tree, but the actual response time used by previous execution(s). As I showed above, Oracle can provide quite a lot of metrics for every SQL plan operator, but the tabular plan output with performance metrics doesn’t always work well with very large plans. The “parent operator” of an execution plan line may be multiple pages of scrolling away or the resource consumption is spread across many “distant” locations in the execution plan tree.
  
  SQL FlameGraphs complement such low-level views with excellent high level overview, allowing to see parent-child relationships visually close together and the cumulative response time (or whatever other metric plotted) as the width of the “flame bar” in the same place.
  
  And thanks to how Brendan has built the SVG generator, we can even click on individual areas (SQL plan tree branches) and zoom in to the interesting parts. Typically the widest parts are most interesting here though as the more we “shrink” the width of an operator via some optimization, the faster it will run!
  
  Here’s an annotated example that shows most of the response time being spent on plan node `10 - HASH JOIN`:
  
  As the line `10` (and lines `11`, `19` “deeper under” it) take most of the width of this chart, it’s evident that most of the response time is spent somewhere in “#10 and deeper”. For example, I don’t need to focus on lines `1 - SORT ORDER BY` and `2 - HASH GROUP BY` as they don’t add any additional width to the flamegraph, so there’s no noticeable *additional* execution time spent in them on top of whatever their child operators are consuming.
  
  In fact, we can visually identify how much time is spent specifically within `10 - HASH JOIN` (self-time) vs. cumulative response time coming from its child operators. I know that most of the plan execution time was spent *within* that hash join (and not in reading data blocks from a table or index) as it’s the widest line of this chart that does not have any layers on top of it. So this operator `10` was effectively active, doing its hashing, joining and perhaps spilling-to-disk I/O without waiting for work delegated to its child operators to complete.
  
  As a starting point, one option for making my SQL complete faster would be to look for making this hash join itself faster (likely by either allocating more memory for this join or finding ways to send less data to this operator to process). This would require us to understand more detailed metrics, like number of rows processed and amount of hashtable spill I/Os done, than this high level FlameGraph visualization shows. It is possible to append some key metrics as plain text into the plan operator names themselves as I have done with table/index names in the next example.
  
  There’s more to be said about interpreting the structure of this plan, especially as this time-consuming hash join seems to be a grandchild of some `NESTED LOOPS` joins “higher up” in the plan tree and one would want to investigate how many times these parents invoked (looped through) this hash join operator. The Oracle SQL Monitoring screenshot earlier shows (in the “Exec…” column) that it’s just one invocation of this hash join and not an excessive nested looping problem. In a future version it would be possible to use FlameGraph [color coding](http://www.brendangregg.com/blog/2017-07-30/coloring-flamegraphs-code-type.html) to indicate the frequency of operator invocations/function calls.
- ## More Examples
  
  While the previous FlameGraph example showed most of the time spent in a “data processing” phase of the plan, the next ones below show “data retrieval” being the main bottleneck:
  
  *^ All 3 widest bars in the top (12,16, 20) are INDEX RANGE SCANs – accessing data from database blocks. All of them are grandchildren of the 10 – FILTER operator that is apparently doing some IN or EXISTS lookups in a loop (using the NESTED LOOPS SEMI-join operator).*
  
  *^ In the above example the majority of time has been spent in plan operation “14 – FILTER and under”. Apparently the 15 – PX RECEIVE branch is driving this filter and IN/EXISTS probes are done into the plan operation 38 – NESTED LOOPS SEMI that in turn spends most time “waiting” for its child operator 39 – INDEX RANGE SCAN retrieving records from the STORE_SALES_IDX2 index.*
  
  I’ll paste some more examples here so you can have fun reading them:
  
  *^ There’s no single obvious troublemaker operation in the query above, but the FlameGraph gives a nice overview of in which execution plan branches most of the time is spent — looks like half of all time is spent in SORT UNIQUE operations (15,31,47) **and** their children doing hash joins and full table scanning. Why do we have SORT UNIQUEs – looks like due to this query using the INTERSECT keyword somewhere in it (13, 14)*.
  
  *^ This last query seems to be quite a straightforward one with lots of repeated subqueries all using around the same amount of time*.
- ## Summary
  
  This article hopefully serves two purposes. First, it introduces a new way for applying FlameGraphs for visualizing RDBMS SQL execution plan response time and resource usage at the plan operator level, while still maintaining the ability to see the big picture at a glance even with very large plans.
  
  And second, it illustrates the fact that a typical RDBMS SQL plan execution is just a bunch of function calls executed in the hierarchy and order that’s defined in the plan itself. It’s very much similar to how regular applications loop through subroutines in their modules, thus the FlameGraph stack trace visualization mechanism can be applied without any modifications needed.
  
  I wrote a proof-of-concept script for extracting Oracle SQL plan timing and formatting the output in the `flamegraph.pl` friendly format and you can download it here ([sqlflame.sql](https://github.com/tanelpoder/tpt-oracle/blob/master/sqlflame.sql)). It’s a prototype, you probably need to read it to understand what it needs to work. And as mentioned above, Brendan’s FlameGraph introduction is [here](http://www.brendangregg.com/flamegraphs.html).
  
  *Update: As people have asked to see the raw input file processed by flamegraph.pl, I’ve uploaded it [here](https://github.com/tanelpoder/tpt-oracle/blob/master/tools/optimizer/sqlflame_stacks.txt).*
  
  [Comments](https://twitter.com/TanelPoder/status/1056674082765320194) are currently in Twitter / X.
- ## Watch Tanel’s talk from P99 CONF
  
  *Here’s a look at [what Tanel presented at P99 CONF 23](https://www.p99conf.io/session/always-on-profiling-of-all-linux-threads-on-cpu-and-off-cpu-with-ebpf-context-enrichment/)…*
  
  I will be introducing a new open source eBPF tool for efficiently sampling both on-CPU events and off-CPU events for every thread (task) in the OS. Linux standard performance tools (like perf) allow you to easily profile on-CPU threads doing work, but if we want to include the off-CPU timing and reasons for the full picture, things get complicated. Combining eBPF task state arrays with periodic sampling for profiling allows us to get both a system-level overview of where threads spend their time, even when blocked and sleeping, and allow us to drill down into individual thread level, to understand why.
  
  ![1200x628-p99conf-tanel-poder-poder.jpg](1200x628-p99conf-tanel-poder-poder.jpg)
  
  ![companies-2023-p99-1.png](companies-2023-p99-1.png)
  
  *P99 CONF 2023 is now a wrap! You can (re)watch all videos and access the decks now.*
  
  [ACCESS ALL THE VIDEOS AND DECKS NOW](https://www.p99conf.io/on-demand/)
  
  With over 60 tech talks on industry trends, performance optimization trainings, and insider insights on new tracing tools and measurement techniques, P99 CONF truly has something for every performance-minded engineer. As a category, “engineering case study” sessions are historically among the most watched (and discussed) sessions. At P99 CONF 2023, we’re thrilled to host an extensive spectrum of engineers sharing how they and their teams tackled their toughest performance challenges.
  
  Here’s a taste of the talks from P99 CONF 23
- ### How Netflix Builds High Performance Applications at Global Scale
  
  Prasanna Vijayanathan covers how Netflix built high performance applications that work for every user, every time – including a technical look at the data and modeling techniques they use.
- ### Measuring the Impact of Network Latency at Twitter
  
  Widya Salim, Zhen Li, and Victor Ma outline the causal impact analysis, framework, and key learnings used to quantify the impact of reducing Twitter’s network latency.
- ### Architecting a High-Performance (Open Source) Distributed Message Queuing System in C++
  
  Vitaly Dzhitenov presents a new open source distributed message queuing system, developed and used by Bloomberg, that provides highly-performant queues to applications for asynchronous, efficient, and reliable communication.
- ### 3 Gb/s L7 Egress Traffic Inspection at TikTok Using Squid & Go on K8s
  
  Daniel Haimanot shares how TikTok achieved real-time privacy compliance inspecting 3 Gb/s L7 egress traffic in-band using Squid and Golang on K8s.
- ### Cache Me If You Can: How Grafana Labs Scaled Up Their Memcached 42x & Cut Costs Too
  
  Danny Kopping walks us through how Grafana Labs managed to increase their cache size by 42x and reduce costs by using a little-known feature of memcached called “extstore”.
- ### Optimizing for Tail Latency and Saturation at Uber Scale: Macro and Micro Considerations
  
  Ranjib Dey talks about Uber’s micro (JVM, Go GC tuning, concurrency tuning) and macro (architectural: consistency, caching, sharding…) lessons learned optimizing cloud-native microservices for tail latency and efficiency.
- ### Taming P99 Latencies at Lyft: Tuning Low-Latency Online Feature Stores
  
  Bhanu Renukuntla shares challenges and strategies of tuning low latency online feature stores to tame P99 latencies, shedding light on the importance of choosing the right data model.
- ### Interaction Latency: Square’s User-Centric Mobile Performance Metric
  
  Pierre-Yves Ricau shares why and how to track “Interaction Latency,” a user-centric mobile performance metric that Square uses instead of app launch time and smoothness.
- ### Square’s Lessons Learned from Implementing a Key-Value Store with Raft
  
  Omar Elgabry offers up the micro-lessons engineers can learn from Square’s experience building fault-tolerant, strongly consistent distributed systems using Raft.
- ### How We Reduced the Startup Time for Turo’s Android App by 77%
  
  Pavlo Stavytskyi details how Turo engineers reduced Android app startup time by 77%, including how to apply best practices and Android developer tools to improve the startup performance of your own Android apps.
- ### From 1M to 1B Features Per Second: Scaling ShareChat’s ML Feature Store
  
  Ivan Burmistrov and Andrei Manakov present a case study in building a low-latency ML feature store (using ScyllaDB, Golang, and Flink) that handles 1B features per second, including data modeling tips for performance & scalability and caching strategies.
- ### Conquering Load Balancing: Experiences from ScyllaDB Drivers
  
  Piotr Grabowski delves into the intricacies of load balancing within ScyllaDB drivers, sharing how we employed the Power of Two Choices algorithm, optimized the implementation of load balancing in Rust Driver, and more.
- ### Building Low Latency ML Systems for Real-Time Model Predictions at Xandr
  
  Chinmay Abhay Nerurkar Moussa Taifi outline the challenges of building an ML system with the low latency required to support the high volume and high throughput demands of ad serving at Xandr, the advertising and analytics subsidiary of Microsoft.
- ### Peak Performance at the Edge: Running Razorpay’s High-Scale API Gateway
  
  Jay Pathak details how RazorPay solved availability and authorization challenges using their API gateway, plus insights on how their rate limiter plugin handles more than 200K RPS workloads seamlessly with latency under sub milliseconds.
- ### P99 Publish Performance in a Multi-Cloud NATS.io System
  
  Derek Collison walks through the strategies and improvements made to the NATS server to accomplish P99 goals for persistent publishing to NATS JetStream that was replicated across all three major cloud providers over private networks.
- ### Adventures in Thread-per-Core Async with Redpanda and Seastar
  
  Travis Downs looks at the practical experience of building high performance systems with C++20 in an asynchronous runtime, the unexpected simplicity that can come from strictly mapping data to cores, and the challenges & tradeoffs in adopting a thread-per-core architecture.
- ### Ingesting in Rust at Sentry
  
  Armin Ronacher shares Sentry’s experience building a Rust based ingestion service that handles hundreds of thousands of events per second with low latency globally.
- ### A Deterministic Walk Down TigerBeetle’s main() Street
  
  Aleksei Kladov dives into how TigerBeetle used Zig to implement a fully deterministic distributed system that will never fail with an out of memory error, for predictable performance and 700x faster tests!
- ### Cost-Effective Burst Scaling For Distributed Query Execution
  
  Dan Harris presents a case study in building a distributed execution model that can dynamically execute across both AWS Lambda and EC2 resources – shedding excess load to lambda functions to preserve low latency while scaling EC2 capacity to manage costs.
- ### High-Level Rust for Backend Programming
  
  Adam Chalmers shares why Rust is a great language for writing API servers and backends, based on his experiences at Cloudflare and KittyCAD.
- ### Mitigating the Impact of State Management in Cloud Stream Processing Systems
  
  Yingjun Wu outlines how RisingWave Labs is addressing the high latency issues associated with S3 storage in stream processing systems that employ a decoupled compute and storage architecture.
- ### Making Python 100x Faster with Less Than 100 Lines of Rust
  
  Ohad Ravid shares how the Trigo team was able to bridge the Python-Rust performance gap using just a bit of Rust and some profiling – ultimately improving performance 100x.
- ### 5 Hours to 7.7 Seconds: How Database Tricks Sped up Rust Linting Over 2000X
  
  Predrag Gruevski offers a case study in using database ideas to build a linter that looks for breaking changes in Rust library APIs.
  
  ![books-by-speakers-p99.jpg](books-by-speakers-p99.jpg)
  
  *P99 CONF 2023 is now a wrap! You can (re)watch all videos and access the decks now.*
  
  [ACCESS ALL THE VIDEOS AND DECKS NOW](https://www.p99conf.io/on-demand/)
  
  If you’ve seen the P99 CONF agenda, you know that the stars have aligned nicely this year. In just two half days, from anywhere you like, you can learn from 60+ outstanding speakers – all sharing performance insights from a broad range of perspectives. Front-end/back-end. Rust/Zig/C++/Java/WebAssembly. SQL/NoSQL…
  
  As we were posting their bios, we noticed – not surprisingly – that our speakers have amassed a rather impressive list of publications, including quite a few books. This blog highlights 15 of those P99 speaker books, which we highly encourage you to read.
  
  Also – if you **registered for P99 CONF**, you should have **30-day full access to the complete O’Reilly library** (thanks to O’Reilly, the conference’s media sponsor). In addition to the iconic O’Reilly animal books, this also includes access to books by Apress, Manning, No Starch Press, and more.
- ## How to Make Things Faster
  
  ![makethingsfaster.jpg](makethingsfaster.jpg)
  
  **By Cary Millsap**
  
  June 2023[Bookshop.org](https://bookshop.org/p/books/how-to-make-things-faster-lessons-in-performance-from-technology-and-everyday-life-cary-millsap/19662208?ean=9781098147068) | [Amazon](https://www.amazon.com/How-Make-Things-Faster-Performance/dp/1098147065/ref=sr_1_1?qid=1693525672&refinements=p_27%3ACary+Millsap&s=books&sr=1-1) | [O’Reilly](https://www.oreilly.com/library/view/how-to-make/9781098147051/?_gl=1*ewr21j*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDA3MzcuNTMuMC4w)
  
  Slow systems are frustrating. They waste time and money. But making consistently great decisions about performance can be easy, if you understand what’s going on. This book explains in a clear and thoughtful voice why systems perform the way they do. It’s for anybody who’s curious about how computer programs and other processes use their time and about what you can do to improve them.
  
  Through a mix of personal vignettes and technical use cases, Cary Millsap reviews the process of improving performance and provides best practices for optimizing systems efficiently. You’ll learn how to identify the information needed to improve a system, how to find the root causes of performance issues, and how to fix them. You’ll also learn how performance optimization is both a skill set and a mindset, and how to develop both over time.
  
  If you’re a computer professional whose success relies on software that goes fast, by the end of this book you’ll be able to identify, view, scope, analyze, and remedy performance issues with consistency and confidence.
  
  *Cary is presenting “The History of Tracing Oracle” at P99 CONF.*
- ## Database Performance at Scale
  
  **By Felipe Cardeneti Mendes, Piotr Sarna (P99 CONF speaker), Pavel Emelyanov, and Cynthia Dunlop**October 2023[Bookshop.org](https://bookshop.org/p/books/database-performance-at-scale-a-practical-guide-cynthia-dunlop/20260587?ean=9781484297100) | [Amazon](https://www.amazon.com/Database-Performance-Scale-Practical-Guide/dp/1484297105) | [ScyllaDB](https://lp.scylladb.com/database-performance-book-offer) (free book)
  
  Discover critical considerations and best practices for improving database performance based on what has worked, and failed, across thousands of teams and use cases in the field. This book provides practical guidance for understanding the database-related opportunities, trade-offs, and traps you might encounter while trying to optimize data-intensive applications for high throughput and low latency.
  
  Whether you’re building a new system from the ground up or trying to optimize an existing use case for increased demand, this book covers the essentials. The ultimate goal of the book is to help you discover new ways to optimize database performance for your team’s specific use cases, requirements, and expectations.
- Understand often overlooked factors that impact database performance at scale
- Recognize data-related performance and scalability challenges associated with your project
- Select a database architecture that’s suited to your workloads, use cases, and requirements
- Avoid common mistakes that could impede your long-term agility and growth
- Jumpstart teamwide adoption of best practices for optimizing database performance at scale
  
  *Piotr is presenting “Less Wasm” at P99 CONF.*
- ## Learning eBPF
  
  ![learningebpf.jpg](learningebpf.jpg)
  
  **By Liz Rice**March 2023[Bookshop.org](https://bookshop.org/p/books/learning-ebpf-programming-the-linux-kernel-for-enhanced-observability-networking-and-security-liz-rice/19244244?ean=9781098135126) | [Amazon](https://www.amazon.com/Learning-eBPF-Programming-Observability-Networking/dp/1098135121) | [O’Reilly](https://www.oreilly.com/library/view/learning-ebpf/9781098135119/?_gl=1*1vys6lt*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDU1MjY4MC43NS4wLjE2OTQ1NTI2ODQuNTYuMC4w) | [Isovalent](https://isovalent.com/books/learning-ebpf/)
  
  What is eBPF? With this revolutionary technology, you can write custom code that dynamically changes the way the kernel behaves. It’s an extraordinary platform for building a whole new generation of security, observability, and networking tools.
  
  This practical book is ideal for developers, system administrators, operators, and students who are curious about eBPF and want to know how it works. Author Liz Rice, chief open source officer with cloud native networking and security specialists Isovalent, also provides a foundation for those who want to explore writing eBPF programs themselves.
- Learn why eBPF has become so important in the past couple of years
- Write basic eBPF code, and manipulate eBPF programs and attach them to events
- Explore how eBPF components interact with Linux to dynamically change the operating system’s behavior
- Learn how tools based on eBPF can instrument applications without changes to the apps or their configuration
- Discover how this technology enables new tools for observability, security, and networking
  
  *Liz Rice is presenting “eBPF vs Sidecars” at P99 CONF.*
- ## Efficient Go: Data-Driven Performance Optimization
  
  ![efficientgo.jpg](efficientgo.jpg)
  
  **By Bartlomiej Plotka**January 2023[Bookshop.org](https://bookshop.org/products/efficient-go-data-driven-performance-optimization-bartlomiej-plotka/18529885?ean=9781098105716) | [Amazon](https://www.amazon.com/Efficient-Go-Data-Driven-Performance-Optimization/dp/1098105710/) | [O’Reilly](https://www.oreilly.com/library/view/efficient-go/9781098105709/)
  
  Software engineers today typically put performance optimizations low on the list of development priorities. But despite significant technological advancements and lower-priced hardware, software efficiency still matters. With this book, Go programmers will learn how to approach performance topics for applications written in this open source language.
  
  How and when should you apply performance efficiency optimization without wasting your time? Author Bartlomiej Plotka provides the tools and knowledge you need to make your system faster using fewer resources. Once you learn how to address performance in your Go applications, you’ll be able to bring small but effective habits to your programming and development cycle.
- Continuously monitor for performance and efficiency regressions
- Find the root cause of performance bottlenecks using metrics, logging, tracing, and profiling
- Use tools like pprof, go test, benchstat and k6.io to create reliable micro- and macro-benchmarks
- Improve and optimize your code to meet your goals without sacrificing simplicity and readability
- Make data-driven decisions by prioritizing changes that make a difference
- Introduce basic “performance hygiene” in day-to-day Go programming and testing
  
  *Bartlomiej Plotka is presenting “The Art of Macro Benchmarking: Evaluating Cloud Native Services Efficiency” at P99 CONF.*
- ## 100 Go Mistakes and How to Avoid Them
  
  ![gomistakes.jpg](gomistakes.jpg)
  
  **By Teiva Harsanyi**
  
  September 2022
  
  [Bookshop.org](https://bookshop.org/p/books/100-go-mistakes-and-how-to-avoid-them-teiva-harsanyi/17746369?ean=9781617299599) | [Amazon](https://www.amazon.com/100-Mistakes-How-Avoid-Them-ebook/dp/B0BBHQD8BQ/ref=sr_1_1?crid=912LPEIQJMNC&keywords=100+Go+Mistakes+and+How+to+Avoid+Them&qid=1694146066&s=books&sprefix=100+go+mistakes+and+how+to+avoid+them%2Cstripbooks%2C166&sr=1-1) | [O’Reilly](https://www.oreilly.com/library/view/100-go-mistakes/9781617299599/?_gl=1*1pp2gmy*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0NTQ4MC43MS4xLjE2OTQxNDYwODcuNTkuMC4w)
  
  *100 Go Mistakes and How to Avoid Them* shows you how to replace common programming problems in Go with idiomatic, expressive code. In it, you’ll explore dozens of interesting examples and case studies as you learn to spot mistakes that might appear in your own applications. Expert author Teiva Harsanyi organizes the error avoidance techniques into convenient categories, ranging from types and strings to concurrency and testing.
- Identify and squash code-level bugs
- Avoid problems with application structure and design
- Perfect your data and control structures
- Optimize your code by eliminating inefficiencies
  
  *Teiva is presenting “Running a Go App in Kubernetes: CPU Impacts” at P99 CONF.*
- ## WebAssembly: The Definitive Guide
  
  ![wasmbook.jpg](wasmbook.jpg)
  
  **By Brian Sletten**
  
  December 2021
  
  [Bookshop.org](https://bookshop.org/p/books/webassembly-the-definitive-guide-safe-fast-and-portable-code-brian-sletten/17135515?ean=9781492089841) | [Amazon](https://www.amazon.com/WebAssembly-Definitive-Guide-Brian-Sletten-ebook/dp/B09N5VGRKS/ref=sr_1_1?crid=2EBSQ0ZR3TLN7&keywords=brian+sletten&qid=1693525834&s=books&sprefix=briam+sletten%2Cstripbooks%2C168&sr=1-1) | [O’Reilly](https://www.oreilly.com/library/view/webassembly-the-definitive/9781492089834/?_gl=1*13t6360*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDE3NzguNTguMC4w)
  
  *WebAssembly: The Definitive Guide* is a thorough and accessible introduction to one of the most transformative technologies hitting our industry. What started as a way to use languages other than JavaScript in the browser has evolved into a comprehensive path toward portability, performance, increased security, and greater code reuse across an impressive collection of deployment targets.
  
  Author Brian Sletten introduces elements of this technology incrementally while building to several concrete, code-driven examples of practical, cutting-edge WebAssembly uses. Whether you work with enterprise software or embedded systems, or in entertainment, scientific computing, or startup environments, you’ll learn how WebAssembly can have a positive impact on the way you develop software.
- Use WebAssembly to increase code portability across platforms
- Reuse more of your software assets in a wider number of deployment targets
- Learn how WebAssembly increases protection against prominent security attacks
- Use WebAssembly to deploy legacy code in web environments
- Increase your user base across languages and development environments
- Integrate JavaScript code with other languages and environments to improve performance, security, and productivity
- Learn how WebAssembly will affect your career as a software developer
  
  *Brian is presenting “HTTP 3: Moving on From TCP” at P99 CONF.*
- ## Apache Pulsar in Action
  
  ![pulsarinaction.jpg](pulsarinaction.jpg)
  
  **By David Kjerrumgaard**
  
  December 2021
  
  [Bookshop.org](https://bookshop.org/p/books/apache-pulsar-in-action-david-kjerrumgaard/15059400?ean=9781617296888) | [Amazon](https://www.amazon.com/Apache-Pulsar-Action-David-Kjerrumgaard-ebook/dp/B09L8M2JGZ/ref=sr_1_1?crid=1MMOS78F7OX4V&keywords=David+Kjerrumgaard&qid=1693525897&sprefix=david+kjerrumgaard%2Caps%2C258&sr=8-1) | [O’Reilly](https://www.oreilly.com/library/view/apache-pulsar-in/9781617296888/?_gl=1*sllf31*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDI5OTguNTkuMC4w)
  
  *Apache Pulsar in Action* is a comprehensive and practical guide to building high-traffic applications with Pulsar. You’ll learn to use this mature and battle-tested platform to deliver extreme levels of speed and durability to your messaging. Apache Pulsar committer David Kjerrumgaard teaches you to apply Pulsar’s seamless scalability through hands-on case studies, including IOT analytics applications and a microservices app based on Pulsar functions.
- Publish from Pulsar into third-party data repositories and platforms
- Design and develop Apache Pulsar functions
- Create an event-driven food delivery application
  
  *David is presenting “Segment-Based Storage vs. Partition-Based Storage: Which is Better for Real-Time Data Streaming?” at P99 CONF.*
- ## Kafka: The Definitive Guide, 2nd Edition
  
  ![kafkaguide.jpg](kafkaguide.jpg)
  
  **By Gwen Shapira (P99 CONF speaker), Todd Palino, Rajini Sivaram, Krit Petty**
  
  November 2021
  
  [Bookshop.org](https://bookshop.org/p/books/kafka-the-definitive-guide-real-time-data-and-stream-processing-at-scale-gwen-shapira/17135467?ean=9781492043089) | [Amazon](https://www.amazon.com/Kafka-Definitive-Guide-Gwen-Shapira-ebook/dp/B09L6KLWDG) | [O’Reilly](https://www.oreilly.com/library/view/kafka-the-definitive/9781492043072/?_gl=1*1feomdk*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDE1NTcuMzAuMC4w)
  
  Engineers from Confluent and LinkedIn responsible for developing Kafka explain how to deploy production Kafka clusters, write reliable event-driven microservices, and build scalable stream processing applications with this platform. Through detailed examples, you’ll learn Kafka’s design principles, reliability guarantees, key APIs, and architecture details, including the replication protocol, the controller, and the storage layer.
- Best practices for deploying and configuring Kafka
- Kafka producers and consumers for writing and reading messages
- Patterns and use-case requirements to ensure reliable data delivery
- Best practices for building data pipelines and applications with Kafka
- How to perform monitoring, tuning, and maintenance tasks with Kafka in production
- The most critical metrics among Kafka’s operational measurements
- Kafka’s delivery capabilities for stream processing systems
  
  *Gwen is presenting “High Performance on a Low Budget” at P99 CONF.*
- ## The Hitchhiking Guide To Load Testing Projects: A Fun, Step-by-Step Walk-Through Guide
  
  ![hitchhikers.jpg](hitchhikers.jpg)
  
  **By Leandro Melendez**
  
  September 2021
  
  [Amazon](https://www.amazon.com/Hitchhiking-Guide-Testing-Projects-Step/dp/0988540207/ref=sr_1_1?crid=2FY09YXDJPFYP&keywords=leandro+melendez&qid=1663204568&sprefix=leandro+melende%2Caps%2C185&sr=8-1) | [AbeBooks](https://www.abebooks.com/9780988540200/Hitchhiking-Guide-Load-Testing-Projects-0988540207/plp)
  
  Here comes the book that will help everyone who always wanted to learn, understand, and deliver load test projects.
  
  You will be guided through every phase and sub phase of a traditional load testing project. Holding your hand at every step of the journey, explaining what you should do, the required items, how to gather them, and how to use them.
  
  It’s all explained through fun examples that will help you understand all the complicated technical terms. They will be useful analogies to explain the work to management (or learn it if you are a manager). Each paired up with a translation into the technical boring terms, so you can learn and use the official lingo.
  
  *Leandro Melendez is presenting “Chihuahua-Sized Load Tests!” at P99 CONF.*
- ## PostgreSQL Query Optimization: The Ultimate Guide to Building Efficient Queries
  
  ![postgres.jpg](postgres.jpg)
  
  **By Henrietta Dombrovskaya (P99 CONF speaker), Boris Novikov, Anna Bailliekova**
  
  April 2021[Bookshop.org](https://bookshop.org/p/books/postgresql-query-optimization-the-ultimate-guide-to-building-efficient-queries-boris-novikov/15908440?ean=9781484268841) | [Amazon](https://www.amazon.com/PostgreSQL-Query-Optimization-Ultimate-Efficient/dp/1484268849/ref=sr_1_1?qid=1693525755&refinements=p_27%3AHenrietta+Dombrovskaya&s=books&sr=1-1&text=Henrietta+Dombrovskaya) | [O’Reilly](https://www.oreilly.com/library/view/postgresql-query-optimization/9781484268858/?_gl=1*790ppa*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDEzODMuNTguMC4w)
  
  This book helps you write queries that perform fast and deliver results on time. You will learn that query optimization is not a dark art practiced by a small, secretive cabal of sorcerers. Any motivated professional can learn to write efficient queries from the get-go and capably optimize existing queries. You will learn to look at the process of writing a query from the database engine’s point of view, and know how to think like the database optimizer.
- Identify optimization goals in OLTP and OLAP systems
- Read and understand PostgreSQL execution plans
- Distinguish between short queries and long queries
- Choose the right optimization technique for each query type
- Identify indexes that will improve query performance
- Optimize full table scans
- Avoid the pitfalls of object-relational mapping systems
- Optimize the entire application rather than just database queries
  
  *Henrietta is presenting “ORM is Bad, But is There an Alternative?” at P99 CONF.*
- ## Container Security: Fundamental Technology Concepts that Protect Containerized Applications
  
  ![containersecurity.jpg](containersecurity.jpg)
  
  **By Liz Rice**
  
  April 2020[**Bookshop.org](https://bookshop.org/books/container-security-fundamental-technology-concepts-that-protect-containerized-applications/9781492056706) | [Amazon](https://www.amazon.com/Container-Security-Fundamental-Containerized-Applications/dp/1492056707/ref=sr_1_1?crid=3RY6SXYLJQ2KS&keywords=liz+rice&qid=1663205912&s=books&sprefix=liz+rice%2Cstripbooks%2C144&sr=1-1) | [O’Reilly](https://www.oreilly.com/library/view/container-security/9781492056690/)**
  
  To facilitate scalability and resilience, many organizations now run applications in cloud native environments using containers and orchestration. But how do you know if the deployment is secure? This practical book examines key underlying technologies to help developers, operators, and security professionals assess security risks and determine appropriate solutions.
  
  Author Liz Rice, Chief Open Source Officer at Isovalent, looks at how the building blocks commonly used in container-based systems are constructed in Linux. You’ll understand what’s happening when you deploy containers and learn how to assess potential security risks that could affect your deployments. If you run container applications with kubectl or docker and use Linux command-line tools such as ps and grep, you’re ready to get started.
- Explore attack vectors that affect container deployments
- Dive into the Linux constructs that underpin containers
- Examine measures for hardening containers
- Understand how misconfigurations can compromise container isolation
- Learn best practices for building container images
- Identify container images that have known software vulnerabilities
- Leverage secure connections between containers
- Use security tooling to prevent attacks on your deployment
  
  *Liz Rice is presenting “eBPF vs Sidecars” at P99 CONF.*
- ## Time Is Money: The Business Value of Web Performance
  
  ![timeismoney.jpg](timeismoney.jpg)
  
  **By Tammy Everts**
  
  June 2016[Bookshop.org](https://bookshop.org/p/books/time-is-money-the-business-value-of-web-performance-tammy-everts/8131909?ean=9781491928745) | [Amazon](https://www.amazon.com/Time-Money-Business-Value-Performance/dp/1491928743/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=1695702812&sr=1-1) | [O’Reilly](https://www.oreilly.com/library/view/time-is-money/9781491928783/?_gl=1*efbp82*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDI3MDguMzcuMC4w)
  
  If you want to convince your organization to conduct a web performance upgrade, this concise book will strengthen your case. Drawing upon her many years of web performance research, author Tammy Everts uses case studies and other data to explain how web page speed and availability affect a host of business metrics. You’ll also learn how our human neurological need for quick, uncomplicated processes drives these metrics.
- What happens neurologically when people encounter slow or interrupted processes
- How page speed affects metrics in retail and other industries, from media sites to SaaS providers
- Why internal applications are often slower than consumer apps, and how this hurts employee morale and productivity
- Common performance problems and the various technologies created to fight them
- How to pioneer new metrics, and create an organizational culture of performance
  
  *Tammy is presenting “Performance Budgets for the Real World” at P99 CONF.*
- ## Go in Action
  
  ![Goinaction.jpg](Goinaction.jpg)
  
  **By William Kennedy (P99 CONF speaker), Brian Ketelsen, and Erik St Martin**
  
  November 2015
  
  [Bookshop.org](https://bookshop.org/p/books/go-in-action-william-kennedy/10667037?ean=9781617291784) | [Amazon](https://www.amazon.com/Go-Action-William-Kennedy/dp/1617291781) | [O’Reilly](https://www.oreilly.com/library/view/go-in-action/9781617291784/?_gl=1*5qyqir*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDMxNjYuNTguMC4w)
  
  *Go in Action* is for any intermediate-level developer who has experience with other programming languages and wants a jump-start in learning Go or a more thorough understanding of the language and its internals. This book provides an intensive, comprehensive, and idiomatic view of Go. It focuses on the specification and implementation of the language, including topics like language syntax, Go’s type system, concurrency, channels, and testing.
- Language specification and implementation
- Go’s type system
- Internals of Go’s data structure
- Testing and benchmarking
  
  *William is presenting “Practical Go Memory Profiling” at P99 CONF.*
- ## High Performance MySQL: Optimization, Backups, and Replication
  
  ![mysqlzaitsev.jpg](mysqlzaitsev.jpg)
  
  **By Peter Zaitsev**
  
  April 2012
  
  [Amazon](https://www.amazon.com/High-Performance-MySQL-Optimization-Replication/dp/1449314287/ref=sr_1_2?crid=2ILBN4OYKCUUH&keywords=peter+zaitsev&qid=1663206517&sprefix=peter+zaitsev%2Caps%2C133&sr=8-2) | [O’Reilly](https://www.oreilly.com/library/view/high-performance-mysql/9781449332471/)
  
  How can you bring out MySQL’s full power? With *High Performance MySQL*, you’ll learn advanced techniques for everything from designing schemas, indexes, and queries to tuning your MySQL server, operating system, and hardware to their fullest potential. This guide also teaches you safe and practical ways to scale applications through replication, load balancing, high availability, and failover.
  
  This book not only offers specific examples of how MySQL works, it also teaches you why this system works as it does, with illustrative stories and case studies that demonstrate MySQL’s principles in action. With this book, you’ll learn how to think in MySQL.
- Learn the effects of new features in MySQL 5.5, including stored procedures, partitioned databases, triggers, and views
- Implement improvements in replication, high availability, and clustering
- Achieve high performance when running MySQL in the cloud
- Optimize advanced querying features, such as full-text searches
- Take advantage of modern multi-core CPUs and solid-state disks
- Explore backup and recovery strategies – including new tools for hot online backups
  
  *Peter Zaitsev is presenting “MySQL Performance on Modern CPUs: Intel vs AMD vs ARM” at P99 CONF.*
- ## Expert Oracle Exadata
  
  ![oracleexadata.jpg](oracleexadata.jpg)
  
  **By Kerry Osborne (P99 CONF speaker), Randy Johnson, Tanel Pöder (P99 CONF speaker)**
  
  August 2011
  
  [Bookshop.org](https://bookshop.org/p/books/expert-oracle-exadata-randy-johnson/9414684?ean=9781430233923) | [Amazon](https://www.amazon.com/Expert-Oracle-Exadata-Experts-Voice-ebook/dp/B005PZ09JM/ref=sr_1_3?crid=1T4ALODQ09N7V&keywords=Expert+Oracle+Exadata+kerry&qid=1694143545&sprefix=expert+oracle+exadata+kerry%2Caps%2C186&sr=8-3) | [O’Reilly](https://www.oreilly.com/library/view/expert-oracle-exadata/9781430233923/?_gl=1*p2c0kp*_ga*NTQ0Njc5MTc4LjE2NzE1OTA5MDQ.*_ga_092EL089CH*MTY5NDE0MDczMC43MC4xLjE2OTQxNDMzMjkuMjQuMC4w)
  
  **Expert Oracle Exadata** will give you a look under the covers at how the combination of hardware and software that comprise Exadata actually work. Authors Kerry Osborne, Randy Johnson, and Tanel Pöder share their real-world experience, gained through multiple Exadata implementations with the goal of opening up the internals of the Exadata platform. This book is intended for readers who want to understand what makes the platform tick and for whom—”how” it does what it does is as important as what it does. By being exposed to the features that are unique to Exadata, you will gain an understanding of the mechanics that will allow you to fully benefit from the advantages that the platform provides.
- Configure Exadata from the ground up
- Optimize for mixed OLTP/DW workloads
- Migrate large data sets from existing systemsConnect Exadata to external systems
- Support consolidation strategies using the Resource Manager
- Configure high-availability features of Exadata, including real application clusters (RAC) and automatic storage management (ASM)
- Apply tuning strategies utilizing the unique features of Exadata
  
  *Kerry Osborne is presenting “How to Improve Your Ability to Solve Complex Performance Problems” at P99 CONF.*
  
  *Tanel Pöder is presenting “Always-on Profiling of All Linux Threads, On-CPU and Off-CPU, with eBPF & Context Enrichment” at P99 CONF.*
  
  ![wasm_sarna.png](wasm_sarna.png)
  
  **How WebAssembly addresses key issues with SQLite UDFs — so you can skip the low-level C API and use languages like Rust, Zig, or Go**
  
  > Editor’s note: The following is a post from Piotr Sarna, a long-time ScyllaDB contributer who’s now at Turso. At P99 CONF 23, he presented “Less Wasm,” a short case study on how to “minify” WebAssembly code compiled with the Rust toolchain so that it loads faster and consumes less resources. This article was originally published on Turso’s blog.
  > 
  
  [Watch Piotr’s talk](https://www.p99conf.io/session/less-wasm/)
  
  [Access all the videos and decks](https://www.p99conf.io/on-demand/)
  
  A while back, [Turso](https://turso.tech/) announced that we were forking SQLite, into a project called [libSQL](https://github.com/tursodatabase/libsql). While we love SQLite, we respectfully disagree with (even if we understand) their focus on being fully public domain with no 3rd party code and rarely accepting contributions. Our goal was to create a community of database enthusiasts who want to explore other directions that could be taken for an OLTP-oriented embedded database if SQLite would be more open, while standing on the shoulders of giants, as we all should aspire to do.
  
  In the first official release of libSQL, one of our main goals was to address the challenges of SQLite UDFs with a new approach: the ability to dynamically create WebAssembly-powered user-defined functions. We wanted to address key issues with SQLite UDFs so users could skip the low-level C API and use languages like Rust, Zig, or Go.
- ## Problems with SQLite user-defined functions (UDFs)
  
  SQLite supports user-defined functions. UDFs in SQLite work by allowing users to provide a piece of C code that will be executed directly into the data, performing some in-statement computation.
  
  For example, you could define a function to calculate a hash of a particular string, and then obtain hashes for all values in a column col from a table table by writing:
  
  ```
  SELECT hash(col) from table;
  ```
  
  In an over-the-network database like Postgres, not using UDFs means that before any computation can be performed, the client needs to first fetch the data. This can be very wasteful.
  
  For an embedded database, there is no network activity involved in fetching this data (although we are also exploring changing that). Still, using UDFs, as opposed to materializing the data and then transforming, can avoid memory copies and extra passes, resulting in faster code. But there are problems…
- ### A more convenient API
  
  The first problem is that in the original SQLite, UDFs are available through the C API or its derivatives, which means that they can only be registered programmatically. The SQL layer is what is ultimately exposed, so that’s where we should aim for function registration to live.
  
  Many projects (like [rqlite](https://github.com/rqlite/rqlite), [dqlite](https://dqlite.io/), [mvsqlite)](https://github.com/losfair/mvsqlite) do try to push the boundaries, and add network functions around SQLite, which is one more point in favor of function manipulation at the statement level, as opposed to the low-level C API.
  
  That’s why other SQL databases customarily offer a `CREATE FUNCTION` statement, and we want one as well. `CREATE FUNCTION` statements would be a perfect gateway for users to add their specific logic to the database.
- ### The choice of language
  
  Aside from not being available from the SQL statements, the SQLite function API expects you to register a pointer to a C function. With the help of your driver, that doesn’t mean that you have to write your function in C: your language of choice likely has a C [FFI](https://en.wikipedia.org/wiki/Foreign_function_interface). The driver just has to provide C bindings to your functions.
  
  That is easy from the programmatic interface from a single-language driver. But if we want this to work from the SQL statements in a consistent way, we need a language that is cross platform enough so that it will work with any driver.
  
  It could be C. But for a large contingent of our industry, we’re usually talking about higher level languages like Go, Ruby, or TypeScript. Even in the domain of systems programming, historically a stronghold of C and C++, Zig and Rust are rapidly gaining momentum.
- ## WebAssembly for User-Defined Functions
  
  Thankfully, there is a language, also gaining rapid momentum across different ecosystems, that is a great fit for user-defined functions: WebAssembly. One of its core foundations is isolation, which is essential for running untrusted code on your own machines. It also ticks all the other boxes:
- thriving open-source community
- robustness
- portability
- performance
- sandboxing
  
  You don’t actually have to write your code directly into WebAssembly. It is a common compile target for many modern languages, such as Rust and Zig.
  
  There are multiple WebAssembly runtimes to choose from, including Google’s [V8](https://v8.dev/), [Wasmtime](https://wasmtime.dev/), [Wasmer](http://wasmer.io/), [WasmEdge](https://wasmedge.org/) and many others.
  
  The language is publicly specified. So, true to the original SQLite’s approach, it would not be impossible to write an entire new WebAssembly runtime into SQLite. But we believe there are benefits to keeping to the existing runtimes, and for libSQL, we will just integrate.
- ## Example: How to run an encryption routine as a UDF with libSQL
  
  Let’s go through a full example of how to run an encryption routine as a UDF with libSQL.
- ### Get the latest libSQL release
  
  In order to run WebAssembly user-defined functions in libSQL, the first step is to get the latest libSQL release. Release artifacts for x86_64 Linux can be downloaded from the official release page. The release is also available in a container.
  
  To run the shell, use the following command:
  
  ```
  docker run -it piotrsarna/libsql:libsql-0.1.0-wasm-udf ./libsql
  ```
  
  The source code is available on GitHub.
- ### Compile your first function
  
  The first step is to compile your code into a WebAssembly binary. You can then load a file containing the WebAssembly binary, or even add the resulting binary blob straight into the SQL statement.
  
  For this example, we will write our code in Rust. Your code can do pretty much any computations, as long as it doesn’t try to access system resources (including time/date and sources for entropy for pseudorandom number generation), use the network, and so on — that’s something that WebAssembly isolation rules will prevent.
  
  In addition to WebAssembly isolation rules, we require that you limit the function parameters and return type to something that both WebAssembly and libSQL can handle, specifically, for our Rust example:
- Any primitive integer type for libSQL’s `INTEGER` type
- `f32` or `f64` for libSQL’s `REAL` type
- `String` or `&str` for libSQL’s `TEXT` type
- `Vec<u8>` for libSQL’s `BLOB` type
  
  To make this process easier, we provide a crate, [libsql_bindgen](https://crates.io/crates/libsql_bindgen). It allows you to add the `#[libsql_bindgen]` macro to a Rust function, making sure all types in the function signature are transformed the the types libSQL understands.
- ### Come play at our playground instead?
  
  If you don’t feel like doing this all manually, that’s okay: we deliver all the tools to make the experience as smooth as possible, at our playground [bindgen](https://bindgen.libsql.org/).
  
  Navigate there and click the “Generate” button. Now paste the resulting SQL statement right into the libSQL shell.
- ### Calling your first function
  
  For this example, let’s compile the following Rust function, using bindgen:
  
  |  | pub fn decrypt(data: String, key: String) -> String { |
  | --- | --- |
  |  | use magic_crypt::MagicCryptTrait; |
  |  | let mc = magic_crypt::new_magic_crypt!(key, 256); |
  |  | mc.decrypt_base64_to_string(data) |
  |  | .unwrap_or("[ACCESS DENIED]".to_owned()) |
  |  | } |
  
  [view raw](https://gist.github.com/scynthiadunlop/cfe52bc207f2ee5ac7c926b904fb8009/raw/2f794280e22a06f2cb58dac4f518d5dad4c23a84/blog1.rs)  [blog1.rs](https://gist.github.com/scynthiadunlop/cfe52bc207f2ee5ac7c926b904fb8009#file-blog1-rs)  hosted with ❤ by [GitHub](https://github.com/)
  
  Start by launching the libSQL shell:
  
  ```
  ./libsql
  ```
  
  As a next step, let’s instantiate the functions and create a demo table with some data we want encrypted. Note that we will paste the statements as blobs, by clicking “as binary blob” in the bindgen playground. That is just to allow a more compact representation.
  
  Now, let’s see if we’re able to read the results as key owners, and get refused otherwise:
  
  Voilà! All the secrets are properly encrypted, and the decryption key works too.
- ## WebAssembly triggers in libSQL
  
  WebAssembly-powered user-defined functions are exciting on their own, but combined with database triggers, they become a powerful building block for automating your workflows. [This follow-up blog](https://blog.turso.tech/webassembly-triggers-in-libsql-b5eb62cc1c6) shares a few examples of WebAssembly triggers in action within a database flow for creating new user records. It walks you through how triggers can be used to:
- Save passwords in an encrypted form instead of plaintext
- Check if the encryption works
- Generate a unique single-use token for each user and put it in a separate table
- Verify that a single-use token was indeed generated and inserted into the table
  
  Read about [how to use WebAssembly for database triggers](https://blog.turso.tech/webassembly-triggers-in-libsql-b5eb62cc1c6).
- ## Watch Piotr’s Talk from P99 CONF 23
  
  Piotr’s **“Less Wasm”** tech talk is a case study on how getting rid of WebAssembly is great for your latency. More specifically, it’s about how you can reduce the size of your WebAssembly binaries so that they load faster and perform better. He walks through a handful of “minification” techniques he’s found useful, then shares the results from applying these techniques to libSQL. (Spoiler: they achieved a 24000% reduction in size).
  
  ![1200x628-p99conf-piotr-sarna-turso.jpg](1200x628-p99conf-piotr-sarna-turso.jpg)
  
  ![circle-lines-2x-1.png](circle-lines-2x-1.png)
  
  lines masked in circle
  
  ![1200x628-low-latency-ditsributed-strategies-768x402-1.png](1200x628-low-latency-ditsributed-strategies-768x402-1.png)
  
  *P99 CONF 2023 is now a wrap! You can (re)watch all videos and access the decks now.*
  
  [ACCESS ALL THE VIDEOS AND DECKS NOW](https://www.p99conf.io/on-demand/)
  
  P99 CONF is a (free + online) highly-technical conference for engineers who obsess over P99 percentiles and long-tail latencies. The open source, community-focused event is hosted by [ScyllaDB](https://www.scylladb.com/), the company behind the [monstrously fast and scalable NoSQL database](https://www.scylladb.com/) (and the adorable one-eyed sea monster).
  
  ![ScyllaDB2017_223-scaled.jpg](ScyllaDB2017_223-scaled.jpg)
  
  Since database performance is so near and dear to us at ScyllaDB, we quite eagerly reached out to our friends and colleagues across the community to ensure a wide spectrum of distributed data systems, approaches, and challenges would be represented at P99 CONF. This year’s agenda covers SQL and NoSQL, ORMs, tuning, infrastructure, event-driven architectures, edge DBs, AI/ML feature stores, drivers, benchmarking, tracing, Raft, tablets, and much more.
  
  If you share our obsession with high-performance low-latency data systems, here’s a rundown of sessions to consider watching at P99 CONF 2023.
- ## A Deterministic Walk Down TigerBeetle’s main() Street
  
  ![600x420-P99-23-aleksei-kladov-tiger-beetle.jpg](600x420-P99-23-aleksei-kladov-tiger-beetle.jpg)
  
  **Aleksei Kladov (TigerBeetle)**
  
  Dive into how TigerBeetle used Zig to implement a fully deterministic distributed system that will never fail with an out of memory error, for predictable performance and 700x faster tests!
- ## Armin Ronacher Creator of Flask and Principal Architect at SentryIngesting in Rust
  
  ![600X420-P99-23-armin-ronacher-sentry.jpg](600X420-P99-23-armin-ronacher-sentry.jpg)
  
  **Armin Ronacher (Sentry)**
  
  Hear about building a Rust based ingestion service that handles hundreds of thousands of events per second with low latency globally.
- ## Taming P99 Latencies at Lyft: Tuning Low-Latency Online Feature Stores
  
  ![600x420-P99-23-bhanu-renukuntla-lyft.jpg](600x420-P99-23-bhanu-renukuntla-lyft.jpg)
  
  **Bhanu Renukuntla (Lyft)**
  
  Explore the challenges and strategies of tuning low latency online feature stores to tame P99 latencies, shedding light on the importance of choosing the right data model.
- ## The History of Tracing Oracle
  
  ![600x420-P99-23-cary-millsap-method-r.jpg](600x420-P99-23-cary-millsap-method-r.jpg)
  
  **Cary Millsap (Method R Corporation)**
  
  Delve into the history of tracing Oracle, why it has been overlooked despite its usefulness, and examples of how Oracle traces can help improve performance across your whole technology stack.
- ## Building Low Latency ML Systems for Real-Time Model Predictions at Xandr
  
  ![600x420-P99-23-chinmay-abhay-nerurkar-microsoft.jpg](600x420-P99-23-chinmay-abhay-nerurkar-microsoft.jpg)
  
  **Chinmay Abhay Nerurkar Moussa Taifi (Microsoft)**
  
  Learn about the challenges of building an ML system with the low latency required to support the high volume and high throughput demands of ad serving.
- ## Cost-Effective Burst Scaling For Distributed Query Execution
  
  ![600x420-P99-23-dan-harris-coralogix.jpg](600x420-P99-23-dan-harris-coralogix.jpg)
  
  **Dan Harris (Coralogix)**
  
  A case study in building a distributed execution model that can dynamically execute across both AWS Lambda and EC2 resources – shedding excess load to lambda functions to preserve low latency while scaling EC2 capacity to manage costs.
- ## Cache Me If You Can: How Grafana Labs Scaled Up Their Memcached 42x & Cut Costs Too
  
  ![600x420-P99-23-danny-kopping-grafana-1.jpg](600x420-P99-23-danny-kopping-grafana-1.jpg)
  
  **Danny Kopping (Grafana Labs)**
  
  How Grafana Labs managed to increase their cache size by 42x and reduce costs by using a little-known feature of memcached called “extstore”.
- ## Segment-Based Storage vs. Partition-Based Storage: Which is Better for Real-Time Data Streaming?
  
  ![600x420-P99-23-david-kjerrumgaard-streamnative.jpg](600x420-P99-23-david-kjerrumgaard-streamnative.jpg)
  
  **David Kjerrumgaard (StreamNative)**
  
  Explore key differences between segment-based and partition-based storage models (including how data is organized, stored, and accessed) with an eye toward what’s best for real-time data streaming system performance, scalability, and resiliency.
- ## Demanding the Impossible: Rigorous Database Benchmarking
  
  ![600x420-P99-23-dmitrii-dolgov-redhat.jpg](600x420-P99-23-dmitrii-dolgov-redhat.jpg)
  
  **Dmitrii Dolgov (Red Hat)**
  
  An analysis of how to design an effective database benchmark, including selecting a mode, overcoming technical challenges, and analyzing the results (using PostgreSQL as an example).
- ## Dor Laor CEO of ScyllaDBQuantifying the Performance Impact of Shard-per-core Architecture
  
  ![600X420-P99-23-dor-laor-scylladb.jpg](600X420-P99-23-dor-laor-scylladb.jpg)
  
  **Dor Laor (ScyllaDB)**
  
  Most software isn’t architected to take advantage of modern hardware. How does a shard-per-code and shared-nothing architecture help – and exactly what impact can it make? Dor will examine technical opportunities and tradeoffs, as well as disclose the results of a new benchmark study.
- ## Writing Low Latency Database Applications Even if Your Code Sucks
  
  ![600X420-P99-23-glauber-costa-turso.jpg](600X420-P99-23-glauber-costa-turso.jpg)
  
  G**lauber Costa (Turso)**
  
  How – by putting data close to its users –you can save hundreds of milliseconds and still be faster than the most optimized code … even if your code sucks.
- ## ORM is Bad, But is There an Alternative?
  
  ![600x420-P99-23-henrietta-dombrovskaya-drw.jpg](600x420-P99-23-henrietta-dombrovskaya-drw.jpg)
  
  **Henrietta Dombrovskaya (DRW)**
  
  Why optimizing the application/database interaction is important and how the No-ORM framework provides an escape to common ORM pitfalls while maintaining their ease of use.
- ## The Art of Event Driven Observability with OpenTelemetry
  
  ![600x420-P99-23-henrik-rexed-dynatrace.jpg](600x420-P99-23-henrik-rexed-dynatrace.jpg)
  
  **Henrik Rexed (Dynatrace)**
  
  Explore the various components of OpenTelemetry, examples of unuseful traces from event driven architecture, and the purpose/usage of span links in event driven architecture.
- ## From 1M to 1B Features Per Second: Scaling ShareChat’s ML Feature Store
  
  ![600X420-P99-23-ivan-burmistrov-sharechat.jpg](600X420-P99-23-ivan-burmistrov-sharechat.jpg)
  
  **Ivan Burmistrov and Andrei Manakov (Sharechat)**
  
  A case study in building a low latency ML feature store (using ScyllaDB, Golang, and Flink) that handles 1B features per second, including data modeling tips for performance & scalability and caching strategies.
- ## Jon Haddad Founder at Rustyrazorblade ConsultingDistributed System Performance Troubleshooting Like You’ve Been Doing It for 20 Years
  
  ![600X420-P99-23-jon-haddad-rustyrazorblade.jpg](600X420-P99-23-jon-haddad-rustyrazorblade.jpg)
  
  **Jon Haddad (Rustyrazorblade Consulting)**
  
  Discover how to go about diagnosing performance problems in complex distributed systems and learn the tools and processes for getting to the bottom of any issue, quickly – even when it’s one of the biggest distributed database deployments on the planet.
- ## Low-Latency Data Access: The Required Synergy Between Memory & Disk
  
  ![600x420-P99-23-kriti-kathuria-centrum-wiskunde-1.jpg](600x420-P99-23-kriti-kathuria-centrum-wiskunde-1.jpg)
  
  **Kriti Kathuria (University of Waterloo)**
  
  Learn about the synergy required between memory and disk to achieve efficient data processing and the general techniques that databases use for efficient data storage and retrieval.
- ## Square’s Lessons Learned from Implementing a Key-Value Store with Raft
  
  ![600x420-P99-23-omar-elgabry-square.jpg](600x420-P99-23-omar-elgabry-square.jpg)
  
  **Omar Elgabry (Square)**
  
  The micro-lessons engineers can learn from Square’s experience building fault-tolerant, strongly consistent distributed systems using Raft.
- ## MySQL Performance on Modern CPUs: Intel vs AMD vs ARM
  
  ![600X420-P99-23-peter-zaitsev-percona-1.jpg](600X420-P99-23-peter-zaitsev-percona-1.jpg)
  
  **Peter Zaitsev (Percona)**
  
  Look into the current CPU choices through a MySQL lens: which CPUs provide the best performance for single-threaded and high-concurrency workloads and which help to achieve the best price/performance.
- ## Conquering Load Balancing: Experiences from ScyllaDB Drivers
  
  ![600X420-P99-23-piotr-grabowski-scylladb.png](600X420-P99-23-piotr-grabowski-scylladb.png)
  
  **Piotr Grabowski (ScyllaDB)**
  
  Get insight into the intricacies of load balancing within ScyllaDB drivers with Piotr sharing how we employed the Power of Two Choices algorithm, optimized the implementation of load balancing in Rust Driver, and more.
- ## 5 Hours to 7.7 Seconds: How Database Tricks Sped up Rust Linting Over 2000X
  
  ![600x420-P99-23-predrag-gruevski-trustfall.jpg](600x420-P99-23-predrag-gruevski-trustfall.jpg)
  
  **Predrag Gruevski (Trustfall)**
  
  A case study about using database ideas to build a linter that looks for breaking changes in Rust library APIs.
- ## Adventures in Thread-per-Core Async with Redpanda and Seastar
  
  ![600X420-P99-23-travis-downs-redpanda.jpg](600X420-P99-23-travis-downs-redpanda.jpg)
  
  **Travis Downs (Redpanda)**
  
  A look at the practical experience of building high performance systems with C++20 in an asynchronous runtime, the unexpected simplicity that can come from strictly mapping data to cores, and the challenges & tradeoffs in adopting a thread-per-core architecture.
- ## Automatically Sharding and Scaling-out Databases on Kubernetes
  
  ![600x420-P99-23-trista-pan-sphere-ex.jpg](600x420-P99-23-trista-pan-sphere-ex.jpg)
  
  **Trista Pan (SphereEx)**
  
  New ways to create a distributed/sharding database system based on your existing monolithic databases – without exacerbating data management, auto-scaling, and query performance issues.
- ## Mitigating the Impact of State Management in Cloud Stream Processing Systems
  
  ![600x420-P99-23-yingjun-wu-risingwave-labs.jpg](600x420-P99-23-yingjun-wu-risingwave-labs.jpg)
  
  **Yingjun Wu (RisingWave Labs)**
  
  How RisingWave Labs is addressing the high latency issues associated with S3 storage in stream processing systems that employ a decoupled compute and storage architecture.
- ## Unconventional Methods to Identify Bottlenecks in Low-Latency and High-Throughput Data Pipelines
  
  ![600x420-P99-23-zamir-paltiel-hyperspace.jpg](600x420-P99-23-zamir-paltiel-hyperspace.jpg)
  
  **Zamir Paltiel (Hyperspace)**
  
  Standard profiling and monitoring methods may fall short in identifying bottlenecks in low-latency data ingestion workflows; discover unconventional techniques to apply instead.
  
  ![1200x628-p99-23-day-one-recap.jpg](1200x628-p99-23-day-one-recap.jpg)
  
  Hello readers, or should I say G’day?
  
  I’m excited to share the behind-the-scenes journey, the incredible numbers, and the impact of this year’s conference [P99 CONF](https://www.p99conf.io/) from the perspective of one of your hosts.
  
  Hosting the conference has been nothing short of a whirlwind adventure for me. From helping to select and review all the content through to the excitement, challenges, and triumphs of hosting a rather large virtual event with a wonderful team – it’s been so much fun.
  
  Firstly, I’d like to comment on the high-quality content provided by so many individuals from around the world. There were over 160 submissions, from which the organizing team had to distill down to around 60 recorded sessions over 2 half days. Those numbers alone speak to what strong an interest there is in the world of low-latency, high-performance distributed computing challenges. Why does this matter so much to me? I’ve been a long-term advocate for performance engineering from different roles, so it’s stunning to see such keen interest in this space. A big thank you to all those who submitted an idea – hopefully the team can keep expanding the conference as a whole, and I’d encourage you to consider submitting again next year.
  
  For the 60 presentations that made it through, what a smorgasbord of information there was! So another big thank you for all the preparation, practice, and performance of your own individual presentations. I’m sure that amounts to days, if not weeks of combined effort, so well done.
  
  The irony of this being a virtual event, with live in-person hosting by myself and Wayne Ariola, was not lost on me. However, secretly, I always love an opportunity to travel, so I really appreciated flying over from Australia to San Francisco to help host live from the production studio. As I mentioned in my opening, I trust that you all found the conference to be bigger, better and way less sweaty than an in-person conference. It was great to see the lively discussions being held in each stage’s chat. To be honest, I think this is the real beauty of this event format. The stress of preparing and delivering content by the presenters has already been overcome, which frees them up to reflect, observe, and answer attendees questions live. Way better than standing around in a line hoping to bend someone’s ear at the end of a talk in a noisy hall!
  
  [Watch P99 CONF Talks on Demand](https://www.p99conf.io/)
  
  Ok, so let’s recap some stand-out presentations for me. The conference opened up with puppies – err – “[Quantifying the Impact of Shard-per-core Architecture](https://www.p99conf.io/session/quantifying-the-performance-impact-of-shard-per-core-architecture/)” by Dor Laor, Co-Founder of ScyllaDB. What a great start to the conference – this really set the stage for what was going to be a highly technical yet very informative event. I walked away from that presentation feeling guilty about all the times I had hit `terraform apply` to scale out with more infrastructure, not having thought about the option to simply scale up. ScyllaDB takes advantage of both directions in scaling, with impressive numbers presented and some interesting insights into what’s next on their roadmap, particularly distributing data among shards dynamically with a feature called Tablets. Excited to hear more about that.
  
  Next was Jon Haddad’s presentation “[Distributed System Performance Troubleshooting Like You’ve Been Doing it for Twenty Years](https://www.p99conf.io/session/distributed-system-performance-troubleshooting-like-youve-been-doing-it-for-twenty-years/).” As the title suggested, this was literally 20 years of experience wrapped up in 20 minutes. If you’re new to the world of performance, then treat this like a blueprint for observing performance. If you consider yourself a veteran, then USE it as a checklist to see if there’s anything you missed 😉
  
  Another hidden gem in the instant access area was Kerry Osbourne’s presentation on “[How to Improve Your Ability to Solve Complex Performance Problems](https://www.p99conf.io/session/how-to-improve-your-ability-to-solve-complex-performance-problems/).” This was more like 40 years of experience in 40 minutes. Some great thinking in this one (both fast and slow) about problems and how we resolve those problems in a deeply technical context. Great to see so many of our cognitive biases mentioned here. Definitely worth adding to your blueprint for success in this space.
  
  Mark Gritter gave an excellent presentation on “[The Latency Stack: Discovering Surprising Sources of Latency](https://www.p99conf.io/session/how-to-improve-your-ability-to-solve-complex-performance-problems/)” from his trials and tribulations solving performance issues over the years. The list was long, and had the usual suspect, DNS (hands up if you’ve been caught by this before) among many other culprits including hypervisors, hardware, and queues to name a few. I truly enjoyed the story telling element to this presentation.
  
  I have grown fond of coding in Rust, so it was great to hear Carl Lerche explore Rust’s potential benefits to application backend development in his presentation “[Expanding Horizons: A Case for Rust Higher Up the Stack](https://www.p99conf.io/session/expanding-horizons-a-case-for-rust-higher-up-the-stack/)”. Glauber Costa delved into the challenges of massive data replication to the edge with his presentation “[Writing Low Latency Database Applications Even If Your Code Sucks](https://www.p99conf.io/session/writing-low-latency-database-applications-even-if-your-code-sucks/).” That really set the scene for my favorite part of day 1: a live discussion panel with Glauber, Carl and Jarred Sumner (creator of Bun.js). What a trio – I fell away to the sidelines to listen in with awe as these three hashed out the differences, and also what features languages like Zig and Rust might borrow or benefit from each other. To share some behind the scenes, getting three great personalities online at the same time is no easy task. A big thanks to Glauber and the organizing team for helping make this happen over some (cold) pizza and lobby refreshments the night before!
  
  There were many other favorite presentations tucked away in the day (it was a blur to me) but the most memorable was Liz Rice’s presentation on “[eBPF vs Sidecars](https://www.p99conf.io/session/ebpf-vs-sidecars/)” showing some novel ways to approach the problem of application instrumentation with less fuss. Henrietta Dombrovskaya also gave a presentation on “[ORM is Bad, But is There an Alternative?](https://www.p99conf.io/session/orm-is-bad-but-is-there-an-alternative/)” and it was wonderful to see such strong advocacy between the boundaries of development and databases – something I’ve found difficult to negotiate in the past. I would love to learn more about her use of contracts within the No-ORM Framework.
  
  More great content in the afternoon from Steven Rostedt with “[Using Libtracecmd to Analyze Your Latency and Performance Troubles](https://www.p99conf.io/session/using-libtracecmd-to-analyze-your-latency-and-performance-troubles/).” This was a deep dive into what happens at the kernel level – not just the scheduler, but also how long locks are held and where and when the interrupts are coming from. Surfacing from the deep was an excellent presentation “[Beyond Availability: The Seven Dimensions for Data Product SLOs](https://www.p99conf.io/session/beyond-availability-the-seven-dimensions-for-data-product-slos/)” by Emily Gorcenski which really cemented my understanding of the hierarchy of all the SL* including indicators, objectives, and agreements.
  
  To wrap up the day, we had a closing keynote from Paul McKenney on “[How to Avoid Learning the Linux-Kernel Memory Model](https://www.p99conf.io/session/how-to-avoid-learning-the-linux-kernel-memory-model/).” Paul seems to have a knack for explaining deeply technical concepts at a level I can understand. I only wish I had someone like Paul as my professor at University. Be sure to watch this presentation to get a glimpse at finger measurements of the speed of light at the CPU core level. Fascinating stuff!
  
  There were no major bloopers from the live hosting side that day. Apart from the normal nerves of presenting to an invisible audience of close to 18K peers, it was an incredible experience within the green screen studio. I definitely slept well after day 1. Stay tuned for an update on day 2
  
  ![p99conf_behindthescenes-scaled.jpg](p99conf_behindthescenes-scaled.jpg)
  
  ![1200x628-day-two-recap-p99.jpg](1200x628-day-two-recap-p99.jpg)
  
  Hello again readers.
  
  After some in-person catch up with the rest of the ScyllaDB team (yes, there are advantages to in-person events), we were up at sparrow’s fart to get ready for another big day of P99 CONF.
  
  [Read the Day 1 Recap](https://www.p99conf.io/2023/10/19/p99-conf-day-1-recap/)
  
  By this point, we all had time to reflect and read back through the many comments in chat. The organizing team were busy little beavers tweaking pre-recordings, sound levels and of course the now infamous P99 CONF playlist! This was a bit of a surprise for the team. So many people online commented on the groovy tracks picked by the conference organizer Natalie Estrada that we felt compelled to share that playlist. So here it is – the unofficial (and apparently un-shazam’able) [list of tracks that kept you entertained between sessions](https://artlist.io/mycollection/8a844d80-f0ea-469a-9505-704f79f8bbc5/1700490).
  
  With a liquid breakfast, some quick sound checks, and review of the packed schedule, we were back into day 2 with some exciting presentations to open. First up was Gwen Shapira speaking about “[High Performance on a Low Budget](https://www.p99conf.io/session/high-performance-on-a-low-budget/).” This is another presentation that I would like to replay and take notes from. I loved the opening statement around setting performance expectations early. This was reassuring to me, a performance advocate, who often hits the brick wall of “No, performance is not a concern right now”. So it was great to know we’re not alone with this sentiment. There were also some quotable quotes in this presentation, like making your benchmarks “pay rent”, and if you, “have no time to optimize, at least don’t pessimize”. It was also refreshing to hear of Gwen’s experience taking lessons from a prior big organization and applying them to a relatively smaller team – not to mention cracking the whip and busting out Wireshark on unsuspecting developers 🙂
  
  Speaking of quotable quotes, there were great tweets on social – I’m personally a fan of the “CAT” theorem, and also the two button meme, well played 😉
  
  > 
  > 
  > 
  > CAP Theorem? I thought it was CAT Theorem!
  > 
  > – Yogi, the distributed systems enthusiast, refreshing his Raft knowledge at [#P99Conf](https://twitter.com/hashtag/P99Conf?src=hash&ref_src=twsrc%5Etfw)
  > 
  > Excellent talk by [@Omar_ElGabry](https://twitter.com/Omar_ElGabry?ref_src=twsrc%5Etfw) [pic.twitter.com/SVn81kId5l](https://t.co/SVn81kId5l)
  > 
  > — Naz Ahmed 🚢 (@naz_io) [October 19, 2023](https://twitter.com/naz_io/status/1715056349166416025?ref_src=twsrc%5Etfw)
  > 
  
  > 
  > 
  > 
  > True before, true this year too.
  > 
  > Good thing that [#P99conf](https://twitter.com/hashtag/P99conf?src=hash&ref_src=twsrc%5Etfw) talks are available on demand later![#ScyllaDB](https://twitter.com/hashtag/ScyllaDB?src=hash&ref_src=twsrc%5Etfw) [#rustlang](https://twitter.com/hashtag/rustlang?src=hash&ref_src=twsrc%5Etfw) [#NoSql](https://twitter.com/hashtag/NoSql?src=hash&ref_src=twsrc%5Etfw) [#database](https://twitter.com/hashtag/database?src=hash&ref_src=twsrc%5Etfw) [#AI](https://twitter.com/hashtag/AI?src=hash&ref_src=twsrc%5Etfw) [#SQL](https://twitter.com/hashtag/SQL?src=hash&ref_src=twsrc%5Etfw) [#opensource](https://twitter.com/hashtag/opensource?src=hash&ref_src=twsrc%5Etfw) [#memes](https://twitter.com/hashtag/memes?src=hash&ref_src=twsrc%5Etfw) [pic.twitter.com/3qLPBc7ckV](https://t.co/3qLPBc7ckV)
  > 
  > — Paul Philleo (@philpauleo) [October 18, 2023](https://twitter.com/philpauleo/status/1714694983339459036?ref_src=twsrc%5Etfw)
  > 
  
  That reminds me… as a host, I was glued to stage 1 helping out and monitoring the chat. There was also a whole team of ScyllaDB staff working remotely, some all the way from Brazil including Felipe Cardeneti Mendes, who happens to be one of the authors of the new book “[Database Performance at Scale](https://www.scylladb.com/2023/10/02/introducing-database-performance-at-scale-a-free-open-source-book/).” Given I had some time to burn at the hotel the night before, I got a sneak peek at this book and can confidently say it’s a nice side companion to the art of scaling databases for high throughput, low latency applications. I encourage you all to have a read of the free book.
  
  [Get the Book & Interact with the Authors](http://bit.ly/dbscalemc)
  
  The next highlight of the day was hearing from Bryan Cantrill on the topic of “[Corporate Open Source Anti-Patterns: A Decade Later](https://www.p99conf.io/session/corporate-open-source-anti-patterns-a-decade-later/)”. Now I must admit, I’m not great with names, so it took some time for me to make the connection that Bryan developed DTrace, something I used daily way back when. But once that clicked, I once again listened in awe to an industry great, and felt privileged to hear his account of what’s changed, and where we’re at with open-source ten years down the track. Bryan showed us why he’s a renowned public speaker with his entertaining presentation, and set the scene for another live discussion with two of his mates, Adam Jacob and Ashley Williams. Essentially, the creators of DTrace and Chef and a former Rustlang team member, all in one virtual room and really sticking it to the issues, concerns, and expectations around open-source. I genuinely felt bad ending the discussion at the 20-minute mark, but the show had to go on! I feel this discussion should be given more airtime in another format.
  
  [Catch the Sessions You Missed, On-Demand](https://www.p99conf.io/)
  
  Now that you have the luxury of watching the recordings in slow time, without being forced to choose between stage 1, 2 or 3, there were also a couple more must see presentations during the live discussion. Be sure to check out Stefan Johansson’s presentation “[Reducing P99 Latencies with Generational ZGC](https://www.p99conf.io/session/reducing-p99-latencies-with-generational-zgc/)” and also Tammy Everts on ”[Performance Budgets for the Real World](https://www.p99conf.io/session/performance-budgets-for-the-real-world/)” which featured around the same time.
  
  Flipping back into a technical mode, Travis Downs took us on “[Adventures in Thread-per-Core Async with Redpanda and Seastar](https://www.p99conf.io/session/adventures-in-thread-per-core-async-with-redpanda-and-seastar/)” which is the open-source C++ framework for high-performance server applications on modern hardware, built and maintained by ScyllaDB. I feel this was an excellent example of some lessons learned in the previous live panel around integrating open-source with commercial products. I’m not a C++ expert myself, but judging by the detailed conversations in chat, this presentation really hit a chord with technical experts present at the conference.
  
  We also had a splendid presentation from Danny Kopping on “[Cache Me If You Can: How Grafana Labs Scaled Up Their Memcached 42x & Cut Costs Too](https://www.p99conf.io/session/cache-me-if-you-can-how-grafana-labs-scaled-up-their-memcached-42x-cut-costs-too/)” which was definitely my cup of tea. Danny laid out the problem space and how they approach tuning and optimization to achieve impressive performance. It was also great to hear about the perspectives of large SaaS applications and open-source products, such as Loki referenced in this presentation, but also many of the other industry leaders in similar presentations.
  
  Closing out the day for me, I was genuinely interested in Dmitrii Dolgov’s views on “[Demanding the Impossible: Rigorous Database Benchmarking](https://www.p99conf.io/session/demanding-the-impossible-rigorous-database-benchmarking/).” This presentation was the perfect balance of math, statistics and referenced studies for performance benchmarking in general, which, I felt, could be applied to wider performance topics. Definitely a track worth listening to if you want to expand your understanding of this topic. Tim Vereecke also gave a great presentation on “[Noise Canceling RUM](https://www.p99conf.io/session/noise-canceling-rum/)” and plenty of thinking material on the pitfalls in chasing percentiles, and how to improve that signal-to-noise ratio.
  
  I’ve got no other secrets to share short of what was already made public by Wayne at the end of the conference – 18K participants, 4K chats and a now 30K strong P99 conference community. It was a pleasure to be part of this conference and I can’t wait to see how it turns out in future.