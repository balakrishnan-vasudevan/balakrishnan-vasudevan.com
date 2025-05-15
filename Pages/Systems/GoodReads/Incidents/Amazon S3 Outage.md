

Tags: #incident, #aws
Category: Articles
Company: Amazon
Status: Not started
URL: https://www.gremlin.com/blog/the-2017-amazon-s-3-outage

*Systems fail. Even Amazon breaks. Despite our best efforts, technology is never perfect. In this first post of a series, we look at the Amazon S3 outage of 2017 in a blameless way, seeking to learn from it things we can do to enhance the reliability of our own systems.*

*The bottom line is that Amazon S3 went down because of a typo. The company took specific action to update the tool to add safeguards and audited similar tools to ensure they had similar checks, made changes to systems for faster recovery. They also changed the AWS dashboard to run across multiple regions while communicating proactively in the interim with those impacted using alternative channels to get the word out.*

**Editor's note:** we have an excellent tutorial demonstrating [how to reproduce this outage using Scenarios](https://www.gremlin.com/community/tutorials/how-to-use-gremlin-scenarios-to-reproduce-the-aws-s-3-outage/), to test your system's reliability in the face of a similar occurrence.

On February 28, 2017 a problem occurred with Amazon’s Simple Storage Service (S3) in the US-EAST-1 region that took down a significant percentage of the internet for approximately four hours. The problem was so severe that for a while Amazon couldn’t even get into its own dashboard to warn users and instead [used Twitter to give updates](https://twitter.com/awscloud/status/836656664635846656). Making matters worse, it seemed that half of the internet was using S3 in the impacted region without multiple region failover schemes in place. A large number of significant websites were impacted.

We may not be Amazon, but we are still building systems in the cloud that can fail in unexpected ways. And those failures can impact our customers (and our engineering productivity). From their outage, we can learn a lot about how to prevent failure from impacting end users of our own systems; things like how to better scope config changes, restart services, and understand knock-off effects and bottlenecks.

This post illustrates how information from a retrospective (often called a postmortem) after a failure event can be used to help plan and test ways to mitigate against similar problems in the future.

*[ Related: [After the Retrospective: Heroku Incident #1892](https://www.gremlin.com/blog/heroku-incident-1892/) ]*

Here is a list of just some of the companies and services impacted, according to articles in [The Register](https://www.theregister.co.uk/2017/03/01/aws_s3_outage/) and [Venturebeat](https://venturebeat.com/2017/02/28/aws-is-investigating-s3-issues-affecting-quora-slack-trello/):

Adobe’s services, Amazon’s Twitch, Atlassian’s Bitbucket and HipChat, Autodesk Live and Cloud Rendering, Buffer, Business Insider, Carto, Chef, Citrix, Clarifai, Codecademy, Coindesk, Convo, Coursera, Cracked, Docker, Docker's Registry Hub, Elastic, Expedia, Expensify, FanDuel, FiftyThree, Flipboard, Flippa, Giphy, GitHub, GitLab, Google-owned Fabric, Greenhouse, Heroku, Home Chef, iFixit, IFTTT, Imgur, Ionic, isitdownrightnow.com, Jamf, JSTOR, Kickstarter, Lonely Planet, Mailchimp, Mapbox, Medium, Microsoft’s HockeyApp, the MIT Technology Review, MuckRock, New Relic, News Corp, OrderAhead, PagerDuty, Pantheon, Quora, Razer, Signal, Slack, Sprout Social, Square, StatusPage (which Atlassian recently acquired), Talkdesk, Travis CI, Trello, Twilio, Unbounce, the U.S. Securities and Exchange Commission (SEC), The Verge, Vermont Public Radio, VSCO, Wix, Xero, Yahoo! Mail, Zendesk, and numerous publications that stored images and other media in S3.

## What Really Happened with Amazon in February 2017?

It is to Amazon’s credit that after they found and fixed the problem, they not only held a proper retrospective after the Amazon outage in 2017, but they also [shared the details publicly](https://aws.amazon.com/message/41926/).

As in any good retrospective, all the ingredients are present. Amazon gives a clear high-level summary of what happened. They include an analysis of the contributing factors accompanied by a description of the steps taken to diagnose the issue, assess the damage, and resolve it. We are given a timeline of all related activities. Finally, they include a clear statement of lessons that were learned and next steps.

Let’s take the opportunity to learn from they shared to help all of us think about how to improve the reliability of our own systems.

While troubleshooting a problem with the S3 billing system, an Amazon operator ran a command to remove a small set of servers in US-EAST-1.

> Unfortunately, one of the inputs to the command was entered incorrectly and a larger set of servers was removed than intended.
> 

Some would call this typo the root cause of what ultimately impacted two other services in that region, the S3 index subsystem and the S3 placement subsystem. The index subsystem “manages the metadata and location information of all S3 objects in the region,” which is necessary necessary to serve all GET, LIST, PUT, and DELETE requests. The placement subsystem “manages allocation of new storage and requires the index subsystem to be functioning properly to correctly operate.”

The blast radius of this change was clearly too wide. We must think about the impact of our code and configuration changes and intentionally limit what we impact with each change. It may be worth questioning whether the operator was able to enter a command that took out more capacity than should have been allowed.

Volumes have been written about information technology risk management, including the risks related to hardware and software failure, human error, and malicious attacks. These often parallel the team structures and risk/severity levels that have been standardized and used for disaster incident management planning and response for decades by groups like [FEMA](https://www.fema.gov/pdf/emergency/nims/incident_mgmt.pdf).

Often commands that have the potential to affect production like this can be scripted in a more limited fashion. The code can then be reviewed by the reliability team with an eye toward keeping its potential impact as restricted as possible. Ultimately, we will allow only the ability to do what must be done, before being made available for use.

The only mechanism AWS had available to realize this was a broken process was for them to experience a disruptive, costly outage...unless perhaps another way could be found. Rather than waiting for a massive outage and a retrospective is held, many insights into a system can be proactively learned during a thoughtfully planned Chaos Engineering FireDrill or [GameDay](https://www.gremlin.com/community/tutorials/how-to-run-a-gameday/) to help us make our tools as fool proof as possible.

The lack of capacity resulting from the unintentionally larger set of servers being removed required both services to be restarted. As the retrospective states, “While this [removing and replacing capacity] is an operation that we have relied on to maintain our systems since the launch of S3, we have not completely restarted the index subsystem or the placement subsystem in our larger regions for many years.” The restarts took longer than expected.

Large systems are scary to restart, especially as uptime grows longer and longer and our experience doing so becomes less recent. In the case of this outage, it had been so long since a restart and the systems had changed so much over time, that time expectations were based on faulty premises.

One of the things we can do to prepare for an unexpected need to restart a system is to gather actual data about how long the process will take. There is no way to actually know how much time a process requires until we’ve run said process in the current environment. Causing a restart in a chaos experiment will give you that knowledge, which will in turn help you be prepared for future failure events. It will also help you think about and find ways to simplify and streamline the process to make future restarts more efficient and faster. It is also the only way you can set accurate expectations for customers as to either how long the restart will take, or when your service and its dependencies will be available again.

Even after those subsystems were restored to service, some other AWS services had a backlog of work due to S3 being unavailable and took additional time to recover. For example, the AWS Service Health Dashboard depended on assets stored on S3, and was hosted in the affected region, so it never could have functioned properly during an S3 outage in that region without changes. Those changes were made while the main issue was being worked on, but Amazon was still two hours into the four hour outage before the dashboard was again able to be updated.

These knock-on effects are notoriously hard to predict. They are, however, fairly easy to uncover with well-designed tests that show how the system behaves when part of it fails. It is useful to discover that another service can’t start or that it takes much longer to start when S3 is down, for example. Having this sort of information gives you better context as you update your [disaster recovery runbooks](https://www.gremlin.com/chaos-engineering/) and plan your automated failover schemes.

## How did Amazon Respond to the Details in Their Retrospective?

What did Amazon do after their retrospective? They took action to find and fix the problem.

Amazon tried to be proactive in communicating with everyone who was affected. Even though their usual means of communication (the dashboard) went down, they found an alternate method of communicating to get out word that work was in progress (Twitter) until they got the dashboard back up and running. It took time, but they did it.

Businesses who were affected also had problems communicating with their customers. While most also found an alternative means of communication, for a significant amount of time Twitter and various discussion venues were filled with “what’s going on” messages. Atlassian typically communicates about issues using their Statuspage blog, but [hosts most of their CSS and image files on S3](https://www.atlassian.com/blog/statuspage/a-birds-eye-view-of-the-amazon-s3-outage) so pages served either looked bad or were slow to load. [MailChimp used Twitter](https://twitter.com/MailChimpStatus/status/836681952342257665).

Amazon’s public document says they:

- Updated their tool to “remove capacity more slowly and added safeguards to prevent capacity from being removed when it will take any subsystem below its minimum required capacity level”
- Audited other operational tools to ensure they had similar checks
- Made changes to make the subsystems recover quicker, noting that they had planned to do this work on the index subsystem later in the year but reprioritized it and did the work sooner
- Changed the AWS Service Health Dashboard to run across multiple regions

Most of the non-Amazon companies impacted would have significantly reduced their downtime if they had multi-region failover in place. It was only one Amazon region that went down out of 16 total. While [the idea had been around for years](https://aws.amazon.com/about-aws/whats-new/2013/11/14/amazon-redshift-cross-region-backups/), it was not a focus for most of us.

For example, [PagerDuty learned from a 2012 outage](https://www.pagerduty.com/blog/aws-outage-june-29th-weathering-the-storm/) and had been proactive in separating the region on which they deployed their services from the region where most of their customers deployed theirs, but they were affected by this 2017 outage. As Robert Burns would say, “The best laid plans of mice and men often go awry.” We can’t foresee everything.

This outage awakened the industry to understand that creating redundancy across regions is vital for reliability. But in addition, as part of this redundancy, we want to create automated failover schemes in place to detect and reroute traffic to a different region the moment failure is detected in one region.

In addition, we now realize that engineers who work in the cloud should be encouraged to plan and prepare for the failure of third-party dependencies. It happens, but when we find ways to reduce or eliminate the impact to customers of the loss of those dependencies, we save a lot of heartache and money.

## How Can We Reproduce and Experiment with Gremlin to Help Prevent Outages?

How will our system respond if a similar failure with one of your external, third-party dependencies happens? Do we know, or do we just think we know? The only way to be certain is to test the system and see if it is reliable under similar failure conditions.

The best way to reproduce the S3 outage as part of a Chaos Engineering experiment with Gremlin is by running a [scenario](https://www.gremlin.com/docs/scenarios/overview/) involving a series of [Blackhole attacks](https://www.gremlin.com/docs/infrastructure-layer/attacks/), blocking access to S3 by AWS provider. The Blackhole attack is designed to drop all network traffic matching a set of criteria. It simulates the loss of any part of a system we designate, including testing what happens when an external dependency disappears. We can set up a scenario that begins with a small impact and small blast area, then have it grow larger to find the tipping point.

There is a pre-made ready-to-use recommended scenario called Unavailable Dependency in the Gremlin app that does exactly what we want.

Part of the experiment design process is defining an executable rollback or exit plan. Gremlin has that built in with our Halt Attack button.

Our first step is to check that our monitoring is [gathering some key metrics](https://www.gremlin.com/chaos-engineering/) that will be useful to us, such as error rate and latency. The data you collect will help you understand where your system is reacting with reliability and where it fails and these observations will guide your improvement efforts.

Next, we find the specific AWS provider that we are accessing and run a Blackhole attack against it. Watch how all the impacted parts of our system respond (or fail to compensate), how quickly or slowly, and look for any aspect we can improve.

## What is the Ultimate Takeaway for Us from the Amazon S3 Outage of 2017?

Failure happens in complex systems. Detecting and paging engineers to fight fires when failure happens is what we need in the moment but is not our best option for consistent, good reliability. We can plan for failure and prevent it from affecting our customers.

We can and should test and experiment on our systems to learn as much as possible now, creating small failures in a controlled way and using what we learn from those failures to design automated work-arounds, redundancy, fail-overs, and eliminate bottlenecks. We should focus on reliability and decrease the need for disaster recovery as much as we can. Our customers are counting on us.
