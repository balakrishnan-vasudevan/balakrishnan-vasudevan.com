
[Duolingo | Sending 6M+ Notifications Within 5 Seconds](https://medium.com/p/c630145038c3)

![[Pasted image 20250514134511.png]]

In the example described below, the requirement from the marketing team was to send 6 million+ notifications within 5 seconds during a specific time (kind of specific, as it should be done right after the ad shown during 2024 Super Bowl)

![[Pasted image 20250514134703.png]]

- The current system usually typically handles 10,000 notifications per second and the requirement is to send notifications at 80 times faster speed.
- The developers discovered an issue with the Android app. When it sends out a notification to the Android app, it sends a request right back to the backend. It is a little bit similar to a DDoS attack.
- The system should continue handling the organic traffic.
- The requirements were changing (_Can we add an icon to the notification? Can we send it to more cities? Can you localize the push into different languages? Can we use the vendor for this?_)
- One of the operating principles at Duolingo is to test it first. Meaning the solution should be tested before that day.
- The system should be able to scale at that rate. There are multiple technologies involved (Apple, Android APIs, AWS services scale limits, Rate limits of some services, etc.)
- The system should be ready as close to the Super Bowl day as possible. Because if they scaled the system a couple of days before the event, that would cost a lot.

# The Solution

**First of all the changing requirements** should be clarified. Meaning, that it’s okay to make some changes during the last couple of days, but some changes are forbidden, for example, “Is it ok to add 2 million users the day before, after basically we finalized the audience list?” The answer was no because it can not be tested that quickly. And if it’s not tested then they don’t ship it.

**The speed problem, which is 800,000 req/sec**. Duolingo has a lot of services on AWS. Some of the services related to this project are S3, DynamoDB and SQS. 

1. A couple month before any marketing campaign starts, the team will get a list of users from the DynamoDB (userId and deviceId) and will store it in S3. 
2. Once the day comes, engineers will scale ASG (collection of EC2 instances) and EC2 instances. 
3. The workers will then fetch data from S3, which we previously stored all the data, and store that data in memory. The data will be mapping from the user ID to the device IDs.
4. After that, the API server will actually send out 50-plus messages to the FIFO, First In, First Out SQS queue. 
5. The interim worker in between after receiving those messages, they’ll dispatch 10,000-plus SQS messages to the next queue. 
6. Finally, the last tier of notification workers will send notifications by calling the batch APNS and FCM’s API. They are Apple and Google’s notification API.

But the SQS in itself has an in-flight message limit of 120,000 messages per second. Just to send millions notifications within 5 seconds. They will use the technique of batching. They batched 500 iOS users together in one message, 250 for Android, which puts them under the limit.

**Can the AWS provision all the necessary resources in time?** To solve this problem, they connected with a technical contact from AWS, who helped to draft an Infrastructure Event Management document, which included detailed steps, like when and how to scale up, as well as some of the more concrete steps like the cache and the cache connection limits, and the Dynamo limits. A dedicated ECS cluster also helped to solve some of the problems.

# Testing
At the beginning (during the MVP phase) testing was done using silent notifications. Which is an empty payload sent to the client devices and to see what happens. One of the discovered bottleneck was thread count. As they are using Python applications it has some known issues when it comes to multi-threaded programs. Decreasing the number of threads from 10 to 5 to 1, helped to overcome that problem.

Another problem occurred when they tried to scale both the notification service (dedicated to this project) and the backend. The service had to wait for all the other backend services to scale up so that it can scale up, or vice versa. That’s why they dedicated separate ECS cluster mentioned before.

Testing the availability of both the notification service and the backend within the 3 hours window also succeeded.

https://youtu.be/J_sGZnAJhbw?si=iySQQoAhIcUlrNsJ