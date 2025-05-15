

![[Pasted image 20231107115939.png]]

## Well-Architected Pillars

![](https://d1.awsstatic.com/apac/events/2021/aws-innovate-aiml/2022/eng/innovate-aiml-22-UI_Gradient-Divider.082bb46e8d9654e48f62bf018e131dd8ec563c4e.jpg)

The [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) helps you understand the pros and cons of the decisions you make when building systems in the cloud. The six pillars of the Framework allow you to learn architectural best practices for designing and operating reliable, secure, efficient, cost-effective, and sustainable systems. Using the [AWS Well-Architected Tool](https://aws.amazon.com/well-architected-tool/), available at no charge in the [AWS Management Console](https://console.aws.amazon.com/wellarchitected), you can review your workloads against these best practices by answering a set of questions for each pillar.

The architecture diagram above is an example of a Solution created with Well-Architected best practices in mind. To be fully Well-Architected, you should follow as many Well-Architected best practices as possible.

- Operational Excellence
    
    **Amazon EKS**, **Amazon ECR**, and a test automation framework are used in this Guidance to enhance your operational excellence. It helps you visualize, customize, and understand the concept of serving ML models using a FastAPI framework, providing you the flexibility to choose the **Amazon EKS** node compute instances of your choice in order to optimize performance and costs. **Amazon EKS** and **Amazon ECR** are managed Kubernetes and image repository services, respectively, and fully support API-based automation of all phases of the machine learning operations (MLOps) cycle. We also show how you can automatically deploy and run a large number of customized machine learning models, as well as automate load and scale testing of those models' performance using an automation framework.  
    
    [Read the Operational Excellence whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html) 
    
- Security
    
    **Amazon EKS**, **Amazon VPC**, **IAM** roles and policies, and **Amazon ECR** work in tandem to protect your information and systems. The **Amazon EKS** cluster resources are deployed into a VPC that provides a logical isolation of its resources from the public internet. A VPC  supports a variety of security features, such as security groups and network access control lists (ACLs), which are used to control inbound and outbound traffic to resources, as well as **IAM** roles and policies for authorization to limit access. The **Amazon ECR** image registry provides additional container-level security features, such as vulnerability scanning.   
    
    [Read the Security whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html) 
    
- Reliability
    
    **Amazon EKS** and **Amazon ECR** are used throughout this Guidance to help your workloads perform their intended functions correctly and consistently. **Amazon EKS** deploys the Kubernetes control plane (the instances that control how, when, and where your containers run) and the compute planes (the instances where your containers run) across multiple Availability Zones (AZs) in AWS Regions. This ensures that both the control and compute planes are always available, even if one AZ goes down. Also, **Elastic Load Balancing** (ELB)  will route application traffic to functional nodes. Additionally, the **Amazon EKS** cluster components are sending metrics to an [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) portal, where events can be configured to invoke alerts in case certain thresholds are crossed.   
    
    [Read the Reliability whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) 
    
- Performance Efficiency
    
    **Amazon ECR**, **Amazon EKS**, and **Amazon EC2** were used in this Guidance to support a structured and streamlined allocation of IT and computing resources. The compute nodes within the **Amazon EKS** cluster (that are **Amazon EC2** instances) can be scaled up and down based on the application's workload requirement while conducting the tests. Moreover, **Amazon ECR** and **Amazon EKS** are highly available services, optimized for scalability and performance of containerized applications. This Guidance leverages those and other services (such as **Amazon S3**, and the GitHub open-source software) to monitor and optimize performance characteristics of machine learning inference workloads through customization and automation.  
    
    [Read the Performance Efficiency whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html) 
    
- Cost Optimization
    
    **Amazon ECR** is a managed service that optimizes the costs of both storing and serving container image applications that are deployed on **Amazon EKS**. The compute nodes of the **Amazon EKS** cluster can scale up or down, based on projected workloads, when performing tests. Also, **Amazon EKS** node groups can be efficiently scaled, helping you to identify the most cost-efficient compute node configuration for running ML inferences at scale.  
    
    [Read the Cost Optimization whitepaper](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html) 
    
- Sustainability
    
    **Amazon EKS** with the **Amazon EC2** compute node instances deployed into the VPC and **Amazon ECR** do not use custom hardware. Meaning, you do not need to purchase or manage any physical servers. Instead, this Guidance uses managed services that run on the AWS infrastructure. Furthermore, by supporting the use of energy-efficient processor instance types, like [AWS Graviton Processors](https://aws.amazon.com/ec2/graviton/), this architecture provides increased sustainability. Using Graviton running in **Amazon EC2** can improve the performance of your workloads with less resources and thereby decreasing your overall resource footprint.