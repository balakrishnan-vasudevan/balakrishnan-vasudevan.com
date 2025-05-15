https://www.linkedin.com/pulse/basics-chaos-engineering-ganesh-ghag/

_“Chaos engineering is the discipline of experimenting on a software system in production in order to build confidence in the system's capability to withstand turbulent and unexpected conditions” –Wikipedia_

Chaos engineering tests an application’s resilience. **Resilience is the ability of a system to provide and maintain acceptable level of services in the face of faults and challenges.**

Given a steady state load of end users on the application, chaos engineering attempts to randomly cause faults in the application deployment system and then measures, the extent of failures and latencies experienced by the end users of the application, during the time interval of the chaos. The application can be monitored, to find the critical services, root causes of failures and fixes can be applied in the form of deployment parameters, config changes or even code chages, to ensure, that the application’s resilience increases.

Since chaos engineering does not concern with application’s functional defects, neither with negative testing nor with load testing, the main environment variables that are tested in chaos engineering are resources such as cpu, memory, network and IO. Inducing failures related to cpu and memory starvation, network outages and storage failures are some primary usecase for chaos engineering.

**Resource faults can occur at numerous levels due to the following complexities of cloud native deployments:**

- Microservices devops based architctures: tens of unique microservices, hundreds of instances (pods) of services
- Highly virtualized stacks on infra, k8s worker nodes host pods which host containers, which run processes
- Resources like cpu, memory and storage are pooled, virtualized and dynamically allocated/deallocated within a k8s cluster
- A few instances of a service can overdraw cpu, memory and storage, thereby cannibalizing these resources from other pods
- Network usage is now, shared by applications with stack compoments like istio service mesh, sidecar proxies. K8s networking