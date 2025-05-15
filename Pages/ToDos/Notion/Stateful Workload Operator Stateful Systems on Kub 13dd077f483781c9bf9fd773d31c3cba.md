# Stateful Workload Operator: Stateful Systems on Kubernetes at LinkedIn

Tags: Kubernetes
Category: Articles
Company: LinkedIn
Status: Not started
URL: https://www.linkedin.com/blog/engineering/infrastructure/stateful-workload-operator-stateful-systems-on-kubernetes-at-linkedin

For over a decade, LinkedIn has operated stateful systems at scale across hundreds of thousands of machines in our data centers, powering critical services such as [Kafka](https://kafka.apache.org/), [Zookeeper](https://zookeeper.apache.org/), [Liquid](https://www.linkedin.com/blog/engineering/graph-systems/liquid-the-soul-of-a-new-graph-database-part-1), and [Espresso](https://engineering.linkedin.com/espresso/introducing-espresso-linkedins-hot-new-distributed-document-store). These systems are highly sensitive to latency and therefore rely heavily on locally attached disks to ensure they can serve requests quickly and reliably. Since LinkedIn's early days, we have used a custom in-house scheduler to allocate bare-metal servers to private pools for teams operating stateful services. While this provided persistence and predictability for stateful system operators, it forced teams to independently manage hardware health, operating system (OS) upgrades, hardware maintenance and refreshes, and other fleet-level duties. Unfortunately, the intense support for managing stateful systems has scaled with the size of our fleet.

To address this, we are prioritizing stateful applications and host lifecycle maintenance as we transition from our bespoke, home-grown scheduler to Kubernetes. While many people might say "stateful applications and Kubernetes don’t mix," with so many solutions tailored to the complexities of individual apps, we’ve seen an opportunity to take a different approach. Traditionally, stateful applications on Kubernetes rely on bespoke [Operators](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) that fully manage their lifecycle, offering fine-grained control through domain-specific [Custom Resource Definitions](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) (CRDs) to specify their desired state.

In this blog, we present our Stateful Workload Operator, an alternative model to the traditional approach: all stateful applications now share a common operator with a single custom resource, while application-specific customizations are handled by pluggable external policy engines. At LinkedIn, we've inverted the traditional stateful application operator model, providing application owners with a generic building block and a centralized point to manage storage, external integrations, tooling, and other features. The ultimate goal is for teams to focus solely on the specific logic required to maintain the health of their applications during deployment, maintenance, and scaling operations, while the orchestration of these processes is managed centrally, ensuring consistency and reducing operational overhead.

## Why StatefulSet doesn’t cut it

Kubernetes StatefulSet provides a convenient way to manage persistent volume claims and orchestrate the ordered rollout of changes. However, we faced several key limitations that made it less suited to our needs:

- StatefulSet is not aware of the sharding policy of stateful applications, so we would still need to build an entire layer on top of the StatefulSet to achieve application shard awareness and coordination.
- StatefulSet only supports scaling out, scaling in and deploying pods. It does not manage planned or unplanned host maintenance such as temporarily shutting down all pods on a specific node or swapping pods from one node to another.
- StatefulSet didn’t allow us to run with multiple canary versions within the same set of pods.

While it was technically possible to work around these limitations using webhooks and custom logic, this approach felt more like a patchwork of solutions than a clean, maintainable system. The benefits of using StatefulSet were minimal, and it would have only reduced a small portion of the overall code complexity versus developing our own pod management. By developing our own custom resources, we were able to overcome these challenges, achieve the flexibility we needed, and align more closely with our specific requirements.

## Making Kubernetes shard aware with application cluster managers

Stateful applications often have varied architectures, each with unique requirements for managing their lifecycle. For example, in a database application where only one live instance of a partition exists, losing that instance could lead to data loss or significant downtime. Kubernetes, however, lacks partition awareness, which meant we needed a mechanism to signal when an application was actually prepared to lose a pod without risking critical outages.

To address these complexities, we introduced the Application Cluster Manager (ACM), a service running within the cluster that works in coordination with our operator through “cooperative scheduling”. The ACM evaluates whether it is safe for the operator to proceed with deployment or maintenance operations, ensuring the application cluster remains healthy. Each ACM implementation includes logic tailored to the specific stateful application, ensuring safety across all operations. This could involve guaranteeing sufficient shard replication before allowing temporary pod downtime, ensuring deployments are ordered across maintenance zones, or preventing unnecessary leader election thrashing during updates. Our data centers are divided into 20 maintenance zones, and during a fleet maintenance event, an entire zone is evacuated. We can safely take down servers in any given maintenance zone because all applications are sharded across these zones.

The diagram above illustrates how our operator and the ACM collaborate to schedule operations for stateful application clusters. We send four types of requests to the ACM: deployment, disruption, scaling, and swap. Scaling operations add or remove pods from the cluster, disruption temporarily removes pods while preserving their data, and swap moves a pod from one node to another, maintaining both its data and identity. The ACM then evaluates the safety of applying these operations to the application cluster. If it determines that the operation is safe, the ACM responds with an acknowledgment, allowing the operator to proceed. If no acknowledgement is given, we take no action. This process ensures the stability and security of stateful application clusters.

For instance, consider the above example, which has the following operations queued: a deployment, disruption, scaling, and swap operation. After performing application-specific checks, the ACM sends acknowledgments for safe actions, such as approving the deployment for Pod 1, adding Pod 5, and beginning to swap Pod 7 to a different node. Once we receive these acknowledgments, we proceed with the respective actions—deploying a new version of Pod 1, bringing up Pod 5, and moving Pod 7 to a new node.

The Application Cluster Manager significantly simplifies lifecycle management and maintenance coordination for stateful applications. If each team were to develop its own operator, each application would need to build state machines for deployments and integrate with both the IaaS layer and Kubernetes. These implementations would demand extensive knowledge of the internal workings of the underlying systems, placing a heavier operational burden on each application team. By managing all orchestration and integration centrally, the Application Cluster Manager alleviates these challenges, allowing individual applications to focus on the logic necessary for ensuring safety during cluster and host lifecycle operations, while the operator handles the complexities of both the IaaS layer and Kubernetes.

## Stateful operator architecture

[https://media.licdn.com/dms/image/v2/D4D08AQEjZF9f7GzqmQ/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731086733677?e=2147483647&v=beta&t=rV77YyuxyPVaRoNBLh_zKABWduDym-RjBzCshIl7upM](https://media.licdn.com/dms/image/v2/D4D08AQEjZF9f7GzqmQ/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731086733677?e=2147483647&v=beta&t=rV77YyuxyPVaRoNBLh_zKABWduDym-RjBzCshIl7upM)

Figure 2: High-level architecture of our Stateful Operator

The [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) extends Kubernetes' functionality by automating the management of complex applications. Operators encapsulate operational expertise into Kubernetes-native controllers, automating tasks such as deployment, upgrades, scaling, and recovery. Operators typically interact with CRDs, which define new resource types within the Kubernetes API. By monitoring these resources, the operator responds to state changes and adjusts application components to match the desired state.

OurStateful Workload Operator is a Kubernetes operator built around five core CRDs: LiStatefulSet, Revision, PodIndex, Operation, and StatefulPod. Each CRD has a specific purpose in the overall lifecycle of our operator and helps us separate concerns between different layers.

- **LiStatefulSet CRD** is the user-facing API where users configure application deployment details, including container information, pod count, volume support, and health checks.
- **Revision CRD** tracks the version history of LiStatefulSets, with each revision representing an immutable PodTemplateSpec, similar to the Kubernetes built-in ControllerRevision API.
- **PodIndex CRD** serves as a staging object for proposed changes to pods, allowing the operator to compare the current state with the desired state and generate operations accordingly. For example, if the LiStatefulSet specifies 4 pods, the PodIndex might look like: podIndex: { running: [a, b, c, d] }.
- **Operation CRD** defines the types of operations—deployment, scaling, disruption, and swaps—indicating which pods should undergo specific changes. For instance, operation[type:deployment, instances:[a, b, c, d]] directs Kubernetes to deploy new versions of pods a, b, c, and d.
- **StatefulPod CRD** manages pods and PersistentVolumeClaims, ensuring that data and pod configurations are correctly handled during lifecycle changes.

## Example high-level flow

An example high-level flow of how a user configures an LiStatefulSet, from the initial configuration to the creation of a pod, is outlined as follows:

1. User Configuration: The user configures and applies a LiStatefulSet YAML file to Kubernetes.
2. Revision Creation: we create a new Revision to track the scale-out PodTemplate version
3. Pod Index Creation: we generate a PodIndex object, which contains detailed information about all the pods that need to be deployed.
4. Operation Creation: Based on the PodIndex, we generate a scale-out operation that specifies which pods should be deployed.
5. Interaction with ACM: we send the operation to the ACM via a well-defined gRPC interface and continuously polls the ACM to monitor when the specified pods are ready for execution.
6. Pod Creation: Once the ACM signals that certain pods are ready, we instruct Kubernetes to create the corresponding pods.
7. Pod Scheduling: Kubernetes schedules these pods and deploys them across the appropriate nodes.

## Auto remediation: a self-healing platform

[https://media.licdn.com/dms/image/v2/D4D08AQHIV0tJe2NXgg/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731086887277?e=2147483647&v=beta&t=Xc_85lZEEp1UwPv41YzI0SocOMPzPXUaV1W80uSX35M](https://media.licdn.com/dms/image/v2/D4D08AQHIV0tJe2NXgg/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731086887277?e=2147483647&v=beta&t=Xc_85lZEEp1UwPv41YzI0SocOMPzPXUaV1W80uSX35M)

Figure 3: A high-level logical view of how the stateful operator is always reconciling differences between declared state and live state.

Our system continuously monitors pod state changes in the Kubernetes cluster and compares them with the desired state specified by the user in the LiStatefulSet. It calculates the difference between the actual and desired states, then generates the necessary operations to reconcile these differences. These operations fall into five categories: scale-out, scale-in, swap, disruption, and deployment.

For example, if the user specifies four pods [a, b, c, d], but only two pods [a, b] are running in the cluster, a scale-out operation for pods [c, d] will be generated.

To ensure consistency during repeated reconciliation cycles, the system employs a deduplication mechanism to avoid creating duplicate operations. If an existing operation already includes the affected pod and matches the operation type, no new operation will be generated for that pod.

## Coordinating maintenance: seamless node lifecycle management

A primary goal in designing our operator was to simplify node maintenance for application owners. In our data centers, nodes frequently undergo OS, firmware, and hardware upgrades, all of which require the evacuation of workloads. Our approach alleviates application owners from the burdens of evacuating nodes, monitoring their health, and provisioning replacements for faulty hardware. Instead, their ACM receives disruption events from our maintenance stack, which inform them of either temporary or permanent node loss. The ACM then notifies us when they are ready for their pod to be temporarily taken offline or relocated to a new node.

### Temporary node disruption

[https://media.licdn.com/dms/image/v2/D4D08AQH5Xbxk34p_Ew/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731087212996?e=2147483647&v=beta&t=DkXAht4OsSos5eckKtvU6u48jd2zwcIhsgRXUx6djqA](https://media.licdn.com/dms/image/v2/D4D08AQH5Xbxk34p_Ew/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731087212996?e=2147483647&v=beta&t=DkXAht4OsSos5eckKtvU6u48jd2zwcIhsgRXUx6djqA)

Figure 4: An example high-level flow of a temporary disruption, such as a reimage. The process begins at the IaaS layer and is proxied to the ACM for approval. Once approved, the operator takes down the pod and approves the disruption in the IaaS layer.

When a node needs to be re-imaged, upgraded, or undergo temporary maintenance without data loss, the stateful operator proxies the request from the IaaS layer to the ApplicationClusterManager. Once approved, the pod is deleted, but the PersistentVolumeClaims are retained to preserve the data. The IaaS layer then re-images or remediates the underlying node. After the process is complete, the node re-joins the cluster, the operator detects it, and the pod is brought back up on the node, completing the disruption operation.

### Permanent node loss

[https://media.licdn.com/dms/image/v2/D4D08AQF-_VZq4PXDyQ/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731087154454?e=2147483647&v=beta&t=v-CfNt30PtL4SEeVw3rSpFXaNuQvpGkAWFvqkzymADA](https://media.licdn.com/dms/image/v2/D4D08AQF-_VZq4PXDyQ/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1731087154454?e=2147483647&v=beta&t=v-CfNt30PtL4SEeVw3rSpFXaNuQvpGkAWFvqkzymADA)

Figure 5: An example of a high-level flow in the event of permanent node loss, such as a node decommission. The process begins at the IaaS layer and is then proxied to the ACM for approval. Once approved, the operator brings up a replacement pod, removes the old pod from the target node, and approves the decommission in the IaaS layer.

When a planned node decommission or our IaaS layer detects a critical node health issue, a request is received from the IaaS layer to permanently evict the node. In response, the stateful operator generates swap requests, tearing down the pods on the affected node and bringing them up with the same identity on other nodes. A common pattern in happy path scenarios involves an ACM acknowledging the addition of the new pod first, while delaying acknowledgment of the old pod's removal. The ACM will then wait until the new pod is fully up and ready to serve traffic before confirming the old pod's removal. Once removal is confirmed, the old pod and its associated resources are deleted, the IaaS layer is informed, and the node is permanently removed from the cluster.

## Learnings and improvements from our legacy stack

### Toil reduction through cooperative scheduling

We mentioned before that the Application Cluster Manager enables stateful application owners to seamlessly integrate their application with Kubernetes and our IaaS layer. This integration allows users to focus on their specific application logic without needing a deep understanding of the underlying infrastructure. By adopting this approach, teams can move away from cumbersome homegrown automation or manual operations—like node allocation, maintenance zone balancing, and replacing unhealthy hosts—which all carry significant maintenance costs. With the Stateful Workload Operator managing their fleets, stateful system owners can dictate how their systems should be managed, freeing them from the complexities of operational workflows.

### Prioritizing deployment and maintenance leads to a simpler stack

Our Stateful Workload Operator centralizes deployment and maintenance operations for both applications and hosts. Previously, operations often took longer than necessary because different actors - responsible for deployments, reimages, reboots, etc. - would all compete to get control of the same resources. By treating deployment and maintenance as first-class concerns, we can handle all disruptive operations consistently, eliminating issues like racing conditions that arose from the old stack's architecture. Additionally, it is also easier for developers to test and understand the full impact of each operation, especially when multiple operations are happening simultaneously, since the whole state machine is confined to a single repository.

### Scalable software development practices

The speed and success of our development over the last year reinforced the benefits of standard software development principles, which we’ll briefly discuss below:

- Separation of concerns - we adhered to SOLID principles when designing our CRDs and ACM APIs, ensuring that each component had a simple and clear business purpose. As a result we were able to achieve significant development parallelization since our components are relatively isolated from each other.
- Continuous investment in test infrastructure - our team’s motto is “test everything to death and then test it again”. Every component underwent in-depth local testing, with rigorous unit and integration tests required for every commit. When tests became slow or unreliable, we dropped everything and prioritized their improvement to maintain productivity.
- Frequent Refactoring - we did not get everything right in the initial design nor did we account for every single feature. As time went on, we got new requirements or found new issues which would inevitably add complexity to our code. We chose to refactor early when things started looking messy to keep our code clean and easy to understand. This practice kept our codebase clean and understandable, enabling any team member to navigate it easily.

By sticking to our high standards for software development, our team was able to retain its productivity amid team growth and new requirements while delivering quality software to our users. This project serves as a reminder that there is a reason these standards exist and that they work.

### Our experience with Kubernetes

A year ago we started with just an idea. Today, we have multiple clusters of stateful systems fully migrated and running on our Stateful Workload Operator in a single production region, handling all of the functionality of a decade-old deployment system. Additionally, the operator also handles many features that our legacy system didn’t, such as storage/volume management for each application.

This pace of development was made possible by Kubernetes’ rich ecosystem of built-in resources (e.g. Persistent Volumes/Claims) and extensive customization options through custom resources and operators. However, we’ve also encountered our own share of issues with Kubernetes too, such as grappling with Kubernetes’ declarative API for fundamentally imperative tasks (e.g. restarting a pod through our public API), configuring kube-scheduler to understand our maintenance-zone spread requirements, and achieving full observability of resource reconciliation issues.

Despite these challenges, we still believe using Kubernetes is the right decision for LinkedIn thanks to its robust feature set and developer community that we can continue to leverage in the coming years.

**Acknowledgements**

This post highlights just a fraction of the complex machinery needed to make everything work at scale. We’d like to extend our gratitude to the incredible teams at LinkedIn for their ongoing contributions in making this possible.

Topics:  [Data Streaming/Processing](https://www.linkedin.com/blog/engineering/data-streaming-processing)   [Distributed Systems](https://www.linkedin.com/blog/engineering/distributed-systems)   [Infrastructure](https://www.linkedin.com/blog/engineering/infrastructure)

Related articles

- [Navigating the scale: how design patterns power LinkedIn’s inf...](https://www.linkedin.com/blog/engineering/infrastructure/how-design-patterns-power-linkedin-infrastructure)
    
     [Infrastructure](https://www.linkedin.com/blog/engineering/infrastructure) 
    
    Saira Khanum
    
    Nov 7, 2024
    
- [Right-sizing Spark executor memory](https://www.linkedin.com/blog/engineering/infrastructure/right-sizing-spark-executor-memory)
    
     [Infrastructure](https://www.linkedin.com/blog/engineering/infrastructure) 
    
    Rob Reeves
    
    Nov 6, 2024
    
    [https://media.licdn.com/dms/image/v2/D4D08AQEFejmuyI2nKw/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1730841626739?e=2147483647&v=beta&t=5FWzak9rSQPoE9ZpRpQcGzbVMaW2Ll2jvQE9Ob8NJYM](https://media.licdn.com/dms/image/v2/D4D08AQEFejmuyI2nKw/croft-frontend-shrinkToFit1024/croft-frontend-shrinkToFit1024/0/1730841626739?e=2147483647&v=beta&t=5FWzak9rSQPoE9ZpRpQcGzbVMaW2Ll2jvQE9Ob8NJYM)