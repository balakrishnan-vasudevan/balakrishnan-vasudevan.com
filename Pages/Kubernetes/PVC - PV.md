In Kubernetes, both PVC (PersistentVolumeClaim) and PV (PersistentVolume) are used to manage storage resources for your applications, but they serve different purposes.

1. PersistentVolume (PV):
   - A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by the administrator.
   - It represents physical storage resources in the cluster, such as a disk on a node, a network-attached storage device, or cloud-based storage.
   - PVs are created and managed separately from application pods, and they are meant to be a cluster-wide resource.
   - PVs can have different access modes (e.g., ReadWriteOnce, ReadOnlyMany, ReadWriteMany) and can be pre-allocated or dynamically provisioned.

2. PersistentVolumeClaim (PVC):
   - A PersistentVolumeClaim (PVC) is a request for storage by a user or application.
   - It is used by developers to request access to a specific amount and access mode of storage that matches their application's requirements.
   - PVCs are created within the namespace of the application and are used by pods to request the specific storage they need.
   - PVCs are bound to PVs by the Kubernetes control plane. When a PVC is created, Kubernetes attempts to find an available PV that matches the PVC's requirements.

The relationship between PVCs and PVs is that a PVC requests a specific amount of storage with certain access mode requirements, and the Kubernetes control plane, if properly configured, binds the PVC to an available PV that meets the criteria. Once bound, the pod can use the PVC to access the underlying storage.

Here is an example of a PVC and PV:

PersistentVolume (PV) example:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /my/local/directory
```

PersistentVolumeClaim (PVC) example:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

In this example, the PVC "my-pvc" requests 5Gi of storage with a ReadWriteOnce access mode. If there is a suitable PV available, it will be bound to this PVC, and the PVC can then be mounted in a pod.