# Trusting Metrics at Pinterest

Tags: observability
Category: Articles
Company: Pintrest
Status: Complete
URL: https://medium.com/pinterest-engineering/trusting-metrics-at-pinterest-ed76307e10a0

For those who haven’t thought about metrics, this may seem like an odd problem. Something like Daily Active Users (DAU) may sound simple to measure, but here are some examples of how such a simple metric may go wrong:

- An extension version of the app could decide to keep auth tokens fresh; they could auto login the users every day, regardless of if the user actually used the extension.
- A user being active across midnight may count as an active user on both days for one platform, but not for another platform.
- Non-qualifying activity such as using a browser extension could be counted as DAU.

![Screenshot 2024-10-19 at 4.46.04 PM.png](Screenshot_2024-10-19_at_4.46.04_PM.png)

Step 1:

We create two documents for every certified metric. A **product spec,** which gives a clear definition (such as an active user):

- Visits the Pinterest website or native mobile apps
- Pins or repins using an offsite tool such as a Web browser extension, Web Pin it button, Mobile Web Facebook Messenger extension, or the iOS/Android share extension

This definition gives the driving core for thinking about the metric, but the doc continues on to outline edge cases and describe the correct behavior in a variety of cases (e.g. “opens Pinterest, but leaves before UI is visible” should not count as an active user).

The **product spec** is supplemented by a **technical spec** that is written more for engineers. It aligns on the exact method of logging the event and the metadata, and it documents exactly how each platform achieved the consistent implementation.

These steps may seem obvious, but every metric we’ve audited has had definitional issues. The **product spec** and **technical spec** ensure that everybody means the exact same thing when thinking about a metric.

The simpler the logging solution, the less likely it is to have issues.

## **Step 2: Implement the metric/fix existing issues**

The first layer of this can be done easily by the client engineers just following the definition and implementing accordingly. In practice, there will be edge cases and oddities that are unreasonable to expect a client engineer to anticipate.

These generally will send an alert if the data doesn’t pass a specific “check.” For the DAU example, one of our more successful checker types looks for “unexplained DAU.” This looks for users that have the active user event but lack other activity we would expect, such as seeing a pin.

Additionally, we can prove a metric is accurate through UI tests. For DAU, the most simple case would be to open the app, log in and confirm the user is logged as a DAU. Unlike the data checks, these allow us to find issues before a change ships. 

## **Step 3: Keep the metric accurate**

The UI tests and data checkers made in the last step are run recurrently to prove the metric is accurate. This means that failures in the UI tests can’t be released, and data checkers will lead to investigations. It’s key to keep in mind that uncovering why a metric moved in production is much more difficult and potentially costly than catching it before release.

Lastly, on a recurring basis (quarterly or annually, depending on the metric), we do health checks on the metric. This includes reviewing the checkers to make sure they are still running effectively and working with product teams to ensure that there are not new use cases that need to be considered.