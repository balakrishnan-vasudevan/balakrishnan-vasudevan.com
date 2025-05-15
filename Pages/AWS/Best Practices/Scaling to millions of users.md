Source: https://www.youtube.com/watch?v=yrP3M4_13QM

Managed compute 
	AWS Lambda
	Fargate
	ECS/EKS
	EC2
Exposing business logic to frontend
	Amazon API GW
	Application Load Balancer (L7 proxy)
	AWS AppSync (to host APIs)
AWS App Runner 
	Puts together a full stack to build, deploy, and run containerized web applications
	3 components:
		Public endpoint
		Internet facing LB
		L7 request router
When to use NoSQL?
	1. Super low-latency applications
	2. Metadata-driven datasets
	3. Highly non-relational data
	4. Need schema-less data constructs
	5. Rapid ingestion of data
	6. Massive amounts of data
Observability
	Cloudwatch - Dashboards, Logs, Metrics, Alarms, Events, Real user Monitoring (RUM)
	X Ray - Traces, Analytics, Service map
ML-assisted DevOps
	DevOps Guru - detect unusual behavior, analyze performance, drive correction
	CodeGuru - Analyze application code for common issues, performance and cost improvements
Areas to tune:
	1. Slow DB queries
	2. Slow API requests
	3. Failures due to increased traffic
	4. Service-to-service communication
ElastiCache - managed memcached or redis
	Multi-AZ deployments available
Scaling the data tier:
	1. Increase the size of the instances used
	2. Add read replicas and a proxy to help scale read queries
	3. Use caches to remove queries from even needing to be made.
Break up the Backend:
	Split application into new federated services aligned to data patterns.
DB Federation:
	Split up DBs by function/purpose
	Harder to do cross-function queries
	Delays sharding/No-SQL
	Won;t help with single huge queries or tables with incredible amounts of data.
Users > 10 million
	Use distribution of features/functionality across internal microservices
	Use CodeGuru to analyze stack performance and find areas to improve
	Start to build on self-managed compute
	Evaluate how to improve caching at all tiers.
	
	
	
	
![[Screenshot 2023-11-07 at 3.31.12 PM.png]]