Source: https://froehlich.medium.com/service-level-objectives-sli-slo-sla-explained-simply-fb4b91dd4a07

**Table of Contents**

- [SLI](#SLI)
- [SLO](#SLO)
- [SLA](#SLA)
- [Error Budget](#Error%20Budget)

Order:
SLA
SLO
SLI

# SLI

**what are we going to measure?** To summarize it in one word, **metrics**.
	- **Response time** _(the amount of time it takes between sending a request and getting a response)_
	- **Throughput** _(max number of requests the system needs to handle)_
	- **Error rate** _(ration of failed requests to successful requests)
	-  availability, or the fraction of the time that a service is usable.
a carefully defined quantitative measure of some aspect of the level of service that is provided. 

- _User-facing serving systems_, such as the Shakespeare search frontends, generally care about _availability_, _latency_, and _throughput_. In other words: Could we respond to the request? How long did it take to respond? How many requests could be handled?
- _Storage systems_ often emphasize _latency_, _availability_, and _durability_. In other words: How long does it take to read or write data? Can we access the data on demand? Is the data still there when we need it? See [Data Integrity: What You Read Is What You Wrote](https://sre.google/sre-book/data-integrity/) for an extended discussion of these issues.
- _Big data systems_, such as data processing pipelines, tend to care about _throughput_ and _end-to-end latency_. In other words: How much data is being processed? How long does it take the data to progress from ingestion to completion? (Some pipelines may also have targets for latency on individual processing stages.)
- All systems should care about _correctness_: was the right answer returned, the right data retrieved, the right analysis done? Correctness is important to track as an indicator of system health, even though it’s often a property of the data in the system rather than the infrastructure _per se_, and so usually not an SRE responsibility to meet.

Using percentiles for indicators allows you to consider the shape of the distribution and its differing attributes: a high-order percentile, such as the 99th or 99.9th, shows you a plausible worst-case value, while using the 50th percentile (also known as the median) emphasizes the typical case. The higher the variance in response times, the more the typical user experience is affected by long-tail behavior, an effect exacerbated at high load by queuing effects. User studies have shown that people typically prefer a slightly slower system to one with high variance in response time, so some SRE teams focus only on high percentile values, on the grounds that if the 99.9th percentile behavior is good, then the typical experience is certainly going to be.
Google SREs recommend that you standardize on common definitions for SLIs so that you don’t have to reason about them from first principles each time. Any feature that conforms to the standard definition templates can be omitted from the specification of an individual SLI, e.g.:

- Aggregation intervals: “Averaged over 1 minute”
- Aggregation regions: “All the tasks in a cluster”
- How frequently measurements are made: “Every 10 seconds”
- Which requests are included: “HTTP GETs from black-box monitoring jobs”
- How the data is acquired: “Through our monitoring, measured at the server”
- Data-access latency: “Time to last byte”
# SLO

**what values of SLIs matter?** To summarize it in one phrase, **SLI + thresholds**.
a target value or range of values for a service level that is measured by an SLI. A natural structure for SLOs is thus _SLI ≤ target_, or _lower bound ≤ SLI ≤ upper bound_.

| SLO Metric                           | Threshold  | Interpretation                                                              |     |
| ------------------------------------ | ---------- | --------------------------------------------------------------------------- | --- |
| Availability                         | 99.9%      | The service will be down for no more than 1 hr/month                        |     |
| Error Rate                           | < 1%       | Averaged over a period of time, error rate for service will be less than 1% |     |
| Throughput                           | 10,000 RPS | Service can handle 10,000 rps while maintaining other SLO thresholds        |     |
| Response Time <br> (50th percentile) | 10ms       | Service will have 50th percentile response time <= 10ms                     |     |
| Response Time <br> (95th percentile) | 100ms      | Service will have 95th percentile response time <= 100ms                    |     |

Choose just enough SLOs to provide good coverage of your system’s attributes. Defend the SLOs you pick: if you can’t ever win a conversation about priorities by quoting a particular SLO, it’s probably not worth having that SLO. However, not all product attributes are amenable to SLOs: it’s hard to specify "user delight" with an SLO.
# SLA

**what happens if we don’t stay within the thresholds of the SLOs?** In other words what happens if we don’t live up to the bar set by our SLOs? To summarize it in one phrase **SLO + consequences**.
an explicit or implicit contract with your users that includes consequences of meeting (or missing) the SLOs they contain. The consequences are most easily recognized when they are financial—a rebate or a penalty—but they can take other forms.

# Error Budget

an error budget serves as a data point for deciding when to accelerate innovation or implement freezes. When a company exceeds its error budget, SRE teams can pause innovation to eliminate persistent causes of errors from the system.
Error budgets can be measured in relation to availability or uptime, both of which are defined by a company’s Service Level Objective (SLO). In other words, an error budget is 1 minus the SLO of the service. A 99.9% SLO service has a 0.1% error budget.
As part of operationalizing SLOs, SRE teams translate SLI percentages in terms of days and hours for software engineers. Service-level indicators (SLIs) are the measures that indicate if an SLO is met or not. The SLI ranges from 0% to 100%, where 0% means nothing works, and 100% means nothing is broken.