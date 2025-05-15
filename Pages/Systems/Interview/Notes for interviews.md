
[[Cheatsheet]]
[[Cheat Sheet for Systems Design]]
[[Concepts]]
[[Components Primer]]
[[Tips]]
[[Trade Offs]]


![[Pasted image 20250430110924.png]]

Playbook:
- **5 min:** Functional Requirements
- **5 min:** Non-Functional Requirements
- **3 min:** API Design
- **5 min:** Identify Key Components
- **10 min:** High-Level Design Diagram
- **Remaining Time (~25 min):** Deep Dive on Data Models, Caching, Partitioning, and Scaling

## Step 1: Functional Requirements

- **Identify Key Use Cases**: List the top 5 core requirements to cover the main functionalities.
- **State Assumptions**: Clarify any assumptions to address uncertainties or ambiguous requirements.
- **Verify Scope**: Confirm scope with the interviewer to ensure alignment on features and constraints.

## **Step 2: Non-Functional Requirements**

Quantifying non-functional requirements is critical for setting clear expectations and guiding design decisions. Here’s how to define these requirements effectively:

1. **Resource Estimation**: Estimating system capacity in terms of users, storage, and traffic.

- **Users**: Define total users and active users. Example: 200M users, 100M active.
- **Storage Needs**: Estimate daily data generation and retention. Example: 1 TB/day, 1-year retention = 365 TB.
- **QPS**: Calculate average and peak QPS. Example: Avg QPS 10,000, Peak QPS 30,000.

**2. Availability**:The ability of the system to remain operational and accessible.Aim for 99.9% availability with redundancy, failover, and multi-region deployments. Example: ~8.77 hours downtime/year.

**3. Consistency**: Ensuring data accuracy and correctness across the system. Specify consistency models. Example: Strong consistency for critical transactions, eventual consistency for feeds with <1 sec delay.

**4. Availability vs Consistency**:Trade-off between ensuring data accuracy (consistency) and system uptime (availability). Choose availability over consistency when user access is critical, even if data is slightly outdated.

**5. Scalability**: The ability of a system to handle increased load by adding resources. Plan for horizontal scaling. Example: Design for 100K QPS with load balancers and sharding to support growth without performance loss.

**6. Latency**: The time taken by the system to respond to user actions. Define response time targets. Example: Read < 50ms, Write < 100ms, User actions < 1 sec. Use caching and optimized queries to achieve targets.

**7. Reliability**:The system’s ability to operate without failure over a specified period. Ensure reliability with redundancy, error detection, and failover strategies. Example: Handle 2 node failures without service interruption.

**8. Security**: Measures to protect the system from unauthorized access or attacks. Encrypt data at rest and in transit, enforce authentication. Example: AES-256, TLS 1.3, bi-weekly vulnerability scans.

**9. Observability**:The ability to understand the internal state of a system through its outputs. Use metrics, logging, and tracing. Example: Error rate < 0.01%, P99 latency < 100ms, real-time monitoring dashboards.

## **Step 3: API Design (5 min)**
Outline the essential APIs to support each feature.

1. **Identify Core APIs**:

- Define endpoints for each primary functionality, specifying their purpose and actions (e.g., `/users` for managing user data, `/orders` for order operations).
- Use consistent and intuitive naming conventions for endpoints, organized hierarchically when necessary.

**2. Request & Response Schema**:

- Clearly detail required and optional parameters for each endpoint.
- Define response structures, including success and error payloads, ensuring they are comprehensive and consistent across APIs.
- Use widely adopted formats like **JSON** or **Protocol Buffers** for seamless integration and readability.

**3. Protocol and Communication**:

- Use **HTTP/HTTPS** for REST APIs with standard HTTP methods (GET, POST, PUT, DELETE).
- For high-performance or low-latency requirements, consider **gRPC**, which offers efficient communication and type-safe interfaces.

## **Step 4: Identify Key Components of the System (10 min)**

Identify the major components specific to the system’s core functionality and requirements. This list will adapt based on the use case.

**Example for Google Drive-like System:**  
— **Chunker**: Splits large files into manageable parts, enabling distributed storage and retrieval.  
— **Indexer**: Manages file metadata and indexing to enable efficient search and retrieval.  
— **File Storage Handler**: Interfaces with storage services (e.g., S3 or HDFS) to store, retrieve, and manage file chunks.  
— **Metadata Store**: Maintains structured data such as file details, directory hierarchy, and access permissions.  
— **Watcher**: Monitors changes to files, supporting real-time collaboration and synchronization across devices.  
— **Version Control Manager**: Manages file versions, enabling users to access and restore previous versions if needed.

## **Step 5: Design Diagram and High-Level Architecture (10 min)**
In this step, create a high-level architecture diagram that includes both foundational infrastructure and system-specific components. This diagram will show how data flows through the system and how each component interacts.

**Checklist for Core Infrastructure Components:**

Evaluate each for relevance to the design:

1. **Load Balancer :** Distributes incoming traffic across multiple servers to improve availability and balance resource usage.
2. **Message Queue:** Enables asynchronous processing for non-immediate tasks (e.g., Kafka, RabbitMQ).
3. **Coordination Service** (e.g., ZooKeeper): Manages distributed coordination, such as leader election and configuration consistency.
4. **Storage (Database/File Storage):**  
    — **Database:** Choose SQL for relational data or NoSQL for flexibility with unstructured data.  
    — **File/Blob Storage**: For storing large or unstructured files (e.g., S3, HDFS).
5. **Caching:** Reduces latency for frequently accessed data (e.g., Redis, Memcached).
6. **Content Delivery Network (CDN)**: Speeds up content delivery by caching static content close to end users.
7. **Monitoring and Logging Tools**: Services like Prometheus, Grafana, or ELK stack to ensure observability and operational insights.

## Step 6: Deep Dive into Workflows, Data Models, Caching, Partitioning, and Scaling

1. **Workflows:** Illustrate how components interact to fulfill core functional requirements.

- Example for file upload in a Google Drive-like system:**Client uploads a file** to the system via the API Gateway.The **Chunker** splits the file and stores metadata in the **Metadata Store**.The **File Storage Handler** saves chunks in distributed storage.The **Watcher** notifies devices about changes or availability updates.

**2. Data Model:** Sketch out key tables or collections based on system needs, such as User, Document, FileChunk, and AccessControl.

**3. Partitioning Strategy:** Discuss sharding or partitioning based on access patterns and scale requirements (e.g., by user ID or document ID).

4. **Caching Strategy:**Implement caching for frequently accessed data. Use Redis or Memcached and define eviction policies based on data access patterns.

**5. Scaling Considerations:** Describe how components can scale independently to handle increased load. For instance, add nodes for storage or replicas for databases as the user base grows.