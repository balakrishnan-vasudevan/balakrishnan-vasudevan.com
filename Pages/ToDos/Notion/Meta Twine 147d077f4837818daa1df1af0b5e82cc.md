# Meta Twine

Tags: cluster-management
Category: Articles
Company: Facebook
Status: Not started
URL: https://medium.com/@tahir.rauf/twine-metas-unified-cluster-management-system-part-1-3d584441d1ee

# Twine — Meta’s Unified Cluster Management System — Part 1

![https://miro.medium.com/v2/resize:fill:44:44/1*YQuAvuPxBzFg_-rj8SkOYQ.png](https://miro.medium.com/v2/resize:fill:44:44/1*YQuAvuPxBzFg_-rj8SkOYQ.png)

[Tahir Rauf](https://medium.com/@tahir.rauf?source=post_page---byline--3d584441d1ee--------------------------------)

·

[Follow](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fsubscribe%2Fuser%2F1d277ab3f844&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40tahir.rauf%2Ftwine-metas-unified-cluster-management-system-part-1-3d584441d1ee&user=Tahir+Rauf&userId=1d277ab3f844&source=post_page-1d277ab3f844--byline--3d584441d1ee---------------------post_header-----------)

5 min read

·

Oct 9, 2024

[https://miro.medium.com/v2/resize:fit:700/0*tqI_CrYpUAp6YiKL](https://miro.medium.com/v2/resize:fit:700/0*tqI_CrYpUAp6YiKL)

This blog post is my notes of Meta’s [Twine: A Unified Cluster Management System for Shared Infrastructure](https://www.usenix.org/system/files/osdi20-tang.pdf) paper.

# Abstract

Twine helped convert the infrastructure from a collection of siloed pools of customized machines dedicated to individual workloads, into a large-scale shared infrastructure with fungible hardware (no longer specialized for specific tasks or workloads).

Twine takes some decisions counter to common practice. For example,

- Unlike conventional practice of deploying an isolated control plane per cluster, Twine scales a single control plane to manage one million machines across all data centers in a geographic region and transparently move jobs across clusters.
- Rather than prioritizing stacking workloads on big machines to increase utilization, Twine deploy power-efficient small machines outfit with a single CPU and 64GB RAM to achieve higher performance per watt.

**Note:** A single Kubernetes cluster is typically designed to manage up to *5,000 nodes* (machines), as per Kubernetes’ official scalability limits. Additionally, it can support *150,000 total pods* and *300,000 total containers* running simultaneously.

# 1. Introduction

Cluster management systems help organizations utilize shared infrastructure effectively through automation, standardization and economics of scale.

- **automation**: ability to automatically handle routine and complex tasks without requiring manual intervention. *Task allocation:* Automatically determining where and when to run specific jobs or applications based on resource availability.*Failure recovery:* Automatically detecting failures and restarting applications or migrating them to healthy nodes.*Scaling:* Automatically adding or removing nodes, or adjusting resources as workload demand fluctuates.
- **Standardization:** refers to establishing consistent methods and practices for deploying, managing, and operating workloads across the infrastructure.
- **Economies of scale:** refer to the cost advantages and efficiency gains that arise when an organization operates at a large scale, typically by consolidating resources into a shared infrastructure.

Existing systems however, still have limitations in supporting large-scale shared infrastructure.

- They usually focus on isolated clusters, with limited support for cross-cluster management as an afterthought. These silos may strand unused capacity in clusters.
- They usually prefer big machines with more CPUs and memory in order to stack workloads and increase utilization. If not managed well, underutilized big machines waste power, often a constrained resource in data centers.
- They rarely allow an application to provide its preferred custom hardware and OS settings to shared machines. Lack of customization may negatively impact application performance on shared infrastructure.

Twine is Facebook’s cluster management system. It a) scales a single Twine control plane to manage one million machines across data centers in geographic region while providing high reliability and performance guarantees b) supports workload-specific customization, which allows applications to run on shared infra without sacrificing performance or capabilities.

Twine packages applications into Linux containers and manage the lifecycle of machines, containers, and applications.

## A single control plane to manage one million machines

`A region` consists of multiple data centers, and a data center is usually divided into `clusters` of tens of thousands of machines connected by a high-bandwidth network. With Kubernetes, an isolated control plane per cluster results in stranded capacity and operational burden because workloads cannot easily move across clusters.

Twine scaled a single Twine control plane to manage one million machines across all data centers in a region.

## Host Level Customizations

Hardware and OS settings may significantly impact application performance. Twine leverages `entitlements` , a quota system to handle hardware and OS tuning. For example, an entitlement for business unit may allow it to use up to 30K machines. Each entitlement is associated with `host profile` , a set of host customizations that the entitlement owner can tune. Out of a shared machine pool, Twine allocates machines to entitlements and switches host profiles accordingly.

## Power Efficient machines

Twine adopts small machines with a single CPU and 64GB RAM because:

a) Small machines provide higher performance per watt.

b) They allow for better utilization of resources, as large machines often lead to underutilized resources when workloads don’t require their full capacity.

