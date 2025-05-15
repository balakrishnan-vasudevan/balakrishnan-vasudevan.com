**Table of Contents**

- [RED Method](#RED%20Method)
- [USE Method](#USE%20Method)
- [READS](#READS)


# RED Method

The **RED Method** was created by Tom Wilkie, from Weaveworks. It is heavily inspired by the Golden Signals and it’s focused on microservices architectures.

RED stands for:

- Rate
- Error
- Duration

**Rate** measures the number of requests per second (equivalent to Traffic in the Golden Signals).

**Error** measures the number of failed requests (similar to the one in Golden Signals).

**Duration** measures the amount of time to process a request (similar to Latency in Golden Signals).

# USE Method

The **USE Method** was created by Brendan Gregg and it’s used to measure infrastructure.

USE stands for:

- Utilization
- Saturation
- Errors

That means for every resource in your system (CPU, disk, etc.), you need to check the three elements above.

**Utilization** is defined as the percentage of usage for that resource.

**Saturation** is defined as the queue for requests in the system.

**Errors** is defined as the number of errors happening in the system.

While it may not be intuitive, Saturation in Golden Signals is not similar to the Saturation in USE, but rather Utilization.

![Golden Signals vs Red vs Use](https://sysdig.com/wp-content/uploads/GoldenSignals-05-1170x439.png)



# READS
Salesforce 
- Request (rate/min)
- Errors (5xx errors)
- Availability (% of time that service is up)
- Duration - p95 latency
- Saturation - How full the service is 