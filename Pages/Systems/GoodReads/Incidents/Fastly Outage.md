# What the Fastly Outage Can Teach Us About Observability | Splunk

Tags: incident, observability
Category: Articles
Company: Fastly
Status: Not started
URL: https://www.splunk.com/en_us/blog/devops/what-the-fastly-outage-can-teach-us-about-observability.html?splukn

On Tuesday June 8th, the Content Delivery Network Fastly experienced an [outage that made large swaths of the web unavailable](https://arstechnica.com/gadgets/2021/06/fast-ly-broke-the-internet-for-an-hour-this-morning/) for nearly an hour. To focus on the positive, this outage can serve as a wakeup call for Observability teams, because it shows how much modern sites depend on resources beyond their immediate control, and how hard it is to "observe" these kinds of issues with an incomplete Observability mindset. In this blog post, I will talk about the Fastly outage, examine how traditional monitoring technologies would have responded to that outage, and show how adopting [Digital Experience Monitoring inside your Observability practice](https://www.splunk.com/en_us/devops/digital-experience-monitoring.html) is crucial to detecting and responding to these types of issues.

## Inside a CDN Outage

Fastly is a [Content Delivery Network (CDN)](https://www.splunk.com/en_us/blog/learn/cdns-vs-load-balancers.html). While today’s CDNs serve many different functions, their primary job is to cache copies of a website's content or resources in data centers around the world, so that this data is geographically closer to a website's visitors when they request it, thus reducing the latency and improving performance. CDNs do this by sitting "in front" of a website or API. For example, when someone accesses splunk.com, the requests for this site’s images, CSS, fonts, and perhaps even its HTML markup are all served by the CDN instead of by the origin server.

In the diagram below, we can see how the CDN sits between the site visitor and the origin server. When the browser requests main.js, the CDN already has a copy, and returns it more quickly than the origin server would have. When the browser makes an API call, the CDN passes that request through to the origin server.

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_6.png](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_6.png)

On Tuesday, [due to an internal issue](https://www.fastly.com/blog/summary-of-june-8-outage), Fastly could not respond to any requests. These requests didn't pass through to the origin server so it couldn’t service those requests either. The diagram below illustrates this breakdown:

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_5.png](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_5.png)

## What a User Experiences During a CDN Outage

The Splunk Observability team has a sample online store, [BroomsToGo](https://broomstogo.com/), that was actually impacted by the CDN outage this week. It runs on Shopify, which uses Fastly, so I was able to use our Observability tools to see first-hand what users experienced. Below is a [waterfall chart](https://rigor.com/blog/read-waterfall-chart/) from [Splunk Synthetic Monitoring](https://www.splunk.com/en_us/observability/synthetic-monitoring.html) that shows the requests the browser made when it tried to load BroomsToGo:

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_4.png](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_4.png)

Requests that were sent directly to the application host broomstogo.com, such as base HTML and an API request, were successful. All of the site's assets, including CSS, most images, and JavaScript, were served by the host cdn.shopify.com, which was fronted by Fastly. Because of the outage, requests for those assets all returned a 503 error. Failing to load the CSS and JS had a catastrophic effect! I captured the image below that shows how poorly the site looked and behaved during the CDN outage:

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_3.jpg](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_3.jpg)

That bad user experience was also bad for business. Even if you could have scrolled around to find the unstyled "checkout" button, it wouldn’t have worked! The JavaScript functions attached to that button didn't load, because the main.js file failed to load from the CDN.

## What an Incomplete Observability Practice Sees During a CDN Outage

Consider the impact if BroomsToGo were a legitimate store, instead of a fun sample application. Would the team have been able to detect this issue using only a few of the traditional monitoring tools?

Imagine Melanie, an SRE for BroomsToGo, who is sipping her coffee when Ethan from Bizdev calls in a panic: "The website is down! No one can check out! We are losing thousands of sales!"

Impossible! Melanie thinks as she pulls up her traditional monitoring tools. Everything is green. There are no alerts posted in the Ops channel in Slack. Surely her infrastructure or application monitors would have detected something?

Unfortunately not. The CDN is sitting in front of some or all of the application. A CDN failure therefore impacts the ability to "observe" the outage via traditional means. Here is how traditional monitoring tools would have handled this outage

