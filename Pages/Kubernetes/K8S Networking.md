
Kubernetes dictates the following requirements on any networking implementation:

- all Pods can communicate with all other Pods without using _network address translation_ (NAT).
- all Nodes can communicate with all Pods without NAT.
- the IP that a Pod sees itself as is the same IP that others see it as.

Given these constraints, we are left with four distinct networking problems to solve:

1. Container-to-Container networking
2. Pod-to-Pod networking
3. Pod-to-Service networking
4. Internet-to-Service networking

Container-to-Container 
In terms of Docker constructs, a Pod is modelled as a group of Docker containers that share a network namespace. Containers within a Pod all have the same IP address and port space assigned through the network namespace assigned to the Pod, and can find each other via localhost since they reside in the same namespace. We can create a network namespace for each Pod on a virtual machine. This is implemented, using Docker, as a “Pod container” which holds the network namespace open while “app containers” (the things the user specified) join that namespace with Docker’s –net=container: function.

![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pod-namespace.png)

Figure 3. A network namespace per pod.
Applications within a Pod also have access to shared volumes, which are defined as part of a Pod and are made available to be mounted into each application’s filesystem.

## Pod-to-Pod
In Kubernetes, every Pod has a real IP address and each Pod communicates with other Pods using that IP address. The task at hand is to understand how Kubernetes enables Pod-to-Pod communication using real IPs, whether the Pod is deployed on the same physical Node or different Node in the cluster.
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pods-connected-by-bridge.png)

Figure 5. Connecting namespaces using a bridge.

## Pod-to-Pod, Same Node
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pod-to-pod-same-node.gif)

Pod 1 sends a packet to its own Ethernet device `eth0` which is available as the default device for the Pod. For Pod 1, `eth0` is connected via a virtual Ethernet device to the root namespace, `veth0` (1). The bridge `cbr0` is configured with `veth0` a network segment attached to it. Once the packet reaches the bridge, the bridge resolves the correct network segment to send the packet to — `veth1` using the ARP protocol (3). When the packet reaches the virtual device `veth1`, it is forwarded directly to Pod 2’s namespace and the `eth0` device within that namespace (4). Throughout this traffic flow, each Pod is communicating only with `eth0` on `localhost` and the traffic is routed to the correct Pod. The development experience for using the network is the default behaviour that a developer would expect.

## Pod-to-Pod, Across Nodes
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pod-to-pod-different-nodes.gif)

Figure 7. Packets moving between Pods on different Nodes.
Figure 7 begins with the same request as in Figure 6, except this time, the destination Pod (highlighted in green) is on a different Node from the source Pod (higlighted in blue). The packet begins by being sent through Pod 1’s Ethernet device which is paired with the virtual Ethernet device in the root namespace (1). Ultimately, the packet ends up at the root namespace’s network bridge (2). ARP will fail at the bridge because there is no device connected to the bridge with the correct MAC address for the packet. On failure, the bridge sends the packet out the default route — the root namespace’s `eth0` device. At this point the route leaves the Node and enters the network (3). We assume for now that the network can route the packet to the correct Node based on the CIDR block assigned to the Node (4). The packet enters the root namespace of the destination Node (`eth0` on VM 2), where it is routed through the bridge to the correct virtual Ethernet device (5). Finally, the route completes by flowing through the virtual Ethernet device’s pair residing within Pod 4’s namespace (6). Generally speaking, each Node knows how to deliver packets to Pods that are running within it. Once a packet reaches a destination Node, packets flow the same way they do for routing traffic between Pods on the same Node.

## Pod-to-service
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pod-to-service.gif)

Figure 8. Packets moving between Pods and Services.


## Service to Pod
  
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/service-to-pod.gif)

Figure 9. Packets moving between Services and Pods.


## Node to internet
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/pod-to-internet.gif)

Figure 10. Routing packets from Pods to the Internet.

## Load balancer to service
![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/internet-to-service.gif)

Figure 11. Packets sent from the Internet to a Service.

## Ingress controller


![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/ingress-controller-design.png)

Figure 12. Design of an Ingress Controller.


## Ingress to service

![](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/ingress-to-service.gif)

Figure 13. Packets sent from an Ingress to a Service.