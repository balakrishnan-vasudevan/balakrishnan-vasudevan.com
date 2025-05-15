# Tweets From Ivan Velichko

![rw-book-cover](https://pbs.twimg.com/profile_images/1417581014273122314/2CBEkT0b.jpg)

## Metadata
- Author: [[@iximiuz on Twitter]]
- Full Title: Tweets From Ivan Velichko
- Category: #tweets
- URL: https://twitter.com/iximiuz

## Highlights
- "Containers are just Linux processes" is a popular misconception.
  In reality, containers are as much about files as about processes.
  Here is how you can learn it yourself 👇
  https://t.co/6rcqxGAr8F https://t.co/STWQKOEvY2
  ![](https://pbs.twimg.com/media/FbpIYl8WQAEyGk5.png) ([View Tweet](https://twitter.com/iximiuz/status/1565644053139562497))
- Debunking Container Myths 🧵
  A (never-ending) series of articles that I started writing a couple of years ago to fix my own misconceptions about containers 🔽 https://t.co/bD7Iw48ere
  ![](https://pbs.twimg.com/media/FbPiQqSXoAA-3zb.png) ([View Tweet](https://twitter.com/iximiuz/status/1563851156417298434))
- Kubernetes basics explained by analogy 🧵
  ...or "How Kubernetes Just Repeats Good Old Deployment Patterns"
  1. For a long time, people had been deploying services as groups of virtual (or physical) machines.
  But VMs were often slow and bulky. Hence, not very efficient. https://t.co/u5c8vmSx4V
  ![](https://pbs.twimg.com/media/FYa_1pOX0AkFVpL.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1551148328334901248))
- I wish this article existed when I'd been learning Kubernetes RBAC.
  My fav kind of explanation:
  - Start from a clear problem: how to do access control
  - Show a technology-agnostic solution
  - Map it to K8s primitives: Roles/RoleBindings/ClusterRoles, etc.
  https://t.co/GAHhjV5gDO ([View Tweet](https://twitter.com/iximiuz/status/1515646535069048832))
- How to debug issues in containers 🔽
  You started a server in a container. It's supposed to open a bunch of ports. The container is running fine, but you cannot connect to some of the ports from the outside. You exec into the container, but `ss` is not there. Now what? https://t.co/AUXsOA0Fbs
  ![](https://pbs.twimg.com/media/FPbi1_8XIAkuotM.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1510651667598958592))
- Kubernetes Admission Webhooks illustrated 🔽
  By registering a webhook, it's possible to customize the request processing logic of the Kubernetes API server. https://t.co/pNNZc0RbBS
  ![](https://pbs.twimg.com/media/FPWVq2eXsAgaHN5.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1510280086490128387))
- How to grasp Containers and Docker (Mega Thread)
  When I started using containers back in 2015, I thought they were tiny virtual machines with a subsecond startup time.
  It was easy to follow tutorials from the Internet on how to put your Python or Node.js app into a container... ([View Tweet](https://twitter.com/iximiuz/status/1423984739514454033))
- TIL: How to create Kubernetes manifests real quick 🤯
  Use kubectl create --dry-run=client -o yaml
  Example:
  ```
  kubectl create deployment foo \
  --image=nginx:1.21 \
  --dry-run=client \
  -o yaml
  ``` ([View Tweet](https://twitter.com/iximiuz/status/1483180111579000834))
- Have you ever been confused while reading Kubernetes API docs?
  Wondering what are these:
  - API groups
  - Resources
  - Namespaces
  - API objects
  - CRDs
  - Aggregation layers
  ...and what are their relationships?
  I've got a picture for you!
  #Kubernetes https://t.co/7LbIfyS5uf
  ![](https://pbs.twimg.com/media/Esb62sXXMAYbKvp.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1353045442087571456))
- How to Debug Distroless/Slim Containers 🔽
  Slim containers are smaller, faster, and more secure.
  But these benefits come at a price - they lack the exploration and debugging tools.
  Here are 4 ways to debug slim containers 👇 https://t.co/1ciYSbPYFE
  ![](https://pbs.twimg.com/media/FekgIesX0AA2_sx.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1578829304343187456))
- I made a tool... to debug containers 🧙‍♂️
  It's like "docker exec", but it works even for containers without a shell (scratch, distroless, slim, etc).
  The "cdebug exec" command allows you to bring your own toolkit and start a shell inside of a running container.
  A short demo 👇 https://t.co/82m4vzPYJr ([View Tweet](https://twitter.com/iximiuz/status/1584244173347074049))
- How To Grasp Container Networking 🧵
  A tricky topic... Container networking can feel like magic at times. But it's not!
  Rather it's a bunch of more primitive "LEGO bricks" like net namespaces, veth pairs, and bridges combined into a handy (but complex) higher-level abstraction. https://t.co/xfqayHs2aR
  ![](https://pbs.twimg.com/media/Fi-TvOEXoAE40O5.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1598684797416742914))
- Want to master Docker and become a container expert
  ...but don't know how to even start? 🔽
  Here is the learning order that helped me:
  1. Containers: how Linux does them
  2. Images: why they are needed
  3. Managers: many containers, one host
  4. Orchestrators: many hosts, one app https://t.co/HaXaGnSMkU
  ![](https://pbs.twimg.com/media/FjhzWuuXwAAG822.png) ([View Tweet](https://twitter.com/iximiuz/status/1601166357826981888))
- Kind reminder - If you want to learn Linux, Containers, or Kubernetes, I've got something for you.
  ~Bi-weekly deep reads with a lot of visuals and, since more recently, fun practice exercises 👉 https://t.co/Fne4AemHIm https://t.co/MlkV0Oo5vp
  ![](https://pbs.twimg.com/media/F60b9ReW0AAzarS.jpg)
  ![](https://pbs.twimg.com/media/F60b9RWWkAYd8xn.jpg)
  ![](https://pbs.twimg.com/media/F60b9RVXYAAnNoW.jpg)
  ![](https://pbs.twimg.com/media/F60cEKUWwAA7zX3.jpg) ([View Tweet](https://twitter.com/iximiuz/status/1706053842259857518))
- What is Service Discovery - in general, and in Kubernetes 🧵
  Services (in Kubernetes or not) tend to run in multiple instances (containers, pods, VMs). But from the client's standpoint, a service is usually just a single address.
  How is this single point of entry achieved? https://t.co/N86Wj8YaCG
  ![](https://pbs.twimg.com/media/F_Ik-AkXwAApH35.png) ([View Tweet](https://twitter.com/iximiuz/status/1725492698096755075))
