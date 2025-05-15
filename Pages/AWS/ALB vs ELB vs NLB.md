## ELB
ELB works at both layer 4 (TCP) and 7 (HTTP) and is the only load balancer that works in EC2-Classic, in case you have a very old AWS account. Also, it’s the only load balancer that supports application-defined sticky session cookies; in contrast, ALB uses its own cookies, and you have no control over that.
At layer 7, ELB can terminate TLS traffic. It can also re-encrypt the traffic to the targets as long as they provide an SSL certificate (a self-signed certificate is fine, BTW). This provides end-to-end encryption, which is a usual requirement in many compliance programs. Optionally, ELB can be configured to verify the TLS certificate provided by the target for extra security.

ELB has quite a few limitations. For example, it isn’t compatible with EKS containers running on Fargate. Also, it can’t forward traffic on more than one port per instance, and it doesn’t support forwarding to IP addresses—it can only forward to explicit EC2 instances or containers in ECS or EKS. Finally, ELB doesn’t support websockets; however, you may be able to work around this limitation by using layer 4.
Use discouraged.
Admittedly, there are very few scenarios where the use of an ELB would be preferable; typically, these are cases where you simply don’t have a choice. For example, your workload might still run on [EC2-Classic](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-classic-platform.html), or you need the load balancer to use your own sticky session cookies, in which cases ELB would be the only option available to you.

## Next generation of LBs
Most importantly, they both use the concept of “target groups,” which is one additional level of redirection. It can be conceptualized in this way. Listeners receive requests and decide (based on a wide range of rules) to which target group they will forward the requests. A target group then routes the requests to instances, containers, or IP addresses. Target groups manage the targets in terms of deciding how to split up the traffic and by performing health checks on the targets.

Both ALB and NLB can forward traffic to IP addresses, which allows them to have targets outside the AWS Cloud (for example: on-premises servers or instances hosted on another cloud provider).
### ALB
An Application Load Balancer (ALB) only works at layer 7 (HTTP). It has a wide range of routing rules for incoming requests based on host name, path, query string parameter, HTTP method, HTTP headers, source IP, or port number. In contrast, ELB only allows routing based on port number. Also, contrary to ELB, ALB can route requests to many ports on a single target. Plus, ALB can route requests to Lambda functions.

A very useful feature of ALB is that it can be configured to return a fixed response or a redirection. So you don’t need a server to perform such basic tasks because it is all embedded in the ALB itself. Also very importantly, ALB supports HTTP/2 and websockets.

ALB further supports [Server Name Indication (SNI)](https://www.cloudflare.com/learning/ssl/what-is-sni/), which allows it to serve many domain names. (In contrast, ELB can serve only one domain name). There is a limit, however, to the number of certificates you can attach to an ALB, [namely 25 certificates](https://aws.amazon.com/blogs/aws/new-application-load-balancer-sni/) plus the default certificate.

An interesting feature of ALB is that it supports user authentication via a variety of methods, including OIDC, SAML, LDAP, Microsoft AD, and well-known social identity providers such as Facebook and Google. This can help you off-load the user authentication part of your application to the load balancer.
ALBs are typically used for web applications. If you have a microservices architecture, ALB can be used as an internal load balancer in front of EC2 instances or Docker containers that implement a given service. You can also use them in front of an application implementing a REST API, although [AWS API Gateway](https://aws.amazon.com/api-gateway/) would generally be a better choice here.


### NLB
A Network Load Balancer (NLB) works at layer 4 only and can handle both TCP and UDP, as well as TCP connections encrypted with TLS. Its main feature is that it has a very high performance. Also, it uses static IP addresses and can be assigned Elastic IPs—not possible with ALB and ELB.

NLB natively preserves the source IP address in TCP/UDP packets; in contrast, ALB and ELB can be configured to add additional HTTP headers with forwarding information, and those have to be parsed properly by your application.

NLBs would be used for anything that ALBs don’t cover. A typical use case would be a near real-time data streaming service (video, stock quotes, etc.) Another typical case is that you would need to use an NLB if your application uses non-HTTP protocols.
