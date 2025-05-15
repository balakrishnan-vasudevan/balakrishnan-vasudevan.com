
![[Pasted image 20231107150504.png]]

_An example of a web hosting architecture on AWS_

1. **DNS services with [Amazon Route 53](https://aws.amazon.com/route53/)** – Provides DNS services to simplify domain management.
    
2. **Edge caching with [Amazon CloudFront](https://aws.amazon.com/cloudfront/)** – Edge caches high-volume content to decrease the latency to customers.
    
3. **Edge security for Amazon CloudFront with [AWS WAF](https://aws.amazon.com/waf/)** – Filters malicious traffic, including cross site scripting (XSS) and SQL injection via customer-defined rules.
    
4. **Load balancing with [Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/) (ELB)** – Enables you to spread load across multiple Availability Zones and [Amazon EC2 Auto Scaling](http://aws.amazon.com/ec2/autoscaling/) groups for redundancy and decoupling of services.
    
5. **DDoS protection with [AWS Shield](https://aws.amazon.com/shield/)** – Safeguards your infrastructure against the most common network and transport layer DDoS attacks automatically.
    
6. **Firewalls with security groups** – Moves security to the instance to provide a stateful, host-level firewall for both web and application servers.
    
7. **Caching with [Amazon ElastiCache](https://aws.amazon.com/elasticache/)** – Provides caching services with Redis or Memcached to remove load from the app and database, and lower latency for frequent requests.
    
8. **Managed database with [Amazon Relational Database Service](https://aws.amazon.com/rds/) (Amazon RDS)** – Creates a highly available, multi-AZ database architecture with six possible DB engines.
    
9. **Static storage and backups with [Amazon Simple Storage Service](https://aws.amazon.com/s3/) (Amazon S3)** – Enables simple HTTP-based object storage for backups and static assets like images and video.