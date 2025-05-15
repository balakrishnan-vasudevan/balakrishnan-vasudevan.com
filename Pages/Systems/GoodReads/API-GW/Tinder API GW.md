https://medium.com/tinder/how-we-built-the-tinder-api-gateway-831c6ca5ceca

We have more than 500 microservices at Tinder, which talk to each other for different data needs using a service mesh under the hood. All external-facing APIs are hosted on TAG. We needed a gateway solution that could centralize all these services, giving us more control from maintenance to deployment. The custom gateway also helps in ensuring that services go through a security review before being publicly exposed to the outside world.

Before TAG existed, we leveraged multiple API Gateway solutions and each application team used a different 3rd party API Gateway solution. Since each of the gateways was built on a different tech stack, managing them became a cumbersome effort. More to the point, there were compatibility issues in sharing reusable components across different gateways. This would often result in delays in shipping the code to production. Moreover, different API Gateways had maintenance overheads.

We also saw inconsistent use of Session Management across APIs as the API Gateways were not centralized, as shown in below figure 1.

![](https://miro.medium.com/v2/resize:fit:1400/0*RIqzOFbBl4N7c9UL)

TAG is a JVM-based framework built on top of **Spring Cloud Gateway**. Application teams can use TAG to create their own instance of API Gateway by just writing configurations. It centralizes all external facing APIs and enforces strict authorization and security rules at Tinder. TAG extends components like gateway and global filter of Spring Cloud Gateway to provide generic and pre-built filters.

These filters can be used by application teams for various needs:

- Weighted routing
- Request/Response transformations
- HTTP to GRPC conversion, and more

# A Deeper Look Inside TAG

![](https://miro.medium.com/v2/resize:fit:1400/0*juqW49yqVlcuLopD)


High-Level Design, as shown in figure 2, showcases the following components:

- **Routes** — Developers can expose their endpoints using Route As a Config (**RAC**); we’ll see in detail how routes are set up in TAG later on
- **Service Discovery** — TAG uses Service Mesh to discover backend services for each route
- **Pre-Built Filters** — We’ve added built-in filters in TAG for application teams at Tinder to use;  
    example: setPath, setMethod, etc.
- **Custom Filters** — We’ve added the support of custom filters so that application teams can write their own custom logic if needed, and implement them in a route using configurations. Custom filters are applied at Route Level (i.e. per route); example: custom logic to validate the request before calling backend service.
- **Global Filters** — Global filters are just like custom filters, but they’re global in nature, i.e. they are applied to all the routes automatically if configured at the service level.  
    Example: Auth filter or metrics filter applied to all routes specific to an application.

Below is the step-by-step flow of how TAG builds all the routes at application startup:

![](https://miro.medium.com/v2/resize:fit:1400/0*AHxL2q4g96dsMl3B)