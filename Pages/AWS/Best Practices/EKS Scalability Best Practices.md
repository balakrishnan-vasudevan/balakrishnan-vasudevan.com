Source: https://aws.github.io/aws-eks-best-practices/scalability/docs/

Scalability

Using a single, large EKS cluster can reduce operational load compared to using multiple clusters, but it has trade-offs for things like multi-region deployments, tenant isolation, and cluster upgrades.

## **Kubernetes Control Plane**

in an EKS cluster includes all of the services AWS runs and scales for you automatically (e.g. Kubernetes API server). Scaling the Control Plane is AWS's responsibility, but using the Control Plane responsibly is your responsibility.

Includes kube api server, controller manager, scheduler + other components required for k8s to function.

- Use EKS >1.24 - container runtime switched to containerd instead of docker.
- Limit workload + Node bursting - Control plane will scale as the cluster grows, but there are limits on the speed. Scaling large applications require load balancers to be warmed. Use custom metrics like requests per second in HPA instead of CPU/Memory scaling.
- KEDA for event based workload scaling.
- Replace long running instances - less toil, avoid config drift. TTL in Karpenter or max-instance-lifetime setting for self managed node groups to cycle through nodes.
- Remove underutilized nodes - Remove nodes with no running workloads.
- Use PDB and safe node shutdown - Making updates to multiple resources frequently or too quickly can cause API server throttling and application outages as changes propagate to controllers. [Pod Disruption Budgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) are a best practice to slow down churn to protect workload availability as nodes are removed or rescheduled in a cluster. 
- Use client-side cache when running kubectl - Avoid running scripts that use kubectl repeatedly without a local cache as this causes throttling and unnecessary API calls.
- Disable kubectl compression - By default the server will compress data sent to the client to optimize network bandwidth. This adds CPU load on the client and server for every request and disabling compression can reduce the overhead and latency if you have adequate bandwidth.
- Shard cluster autoscaler - Cluster autoscaler has been tested to scale up to 1000 nodes. For large clusters, run multiple instances of the cluster autoscaler in shard mode.

## **Kubernetes Data Plane**

scaling deals with AWS resources that are required for your cluster and workloads, but they are outside of the EKS Control Plane. Resources including EC2 instances, kubelet, and storage all need to be scaled as your cluster scales.

Includes EC2 instances, load balancers, storage, other APIs used by k8s control plane

