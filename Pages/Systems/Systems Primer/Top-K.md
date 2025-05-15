![[Pasted image 20250501132836.png]]

### Functional Requirements

- **Real-time Data Processing:** Process incoming requests in real-time for up-to-date analytics.
- **Top-K Query Support:** Retrieve the top K requests based on criteria like frequency or response time.
- **Scalability:** Handle a large number of requests and scale horizontally with traffic increases.
- **Data Aggregation:** Aggregate data over various time windows for insights into request patterns.
- **User Access Control:** Implement role-based access to restrict data access and modifications.
- **Alerting and Notification:** Provide alerts for unusual patterns or threshold breaches.
- **API Access:** Offer a RESTful API for external systems to interact with the analysis system.

### Non-Functional Requirements

- **Performance:** Low latency in processing requests, ideally within milliseconds.
- **Reliability:** Target 99.9% uptime with minimal downtime.
- **Security:** Implement encryption for data in transit and at rest, with secure authentication.
- **Resilience:** Gracefully handle failures and recover without data loss.
- **Data Retention:** Define policies for data retention and purging to manage storage costs.
Traffic Estimation and Data Calculation
### Assumptions

- **Request Volume:** 10,000 requests/second during peak hours; 5,000 requests/second during off-peak hours.
- **Data Size per Request:** ~1 KB.
- **Retention Period:** Data retained for 30 days; aggregated data for 1 year.
- **Data Growth:** 10% annual increase in request volume.

### Write Flow

- **Incoming Requests:**Peak: 10 MB/second.
- Off-Peak: 5 MB/second.
- **Total Daily Data Ingestion:** 576 GB.
- **Monthly Data Ingestion:** 17.28 TB.

### Read Flow

- **Top-K Query Load:** 144,000 queries/day.
- **Total Data Retrieved Daily:** 1.44 GB.

### Data Storage

- **Real-Time Data Storage:** 518.4 TB for 30 days.
- **Aggregated Data Storage:** 20.736 TB/year.
- **Total Storage Requirement:** 539.136 TB.

### Summary

- **Peak Traffic:** 10 MB/second
- **Daily Ingestion:** 576 GB
- **Monthly Ingestion:** 17.28 TB
- **Daily Read:** 1.44 GB
- **Total Storage:** 539.136 TB
### API Endpoints

- **Endpoint:** `/api/v1/requests/top-k`
- **Method:** GET
- **Description:** Retrieve top K requests.
- **Request Parameters:**
- `k` (integer, required): Number of top requests.
- `metric` (string, required): Metric for ranking (e.g., `frequency`).
- **Response:**

{
  "status": "success",
  "data": [
    {
      "request_id": "12345",
      "metric_value": 1000
    }
  ]
}

- **Endpoint:** `/api/v1/requests/aggregate`
- **Method:** POST
- **Description:** Submit data aggregation request.
- **Request Body:**

{
  "start_time": "2023-10-01T00:00:00Z",
  "end_time": "2023-10-01T23:59:59Z",
  "metrics": ["frequency", "latency"]
}

- **Response:**

{
  "status": "success",
  "message": "Aggregation request submitted."
}

- **Endpoint:** `/api/v1/requests/alerts`
- **Method:** GET
- **Description:** Retrieve active alerts.
- **Request Parameters:**
- `severity` (string, optional): Filter by severity.
- **Response:**

{
  "status": "success",
  "alerts": [
    {
      "alert_id": "alert123",
      "description": "High error rate detected",
      "timestamp": "2023-10-01T12:00:00Z"
    }
  ]
}

- **Endpoint:** `/api/v1/requests/history`
- **Method:** GET
- **Description:** Retrieve historical data.
- **Request Parameters:**
- `start_date` (string, required): Start date.
- `end_date` (string, required): End date.
- **Response:**

{
  "status": "success",
  "data": [
    {
      "date": "2023-10-01",
      "total_requests": 1000000,
      "average_latency": 200
    }
  ]
}

### Database Type

- **Choice:** NoSQL Database (e.g., MongoDB, Cassandra)
- **Rationale:**
- Efficient high write throughput.
- Flexible schema for evolving data.
- Horizontal scalability for growing data volumes.
- Supports real-time data processing.

### Main Entities and Schema

- **Requests**
- `request_id` (String, PK): Unique request identifier.
- `timestamp` (DateTime): Request receipt time.
- `user_id` (String): User identifier.
- `endpoint` (String): Accessed API endpoint.
- `status_code` (Integer): Returned HTTP status code.
- **AggregatedData**
- `aggregation_id` (String, PK): Unique aggregation identifier.
- `start_time` (DateTime): Aggregation start time.
- `end_time` (DateTime): Aggregation end time.
- `metric_name` (String): Name of the aggregated metric.
- **Alerts**
- `alert_id` (String, PK): Unique alert identifier.
- `description` (String): Alert description.
- `severity` (String): Alert severity level.
- **Users**
- `user_id` (String, PK): Unique user identifier.
- `role` (String): User role (e.g., admin, viewer).

### Relationships

- Requests to Users: Many-to-One
- AggregatedData to Requests: One-to-Many
- Alerts to Requests: Many-to-Many

### Performance Optimizations

- **Indexing:** Create indexes on `timestamp`, `user_id`, and `endpoint`.
- **Sharding:** Implement sharding based on `request_id` or `timestamp`.
- **Caching:** Use an in-memory cache (e.g., Redis) for frequently accessed data.

### Key Components

