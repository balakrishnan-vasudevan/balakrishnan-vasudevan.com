
Source:
https://medium.com/expedia-group-tech/traffic-shedding-rate-limiting-backpressure-oh-my-21f95c403b29

## Summary
- There are three options to handle as much traffic as possible — **scale**, **overprovision**, **queue**;
- And another three to avoid overloading — **traffic shedding**, **rate limiting**, **backpressure** (when the first three aren’t enough);
- If you don’t apply some of the first six options, you have chosen the last option by default — **failing by overloading**.

![[Pasted image 20250309192334.png]]

Scaling - Add sufficient additional capacity to handle traffic increase automatically or manually
Over-provisioning - Already having sufficient additional capacity to handle any traffic increase
Queuing - Temporarily holding traffic somewhere and processing it as resources come free, works when service can handle requests asynchronously.


## Avoiding overloading
1. Drop traffic - traffic shedding
2. Rate limit - Throttle requests, HTTP error code 429
3. Backpressure - The server-side part of backpressure is **rate limiting**. To complete the loop for backpressure, the client needs to understand the rate limiting feedback, and reduce it’s request rate so that it stops exceeding the rate-limit.

