- Tags: #traffic, #meta
- Category: Articles
  Company: Facebook
  Status: Complete
  URL: https://blog.devops.dev/ever-heard-of-the-thundering-herd-problem-heres-how-facebook-solved-it-48bd6a07c2b9
- ## Key Points:
- **Simultaneous Requests:** A lot of users request the same resource at once.
- **Server Overload:** If the server isn’t prepared, it can get overwhelmed, leading to slowdowns or even crashes.

- # How Do You Solve the Thundering Herd Problem?
  
  There are several ways to tackle this problem. Some of the most popular solutions are-
  
  1. **Randomized Backoff:** Introduce random delays before retrying failed requests to prevent synchronized retries and reduce system load.
  
  **2. Circuit Breaker:** Temporarily block requests to a failing service when errors exceed a threshold. Gradually allow requests after a timeout, fully reopening if successful.
  
  **3. Rate Limiting:** Limit the number of requests a client can make in a set time to prevent overload and maintain system stability.


- # **Facebook’s Solution: A Real-World Example**
- ## **The Scenario:**
  
  Facebook’s edge servers are designed to handle up to 200,000 requests per second, keeping the traffic away from the main servers (origin servers). But during a live event, when millions of people are watching, the Thundering Herd Problem can quickly become an issue.
- ## **How Facebook Tackled It:**
  
  1. **Edge Server with an HTTP Proxy and Caching Layer:**Facebook’s edge servers use a caching system and an HTTP proxy. When you request a video, the edge server first checks if it’s already stored in the cache. If not, it asks the origin server for it.
  
  **2. Origin Server:**
  
  If the edge server doesn’t have the video segment in its cache, it forwards the request to the origin server. The origin server either serves the segment or retrieves it from the live stream server and then caches it.
  
  ![[Pasted image 20250314141350.png]]
  
  **3. Live Stream Server:**
  
  On a cache miss, the origin server forwards the request to the live stream server, which streams the requested video segment, caching it for future requests.
  
![[Pasted image 20250314141426.png]]


- ## **The Result:**
  
  These strategies allow Facebook to stream live video to millions without overloading servers, ensuring a smooth experience by managing the Thundering Herd Problem.

# Conclusion
  
  The ***Thundering Herd*** Problem challenges handling large volumes of simultaneous requests, particularly in live streaming.
  
  ***Facebook’s solutions — distributed caching, and load balancing*** — effectively manage this issue and cache thrashing, ensuring robust and responsive systems even under heavy loads.
  
  However, while solving the Thundering Herd Problem, another issue can arise: **Cache Thrashing**. In my next post titled [**“What is the Cache Thrashing Problem? Here’s How Facebook Solved It,”**](https://medium.com/@sanimkhan13/what-is-the-cache-thrashing-problem-heres-how-facebook-solved-it-fcbd4f69266c) I’ll explain what Cache Thrashing is and how to solve it.