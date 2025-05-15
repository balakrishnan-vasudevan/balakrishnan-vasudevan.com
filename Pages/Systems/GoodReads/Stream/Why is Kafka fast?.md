Example 1: There’s this [nice blog](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines) that benchmarks 2 Million writes per second only using three cheap nodes for the Kafka cluster.

Example 2: Paypal uses a complex Kafka architecture which consists of multiple Kafka clusters. As per their [blog](https://medium.com/@vsushko/kafka-performance-how-to-reach-desired-throughput-196d73802e3c) in 2023, they are already supporting 1.3 Trillion messages per day. They claim to have 21 million messages per second during the Black Friday sale.

Example 3: As per [Agoda’s blog](https://medium.com/agoda-engineering/how-agoda-manages-1-5-trillion-events-per-day-on-kafka-f0a27fc32ecb) in 2021, they are able to support 1.5 trillion messages per day using their current Kafka architecture. If you translate that number per second, it would be more than 17 million messages per second (considering the average case).

Why?

# It uses sequential I/O

There are two kinds of _disk_ access patterns: random disk I/O and sequential disk I/O. Random I/O is an expensive operation because the mechanical arm of the writer has to move around physically on the magnetic disk to perform reads and writes. However, Sequential I/O is straightforward and only appends data to the end, thus providing less latency (the seek time + disk rotational latency) for performing reads and writes.


![](https://substackcdn.com/image/fetch/w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40b6bfd9-9828-4755-a22a-a3f2d08a8a41_2504x1264.png)


The underlying advantage of using the Sequential I/O is that you just have to wait for the latency penalty only once (when the mechanical arm moves from its current location to the desired location on the disk) and then write data contiguously without any further penalty. However, you have to pay this latency penalty in random I/O for every read/write operation.



<aside> 💡

Kafka uses the Sequential I/O strategy. Kafka topics are append-only logs, and their contents are immutable. In this way, topics are similar to application log files. Because the events never change once written, Kafka topics are easy to replicate, which allows them to be durably and reliably stored across many nodes in the Kafka cluster.

</aside>

You might ask that if sequential I/O is so efficient, then why to use random I/O at all? Please note that random I/O is inevitable. As we create, delete, modify, read data in a database, the mechanical arm is bound to move and perform the requested operation (read/write) on the disk and thus your database will eventually perform random I/O operations. That’s why it’s recommended to use indexes as much as possible atleast for reading as they provide a logical sorted dataset and promotes more sequential I/O access pattern than random I/O.

# Zero Copy Principle

[[Zero Copy]]

Let’s first consider Data transfer without the Zero Copy Principle:

1. First, the OS (operating system) reads data from the disk and loads it into the OS buffer.
2. Then, the data gets copied from the OS buffer into Kafka’s application buffer.
3. Then, the data gets copied from Kafka’s application buffer to the Socket buffer.
4. Then, the data gets copied from the Socket buffer to the NIC(Network Interface Card) buffer. What is NIC? It’s called a Network Interface card which is a hardware component attached to a chip that’s responsible for sending data packets at the network layer.

![[Pasted image 20250505091224.png]]

Now let’s consider data transfer with the Zero Copy Principle:

1. First, the OS (operating system) reads data from the disk and loads it into the OS buffer.
2. Then, the Kafka application sends a system call called “sendfile()“ to tell the Operating system to copy the data directly from the OS buffer to the NIC buffer.

![[Pasted image 20250505091215.png]]

One thing to note here is that “sendfile” is a system call. It does not have anything to do with Kafka as a streaming platform. “SendFile” is a system call that transfers data between file descriptors. It allows the kernel to directly transfer the data between the source(OS) and destination(network socket), reducing memory usage and context switching between user and kernel space.

> User space refers to all code that runs outside the operating system's kernel and the kernel space refers to a space reserved exclusively for running the kernel and it’s related operations.

<aside> 💡

1. Reduced CPU usage: If we are doing less data copying, that means less CPU utilization and fewer context switches between the user space and kernel space. This allows the CPU to perform more tasks.
2. Less Latency: Hypothetically, if it was taking 100ms earlier to copy the data without the zero-copy technique, now it would take only 50ms with zero-copy. Thus, data can be transferred more quickly between producers and consumers. </aside>

# It is distributed

<aside> 💡

Another point that could contribute to overall Kafka’s success is that it’s distributed: Kafka stores data in a distributed manner on multiple brokers. Every broker in the Kafka cluster stores a subset of the whole data and can process that independently. As the data increases, you can add more brokers to add more parallelism to your Kafka cluster. Thus, Kafka is easily horizontally scalable and you don’t have to worry about increasing volume of data.

</aside>