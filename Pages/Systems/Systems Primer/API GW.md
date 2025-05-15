- https://deploy.equinix.com/blog/how-api-gateways-differ-from-load-balancers-and-which-to-use/
-
- when designing an e-commerce website, you need to understand the roles of load balancers and API gateways before deciding which to use. Load balancers can help you handle the influx of traffic by distributing requests to different servers to ensure a smooth user experience. In contrast, API gateways can handle tasks like authentication and authorization, helping you create a secure online shopping experience.
- Load balancers distribute requests between two or more servers running the same application. Server pools group together servers that a load balancer might send traffic to. When a client sends a request to the load balancer, it delegates the request to one of the servers in the server pool and returns the response.
-API gateways provide a single entry point for all requests to your backend systems. When clients send requests to the API gateway, the gateway maps the request to the correct service in an organization's internal network. When routing requests, API gateways can also handle tasks like authentication, authorization, logging, routing and protocol translation.

![[Pasted image 20250430085517.png]]
-
- API gateways are implemented in the application layer (Layer 7) of the OSI model. This lets them read incoming packets and use the parsed data to route the request. Requests are routed based on their path, headers, query parameters and other attributes. The gateway might also serve a cached response, if configured, for the request endpoint.
- ## Benefits
	- API gateways simplify API management. The centralized control and monitoring make it easy to maintain, update and add new API endpoints pointing to different services on different servers.
	- In addition, many API gateways come with advanced security features. For example, you can integrate your API gateway with your authentication provider to grant users access to specific endpoints. You can also configure API keys and set granular rate limits for different endpoints in the API gateway to prevent clients from overloading or abusing your services.
	- API gateways also provide a consistent, unified API for your internal services. Using transformations, you can convert an incoming request into a protocol and structure that your internal service can accept.
- ## API Gateway Use Cases
  
  API gateways are beneficial when building systems with the following use cases:
- **Centralizing API management and security across multiple services:** If several internal services require security, it can be cumbersome to implement authentication and authorization in each service. This is a common scenario when building a microservices architecture, such as a logistics company with microservices for quoting, tracking, routing and customer support that must authenticate and authorize users using the company's identity provider. Fortunately, API gateways let you implement and manage API security in a central place and, in some cases, even integrate with your company's identity provider.
- **Legacy systems:** Legacy systems often don't conform to modern content formats. For example, a legacy system might only accept requests and respond using XML, even though JSON is a far more popular format for modern web APIs. API gateways' protocol translation lets you map between these different formats directly within the API gateway.
- **Simplifying the developer experience:** If you're building a public-facing or partner API, an API gateway can massively improve the developer experience for engineers consuming your API. They only need a single endpoint to access all your services, instead of using different endpoints for different services. Many API gateways also let you document endpoints configured in the gateway and generate Swagger files.
- **Rate limiting:** If your API is going to be exposed to the public or even consumed in a public app, rate limiting is beneficial. Rate limiting restricts how many requests a client can make in a certain time period (often short, like every hour or day). Without rate limits, malicious actors might try to overload and crash your application by rapidly requesting these endpoints.
- **Throttling:** Throttling is more disruptive than rate limiting and cuts off a client's access until a predefined timeout expires or the client requests a higher rate. For example, if you expose a paid API to developers where a paid plan lets developers make a hundred requests a month, you can use throttling with your API gateway to block the client's requests after they've hit the limit.
- **Caching static content:** Your application might have endpoints that expose infrequently updated data and get called quite often by the client. For example, your application might have an endpoint to retrieve all lookup values for a form field. API gateways give you flexible rules that you can use to cache frequently accessed and infrequently updated data returned by your API. You can configure a lifetime for cached responses, after which the API gateway will refresh its cache by fetching from the application server.
-
- ## Using Load Balancers and API Gateways Together
https://dev.to/somadevtoo/difference-between-api-gateway-and-load-balancer-in-system-design-54dd

- ![[Pasted image 20250303151600.png]]
-.![[Pasted image 20250303151615.png]]

While API gateways and load balancers share some similarities in terms of traffic management, their primary objectives and functionalities differ:

- **API Gateway**: Focuses on API management, security, protocol transformation, and analytics. Ideal for exposing and managing APIs to external clients, enforcing access control policies, and providing a unified interface for diverse backend services.
    
- **Load Balancer**: Primarily concerned with traffic distribution, high availability, and scalability. Suitable for distributing incoming traffic across multiple backend servers or instances to improve performance, reliability, and fault tolerance.
-
![[Pasted image 20250303151638.png]]

![[Pasted image 20250430085533.png]]




- [[Tinder API GW]]


- [[Application Layer]]