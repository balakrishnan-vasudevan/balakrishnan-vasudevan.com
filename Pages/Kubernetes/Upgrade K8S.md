- Upgrade all infrastructural components to a release that supports your current EKS version and the new EKS version (see article)
    
- Update all nodes to the latest point release (re-deploy same node configuration in eksctl with a different name)
    
- Update EKS masters (aka, go into AWS console and tell it to upgrade)
    
- Update all infrastructural components again to a new version (if needed/desired) that is the latest release supporting your new current EKS version
    
- Rollout new node via node groups that are for the new version of EKS you are on
    
- Perform a trial migration to the new nodes slowly (move ingresses and services gently and one at a time, watching monitoring)
    
- Remove old nodes and node groups
    
- Validate that your services still work, namely new deploys. During EKS Upgrades, the APIVersion objects are often auto-upgraded on your existing objects when deprecations occur. Doing a re-deploy of a service may surface a failure in the kubectl/helm command and require you to update your objects/charts to support the new version.
    
- Repeat all these steps for each version you wish to update. **YOU MUST DO ALL OF THEM ONE AT A TIME DO NOT SKIP ANY STEPS** for zero downtime.
    

In regards to your service, doing a blue/green type deployment/pivot... you could do one of the following...

- Spin up an duplicate in a separate namespace, and "takeover" the ingress from one namespace to another, pivoting traffic
    
- Using an ingress controller that supports "canary" deploys and use the similar as above, and slowly transition traffic over gently. Eg: [https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#canary](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#canary)
    
- Spin up a completely new cluster on the new version of EKS, and pivot traffic over with a DNS switchover