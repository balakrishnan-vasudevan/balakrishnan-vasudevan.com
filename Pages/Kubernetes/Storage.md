

## Storage Class
- You need a driver for every storage type you want to use in your K8S cluster
- Examples could be EBS, Ceph etc.
- The StorageClass component may have been called “**Add a Storage Type to the Cluster**”
- There are available two binding modes: **Immediate (**default binding mode**)** and **WaitForFirstConsumer**

**WaitForFirstConsumer** binding mode is available for cloud-based storage (_AWS_, GCP, Azure).

**WaitForFirstConsumer** mode: A **Persistent Volume** will be provisioned when a **Pod** attempts to use the **Persistent Volume Claim**.

**Immediate** mode: A Persistent Volume will be provisioned when a Persistent Volume Claim is created.

## PVC vs PV
[[PVC - PV]]

Imagine that you have storage with **15 TB** of space. You will need to run 3 different projects on the storage. You can split your storage into 3 different **persistent volumes**, and each project can have 5 TB of disk space at most.

The developer of each project can use 5 TB of disk space for their [DTAP](https://en.wikipedia.org/wiki/Development,_testing,_acceptance_and_production) environments. They will have to use the **Persistent Volume Claim** component to ask for the disk space they need. This is **static** provisioning.

A lot of clusters on the cloud tend to use **dynamic** provisioning, as it is a flexible way to provide sufficient disk space.

For **dynamic** provisioning, **you don’t need** to create a **Persistent Volume** manually. The developer of each project can request disk space via the **Persistent Volume Claim** component. Kubernetes will create a **persistent volume** for you automatically. They must define the storage class they want to use.