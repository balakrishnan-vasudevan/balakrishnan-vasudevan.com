#task-scheduler

Manage task execution across multiple servers for efficiency and reliability.  

https://programmingappliedai.substack.com/p/design-distributed-job-scheduler-33a?utm_source=%2Fsearch%2Fuuid&utm_medium=reader2
 [Design a Distributed Job Scheduler for Millions of Tasks in Daily Operations](https://medium.com/p/4132dc6d645f)
  [Distributed Job Scheduler: Journey Zero to 20K+ Concurrent Jobs](https://medium.com/p/1fe8cf8ed288)
  [System Design Interview with a Meta Staff Engineer: Designing a Task Scheduler](https://medium.com/p/1a5041b4860e)

![[Pasted image 20250331094225.png]]
1. **User submits a job** → `Job Management Service`
    
2. **Job is added to queue** → `Queue Management Service` (Redis/Kafka)
    
3. **Worker picks up job** → `Job Execution Service` assigns it
    
4. **Worker executes job** → `Worker Node Service`
    
5. **Worker updates status** → Reports to `Job Execution Service`
    
6. **Job result is stored** → `Job Management Service` updates DB
    
7. **Metrics are tracked** → `Monitoring & Metrics Service` logs performance
    
8. **Notifications are sent** → `Notification Service` informs users

**FR**

1.Users should be able to submit **one-time or recurring jobs**.

2.Jobs can be **delayed** or scheduled at a specific time.

3.Support **High, Medium, Low** priority queues.

4.Support **parallel job execution** across multiple workers.

5.If a worker **crashes**, jobs should be **rescheduled** to another available worker.

6.Jobs should support **dependencies** (e.g., Job B runs **only after** Job A completes).

7.Users should be able to **query job status** (`RUNNING`, `FAILED`, `COMPLETED`).

8.Notify users (via **email, Webhook, Kafka**) upon job completion/failure.

9.Ensure that **duplicate jobs are not scheduled** accidentally.(idempotency should be taken care of)

**NFR**

1.Jobs should be picked up **within milliseconds** of their scheduled time.

2.**P99 latency should be < 50ms** for job assignment.

3. System should **be highly scalable to handle more jobs** (more worker nodes = more jobs processed).

4.The scheduler should be **highly available (99.99% uptime)**.

5.Job status should be **eventually consistent** across distributed nodes.  
  
**Estimates**

```
 Total jobs per day = 10M jobs
 QPS=10M/10^5=100QPS


 Peak traffic (requests per second) = ~200 jobs/sec (assuming peak 6 hours/day)
 Job size (metadata per job) = 1KB (includes ID, status, timestamps, etc.)
 Job execution time = 500ms per job (on average)
 Retention period = 30 days (job history kept in DB)
 Job Failure Rate = 5% (500K jobs need retries)
 Database replication factor = 3 (for HA)
 Cache hit rate = 95% (Redis for job metadata)
```

**Storage**

```
Job metadata= 1KB
total storage=10M*1KB=10GB per day
Retention period for 30 days=10GB*30=300GB
Replication factor (3x) for durable storage=300GB*3=900GB
```

### **Databases for a Distributed Job Scheduler & Their Schema**

A distributed job scheduler requires **different types of databases** for **various components** based on performance, scalability, and consistency needs.

🔹 Stores job metadata, execution history, and scheduling information.  
🔹 Ensures **ACID compliance** for job transactions.  
🔹 Good for **complex queries** (filtering, sorting, pagination).

### **Schema for Relational DB (PostgreSQL/MySQL)**

#### `jobs` **Table (Stores Job Metadata)**

```
CREATE TABLE jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_name VARCHAR(255) NOT NULL,
    job_type ENUM('one-time', 'recurring', 'batch') NOT NULL,
    schedule VARCHAR(255) NULL,  -- cron expression
    command TEXT NOT NULL,
    status ENUM('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    priority ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'MEDIUM',
    max_retries INT DEFAULT 3,
    timeout_seconds INT DEFAULT 300,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

`job_executions` Table (Stores Execution Logs)

```
CREATE TABLE job_executions (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    worker_id VARCHAR(255) NOT NULL,
    status ENUM('RUNNING', 'COMPLETED', 'FAILED', 'RETRYING') NOT NULL DEFAULT 'RUNNING',
    execution_time_ms INT,
    logs TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

## **2️⃣ NoSQL Database (Cassandra/DynamoDB) → Fast Job Lookup & History**

🔹 Used for fast retrieval of **job status and execution history**.  
🔹 **High write scalability** (handles millions of updates).  
🔹 **Schema-less** flexibility.

### **Schema for NoSQL DB (Cassandra)**

#### `jobs_by_status` **Table (For Quick Lookup)**

```
CREATE TABLE jobs_by_status (
    status TEXT,
    job_id UUID,
    job_name TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (status, created_at, job_id)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

```
SELECT * FROM jobs_by_status WHERE status = 'RUNNING' LIMIT 100;
```

`job_execution_logs` Table (For Fast Job History Retrieval)

```
CREATE TABLE job_execution_logs (
    job_id UUID,
    execution_id UUID,
    status TEXT,
    logs TEXT,
    execution_time_ms INT,
    completed_at TIMESTAMP,
    PRIMARY KEY (job_id, completed_at)
) WITH CLUSTERING ORDER BY (completed_at DESC);
```

## **3️⃣ In-Memory Database (Redis) → Fast Job Scheduling & Worker Queues**

🔹 **Low-latency** job scheduling and job dispatching.  
🔹 Used as a **distributed queue** for assigning jobs to workers.

### **Schema for Redis**

#### **Redis Sorted Set for Job Prioritization**

```
ZADD job_queue 10 "job_12345"
ZADD job_queue 20 "job_67890"   # Higher priority job
```

👉 Workers fetch jobs using:

```
ZRANGE job_queue 0 0 WITHSCORES
```

👉 Remove from queue after execution:

```
ZREM job_queue "job_12345"
```

## **4️⃣ Distributed Object Storage (S3/MinIO) → Job Execution Logs & Artifacts**

🔹 Stores **large job logs, execution artifacts, and input/output files**.  
🔹 Used for **batch processing jobs**.

### **S3 Bucket Structure**

```
/job-logs/
  ├── job_12345/
      ├── execution_1.log
      ├── execution_2.log
  ├── job_67890/
      ├── execution_1.log
```

## **5️⃣ Time-Series Database (Prometheus/TimescaleDB) → Job Metrics & Monitoring**

🔹 Stores **execution time, job success rate, worker health metrics**.  
🔹 Optimized for **time-series data**.

### **Schema for Prometheus Metrics**

#### **Job Execution Duration**

```
job_execution_duration_seconds{job_id="12345", status="COMPLETED"} 4.5
```

### **How to Ensure Jobs Are Not Duplicated in a Distributed Job Scheduler**

When running a distributed job scheduler with multiple worker nodes, job duplication can occur due to **network failures, retries, or concurrent processing**. Below are key strategies to **ensure exactly-once execution** or **idempotency** to prevent job duplication.

---

## **1️⃣ Deduplication Strategies**

### **1. Unique Job ID with Idempotency Check (Database or Cache)**

✅ **Ensure each job has a unique** `job_id` stored in a database or Redis.  
✅ **Before executing, check if the job has already been processed.**  
✅ If `job_id` exists with `status=COMPLETED`, reject reprocessing.

### **2. Distributed Locks (Redis/Zookeeper)**

✅ Use **Redis** `SETNX` **(Set if Not Exists) + Expiry** to lock jobs.  
✅ Ensures that only **one worker picks up a job** at a time.

### **3. Exactly-Once Processing Using Kafka (Message Queues)**

✅ If jobs are scheduled via Kafka, use **Kafka Consumer Groups**.  
✅ Kafka ensures **each partition is processed by only one consumer**.  
✅ Use **offset commits** to mark jobs as processed.

### **4. Transactional Job Updates in Database**

✅ Use **atomic transactions** in MySQL/PostgreSQL.  
✅ **Insert job execution record with a unique constraint on** `job_id`.  
✅ If **duplicate job submission occurs, the transaction fails**.

### **5. Leader Election (Zookeeper/Etcd)**

✅ Elect **one leader node** responsible for job assignment.  
✅ Leader **ensures no duplicate job allocation** to multiple workers.

📌 **Using Zookeeper for Leader Election:**

### **Fault-Tolerant Recovery Mechanisms for Failed Jobs**

Ensuring that failed jobs are retried correctly while **avoiding duplicates** and **maintaining consistency** is crucial in a **distributed job scheduler**. Below are **key strategies** for handling failures and ensuring fault tolerance.

## **1️⃣ Failure Handling & Recovery Strategies**

### **1. Job Status Tracking in Database**

✅ Store **job execution status** (`PENDING`, `RUNNING`, `FAILED`, `COMPLETED`).  
✅ Failed jobs are retried **only if their status is** `FAILED`.

📌 **Schema Example:**

```
CREATE TABLE job_executions (
    job_id UUID PRIMARY KEY,
    status ENUM('PENDING', 'RUNNING', 'FAILED', 'COMPLETED'),
    retry_count INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

📌 **Atomic Update on Failure:**

```
UPDATE job_executions 
SET status = 'FAILED', retry_count = retry_count + 1 
WHERE job_id = 'job_12345';
```

### **2. Retry Mechanism with Exponential Backoff**

✅ Instead of retrying **immediately**, use **delayed retries** with exponential backoff.  
✅ Helps avoid **overloading the system** with retries.

📌 **Retry Delays (Exponential Backoff Formula)**

```
Delay = min(initialDelay * (2 ^ retryCount), maxDelay)
```

### **3. Dead Letter Queue (DLQ) for Permanent Failures**

✅ If a job **fails after N retries**, move it to a **Dead Letter Queue (DLQ)**.  
✅ Prevents **stuck jobs from blocking new ones**.

📌 **Using Kafka DLQ**

- If a worker fails after 3 retries, push to DLQ:
    

### **4. Distributed Locks to Avoid Duplicate Retries**

✅ Before retrying, **check if another worker has already picked up the job**.  
✅ Use **Redis Locks** or **Zookeeper Locks**.

📌 **Redis Lock to Prevent Duplicate Retries:**

### **5. Worker Heartbeat & Failover Mechanism**

✅ **Workers send a heartbeat signal** every few seconds.  
✅ If a worker **crashes mid-job**, the job is reassigned.

📌 **Using Redis for Worker Heartbeat Check:**

### **6. Leader Election for Job Reassignment**

✅ If a worker crashes, the **leader node detects failure & reassigns jobs**.  
✅ Use **Zookeeper or Etcd** to elect a leader.

📌 **Zookeeper-Based Leader Election:**

### **7. Monitoring & Alerting for Failed Jobs**

✅ **Log all failures** and trigger alerts for failures beyond a threshold.  
✅ Use **Prometheus + Grafana** for monitoring job failures.


![[Pasted image 20250331094705.png]]
## **1. Requirements Discussion**

The first step in system design is to thoroughly understand the requirements. We started by discussing what types of tasks the scheduler needed to support. Key questions included:

- **Task Type**: Will the system handle periodic tasks (e.g., recurring jobs) or ad-hoc tasks (e.g., one-off executions)?
- **Resource Constraints**: What resources are required to execute a task? This includes runtime duration, network bandwidth, CPU consumption, etc.
- **Optimization Targets**: Which part of the system needs optimization? Should we focus on minimizing latency, maximizing throughput, or ensuring resource fairness across tasks?

This discussion laid the foundation for designing a system that could adapt to both simple and complex task requirements.

## 2. Scalability

Scalability is a crucial aspect of any modern system design, especially for something like a task scheduler that must handle a potentially massive and unpredictable workload.

**Parallel Task Processing with Message Queues**:  
One of the first ideas we discussed was using a **message queue** (e.g., Kafka, RabbitMQ, or AWS SQS) to decouple task production from task execution. By enqueueing tasks, the scheduler can distribute them across multiple worker nodes, enabling parallel processing and preventing bottlenecks.

**Handling Complex Tasks**:  
Another challenge arises when tasks vary in complexity. If a single task consumes disproportionate resources or takes too long to execute, it could block other tasks from running.

To address this, we explored solutions like:

- Using **priority queues** to prioritize smaller, faster tasks.
- **Sharding tasks by type** or resource requirements to ensure that complex tasks are isolated from simpler ones.
- ==Implementing== ==**dynamic worker scaling**== ==so that more workers can be spun up when a burst of heavy tasks is detected.==

## 3. Failure Tolerance

No system is perfect, so designing for failure tolerance is critical to ensure reliability. We discussed several strategies to handle task failures effectively:

**Failure Detection and User Notification**:  
When a task fails, the system should log the failure and notify the user promptly. This could be achieved through a combination of monitoring tools (e.g., Prometheus) and alerting systems (e.g., PagerDuty, Slack notifications).

**Task Retry Mechanism**:  
For transient failures (e.g., network issues or temporary resource unavailability), the scheduler should retry the task a configurable number of times. To avoid overloading the system, retries should follow an **exponential backoff** strategy.

**Handling Persistent Failures**:  
If a task continues to fail after multiple retries, the system needs a way to escalate or quarantine it. Potential solutions include:

- Providing detailed failure logs to help users diagnose the issue.
- Allowing users to reschedule or cancel failed tasks manually.

![[Pasted image 20250331095010.png]]

## **Functional Requirements**

1. **Periodic Content Fetching:** As we deliver real-time content to users, we collaborate with multiple news publishing partners who supply us with their content. They provide this content via [RSS](https://thebridge.in/custom_feeds.xml) feeds or APIs, which we need to fetch periodically to ensure we have the latest updates.
2. **Content Parsing:** The system should be capable of parsing and processing the fetched content, transforming it into a format suitable for real-time delivery.
3. **User-Friendly Onboarding UI:** A user-friendly UI platform is needed to enable product owners or non-technical personnel to onboard new publishing partners. This interface should simplify the process of adding new content sources in a few easy steps.
4. **Scheduling Flexibility:** The system should allow for flexible scheduling of content fetching intervals to accommodate different update frequencies of various publishing partners.

## **Non Functional Requirements**

1. **Scalability:** The system must be scalable to handle an increasing number of content sources and higher frequencies of content fetching as the number of publishing partners grows.
2. **Error Handling:** The system must handle errors gracefully, including issues with fetching or parsing content, and retry fetching content if initial attempts fail.
3. **Performance Monitoring:** The system should include performance monitoring capabilities to identify and address bottlenecks in content fetching and processing, ensuring efficiency and timeliness.
# Major Components of the System

## **Andromeda**

- Responsible for handling API requests, including publisher onboarding and job-related requests.
- Manages storage of parsing logic and publisher-related information.
- Maintains records of job history and job results.
- It uses Postgres as a data store.
- Whenever a job is created, updated, or deleted, Andromeda publishes an event to Kafka, which is then consumed by the scheduler.

## **Scheduler:**

- Responsible for scheduling and executing jobs.
- Utilizes core Redis features such as Sorted Set, Locking, Pub/Sub, and Redis Stream (Queue).

## Scheduler Components:

1. **Queues**: A queue is a pipeline for processing jobs. Each queue can have multiple jobs, which are processed by workers.
2. **Jobs**: Jobs are the individual tasks that need to be processed. Each job is an instance that contains a unique ID, data, and a set of options for its execution.
3. **Workers**: Workers are responsible for processing the jobs in a queue. They can be configured to process jobs concurrently, ensuring efficient use of resources.
4. **Delay Queue:** The Delay Queue utilizes Redis sorted sets as a key data structure, allowing elements to be added with a score. These scores enable the elements to be ordered, ensuring that jobs in the Delay Queue are stored in the precise order of execution.
5. **Delay Queue Worker:** A Polling Worker runs every second to check the sorted set for jobs ready for execution. Using the `ZRANGEBYSCORE queue:delayed 0 currentTimestamp` command, it retrieves all job IDs with a score (scheduled time) less than or equal to the current timestamp and moves these jobs to the Ready state. This Polling Worker operates independently of the Task Worker.

# The Beginning: Setting Up Queues and Workers

We started with the basics: setting up queues and attaching dedicated workers to execute tasks. Every queue required a worker, and each worker was responsible for processing tasks assigned to its queue. This simple setup laid the groundwork for our distributed job scheduler.

## **Managing Delayed Jobs**

Next, we tackled the challenge of managing delayed jobs. When a job was created, it was stored in a delayed job queue, using a sorted set ordered by execution time. This allowed us to keep track of when each job was due for execution. A polling worker, running every second, would check this sorted set for jobs that are ready to be moved to the ready state. The command `ZRANGEBYSCORE queue:delayed 0 currentTimestamp` retrieved all job IDs scheduled to be executed up to the current time, ensuring timely transitions.

## **Real-Time Notifications**

To ensure our workers were always aware of new jobs, we implemented a real-time notification system. Whenever a new job was added to the queue, Redis published a message to notify all subscribed workers. This enabled immediate awareness and response.

## **Efficient Job Fetching and Execution**

For job fetching and execution, we utilized Redis’ BLPOP command. This blocking operation allowed workers to wait for new jobs until one became available or a timeout occurred. When a worker received a notification, it woke up and attempted to fetch the job.

However, we faced a challenge: multiple workers might try to execute the same job simultaneously. To prevent this, we implemented a locking mechanism. When a worker picked up a job, it acquired a lock on that job, ensuring no other worker could process it at the same time. The lock had an expiry time, so if a worker went down, the job would become available again after the lock expired, ready to be picked up by another worker.

## **Managing Job States**

Our system maintained multiple job states: Delayed, Waiting, Ready, Completed, and Failed. To ensure atomic state transitions and prevent race conditions, we used Lua scripts. These scripts executed all operations as a single, indivisible unit, ensuring consistency and reliability.

## **Capturing Metrics and Notifications**

Whenever a job transitioned states, a notification was published. Workers could act accordingly, and we could capture valuable metrics. This included the number of running or failed jobs and the time taken by each job to execute. These insights allowed us to optimize performance and identify bottlenecks.

## **Robust Retry Mechanisms**

Handling job failures and retries was a crucial aspect of our system. We defined clear criteria for job failures, such as errors thrown by the job processor, or timeouts. When a job failed, the system checked if it had remaining retry attempts. If retries were available, the job was re-queued with updated metadata and moved back to the waiting list with an appropriate delay.

Our system supported automatic retries for failed jobs, which were configurable at the queue or job level. We implemented multiple retry strategies, including fixed delays, exponential backoffs, and custom backoff functions, allowing flexibility and robustness in handling retries.

## **The Power of Lua Scripts**

Using Lua scripts for state transitions proved invaluable. These scripts ensured atomicity, reducing the risk of race conditions in a multi-worker environment. They also minimized network latency by performing multiple operations in a single script, ensuring consistency and allowing transactional-like behavior.

# Breaking Down the Workflow: Dedicated Worker Queues

Our initial design processed tasks sequentially, but as the demand grew, this approach proved insufficient. We restructured our workflow by breaking down the entire process into discrete steps:

- **Fetching and Parsing XML:** A worker queue dedicated to fetching XML data from sources and parsing it according to predefined logic.
- **Content Creation:** Another worker queue focused on creating content based on the parsed XML and associated parsing logic.
- **Asset Upload:** A separate queue for handling the upload of assets such as images and videos.
- **Content Moderation:** A specialized queue for running content through a data science (DS) pipeline for moderation.

## **Sequential and Parallel Processing: Enhancing Scalability**

By assigning dedicated worker queues to each task, we could process steps both sequentially and in parallel. This design allowed us to:

- **Sequential Processing:** Ensure that tasks are processed in a logical order, with each step feeding into the next.
- **Parallel Processing:** Utilize multiple worker instances to handle tasks simultaneously within each step, significantly improving throughput and efficiency.

This approach enabled us to distribute the workload across multiple workers, reducing the time required to complete the entire workflow and preventing any single worker from becoming a bottleneck.

## **Fault Tolerance: Efficient Error Handling and Retrying**

A key advantage of our design was improved fault tolerance. If a task failed at any step, the system could retry from the point of failure rather than rerunning the entire workflow.

This targeted retry mechanism significantly enhanced the efficiency and reliability of our system, reducing wasted resources and minimizing downtime.

![[Pasted image 20250331095135.png]]

For our system let’s presume that the given requirements are like this.

- User actions: **Create and delete jobs. Retrieve a list of jobs created by the user. View the execution history for any given job.**
- Job execution style: **The system should support both one-time execution, recurring style**
- ==Number of average estimated daily tasks executions:== ==**50 million tasks each day**==
- Task fail strategy: **The system should have the capability to support a _retry_ feature**
- Our system is configured to perform task executions **every minute**
**Optimal Database Selection**

In any well-designed system, a robust database schema is a crucial element. It directly can affect the overall performance and reliability of the system. Let’s overview and choose the appropriate database based on our requirements.

Retrieve Operations

- Given a `user_id`, retrieve all jobs created by that user
- Retrieve _all scheduled tasks that are scheduled to be executed right now_ **(by scheduling service**, operation**(3)** in the system-design-1 diagram)
- Retrieve **all** or the **latest execution** histories and their status related to a specific `job_id`

Modification Operations

- Allow users to _create_ or _delete_ their job schedules
- Update the _Job’s next execution timestamp_ by`job_id`
- Update task status (Scheduled, Completed, Failed)

As you can see we have both **read** and **write** operations. If you pay special attention we have we don’t have complex transactional operations, therefore we are not tightly coupled to use a relational database.

As we have mentioned above our estimated daily tasks to be executed are 50 million. If we would average system load **per minute** based on this formula (daily tasks)/(24*60) => 50 000 000/24*60 ≈ 34722 tasks/minute.

In addition to executing tasks at the scheduled time, we need to efficiently retrieve tasks that are currently scheduled to be executed. In our design we will choose **Cassandra**, as it is an open-source, distributed NoSQL database system designed to handle large amounts of data across multiple commodity servers, ensuring high availability and fault tolerance. If you are considering using cloud services also Amazon DynamoDB (AWS), and Bigtable (GCP) are recommended options for use. (p.s. I’ll introduce a well-structured schema in this post, providing the flexibility to work seamlessly with also relational databases like PostgreSQL and MySQL)
**Job table design**: When the user creates a job in our platform, we need a table that stores the user’s job and job-related metadata, like retry-interval, recurring, max-retry count and etc. (you can extend these metadata based on your system need) we will store in that table. Remember Cassandra is a NoSQL database and does not support traditional SQL-style joins. The data in a table should in a denormalized format. For this reason, we will keep our data denormalized format in our table.

As each user will retrieve all their jobs using their `user_id`, it would be beneficial to **partition the table by** `user_id` to enhance data locality, optimize query performance, and streamline the retrieval of job information specific to individual users. In each partition, utilize the `job_id` as a **sorted key** for efficient organization and retrieval of job-related data..

**Task_Schedule** _table design:_ In the above, we designed a **job** table and we mentioned the job execution interval there. For example, _job_ with id-_123456_ is scheduled to execute every 3 hours (PT3H- means **P**eriod **T**ime **3 Hours**). But we need another table to store the next execution time for each job. By doing this it will be easy for us to query all scheduled tasks for the current minute(as we execute our tasks in each minute).

**Task_Execution_History** table design: We need one more table to store task’s execution whenever a scheduled task is executed. That table will also store the task’s status, retry count and etc. As a result, users will have the capability to access the execution history of any job. We will access the job’s execution history by `job_id` , therefore it is better to partition this table by `job_id` to be able to access all history for the same job in the same partition. Also, we will define `execution_time` as a sort key, to keep job history as sorted by execution time.
![[Pasted image 20250331100703.png]]

![[Pasted image 20250331100734.png]]

[[Dropbox - Cape]]