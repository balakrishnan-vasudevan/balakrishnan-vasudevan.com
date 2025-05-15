In Kubernetes, several resources are used to manage and control application deployment and scaling. Each of these resources serves a specific purpose, and they can be combined to create a robust and scalable application architecture. Here, I'll provide an overview of Deployment, StatefulSet, ReplicaSet, Service, and PersistentVolumeClaim (PVC) in Kubernetes, along with sample configurations for each.

1. Deployment:
   - Purpose: Deploy and manage stateless applications with features like rolling updates and rollbacks.
   - Sample Configuration:
   
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: sample-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: sample-app
     template:
       metadata:
         labels:
           app: sample-app
       spec:
         containers:
         - name: sample-container
           image: nginx:latest
   ```

2. StatefulSet:
   - Purpose: Deploy and manage stateful applications with stable network identities and ordered scaling.
   - Sample Configuration:
   
   ```yaml
   apiVersion: apps/v1
   kind: StatefulSet
   metadata:
     name: sample-statefulset
   spec:
     replicas: 3
     serviceName: "sample-service"
     selector:
       matchLabels:
         app: sample-app
     template:
       metadata:
         labels:
           app: sample-app
       spec:
         containers:
         - name: sample-container
           image: nginx:latest
   ```

3. ReplicaSet:
   - Purpose: Ensures that a specified number of pod replicas are running at all times.
   - Sample Configuration:

   ```yaml
   apiVersion: apps/v1
   kind: ReplicaSet
   metadata:
     name: sample-replicaset
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: sample-app
     template:
       metadata:
         labels:
           app: sample-app
       spec:
         containers:
         - name: sample-container
           image: nginx:latest
   ```

4. Service: [[Services]]
   - Purpose: Expose your application to the network and load balance traffic to pods.
   - Sample Configuration for a LoadBalancer Service:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: sample-service
   spec:
     selector:
       app: sample-app
     ports:
     - protocol: TCP
       port: 80
       targetPort: 80
     type: LoadBalancer
   ```

5. PersistentVolumeClaim (PVC): [[PVC - PV]]
   - Purpose: Request and manage storage for your pods.
   - Sample Configuration:

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: sample-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 1Gi
   ```

These are the fundamental resources in Kubernetes for deploying, scaling, and exposing applications. Depending on your specific use case, you can combine these resources to create complex and resilient application architectures in Kubernetes.

Deployment vs StatefulSet for stateful applications

|Deployment|StatefulSet|
|---|---|
|all replicas are interchangeable — all pods have random DNS names and are unable to hold unique data on persistent storage|all replicas have specific name — {StatefulSet name}-index|
|common persistent storage for all replicas — all replicated pods use the same PVC and the same volume|unique persistent storage for each replica|
|PVC needs to be created for the deployment|PVC is auto-created for each replica but is not autodeleted (well, this feature is alpha in Kubernetes 1.23)|
||headless service is necessary to create a stable DNS name for each pod|
|load-balancing service is necessary to access pods|As opposed to the Deployment, the StatefulSet creates pods directly. Due to this issue¹ automatic rollback in case of failed upgrade is not possible.|
|implemented with ReplicaSet. When upgrading, a new ReplicaSet is created, and pods are scaled up/down in new/old ReplicaSet based on the selected strategy. Rollback is supported by switching to old ReplicaSet|upgrades/terminations are done sequentially from the pod with the biggest index number to the pod with index number|
|Use Case: Stateless services|Stateful services with multiple replicas, is that one case where the StatefulSet shines. A typical use case is a legacy application that supports clustering, where each replica needs to hold unique data. Good examples are:|

SQL databases, continuously making all replicas the same The storage systems like Elasticsearch or CEPH, spreading copies of data across the cluster, making each node unique. | | | |



![[Untitled (1).png]]

![[Untitled.png]]