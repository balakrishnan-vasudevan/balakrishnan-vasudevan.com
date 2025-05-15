Source:https://sirupsen.com/metrics#user-content-fnref-web-utilization

_† Metrics where you **need** the ability to slice by `endpoint` or `job`, `tenant_id`, `app_id`, `worker_id`, `zone`, `hostname`, and `queue` (for jobs). This is paramount to be able to figure out if it’s a single endpoint, tenant, or app that’s causing problems.
- **Web Backend (e.g. Django, Node, Rails, Go, ..)**
    - Response Time `p50`, `p90`, `p99`, `sum`, `avg` †
    - Throughput by HTTP status †
    - Worker Utilization (This is one of my favorites. What percentage of threads are currently busy? If this is `>80%`, you will start to see counter-intuitive queuing theory take hold, yielding strange response time patterns.  It is given as `busy_threads / total_threads`)
    - Request Queuing Time (How long are requests spending in TCP/proxy queues before being picked up by a thread? Typically you get this by your load-balancer stamping the request with a `X-Request-Start` header, then subtracting that from the current time in the worker thread.)
    - Service calls †
        - Database(s), caches, internal services, third-party APIs, ..
        - Enqueued jobs are important!
        - [Circuit Breaker tripping](https://sirupsen.com/napkin/problem-11-circuit-breakers) † `/min`
        - Errors, throughput, latency `p50`, `p90`, `p99`
    - Throttling †
    - Cache hits and misses `%` †
    - CPU and Memory Utilization
    - Exception counts † `/min`
- **Job Backend (e.g. Sidekiq, Celery, Bull, ..)**
    - Job Execution Time `p50`, `p90`, `p99`, `sum`, `avg` †
    - Throughput by Job Status `{error, success, retry}` †
    - Worker Utilization (Same idea as web utilization, but in this case it’s OK for it to be > 80% for periods of time as jobs are by design allowed to be in the queue for a while. The central metric for jobs becomes time in queue.)
    - **Time in Queue** † (The central metric for monitoring a job stack is to know how long jobs spend in the queue. That will be what you can use to answer questions such as: Do I need more workers? When will I recover? What’s the experience for my users right now?)
    - **Queue Sizes** † (How large is your queue right now? It’s especially amazing to be able to slice this by job and queue, but your canonical logs with how much has been enqueued is typically sufficient.)
        - Don’t forget scheduled jobs and retries!
    - Service calls `p50`, `p90`, `p99`, `count`, `by type` †
    - Throttling †
    - CPU and Memory Utilization
    - Exception counts † `/min`


