#scaling, #kubernetes

Source: https://openai.com/research/scaling-kubernetes-to-7500-nodes 
## Workload 

- Single pod occupies entire node.
- NUMA, CPU, or PCIE resource contention are not factors for scheduling.
- Bin packing and fragmentation are not a problem.
- Cluster have full bisection bandwidth - no need for any rack or n/w topology considerations.
- Even with high number of nodes, relatively low strain on scheduler.
- Strain on kube-scheduler is spiky - new job consists of hundreds of pods being created at once, then returns to low rate of churn.
- Biggest jobs to be run = MPI (message passing interface) - all pods within the job are participating in a single MPI communicator - if any of the pods die, job halts and has to be restarted.
	- Job checkpoints regularly and can be restarted from the last checkpoint.
	- So pods are semi-stateful - killed pods can be replcaed and work can continue - but this is disruptive and should be kept to a minimum.
- They don't rely on load balancing. Very little HTTPS traffic - no need for testing, blue/green, canaries.
- Pods communicate directly with one another on their pod IP address using MPI via SSH - service endpoints not used
- Limited service discovery is limited - only done when pods participating in MPI at job start time.
- Storage - Jobs interact with some form of blob storage. Usually pods either stream some shards of a dataset or checkpoint directly from blob storage, or cache it to a fast ephemeral disk. 
- Some PVs exist, but blob storage is more scalable. 
## Networking
- Flannel had issues with scaling up for the throughput required.
- They used native pod networking technologies to get host level network throughput on pods.
- They use alias-based IP addressing. Route-based pod networking has significant limitations in the number of routes they could use.
- No encapsulation - increases demands on SDN and routing engine, but networking is simple. 
- No worry about packet fragmentation.
- Network policies and traffic monitoring is straightforward; there’s no ambiguity about the source and destination of packets.
- iptables tagging is used on the host to track n/w usage per namespace and pod - this helps with checking reasons for any bottlenecks.
	- iptables mangle rules are used to arbitrarily mark packets matching a particular criteria.
	- Forward rules cover traffic from pods
	- Input/Output rules cover traffic from the host.
- node, pod, and service network CIDR ranges are fully exposed.
- Hub and spoke network model is used, native node and pod CIDR ranges used to route traffic.
- a “NAT” host to translate the service network CIDR range for traffic coming from outside of the cluster.
## API servers
- alert on the rate of HTTP status 429 (Too Many Requests) and 5xx (Server Error) on the API Servers as a high-level signal of problems.
- Both etcd and API servers run on their own dedicated nodes. 
- Our largest clusters run 5 API servers and 5 etcd nodes to spread the load and minimize impact if one were to ever go down.
- API Servers are stateless and generally easy to run in a self-healing instance group or scaleset.
- For our cluster with 7,500 nodes we observe up to 70GB of heap being used per API Server, so fortunately this should continue to be well-within hardware capabilities into the future.
- One big strain on API Servers was WATCHes on Endpoints. There are a few services, such as ‘kubelet’ and ‘node-exporter’ of which every node in the cluster is a member. When a node would be added or removed from the cluster, this WATCH would fire. And because typically each node itself was watching the `kubelet` service via kube-proxy, the # and bandwidth required in these responses would be �2N2 and enormous, occasionally 1GB/s or more. [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/), launched in Kubernetes 1.17, were a huge benefit that brought this load down 1000x.
- We try to avoid having any DaemonSets interact with the API Server. In cases where you do need each node to watch for changes, introducing an intermediary caching service, such as the [Datadog Cluster Agent](https://docs.datadoghq.com/agent/cluster_agent/), seems to be a good pattern to avoid cluster-wide bottlenecks.
- As our clusters have grown, we do less actual autoscaling of our clusters. But we have run into trouble occasionally when autoscaling too much at once.

## Monitoring
- We use Prometheus to collect time-series metrics and Grafana for graphs, dashboards, and alerts. We started with a deployment of [kube-prometheus](https://github.com/coreos/kube-prometheus) that collects a wide variety of metrics and good dashboards for visualization.

## Healthchecks

- Some healthchecks are passive, always running on all nodes. These monitor basic system resources such as network reachability, bad or full disks, or GPU errors.
- Another form of healthcheck tracks maintenance events from the upstream cloud provider. Each of the major cloud providers expose a way to know if the current VM is due for an upcoming maintenance event that will eventually cause a disruption.

## Quotas and Resource Usage
- We have a service in each cluster, “team-resource-manager” that has multiple functions. Its data source is a ConfigMap that specifies tuples of (node selector, team label to apply, allocation amount) for all of the research teams that have capacity in a given cluster. It reconciles this with the current nodes in the cluster, tainting the appropriate number of nodes with `openai.com/team=teamname:NoSchedule`.
- In addition to using cluster-autoscaler to dynamically scale our VM-backed clusters, we use it to remediate (remove & re-add) unhealthy members within the cluster. We do this by setting the “min size” of the cluster to zero, and the “max size” of the cluster to the capacity available. However, cluster-autoscaler, if it sees idle nodes, will attempt to scale down to only needed capacity. For multiple reasons (VM spin up latency, pre-allocated costs, the API server impacts mentioned above) this idle-scaling isn’t ideal.
- So, we introduced a balloon Deployment for both our CPU-only and GPU hosts. This Deployment contains a ReplicaSet with “max size” number of low-priority pods. These pods occupy resources within a node, so the autoscaler doesn’t consider them as idle. However since they’re low priority, the scheduler can evict them immediately to make room for actual work.
- we use pod anti-affinity to ensure the pods would evenly distribute across the nodes. Earlier versions of the Kubernetes scheduler had an  O(N2) performance issue with pod anti-affinity. This has been corrected since Kubernetes 1.18.

## Gang Scheduling
Our experiments often involve one or more StatefulSets, each operating a different portion of the training effort. For Optimizers, researchers need all members of the StatefulSet to be scheduled, before any training can be done (as we often use MPI to coordinate between optimizer members, and MPI is sensitive to group membership changes).

However, Kubernetes by default won’t necessarily prioritize fulfilling all requests from one StatefulSet over another. For example if two experiments each requested 100% of the cluster’s capacity, instead of scheduling all of one experiment or the other, Kubernetes might schedule only half of each experiment’s pods, leading to a deadlock where neither experiment can make progress.

We tried a few things needing a custom scheduler, but ran into edge cases that caused conflicts with how normal pods were scheduled. Kubernetes 1.18 introduced a plugin architecture for the core Kubernetes scheduler, making it much easier to add features like this natively. We recently landed on the [Coscheduling plugin](https://github.com/kubernetes/enhancements/pull/1463) as a good way to solve this problem.

## Unsolved issues
1. Metrics = At our scale we’ve had many difficulties with Prometheus’s built-in TSDB storage engine being slow to compact, and needing long times needed to replay the WAL (Write-Ahead-Log) any time it restarts. Queries also tend to result in “query processing would load too many samples” errors. We’re in the process of migrating to a different Prometheus-compatible storage and query engine.
2. Pod network trafic shaping = As we scale up our clusters, each pod is calculated to have a certain amount of Internet bandwidth available. The aggregate Internet bandwidth requirements per person have become substantial, and our researchers now have the ability to unintentionally put a significant resource strain on other locations on the Internet, such as datasets for download and software packages to install.