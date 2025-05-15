

Tags: #real-time-systems
Category: Articles
Company: general
Status: Not started
URL: https://medium.com/@tahir.rauf/system-design-fundamentals-providing-realtime-updates-080588e29791


Can a web server provide real-time updates? An HTTP server cannot automatically initiate a connection to a browser; therefore, the web browser must be the initiator. So, how do we achieve real-time updates from the HTTP server?

Long Polling, WebSockets, and Server-Sent Events (SSE) are techniques that enable the server to push data to the client without the client needing to request it explicitly. Here’s an overview of each method and their differences.

## Long Polling

The client sends a request to the server, and the server holds the connection open until it has new data to send to the client. Once the server sends the data, the connection is closed, and the client immediately sends another request to ‘poll’ for new data. This process repeats indefinitely, creating a near-real-time communication channel.

Advantages: Universally supported. Disadvantages: a) Creates new connection each time. b) Message ordering c) Increased latency

![[Pasted image 20250509172841.png]]

## Web Sockets

WebSockets enable full-duplex, bidirectional communication between a client and a server over a single, long-lived connection. This allows for real-time communication with lower latency and less overhead compared to Long Polling.

Advantages: Full Duplex, Asynchronous. Disadvantages: Terminated connections aren’t automatically recovered. 

![[Pasted image 20250509172909.png]]

## Server Side Event

SSE (Server-Sent Events) uses the standard HTTP protocol to push real-time updates from the server to the client. It works by keeping an HTTP connection open and streaming updates as they occur. Unlike WebSockets, SSE is unidirectional, meaning the client cannot send messages back to the server.


![[Pasted image 20250509172940.png]]

## Summary

![[Screenshot 2025-05-09 at 5.30.38 PM.png]]


# References

[https://x.com/milan_milanovic/status/1711044053494628687](https://x.com/milan_milanovic/status/1711044053494628687)