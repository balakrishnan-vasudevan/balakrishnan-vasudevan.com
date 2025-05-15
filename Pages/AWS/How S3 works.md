#object-storage , #blob , #aws 
https://youtu.be/sc3J4McebHE 

![[Pasted image 20250330080403.png]]

S3 is an object storage service with an HTTP REST API. There is a frontend fleet with a REST API, a namespace service, a storage fleet that’s full of hard disks, and a fleet that does background operations. In an enterprise context we might call these background tasks “data services,” like replication and tiering. What’s interesting here, when you look at the highest-level block diagram of S3’s technical design, is the fact that AWS tends to ship its org chart. This is a phrase that’s often used in a pretty disparaging way, but in this case it’s absolutely fascinating. Each of these broad components is a part of the S3 organization. Each has a leader, and a bunch of teams that work on it. And if we went into the next level of detail in the diagram, expanding one of these boxes out into the individual components that are inside it, what we’d find is that all the nested components are their own teams, have their own fleets, and, in many ways, operate like indepe
ndent businesses.

![[Pasted image 20240117140649.png]]

Beyond the technology itself, there are human factors that make S3 - or any complex system - what it is. One of the core tenets at Amazon is that we want engineers and teams to fail fast, and safely. We want them to always have the confidence to move quickly as builders, while still remaining completely obsessed with delivering highly durable storage. One strategy we use to help with this in S3 is a process called “durability reviews.” It’s a human mechanism that’s not in the statistical 11 9s model, but it’s every bit as important.

When an engineer makes changes that can result in a change to our durability posture, we do a durability review. The process borrows an idea from security research: the threat model. The goal is to provide a summary of the change, a comprehensive list of threats, then describe how the change is resilient to those threats. In security, writing down a threat model encourages you to think like an adversary and imagine all the nasty things that they might try to do to your system. In a durability review, we encourage the same “what are all the things that might go wrong” thinking, and really encourage engineers to be creatively critical of their own code. The process does two things very well:

1. It encourages authors and reviewers to really think critically about the risks we should be protecting against.
2. It separates risk from countermeasures, and lets us have separate discussions about the two sides.

When working through durability reviews we take the durability threat model, and then we evaluate whether we have the right countermeasures and protections in place. When we are identifying those protections, we really focus on identifying coarse-grained “guardrails”. These are simple mechanisms that protect you from a large class of risks. Rather than nitpicking through each risk and identifying individual mitigations, we like simple and broad strategies that protect against a lot of stuff.