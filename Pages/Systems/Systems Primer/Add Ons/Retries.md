- Requests can be thought of as HTTP requests. They can succeed or fail. Failed requests have spiked edges, successful requests stay smooth.
- Load balancers route requests from clients to servers.
- Servers accept and serve requests.
- Clients send requests to servers via a load balancer. After getting a response, they will wait an amount of time before sending another request.

Strategies to retry
1. Don't retry
2. Retry with a delay - will lead to a bad user experience in practice. Users don't like waiting, and the longer you sleep between retries, the more likely they are to refresh manually or go and do something else. Both bad outcomes.
3. Exponential Backoff - There are lots of things you can configure when calculating exponential backoff, but if you imagine we started off waiting for 1 second and waited twice as long each retry, 10 retries would look like this:
						- 1 second
						- 2 seconds
						- 4 seconds
						- 8 seconds
						- 16 seconds
						- 32 seconds
						- 1 minute and 4 seconds
						- 2 minutes and 8 seconds
						- 4 minutes and 16 seconds
						- 8 minutes and 32 seconds
4. Jitter - "Jitter" is the process of randomising how long we wait between retries to within a specific range. To follow the Google HTTP client library example, they add 50% jitter. So a retry interval can be between 50% lower and 50% higher than the calculated figure.

- **Retrying in a tight loop is dangerous.** You risk getting into overload situations that are difficult to recover from.
- **Retrying with a delay** helps a little bit but is still **dangerous.**
- **Exponential backoff** is a much safer way of retrying, balancing user experience with safety.
- **Jitter** adds an extra layer of protection, preventing clients from sending synchronised surges of requests.