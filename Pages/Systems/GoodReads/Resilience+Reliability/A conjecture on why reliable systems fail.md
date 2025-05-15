

Tags: #reliability, #incident 
Category: Articles
Company: general
Status: Not started
URL: https://surfingcomplexity.blog/2017/06/24/a-conjecture-on-why-reliable-systems-fail/

*(Some of my co-workers call this [Lorin’s Law](https://twitter.com/theckman/status/1185233751028060161))*

Even highly reliable systems go down occasionally. After having read over the details of several incidents, I’ve started to notice a pattern, which has led me to the following conjecture:

Once a system reaches a certain level of reliability, most major incidents will involve:

- A manual intervention that was intended to mitigate a minor incident, *or*
- Unexpected behavior of a subsystem *whose primary purpose was to improve reliability*

Here are three examples from Amazon’s post-mortem write-ups of major AWS outages:

The [S3 outage](https://aws.amazon.com/message/41926/) on February 28, 2017 involved a *manual intervention* to debug an issue that was causing the S3 billing system to progress more slowly than expected.

The [DynamoDB outage](https://aws.amazon.com/message/5467D2/) on September 20, 2015 (which also affected SQS, auto scaling, and CloudWatch) involved healthy storage servers taking themselves out of service by executing a distributed protocol that was (presumably) designed that way *for fault tolerance*.

The [EBS outage](https://aws.amazon.com/message/680342/) on October 22, 2012 (which also affected EC2, RDS, and ELBs) involved a memory leak bug in an agent that *monitors the health of EBS servers*.