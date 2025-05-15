
Source: https://yuminlee2.medium.com/kubernetes-security-contexts-e54624e29d52

Kubernetes security contexts **define runtime security settings for pods or containers**. If no security context is specified, Kubernetes applies a default one, which may not meet requirements. You can add `**_securityContext_**` **field** in the **pod manifest file** to **set up security contexts** at the pod or container level. **Pod-level** settings **inherited by all containers** and **container-level** settings **only** **applying to that container**. **Container-level** settings always **override pod-level settings**. The `**_capabilities_**` field **adds specific capabilities to a container’s security context** at the **container level,** not possible at the pod level.

![[Pasted image 20240116161055.png]]

Adding security context at pod level makes all containers inherited by all containers in that pod.



```
apiVersion: v1  
kind: Pod  
metadata:  
	name: mypod  
spec:  
	securityContext:  
		runAsUser: 1000  
		fsGroup: 2000  
	containers:  
	- name: container1  
	  image: nginx  
	- name: container2  
	  image: busybox
```

runAsUser and fsGroup properties set to 1000 and 2000 respectively. Therefore, both containers will run as the user with UID 1000 and have access to the group with GID 2000.

## Container level setting

```
apiVersion: v1  
kind: Pod  
metadata:  
name: mypod  
spec:  
containers:  
	- name: container1  
	  image: nginx  
	  securityContext:  
		runAsUser: 1000  
	- name: container2  
	  image: busybox  
	  securityContext:  
		runAsUser: 2000
```

each container in the pod has its own security context specified with the `securityContext` field. The runAsUser field is specified with a different value for each container. container1 runs with user ID 1000, while container2 runs with user ID 2000, and there is no inheritance or sharing of the security context between the two containers.

## Pod and Container level contexts

```
apiVersion: v1  
kind: Pod  
metadata:  
	name: mypod  
spec:  
	securityContext:  
		runAsUser: 1000  
	containers:  
	- name: my-container  
	  image: my-image  
	  securityContext:  
		runAsUser: 2000
```

the pod-level `securityContext` sets the runAsUser value to 1000, while the container-level `securityContext` sets the runAsUser value to 2000, which overrides the pod-level security context. This means that **the container will run with the user ID of 2000**, regardless of the pod-level setting.

## Capabilities to containers

`capabilities` **can NOT be specified at the pod level**.
```
apiVersion: v1  
kind: Pod  
metadata:  
	name: mypod  
spec:  
	containers:  
	- name: my-container  
	  image: my-image  
	  securityContext:  
		capabilities:  
			add: ["NET_ADMIN"]
```

the NET_ADMIN capability is added to the `securityContext` of the my-container container.