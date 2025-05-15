#observability , #logging-infra

Source: https://blog.twitter.com/engineering/en_us/topics/infrastructure/2021/logging-at-twitter-updated
### Recall

1. Modular inputs are not resilient - WTF does this mean?
2. What is Scribe?
3. What is the equivalent architecture for logging at CRM? CRM also uses Splunk.

Notes
- Twitter previously used Loglens, it had poor ingestion capacity and limited query capabilities.
- They later migrated to Splunk Enterprise.
- Loglens goals:
    - Ease of onboarding
    - Low cost
    - Very little time investment from developers for ongoing maintenance and improvements
- Logs were written to local Scribe daemons, forwarded onto Kafka, and then ingested into the Loglens indexing system.

![[Pasted image 20231110101847.png]]


- Only around 10% of the logs are submitted, with the remaining 90% discarded by the rate limiter.
- Installed the Splunk Universal Forwarder on each server in the fleet, including on some new dedicated servers running rsyslog to relay logs from network equipment to the universal forwarder.
- Migrating the existing application logs from Loglens to Splunk enterprise - create a new service called “Application Log Forwarder” to subscribe to the Kafka topic that was already in use for Loglens and then forward those logs to Splunk.
- ALF: Reads events from Kafka, submits them to Splunk using HTTP event collector, and has basic rate limiting based on the service name and log level.
- New pipeline:
![[Pasted image 20231110101920.png]]
- The new topology includes stamping a mostly independent cluster of indexers, search heads, deployers, and cluster managers in each of our primary data centers to ingest and index the logs from servers and services in that datacenter. The only interactions between the per-datacenter clusters is between the indexers and the license manager running on one of the deployers and the search head clusters configured to search all indexer clusters.
    
- Issues:
    
    - managing configuration - Tools like puppet and chef are not able to help with managing indexes and access control. When we managed indexes and their access policies with Puppet, the whole process was ultimately limited by the following:
        
        - Using source control as the source of truth
        - The policies of reviewing and testing changes on the source control repository
        
        This needed the engineer’s involvement. The solution we landed on was to create a new service that generates the _indexes.conf_ and _authentication.conf_ files and deploys them to the correct servers. This service presents an API with role-based access control to the rest of the network, letting us integrate index creation with existing provisioning tools.
        
    - Modular inputs are not resilient
        
    - Control of the flow of data is limited - While it is less common in our environment, the Universal Forwarders running across the fleet sometimes also begin forwarding enough log volume to threaten the stability of the cluster. However, the Universal Forwarder lacks the flexibility to throttle or discard events. If a service misbehaves and floods the system with enough logging events that the stability of our Splunk Enterprise clusters is threatened, we can discard events by log level or originating service.
        
    - Server maintenance in large clusters is complicated - While OS updates are applied live, firmware updates or kernel patches require a reboot. This presents a problem primarily for the indexers, as the search heads are less stateful and the cluster manager can be brought down briefly without impacting the indexer clusters or the search head clusters. Process:
        
        - Enable maintenance mode
        - Temporarily offline a small percentage of indexers
        - Reboot the offline indexers
        - Bring them back online
        - Wait for the missing buckets and pending bucket fixup metrics on the cluster manager to stabilize before moving on to the next batch
    
    Future work includes using existing work scheduling and automation services at Twitter to drive these tasks in an intelligent way.
    

<aside> 📌 **SUMMARY: Don’t waste time building your own logging platform.**

</aside>


[[Logging at Twitter Updated]]