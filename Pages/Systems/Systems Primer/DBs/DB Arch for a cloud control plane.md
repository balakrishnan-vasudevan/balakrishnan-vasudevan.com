https://www.linkedin.com/pulse/database-architecture-cloud-control-plane-artem-livshits?utm_source=share&utm_medium=member_ios&utm_campaign=share_via

I work on the database for Nutanix control plane.  A key problem we had to solve was to design a control plane that can operate a distributed cloud consisting of multiple data centers deployed in distant locations.  To accomplish that, the control plane needs a database that can manage globally distributed data.

Obviously, Nutanix is not the first one to tackle these problems.  However there are multiple solutions with different trade-offs and we needed to come up with a solution that meets our requirements.  Would we need to make the global database eventually consistent or strictly consistent? Could we just run a Paxos group across the entire cloud?  Could we just use Google Cloud Spanner as the cloud control plane database? Those are some of the questions that we had to answer to agree on how the database for the cloud control plane is going to look like.

## Control Plane Requirements

The requirements for the control plane availability are the following.  We have a notion of availability zone (AZ), where each AZ needs to be able to operate independently, even if other AZs fail or become unreachable (partitioned).  What it means for the control plane is that the control plane in each AZ must be available to control operations in that AZ, even if the rest of the cloud fails or gets partitioned from the AZ.  To give a concrete example of a control plane operation, let's consider creating a virtual machine (VM) in an AZ: even if the AZ cannot communicate with the rest of the cloud, a user should be able to create a VM in this AZ.

What does the availability requirement mean for the control plane database?  Let's consider a simplified workflow of VM creation. At a high level, the VM creation operation would do the following:

1. Authenticate the user and check that the user has the permissions to create a VM.
2. Find out which tenant the user belongs to.
3. Find a physical machine within the AZ that has enough resources to run the new VM.
4. Create VM and corresponding satellite entities (virtual disks, virtual NICs, etc.).

From the database point of view here are the control plane database operations that need to happen at each step:

1. Get user records that contain authentication information.
2. Get tenant records that contain billing, quotas, policies, etc.
3. Get host and VM records to calculate available resources.
4. Create VM record for the new VM.

The host and VM control plane records are local to the AZ, in the sense that they are neither required for other AZs’ operation nor need to survive AZ failure.  These records can be managed by a Paxos-based highly available database that runs in the same AZ; the database doesn't need to span multiple AZs.

The user records, on the other hand, are needed in every AZ and need to be available even if one or more AZs fail.  If they are not available in an AZ for read, most operations will fail in that AZ. So the database to manage these records needs to be globally available, such that all AZs can access the data even if they are disconnected from each other.

## Trade-offs and Solutions

According to the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem), for distributed data it's possible to provide only two guarantees out of the three: (C) consistency, (A) availability, (P) partition tolerance.  In particular, in the presence of network partitioning (the P of CAP), we need to decide whether we need the data to be globally consistent (i.e. any AZ would see exactly the same data) or available.  In the latter case it means that the data may be eventually consistent.

To practically apply the CAP theorem and understand the trade-offs for read operations and modification operations, we can use the notion of a strictly consistent "master" (e.g. represented by a quorum of participants, or provided as a service, or etc.).  By construction, any operation that is executed on the master is strictly consistent. Now, for operations that are initiated on each participant, if the participant is partitioned from the master the CAP theorem provides two choices:

C - consistency: fail the operation if cannot process the operation on the master

A - availability: process the operation using the participant's local database

These choices can be made independently for readers and writers; moreover they can be made tunable for each specific operation.  To achieve strict consistency, both readers and writers need to choose the option C; choosing the option A on either side would lead to various forms of eventual consistency.

For the global data that we currently need to support, we found the following trade-offs to work the best:

- for modification operations, we chose CP (consistency in case of partitioning) - modifications are always consistent, thus if AZ is partitioned from the master, modifications of global data will fail
- for read operations, AP (availability in case of partitioning) is the default - reads are always available, but if AZ is partitioned from the master, the data may be stale
- the application can force CP for reads - in that case, reads would fail if AZ is partitioned, but never give stale data (this can provide better experience when the read is done with the intention to write)

These trade-offs work very well for the global data that we have -- the data is not frequently changed and modifications can wait until the connectivity is restored.  This way we avoid complexities that arise from merging eventually consistent modifications. When we need to manage data that requires greater availability for modifications, we'll implement eventual consistency option for modification operations -- the actual merge logic may be fairly complex and application-specific, but for the database consumers it's just going to be a flag to set, the underlying replication and merge machinery is going to be handled by the database.

At this point people familiar with distributed systems would probably say "yup, the CAP theorem and eventual consistency have been known for a while".  That's true, and I wouldn't have bothered to write just about that -- there is plenty of discussion on the topic. What I find interesting is the discussions that our team had about practical consequences of CAP, which I think would be interesting to others as well.

## Does it Have to Be Eventually Consistent?

The most frequent point of contention was eventual consistency.  Eventual consistency adds complexity for service developers, so having a database that provides strict consistency would make service development easier.  Could we take advantage of some clever technology to build (or buy) a strictly-consistent highly-available globally distributed database to satisfy our requirements?