- **Traditional Infrastructure Monitoring (IM):** IM provides insights on the health of your infrastructure, such as containers, servers, or cloud resources. Since a CDN outage prevents most, if not all, visitor traffic from accessing your infrastructure, SRE teams using IM would have seen green dashboards with no issues. No company-controlled infrastructure was stressed.
- **Traditional Application Performance Monitoring (APM):** APM goes one level higher, showing you how a database, web server, or application code is functioning. Because the outage prevented most traffic from reaching your application, APM would not have detected any problem and would have sent no alerts. And it would be right! In our example, the application itself was fine. The base HTML page and all API requests returned 200 OK. Instead, it was the latency and availability of those CSS and JavaScript resources hosted by the third party CDN that made the application fail.

Where Melanie would have seen a problem is if she was watching her site analytics. Checkout rates would be going down, depending on how widespread the outage is. Traffic numbers and engagement numbers would also be going down. If she had alerts on social media about her brand, she would see people starting to complain as well.

## Expanding Observability with Digital Experience Monitoring

Melanie mistakenly assumed that the infrastructure and applications she controls represent all important aspects of the app's health and availability. Unfortunately, this is not the case. Modern applications have spread beyond your control. They nearly always include third-party components and run in opaque environments. In some cases, such as when marketing adds a new chat widget to the website, SREs might not even know of all the infrastructure, apps, and dependencies that make up their site. While legacy IM and APM are fantastic tools to help detect and diagnose issues, these tools cannot measure what they cannot see, and modern applications have a lot of surface area beyond SREs’ control.

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_1.png](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_1.png)

This is where [Digital Experience Monitoring](https://www.splunk.com/en_us/devops/digital-experience-monitoring.html) (DEM) comes in. DEM monitors performance and experience from the client's perspective, allowing you to monitor how both your backend performance – and the performance of included 3rd party assets – impacts the user and detect any availability issues with the application, regardless of where in the stack they occur. DEM leverages a combination of [Synthetic Monitoring](https://www.splunk.com/en_us/observability/synthetic-monitoring.html) and [Real User Monitoring](https://www.splunk.com/en_us/software/real-user-monitoring.html) (RUM). Synthetic Monitoring measures the performance of a page or business flow using real browsers running from locations around the world every minute. RUM uses JavaScript to capture data from real users visiting your site or using your app, giving you metrics about the performance, experience, and errors that actually occurred.

In fact, because I used [Splunk Synthetic Monitoring](https://www.splunk.com/en_us/observability/synthetic-monitoring.html) on the BroomsToGo site, I got an alert about this outage. Synthetic monitoring detected an increase in client-side errors exactly when this week’s CDN outage occurred.

![https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_2.png](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2021/06/Fastly_2.png)

In the screenshot above, the teal-colored line represents the [First Contentful Paint](https://developer.mozilla.org/en-US/docs/Glossary/First_contentful_paint) and the black line shows the count of browser errors encountered while downloading resources. We can see that at the moment when the outage started, assets such as CSS and JS failed to load, thus increasing the error count. Meanwhile, the paint time actually improved, because all those request failures meant there was less content to draw!

Of course, DEM solutions cannot see inside your infrastructure and application (in fact, if a client, be it a real user or a synthetic browser, can see inside your app, you have bigger issues!). This is why DEM must be combined with IM, APM, and other solutions in a suite of Observability such as [Splunk Observability Cloud](https://www.splunk.com/en_us/observability.html). This combination provides comprehensive visibility into your application, infrastructure, and user experience, keeping you on top of issues no matter where in your stack they arise.

## Conclusions

The Fastly outage this week is a clear example of how content and infrastructure beyond your control can make your site fail and impact your business. By expanding your point of view and measuring experience from the client's perspective using Digital Experience Monitoring, you can detect these types of issues and respond quickly to minimize their impact. As you develop a comprehensive Observability strategy, remember to include Digital Experience Monitoring.

**To get started with Splunk Synthetic Monitoring, [sign up for a free trial](https://www.splunk.com/en_us/download/o11y-cloud-free-trial.html) today.**

**Additional Splunk resources:**

- [Synthetic Monitoring](https://www.splunk.com/en_us/observability/synthetic-monitoring.html) product page
- [Digital Experience Monitoring](https://www.splunk.com/en_us/devops/digital-experience-monitoring.html) product page
- [Observability Cloud](https://www.splunk.com/en_us/observability.html) product page