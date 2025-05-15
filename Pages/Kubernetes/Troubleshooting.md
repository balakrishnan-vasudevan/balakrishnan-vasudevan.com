
# Pending Pods
## Causes:
- **Resource Constraints:** If there’s insufficient CPU, memory, or another resource on the available nodes, the pod won’t be scheduled.
- **Taints and Tolerations:** Nodes might have taints, and unless a pod has a matching toleration, it won’t be scheduled on that node.
- **Storage Issues:** A pod might be waiting for a Persistent Volume to be attached.
- **Node Selector & Affinity:** If the pod has specific node selectors or affinity rules, and no nodes match those rules, it will stay in the pending state.
- **Network Issues:** If there’s a configuration issue or other problems with the network, it might prevent the pod from starting.
## How to troubleshoot?
$ kubectl get pods --all-namespaces | grep Pending
$ kubectl describe pod <POD_NAME> -n <NAMESPACE>
- **Node Resource Utilization:** Check the resource utilization of nodes.

$ kubectl describe node <NODE_NAME>

- **Pod Resource Requests and Limits:** Review the resource requests and limits set on the pods and deployments. It’s possible that the requests are too high, making it challenging for the scheduler to find a suitable node.
- Check for ResourceQuotas and LimitRange: It’s possible that a `ResourceQuota` or `LimitRange` in a namespace is preventing the pod from being scheduled due to resource constraints.

$ kubectl describe resourcequota -n <NAMESPACE>  
$ kubectl describe limitrange -n <NAMESPACE>


## **Taints and Tolerations**

- Identify and describe the pending pods: Check the pod’s details to see if there are scheduling issues related to taints.

$ kubectl get pods --all-namespaces | grep Pending  
$ kubectl describe pod <POD_NAME> -n <NAMESPACE>

- **Check Node Taints:** List all nodes and their taints with:

$ kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.taints}{"\n"}{end}'

- **Review Pod Tolerations**: Check if the pod has any tolerations set. This can be done by describing the pod or checking its YAML.

$ kubectl get pod <POD_NAME> -n <NAMESPACE> -o=jsonpath='{.spec.tolerations}'

- Modify Taints or Tolerations for Node or Pod based on the above analysis

## **Storage Issues**

- Identify and describe the pending pods: Check the pod’s details to see if there are scheduling issues related to taints.

$ kubectl get pods --all-namespaces | grep Pending  
$ kubectl describe pod <POD_NAME> -n <NAMESPACE>

- Validate PVC/PV/StorageClass:

$ kubectl get pvc  
$ kubectl get pv  
$ kubectl get storageclass

- Review Volume Access Mode: Ensure that the volume mode (Filesystem or Block) matches between the PVC and PV. Verify that the access mode set in the PVC (e.g., ReadWriteOnce, ReadOnlyMany, ReadWriteMany) is compatible with the provisioned PV.

## **Node Selector & Affinity**

- Identify and describe the pending pods: Check the pod’s details to see if there are scheduling issues related to taints.

$ kubectl get pods --all-namespaces | grep Pending  
$ kubectl describe pod <POD_NAME> -n <NAMESPACE>

- Review Node Selectors:

$ kubectl get pod <POD_NAME> -o=jsonpath='{.spec.nodeSelector}'

- Verify Node Labels:

$ kubectl get nodes --show-labels

- Examine the pod’s affinity and anti-affinity rules within its specification. Check both `.spec.affinity.nodeAffinity` and `.spec.affinity.podAffinity` / `.spec.affinity.podAntiAffinity`. Also ensure there are nodes that match the `requiredDuringSchedulingIgnoredDuringExecution` or `preferredDuringSchedulingIgnoredDuringExecution` affinity rules.

## **Network Issues**

- Identify and describe the pending pods: Check the pod’s details to see if there are scheduling issues related to taints.

$ kubectl get pods --all-namespaces | grep Pending  
$ kubectl describe pod <POD_NAME> -n <NAMESPACE>

- Check Pod IP Address: Ensure the pod received an IP address, which would indicate it’s correctly integrated into the network.
- DNS Resolution: If the pod is having issues connecting to services by name, there might be DNS resolution issues. Test DNS lookup from within the pod

$ kubectl exec -it <POD_NAME> -- nslookup kubernetes.default

- Check Network Policies: Review any network policies that might be restricting traffic to or from the pod

$ kubectl get networkpolicies

![[Pasted image 20250513093842.png]]






![[dac10c60ec5d2fe6bd3d3f8736cf0ce0 1.pdf]] 


[[Production issues and resolution]]