There are known ways to build strictly-consistent highly-available distributed databases (and there are a bunch of open source and commercial solutions available) using Paxos or other distributed consensus algorithms.  The obvious downside seems to be that a Paxos-based database requires a quorum (typically a majority) of participants to be available, while an eventually consistent database can be available even if a majority of participants fail.  But if we have many participants properly distributed across failure domains, we could make the probability of the whole quorum failure small enough for practical purposes. Thus for practical purposes we could build (or buy) a highly-available strictly-consistent globally distributed database.  But it actually doesn't work for our requirements.

The reason a strictly-consistent highly-available distributed database with a quorum of available participants cannot provide required availability in our scenarios is because of how we define availability.  The database is considered available as long as there is a quorum of participants available somewhere. But "being available somewhere" doesn't work for our AZ definition -- according to the independent operation requirements, the data needs to be available in each AZ, even if it's partitioned from the rest of AZs.

Let's consider a simple example.  Suppose we have three AZs: AZ1, AZ2 and AZ3, and we have a Paxos-based database that has three participants -- one in each AZ.  As long as any two AZs can form a quorum, the database can process operations and provide strict consistency guarantees. Now suppose, AZ3 is partitioned from AZ1 and AZ2, i.e. it cannot communicate with them.  AZ1 and AZ2 can still talk to each other, so they form a quorum and the database is available, but that doesn't help AZ3 -- it cannot reach the quorum and cannot process operations. Using our example, if we used such a database to store user records, AZ3's control plane wouldn't be able to authenticate any requests, rendering it unavailable.

Now, even though AZ3 is partitioned from the Paxos quorum, the database participant that runs in AZ3 probably has reasonably up-to-date copy of the user records, and could use it to authenticate requests.  But by doing that we give up strict consistency: the data in AZ3 can be different from the master data (i.e. the data that the quorum has consensus on). E.g. if a user changes their password in the database (modification processed and accepted by the quorum running in AZ1 and AZ2), for requests in AZ3 the old password needs to be used.  So from the user perspective even though the global database was modified, the latest modification may not be immediately globally visible, which is what eventual consistency is.

At this point, the discussion would often turn to Google Cloud Spanner -- they seem to have managed to build globally distributed strictly consistent database, so maybe we could do the same (build a similar solution or try to license Spanner's source code).  Google Cloud Spanner couldn't have worked around the CAP theorem, so they must've sacrificed one of the three. According to [this blog](https://cloud.google.com/blog/products/gcp/inside-cloud-spanner-and-the-cap-theorem), Google Cloud Spanner is technically a CP system (i.e. chooses consistency in case of partitioning), but according to their model the risk of partitioning is significantly lower than the risk of failing due to other reasons, so effectively Google Cloud Spanner is a CA system, i.e. it's strictly consistent and highly available, because the risk of partitioning can be ignored due to using their own super reliable networking infrastructure.

From that perspective, Google Cloud Spanner is not a pure software solution, using their networking infrastructure is essential to provide the guarantees they claim to provide.  In other words, even if we could somehow license Spanner's source code and ship it in our products, Spanner wouldn't be able to provide the same CA characteristics, because we don't control the environment that our products are running in.  If we'd used Spanner, it would've provided CP characteristics, which, as I pointed out above, don't satisfy the requirements of independent operation for AZ.

Ok, so running Spanner source code on some arbitrary infrastructure wouldn't work, but could we use Google Cloud Spanner as a service?  Google already has invested into infrastructure to make Google Cloud Spanner a globally distributed strictly consistent database that anyone can use.  But it doesn't work for our availability requirements, for the same reason Paxos doesn't. Google Cloud Spanner is considered available as long as it's available somewhere, but "available somewhere" doesn't work for our AZ definition -- we need data to be available in every AZ.

In a few cases, people wondered whether different ways of structuring services or APIs would have different availability / consistency characteristics.  E.g. if authentication is handled by some kind of "security service", then the control plane just needs to make a REST API call to the security service and doesn't need to worry about how the database is accessed.  This, however, doesn't change the tradeoffs -- if the "security service" doesn't run in every AZ, then some AZs would fail to authenticate requests, if partitioned from the "security service". Thus the "security service" must run in every AZ and have access to user records, and the global database that stores those records needs to have the characteristics described above.  So from the database perspective, the tradeoffs and requirements are the same, no matter how the service logic is structured.

## High Level Architecture

Now that the requirements and the trade-offs are fully understood, here is a high level architecture that satisfies the requirements:

Each AZ runs a Paxos-based highly available strictly consistent database.  The database is deployed to have no single point of failure. The database stores two kinds of data:

1. AZ-local data -- the data that is not needed for other AZs to operate (e.g. VM state)
2. Cloud-global data -- the data that is needed in every AZ to operate (e.g. authentication information)

For the AZ-local data, as the name implies, all the data is just stored in one AZ.  All access to AZ-local data is strictly consistent and goes through Paxos.

For the cloud-global data, each AZ's database also acts as a participant in global Paxos group that runs across all AZs.  Modification operations are strictly consistent and require a quorum across majority of AZs. Read operations can either be eventually consistent (default) and read from AZ's local copy of the data (which itself is highly available within AZ), or can be forced to be strictly consistent and read from the quorum.

Here is a picture that shows this database architecture in a cloud of three AZs:

![[Pasted image 20250316115540.png]]

From these discussions it becomes apparent that distributed service availability is largely defined by data availability.  The service could be one large piece of software or could be split into a bunch of tiny microservices, the APIs between components could be clean and elegant or could break all abstraction boundaries -- no matter what, the availability characteristics are defined by what data is available where.  I personally find it fascinating and that's why I'm so passionate about building databases -- data management is at the core of every service and largely defines service architecture.