- Tags: #traffic
- Category: Articles
  Company: general
  Status: Not started
  URL: https://umangahuja1.medium.com/the-thundering-herd-problem-when-servers-get-mobbed-9be2911e72db
- # What is the Thundering Herd Problem?
  
  The Thundering Herd Problem occurs when a large number of clients simultaneously request access to a common resource. This issue often arises in systems where resources are locked or limited. When the resource becomes available, all the processes attempt to access it at the same time. This sudden influx of traffic can overwhelm the resource, leading to server overload and potential crashes.
  
  A real-world tech example? Cache miss storms. Imagine your website’s cache expires, causing a flood of requests to hit the backend to rebuild it. It’s like everyone rushing to grab the last iPhone on sale the moment it’s restocked.
- # Why Is This a Problem? 
  
  You might be wondering, “Why is this such a big deal?” Well, here’s why:
  
  1. **Server Overload**: The sudden rush can overwhelm your server, causing it to slow down or even crash. 
  2. **Increased Latency**: The massive influx of simultaneous requests can cause delays, meaning clients will have to wait longer to get their hands on those deals. 
  3. **Inefficiency**: Resources are wasted as the server struggles to handle redundant requests, leading to more delays, degraded performance, and frustrated customers due to bad user experience. 
  
  In short, instead of a smooth experience, you get a digital traffic jam, and nobody’s snagging those deals and you lose business!
- # How Do We Solve the Thundering Herd Problem? 
  
  When we discuss solving this problem, we are not talking about scaling the system horizontally or vertically. For the short term, that can help to unblock but to solve the bigger problem, it is a design issue that one needs to take to tackle such instances gracefully and prevent them from happening in the future.
  
  Good news! There are several strategies to avoid or mitigate the Thundering Herd Problem. Here are a few:
  
  1. **Rate limiting per client**: Limiting the number of requests a client can make helps to prevent a single client from overwhelming a system.
  2. **Exponential Backoff**: Instead of retrying immediately, processes wait for an amount of time that increases exponentially. This spreads out the requests over time, like telling the users to wait a bit before trying again for that deal. 
  3. **Token Buckets**: Implement a rate-limiting mechanism where only a certain number of requests are allowed through at a time. It’s like letting only a few people into the store at once. 
  4. **Staggered Timeouts**: Instead of all processes timing out and retrying at the same interval, you can stagger their retry times. It’s like staggering the entry times of users to avoid a stampede. Introducing **Jitter** in such calls can add randomness and break the periodicity.  (Want to read more about jitters: [YouTube Strategy: Adding Jitter isn’t a Bug](https://highscalability.com/youtube-strategy-adding-jitter-isnt-a-bug/) )
  5. **Queueing Requests**: Queue incoming requests and process them in batches. This helps control the flow and ensures the server isn’t overwhelmed, just like a bouncer managing the crowd outside a store. 
  6. **Caching**: With cache in place, the number of requests hitting the database will reduce consequently reducing the load as well.
  
  There was a very well-known thundering herd problem instance witnessed by Facebook when they introduced the Facebook Live feature. Have a read here to learn how they addressed that issue: [Under the hood: Broadcasting live video to millions](https://engineering.fb.com/2015/12/03/ios/under-the-hood-broadcasting-live-video-to-millions/)
- # Conclusion: Avoid the Digital Stampede! 
  
  The Thundering Herd Problem might sound like a niche issue, but it can show up in many systems, especially those with high traffic and shared resources. By understanding the problem and proactively implementing strategies to handle it, you can prevent your servers from getting trampled. No one likes a digital stampede, especially on a launch day or something special!
  
  When designing your system, foresight is your friend. If you think your system might be susceptible to the Thundering Herd Problem, address it in the design phase. Don’t wait for it to occur and then scramble to apply fixes. Proactively tackling this issue can save you a lot of headaches down the road.
  
  The Thundering Herd Problem can have a significant impact, but with the right planning and strategies, you can avoid the chaos and keep everything running smoothly.
  
  I hope you enjoyed this blog post and learned something new! If you have any questions, feel free to leave a comment below.
  
  And remember, if you’ve got more questions or topics you want to dive into, do let me know! Happy coding!

[[Thundering Herd]]
[[Netflix - Load Spikes]]
[[Thundering Herd FB]]