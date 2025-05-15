#sre, #production-readiness, #reliability 
Production Readiness Questions

  

These questions are not meant to be exhaustive.

  

- On which AWS account does this service reside?  Who are the admin users on this account?
    
- Who holds the pager for this service? Is there an on-call rotation? Who is the point of contact for the service?
    
- What is the expected availability? 
    
- Is there alerting set up for the critical path?  What is the critical path?  Who gets these alerts?
    
- Is there monitoring on individual service components, such as load balancers, ec2 instances, database instances, etc?  Who is responsible for acting on these?
    
- Does the service need a rollbar integration?  How are exceptions monitored?
    
- If the service relies on a 3rd-party, is there monitoring on the 3rd-party API endpoint?
    
- How is downtime of the service handled?  How does an outage affect customers?  Who needs to be notified when the service is unavailable? Is there a StatusPage template set up for this service? 
    
- Does a service outage affect APM request latency?  How tightly coupled is the service to APM?
    
- How critical is the data for the service? What is the backup and restore strategy?  Is this automated and monitored? Is there a runbook for this?
    
- In the case of an outage, will the data eventually become consistent? For example, Is there retry logic involved? Are retried requests idempotent?
    
- Is there any possibility that the data in service will be inconsistent with data in APM?  If so, how are these resolved?
    
- How are releases handled?  Are we okay with release downtime?  Do we need to coordinate releases with APM releases?
    
- APM vhost are unavailable during releases.  Does the service handle this?
    
- Do we need to handle AWS region-wide failure?  If so, what is the strategy?  Is there a runbook for this?
    
- How is security handled? Security groups, firewalls, ACL, EBS encryption, credentials, SSL certs, security patches?
    
- How do we do maintenance like SSH user access, AWS instance retirement, OS upgrade and patches, and software upgrades and patches? I.e Rails, Ruby, and Nginx/Passenger?
    
- What is the expected cost in terms AWS services and AppFolio human-hours?
    
- Does the service require the support of the Apple Team?
    
- Is there a runbook for this service?
    

  
  
  
**