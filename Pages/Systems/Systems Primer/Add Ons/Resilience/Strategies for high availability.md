
1. Replication
2. Load Balancing
3. Failover - This ensures seamless service by switching to a standby system when the primary system goes down. Often, this approach is called _active-passive_ approach and it ensures that the system is always available.
4. Autoscaling 
5. Rate limiting - Rate limiting based on Ip addresses or users ensures that the system cannot be abused by malicious users. This prevents Denial of Service instances and possibility of it happening. Ultimately, it ensures that the legitimate users are not impacted negatively.
6. [[Disaster Recovery]]
7. Loose coupling - Close or tight coupling among the components of a system is a sure recipe for a disaster. Designing for loosely coupled systems ensures that failure at one point, won’t affect the other components of the system.