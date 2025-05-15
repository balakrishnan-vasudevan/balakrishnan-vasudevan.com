WebSocket is a duplex protocol used mainly in the client-server communication channel. It’s bidirectional in nature which means communication happens to and fro between client-server.   

The connection, developed using the WebSocket, lasts as long as any of the participating parties lays it off. Once one party breaks the connection, the second party won’t be able to communicate as the connection breaks automatically at its front.  

WebSocket need support from [HTTP](https://www.wallarm.com/what/what-is-http-2-and-how-is-it-different-from-http-1) to initiate the connection. Speaking of its utility, it’s the spine for modern web application development when seamless streaming of data and assorted unsynchronized traffic is concerned.

![[Pasted image 20250429202515.png]]

WebSocket are an essential client-server communication tool and one needs to be fully aware of its utility and avoid scenarios to benefit from its utmost potential. It’s explained extensively in the next section.  

Use WebSocket When You Are:

1. ‍**Developing real-time web application**   
    

The most customary use of WebSocket is in real-time application development wherein it assists in a continual display of data at the client end. As the backend server sends back this data continuously, WebSocket allows uninterrupted pushing or transmitting this data in the already open connection. The use of WebSockets makes such data transmission quick and leverages the application's performance.   

A real-life example of such WebSocket utility is in the bitcoin trading website. Here, WebSocket assist in data handling that is impelled by the deployed backend server to the client.

2. ‍**Creating a chat application**   
    

Chat application developers call out WebSocket for help in operations like a one-time exchange and publishing/broadcasting the messages. As the same WebSocket connection is used for sending/receiving messages, communication becomes easy and quick.

3. ‍**Working up on gaming application**  
    

While gaming application development is going on, it’s imperative that the server is unremittingly receiving the data, without asking for UI refresh. WebSocket accomplish this goal without disturbing the UI of the gaming app.  

Now that it’s clear where WebSocket should be used, don’t forget to know the cases where it should be avoided and keep yourself away from tons of operational hassles.  

WebSocket shouldn’t be taken on board when old data fetching is the need of the hour or need data only for one-time processing. In these cases, using HTTP protocols is a wise choice.

## WebSocket vs HTTP  

As both HTTP and WebSocket are employed for application communication, people often get confused and find it difficult to pick one out of these two. Have a look at the below-mentioned text and gain better clarity on HTTP and WebSocket.  

As told previously, WebSocket is a framed and bidirectional protocol. On the contrary, to this, HTTP is a unidirectional protocol functioning above the TCP protocol.  

As WebSocket protocol is capable to support continual data transmission, it’s majorly used in real-time application development. HTTP is stateless and is used for the development of [RESTful](https://www.wallarm.com/what/differences-soap-vs-rest#what_is_rest_) and SOAP applications. Soap can still use HTTP for implementation, but REST is widely spread and used.  

In WebSocket, communication occurs at both ends, which makes it a faster protocol. In HTTP, the connection is built at one end, making it a bit sluggish than WebSocket.  

WebSocket uses a unified TCP connection and needs one party to terminate the connection. Until it happens, the connection remains active. HTTP needs to build a distinct connection for separate requests. Once the request is completed, the connection breaks automatically.

![[Pasted image 20250429202600.png]]


> Only use websockets when you need to. First like you said when it comes to scaling, the client instance is stuck to a specific socket on a server. Another issue is JWTs which are great for authentication and security. It's so much easier to put JWTs in the header of a REST call when you need it. With a socket connection the token has to be in the initial connection. The biggest of all issues with web sockets is that they can get dropped for any reason...so unless you are constantly monitoring the sockets and performing reconnects your app will randomly cease to function for clients.
> this part seems ok, we can still use JWTs (although I'm still a fan of old fashioned session keys with a session database, because JWTs are tricky when you need to support revoking). Like you said it can be included in the initial data when the socket is established. Alternatively we could just include the token as part of each payload (with a request/response pattern) and that would be similar to HTTP.


[[Pushy - Netflix]]