- **Load Balancer:** Distributes requests across application servers for high availability.
- **API Gateway:** Acts as a single entry point for client requests, managing authentication and routing.
- **Application Servers:** Hosts core logic, processes requests, and interacts with the database.
- **NoSQL Database:** Stores raw data and metrics with high write throughput.
- **In-Memory Cache:** Caches frequently accessed data to enhance response times.
- **Alerting System:** Monitors patterns and triggers notifications based on thresholds.

### End-to-End Request Flow

- **Step 1:** Incoming Request - A client request is received by the Load Balancer.
- **Step 2:** API Gateway - The request is routed through the API Gateway for authentication.
- **Step 3:** Application Server - The request is processed by an Application Server.
- **Step 4:** Real-Time Processing - Updates metrics and checks alert conditions.
- **Step 5:** Data Storage - Raw data and metrics are stored in the NoSQL Database.
- **Step 6:** Caching - Frequently accessed data is cached for quick retrieval.
- **Step 7:** Alerting - Notifications are sent if alert conditions are met.

### Real-Time Processing Engine

- **Rationale:** Processes high volumes of requests and updates metrics in real-time, enabling anomaly detection and alerts.
- **Design Considerations:**
- **Framework:** Use Apache Kafka and Apache Flink.
- **Scalability:** Deploy multiple processing nodes.
- **Fault Tolerance:** Implement checkpointing and state recovery.
- **Latency:** Optimize processing pipelines for minimal latency.

### API Gateway

- **Rationale:** Centralizes request handling, manages security, and ensures fair usage.
- **Design Considerations:**
- **Security:** Use OAuth 2.0 and JWT tokens.
- **Rate Limiting:** Implement token bucket algorithms.
- **Extensibility:** Design for plugins or middleware.

### NoSQL Database

- **Rationale:** Supports high write throughput and flexible schema for diverse request data.
- **Design Considerations:**
- **Data Partitioning:** Use sharding based on `timestamp` or `request_id`.
- **Consistency vs. Availability:** Opt for eventual consistency.

### Alerting System

- **Rationale:** Notifies stakeholders of anomalies in real-time for proactive monitoring.
- **Design Considerations:**
- **Threshold Configuration:** Allow dynamic alert thresholds.
- **Notification Channels:** Support email, SMS, and Slack.
- **Integration:** Integrate with monitoring tools for visibility.

### 1. Database Choice: NoSQL vs. SQL

- **NoSQL:**
- **Pros:** High write throughput, flexible schema, and horizontal scalability.
- **Cons:** Eventual consistency may cause stale reads; complex queries can be less efficient.
- **SQL:**
- **Pros:** Strong consistency, robust transaction support.
- **Cons:** Vertical scaling limits and schema rigidity.

**Final Choice:** NoSQL was selected for its scalability and high write capacity, suitable for real-time processing.

### 2. Real-Time Processing: Batch vs. Stream Processing

- **Stream Processing:**
- **Pros:** Real-time insights and efficient continuous data handling.
- **Cons:** Complexity in state management and higher resource use.
- **Batch Processing:**
- **Pros:** Simpler implementation and efficient for large data volumes.
- **Cons:** Delayed insights; not suitable for real-time needs.

**Final Choice:** Stream processing was chosen for real-time updates and alerting, despite its complexity.

### 3. API Gateway: Monolithic vs. Microservices

- **Monolithic:**
- **Pros:** Simpler development and management.
- **Cons:** Limited scalability and a single point of failure.
- **Microservices:**
- **Pros:** Independent scaling and enhanced fault isolation.
- **Cons:** Increased complexity and need for robust orchestration.

**Final Choice:** Microservices architecture was chosen for its scalability and flexibility.

### 4. Alerting System: Manual vs. Automated Thresholds

- **Manual Thresholds:**
- **Pros:** Simple setup and direct control.
- **Cons:** Requires constant tuning; may not adapt well.
- **Automated Thresholds:**
- **Pros:** Adapts to patterns using machine learning; reduces manual effort.
- **Cons:** Complexity in maintenance; potential for false alerts.

**Final Choice:** Automated thresholds were selected to reduce manual intervention and adapt to dynamic patterns.

### Server Failures

- **Potential Failure Points:**
- Application server crashes due to overload.
- Database server failures causing data inaccessibility.
- **Strategies for Handling Failures:**
- **Redundancy:** Deploy multiple server instances across availability zones.
- **Load Balancing:** Distribute traffic evenly and reroute requests to healthy servers.
- **Health Checks:** Monitor server health and replace unhealthy instances automatically.

### Network Issues

- **Potential Failure Points:**
- Network congestion or outages affecting data flow.
- **Strategies for Handling Failures:**
- **Multi-Region Deployment:** Ensure connectivity across regions.
- **CDN Usage:** Cache data closer to users to reduce latency.

### Data Loss or Corruption

- **Potential Failure Points:**
- Data corruption during writes or hardware failures.
- **Strategies for Handling Failures:**
- **Data Backups:** Regularly back up and verify data integrity.
- **Replication:** Maintain data copies across multiple nodes.

### Real-Time Processing Delays

- **Potential Failure Points:**
- Processing bottlenecks causing delays.
- **Strategies for Handling Failures:**
- **Stream Partitioning:** Distribute processing load across nodes.
- **Monitoring and Alerts:** Detect delays and trigger alerts for action.

### Alerting System Failures

- **Potential Failure Points:**
- Delayed or missed alerts due to overload.
- **Strategies for Handling Failures:**
- **Redundant Alert Channels:** Use multiple channels for alert delivery.
- **Alert Testing:** Regularly test configurations for accuracy.