c) Unlike public cloud providers that need to support diverse customer requirements, Twine only needs to optimize for internal workloads.

d) It is challenging to stack large workloads effectively on big machines.

## Shared infrastructure

`twshared` is Twine’s large scale shared infrastructure. All new compute capacity lands only in twshared. Twine has achieved 100% shared infrastructure consolidation.

# Glossary

**`Shared infrastructure`** a common pool of resources to run any workload.

**`Workload-specific customizations`** refer to the ability for individual applications or workloads to define their own hardware, operating system (OS), and resource management requirements to optimize performance in a shared infrastructure environment. Traditional cluster management systems often lack this flexibility, leading to inefficiencies or reduced performance for certain workloads.

`A **Task**` is one instance of an application deployed in a container, and a **job** is a group of tasks of the same application.

**`TaskControl API`** is a specialized interface that allows applications to collaborate with Twine on managing the lifecycle of tasks in a cluster. This API enables applications to provide input on key decisions regarding task operations, such as when to restart, move, or stop a task. The aim of the TaskControl API is to ensure that lifecycle operations, like upgrades or maintenance, do not negatively impact the availability or reliability of the applications.

**`host profile`** a set of host customizations that the entitlement owner can tune.

**`twshared`** is Facebook’s shared compute pool within the Twine system

**NOTE:** Twine Scheduler = Kubernetes Controller
Twine Allocator = Kubernetes Scheduler

# Summary

Twine, Facebook’s cluster management system, transformed the company’s infrastructure from siloed, customized machine pools into a unified, large-scale shared infrastructure. It diverges from traditional practices by managing over a million machines across data centers with a **single control plane**, which allows workloads to move seamlessly between clusters. Additionally, Twine emphasizes **power efficiency** by deploying small machines (single CPU and 64GB RAM), which provide higher performance per watt and better resource utilization than larger machines.

Unlike conventional systems, Twine supports **workload-specific customizations**, enabling applications to adjust hardware and OS settings to optimize performance without sacrificing capabilities. This is achieved through **entitlements**, a quota system that allocates machines dynamically, and **host profiles**, which manage machine-specific customizations.

Twine’s **twshared** infrastructure serves as the consolidated compute pool for all workloads, achieving nearly 100% infrastructure consolidation. Its **TaskControl API** allows applications to collaborate with the system to manage lifecycle events, ensuring that updates and maintenance do not negatively affect application availability. Overall, Twine’s approach improves performance, flexibility, and efficiency, enabling Facebook to run diverse workloads on shared, dynamically managed infrastructure.

# References

[Twine: A Unified Cluster Management System for Shared Infrastructure](https://www.usenix.org/system/files/osdi20-tang.pdf)