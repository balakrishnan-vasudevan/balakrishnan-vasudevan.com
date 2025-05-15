_Controllers_ are the core abstraction used to build Kubernetes. Once you’ve declared the desired state of your cluster using the API server, controllers ensure that the cluster’s current state matches the desired state by continuously watching the state of the API server and reacting to any changes. Controllers operate using a simple loop that continuously checks the current state of the cluster against the desired state of the cluster. If there are any differences, controllers perform tasks to make the current state match the desired state.

Controllers typically operate in a control loop with a general sequence of events:

1. **Observe:** Each Controller in the cluster will be designed to observe a specific set of Kubernetes objects. For example, the [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) Controller will observe Deployment objects, and the Service Controller will observe Service objects, etc. Every object in a Kubernetes cluster has an associated Controller responsible for watching it to analyze its configuration.
2. **Compare:** The Controller will compare the object configuration with the current state of the cluster to determine if changes are necessary. For example, if a [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) is configured to have five replicas (copies of a pod) , the ReplicaSet Controller will constantly monitor the number of active Pod replicas in the cluster. If a pod is deleted, the ReplicaSet Controller will recognize a difference between the desired state and the current state of the cluster.
3. **Action:** The Controller will apply changes to the cluster to ensure the cluster's current state matches the desired state of the Kubernetes objects. Following the above example, if a Pod is deleted and, therefore, "drifted" from the cluster's current state, the ReplicaSet Controller will mitigate this drift by launching a replacement Pod. In this case, the ReplicaSet Controller's objective is to ensure the number of active Pods in the cluster matches the number of replicas in the ReplicaSets.
4. **Repeat:** All of the above steps are being completed in an infinite loop by all Controllers in the Kubernetes cluster. The Controllers ensure the cluster's current state always matches the desired state specified in the Kubernetes object configuration.

This pattern of behavior is a crucial aspect of how all Kubernetes clusters work "under the hood." Controllers are the core element that drives a cluster's functionality by executing the configurations defined in Kubernetes objects. Without Controllers, no actions (like container orchestration) would occur in the cluster.

## Six examples of Kubernetes Controllers

Many Controllers are built-in to the Kube Controller Manager deployed as part of all Kubernetes clusters, each with a specific purpose.

Here are six examples of Controllers:

- **Node Controller:** Responsible for managing Worker Nodes. It will monitor the new Nodes connecting to the cluster, validate the Node's health status based on metrics reported by the Node's Kubelet component, and update the Node's .status field. If a Kubelet stops posting health checks to the [API Server](https://kubernetes.io/docs/concepts/overview/kubernetes-api/), the Node Controller will be responsible for triggering Pod eviction from the missing Node before removing the Node from the cluster.
- **Deployment Controller:** Responsible for managing Deployment objects and creating/modifying ReplicaSet objects.
- **ReplicaSet Controller:** Responsible for creating/modifying Pods based on the ReplicaSet object configuration.
- **Service Controller:** Responsible for configuring [ClusterIP, NodePort, and LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/) configuration based on Service objects.
- **CronJob Controller:** Responsible for creating Job objects based on the Cron schedule defined in CronJob objects.
- **StatefulSet Controller:** Responsible for creating Pods in a guaranteed order with a sticky identity.


The design principles followed by Controllers to enable Kubernetes to operate as a high-quality distributed system are summarized in the sections below.

### Kubernetes design principle #1: Desired state

This model involves specifying how the desired state of a cluster should look rather than defining execution steps like in traditional configuration management tools (Chef, Puppet, Ansible, etc.). By declaratively defining the cluster's desired state in YAML manifests, users can delegate the implementation details to Controllers to apply the desired changes. Controllers are constantly reconciling the cluster's current state with the desired state, leaving less responsibility to the user to manually reconcile differences by pushing changes through configuration management tools.

### Kubernetes design principle #2: Fault tolerance

Controllers typically run as multiple replicas on the control plane Master Nodes. Even when a Master Node experiences an interruption, such as hardware failure, a separate copy of the Kube Controller Manager will be running on another Master Node. The Controllers will continue the reconciliation activities automatically after failover and ensure reconciliation activities continue without disruption.

### Kubernetes design principle #3: Self-healing

The nature of Controllers constantly observing and comparing the desired state of the cluster with the current state of Kubernetes objects means any drift in cluster configuration will be detected immediately and mitigated. The cluster will self-heal by monitoring for unexpected cluster configuration drift, such as a hardware failure causing the number of active Pods to decline. Since Controllers are continuously monitoring the cluster's desired state, they can take care of configuration drift by continually changing the cluster's state to ensure it matches the desired configuration.

### Kubernetes design principle #4: Atomicity

Controllers are designed to handle interruptions during reconciliation activities. A distributed system should be designed to handle failures in any component, including the control plane, network connectivity issues, hardware failures, node reboots, etc. Controllers will always be capable of picking up the reconciliation steps from wherever the interruption occurred, regardless of which actions were missed or half-finished. By comparing the current and desired states, Controllers will know what steps must be taken to continue the reconciliation.

[[Custom Controllers]]
