
In Kubernetes, several resources are used to manage and control application deployment and scaling. Each of these resources serves a specific purpose, and they can be combined to create a robust and scalable application architecture. Here, I'll provide an overview of Deployment, StatefulSet, ReplicaSet, Service, and PersistentVolumeClaim (PVC) in Kubernetes, along with sample configurations for each.

1. [[Deployment, StatefulSet, RS, Service, PVC]]
2. [[Storage]]
3. [[Controllers]]
4. Webhooks
		In Kubernetes, webhooks are mechanisms for extending the functionality of the Kubernetes API server by allowing custom code to be executed when certain events occur. Webhooks are commonly used for validating, mutating, or otherwise processing resource objects at various stages of their lifecycle. There are different types of webhooks used in Kubernetes, each with its specific use cases. [[Webhooks]]
3. Ingress
		In Kubernetes, Ingress is an API object that manages external access to services within the cluster. It provides a way to configure the HTTP and HTTPS routing rules for traffic entering the cluster. There are different types of Ingress controllers, and each serves specific use cases.  [[Ingress]]
4. [[Access Control]]
5. [[Service mesh]]



 Master Node (Control Plane) Components  
  
🔹 API Server (kube-apiserver)  
- Central control unit, processes API requests, scalable, communicates with etcd.  
  
🔹 Cloud Controller Manager  
- Integrates with cloud APIs, manages Node, Route, and Service controllers, supports independent feature releases.  
  
🔹 etcd  
- Distributed key-value store, stores cluster state, configuration, and metadata, consistent, immutable.  
  
🔹 Scheduler (kube-scheduler)  
- Decides pod placement based on resources, affinity rules, taints, tolerations.  
  
🔹 Controller Manager  
- Manages core controllers, handles lifecycle events like garbage collection, monitors cluster state.  
  
2. Worker Node Components  
  
🔸 Kubelet  
- Manages containers on the node, ensures health, communicates with API server.  
  
🔸 kube-proxy  
- Handles networking, routes traffic to pods, maintains service-to-pod IP translations.  
  
🔸 Container Runtime Interface (CRI)  
- Manages container lifecycle, image pulls, supports runtimes like Docker, containerd.  
  
🔸 Pods  
- Smallest deployable units, contain containers, share network and storage resources.  
  
This architecture ensures efficient, scalable, and reliable management of containerized applications.


![[Pasted image 20250514104623.png]]

