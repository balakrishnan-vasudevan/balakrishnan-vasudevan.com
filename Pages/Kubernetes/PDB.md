There are three main fields in PDB:

- `.spec.selector` in PDB denotes the set of pods on which it is applied. It is the same as the application controller's label selectors.
- `.spec.minAvailable` denotes the number of pods that must be available after eviction. It can be an absolute number or percentage.
- `.spec.maxUnavailable` denotes the number of pods that can be unavailable after eviction. It can be an absolute number or percentage.

**One can only specify the minAvailable or maxUnavailable field in a single pod disruption budget, not both.**


```
# pdb1.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pdb-minavail
spec:
  minAvailable: 5
  selector:
    matchLabels:
      app: nginx
```


- Now, increase the existing pdb **minAvailable field to 6** and drain the node to see what happens.

```
# pdb1.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: pdb-minavail
spec:
  minAvailable: 6
  selector:
    matchLabels:
      app: nginx
```

```
kubectl apply -f pdb1.yaml
kubectl get pdb
```

[![Image description](https://res.cloudinary.com/practicaldev/image/fetch/s--JZYvBjCF--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gb3q420c599pmx2tykwz.JPG)](https://res.cloudinary.com/practicaldev/image/fetch/s--JZYvBjCF--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gb3q420c599pmx2tykwz.JPG)

- Once again, drain the cluster node.

```
k drain <node_name> --ignore-daemonsets  --delete-emptydir-data
```

[![Image description](https://res.cloudinary.com/practicaldev/image/fetch/s--T2wFSGKf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dqjnxsp9lhe2vh55y2dv.JPG)](https://res.cloudinary.com/practicaldev/image/fetch/s--T2wFSGKf--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dqjnxsp9lhe2vh55y2dv.JPG)  
You will observe that the drain will not be completed, and eviction API will retry to evict pods until it can reschedule on another node and throws an **error: cannot evict pod as it would violate the pod’s disruption budget.**

But why has this happened? **Because the minimum available pods in pdb are 6 and the other node can only schedule 5 pods according to its resource capacity.** As mentioned, eviction API gives PDB priority, so to make a minimum of 6 pods available, it will not drain the node and run the pods on it.

[![Image description](https://res.cloudinary.com/practicaldev/image/fetch/s--tvwxoHHj--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ti51t8tinngqh3q3og5l.JPG)](https://res.cloudinary.com/practicaldev/image/fetch/s--tvwxoHHj--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ti51t8tinngqh3q3og5l.JPG)

Although my node will mark SchedulingDisabled, it's not drained.

[![Image description](https://res.cloudinary.com/practicaldev/image/fetch/s--GBcN0qgH--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w4ntfxn3lrwy07bpzr5j.JPG)](https://res.cloudinary.com/practicaldev/image/fetch/s--GBcN0qgH--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w4ntfxn3lrwy07bpzr5j.JPG)

- Delete the pdb and uncordon the node.

```
kubectl delete pdb pdb-minavail
```

Use Case: 4

Reduce the **maxUnavailable field to 2**, which makes 6 pods run all the time. Now if you drain the node, **use case 2** scenario will happen. Node draining will be incomplete, and pods will not be evicted completely by giving weightage to PDB.

Use Case: 5

Now, what if I set **maxUnavailable to 0?** This is equal to the setting of **minAvailable to 100%**. It will be ensured that none of your pods will be disrupted when voluntary disruptions occur.

When not to use PDB?

There are certain cases when pdb cannot be used, such as:

- It doesn’t work for involuntary disruptions
- In voluntary disruptions, it will not work when pods or deployments get deleted.
- Two PDBs can not work together on the same resource.
- PDBs don’t work on a single pod or replica of deployment.