- Automatic node autoscaling - reduces toil.
- Use many different EC2 instance types - you should not arbitrarily limit the type of instances that can be use in your cluster.
- Prefer larger nodes to reduce API server load - When deciding what instance types to use, fewer, large nodes will put less load on the Kubernetes Control Plane because there will be fewer kubelets and DaemonSets running. However, large nodes may not be utilized fully like smaller nodes. Node sizes should be evaluated based on your workload availability and scale requirements. Workloads should define the resources they need and the availability required via taints, tolerations, and [PodTopologySpread](https://kubernetes.io/blog/2020/05/introducing-podtopologyspread/). They should prefer the largest nodes that can be fully utilized and meet availability goals to reduce control plane load, lower operations, and reduce cost. The Kubernetes Scheduler will automatically try to spread workloads across availablility zones and hosts if resources are available. If no capacity is available the Kubernetes Cluster Autoscaler will attempt to add nodes in each Availability Zone evenly.

<aside> 💡 A cluster with three u-24tb1.metal instances (24 TB memory and 448 cores) has 3 kublets, and would be limited to 110 pods per node by default. If your pods use 4 cores each then this might be expected (4 cores x 110 = 440 cores/node). With a 3 node cluster your ability to handle an instance incident would be low because 1 instance outage could impact 1/3 of the cluster.

</aside>

- Use similar node sizes for consistent workload performance - Workloads should define what size nodes they need to be run on to allow consistent performance and predictable scaling. A workload requesting 500m CPU will perform differently on an instance with 4 cores vs one with 16 cores. Avoid instance types that use burstable CPUs like T series instances.
- Use compute resources efficiently - Using compute resources effectively will increase your scalability, availability, performance, and reduce your total cost. Efficient resource usage is extremely difficult to predict in an autoscaling environment with multiple applications.
- Automate AMI updates - Keeping worker node components up-to-date means you will get latest security patches and compatible features with kubernetes API.
- Use multiple EBS volumes for containers - EBS volumes have input/output (I/O) quota based on the type of volume (e.g. gp3) and the size of the disk. If your applications share a single EBS root volume with the host this can exhaust the disk quota for the entire host and cause other applications to wait for available capacity. Applications write to disk if they write files to their overlay partition, mount a local volume from the host, and also when they log to standard out (STDOUT) depending on the logging agent used. To avoid disk I/O exhaustion you should mount a second volume to the container state folder (e.g. /run/containerd), use separate EBS volumes for workload storage, and disable unnecessary local logging.
- Avoid instances with low EBS attach limits if workloads use EBS volumes - Each instance type has a maximum number of [EBS volumes that can be attached](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/volume_limits.html). Workloads need to declare what instance types they should run on and limit the number of replicas on a single instance with Kubernetes taints.
- Disable unnecessary logging to disk - Avoid unnecessary local logging by not running your applications with debug logging in production and disabling logging that reads and writes to disk frequently. Journald is the local logging service that keeps a log buffer in memory and flushes to disk periodically. Journald is preferred over syslog which logs every line immediately to disk.

```bash
runcmd:
  - [ systemctl, disable, --now, syslog.service ]
```

- Patch instances in place when OS update speed is a necessity - Amazon recommends using immutable infrastructure that is built, tested, and promoted from an automated, declarative system, but if you have a requirement to patch systems quickly then you will need to patch systems in place and replace them as new AMIs are made available. Because of the large time differential between patching and replacing systems we recommend using [AWS Systems Manager Patch Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html)  to automate patching nodes when required to do so.

## **Cluster services**

are Kubernetes controllers and applications that run inside the cluster and provide functionality for your cluster and workloads. These can be [EKS Add-ons](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html) and also other services or Helm charts you install for compliance and integrations. These services are often depended on by workloads and as your workloads scale your cluster services will need to scale with them.

Cluster services are expected to have a high up-time and are often critical during outages and for troubleshooting.

They should run on dedicated compute instances such as a separate node group or AWS Fargate. This will ensure that the cluster services are not impacted on shared instances by workloads that may be scaling up or using more resources.

- Scale CoreDNS - Scaling CoreDNS has two primary mechanisms. Reducing the number of calls to the CoreDNS service and increasing the number of replicas.
    
    - Reduce external queries by lowering ndots - The ndots setting specifies how many periods (a.k.a. "dots") in a domain name are considered enough to avoid querying DNS. If your application has an ndots setting of 5 (default) and you request resources from an external domain such as [api.example.com](http://api.example.com/) (2 dots) then CoreDNS will be queried for each search domain defined in /etc/resolv.conf for a more specific domain. You can reduce the number of requests to CoreDNS by [lowering the ndots option](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-dns-config). of your workload or fully qualifying your domain requests by including a trailing . (e.g. `api.example.com.`). If your workload connects to external services via DNS we recommend setting ndots to 2 so workloads do not make unnecessary, cluster DNS queries inside the cluster.
    - Scale coreDNS horizontally - scale by adding additional replicas to the deployment.
        - Node local DNS - run one sintance per node as a daemonset, requries more compute nodes in the cluster, but avoids failed DNS requests + rdecreases response time for DNS queries.
        - Cluster proportional autoscaler - scales coreDNS based on the number of nodes/cores in the cluster.
- Scale kubernetes metrics server vertically - Horizontally scaling the metrics server makes it HA, but it will not scale horizontally to handle more cluster metrics. The Metrics Server keeps the data it collects, aggregates, and serves in memory. As a cluster grows, the amount of data the Metrics Server stores increases. In large clusters the Metrics Server will require more compute resources than the memory and CPU reservation specified in the default installation. Use Vertical Pod Autoscaler to scale the metrics server.
    
- Logging and monitoring agents - can add significant load to the cluster control plane coz agents query the API server to enrich logs+metrics with workload metadata. Querying API server can add more details like kube deployment name + labels, highly useful with troubleshooting, but detrimental with scaling. Two options:
    
    - Disable Integrations - You lose log metadata. Not an option
    - Sampling and filtering - reduces the number of metrics and logs that are collected. This will lower the amount of requests to the Kubernetes API, and it will reduce the amount of storage needed for the metrics and logs that are collected. Reducing the storage costs will lower the cost for the overall system.
    
    To avoid losing logs and metrics you should send your data to a system that can buffer data in case of an outage on the receiving endpoint. With fluentbit you can use [Amazon Kinesis Data Firehose](https://docs.fluentbit.io/manual/pipeline/outputs/firehose) to temporarily keep data which can reduce the chance of overloading your final data storage location.
    

## **Workloads**

are the reason you have a cluster and should scale horizontally with the cluster. There are integrations and settings that workloads have in Kubernetes that can help the cluster scale. There are also architectural considerations with Kubernetes abstractions such as namespaces and services.

- Use IPv6 for pod networking - avoids IP address exhaustion. Also gives per node performance improvements coz pods receive IP addresses faster by reducing the number of ENI attachments per node. You can achieve similar node performance by using [IPv4 prefix mode in the VPC CNI](https://aws.github.io/aws-eks-best-practices/networking/prefix-mode/), but you still need to make sure you have enough IP addresses available in the VPC.
- Limit number of services per namespace - The maximum number of [services in a namespaces is 5,000 and the maximum number of services in a cluster is 10,000](https://github.com/kubernetes/community/blob/master/sig-scalability/configs-and-limits/thresholds.md). To help organize workloads and services, increase performance, and to avoid cascading impact for namespace scoped resources we recommend limiting the number of services per namespace to 500. Generating thousands of IP tables rules and routing packets through those rules have a performance impact on the nodes and add network latency. Create Kubernetes namespaces that encompass a single application environment so long as the number of services per namespace is under 500. This will keep service discovery small enough to avoid service discovery limits and can also help you avoid service naming collisions.
- Understand ELB quotas - When creating your services consider what type of load balancing you will use (e.g. Network Load Balancer (NLB) or Application Load Balancer (ALB)). Each load balancer type provides different functionality and have [different quotas](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-limits.html). Some of the default quotas can be adjusted, but there are some quota maximums which cannot be changed. e.g.: the default ALB targets is 1000. If you have a service with more than 1000 endpoints you will need to increase the quota or split the service across multiple ALBs or use Kubernetes Ingress. The default NLB targets is 3000, but is limited to 500 targets per AZ. If your cluster runs more than 500 pods for an NLB service you will need to use multiple AZs or request a quota limit increase. Alternative to using load balancer coupled to a service is to use an ingress controller. An in-cluster ingress controller allows you to expose multiple Kubernetes services from a single load balancer by running a reverse proxy inside your cluster.
- Use Route53, CloudFront, Gloabl Accelerator - To make a service using multiple load balancers available as a single endpoint you need to use [Amazon CloudFront](https://aws.amazon.com/cloudfront/), [AWS Global Accelerator](https://aws.amazon.com/global-accelerator/), or [Amazon Route 53](https://aws.amazon.com/route53/) to expose all of the load balancers as a single, customer facing endpoint. Route 53 can expose multiple load balancers under a common name and can send traffic to each of them based on the weight assigned. Global Accelerator can route workloads to the nearest region based on request IP address. This may be useful for workloads that are deployed to multiple regions, but it does not improve routing to a single cluster in a single region. CloudFront can be use with Route 53 and Global Accelerator or by itself to route traffic to multiple destinations. CloudFront caches assets being served from the origin sources which may reduce bandwidth requirements depending on what you are serving.
- Use endpointslices instead o endpoints - Endpoints were a simple way to expose services at small scales but large services that automatically scale or have updates causes a lot of traffic on the Kubernetes control plane. EndpointSlices have automatic grouping which enable things like topology aware hints.
- use immutable and external secrets if possible - The kubelet keeps a cache of the current keys and values for the Secrets that are used in volumes for pods on that node. The kubelet sets a watch on the Secrets to detect changes. As the cluster scales, the growing number of watches can negatively impact the API server performance.
- Limit deployment history - Pods can be slow when creating, updating, or deleting because old objects are still tracked in the cluster.
- Disable enableServiceLinks by default - When a Pod runs on a Node, the kubelet adds a set of environment variables for each active Service. Linux processes have a maximum size for their environment which can be reached if you have too many services in your namespace. The number of services per namespace should not exceed 5,000. After this, the number of service environment variables outgrows shell limits, causing Pods to crash on startup.
- Limit dynamic admission webhooks per resource - [Dynamic Admission Webhooks](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) include admission webhooks and mutating webhooks. They are API endpoints not part of the Kubernetes Control Plane that are called in sequence when a resource is sent to the Kubernetes API. Each webhook has a default timeout of 10 seconds and can increase the amount of time an API request takes if you have multiple webhooks or any of them timeout.

<aside> 💡 Mutating webhooks can modify resources in frequent succession. If you have 5 mutating webhooks and deploy 50 resources etcd will store all versions of each resource until compaction runs—every 5 minutes—to remove old versions of modified resources. In this scenario when etcd removes superseded resources there will be 200 resource version removed from etcd and depending on the size of the resources may use considerable space on the etcd host until defragmentation runs every 15 minutes.

This defragmentation may cause pauses in etcd which could have other affects on the Kubernetes API and controllers. You should avoid frequent modification of large resources or modifying hundreds of resources in quick succession.

</aside>