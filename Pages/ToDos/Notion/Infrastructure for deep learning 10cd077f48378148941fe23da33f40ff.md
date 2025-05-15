# Infrastructure for deep learning

Tags: ml-infra
Category: Articles
Company: Open AI
Status: Not started
URL: https://openai.com/index/infrastructure-for-deep-learning/

![https://images.ctfassets.net/kftzwdyauwt9/31860186-a1ba-4d48-95900dc56c4d/f862844197c6d8bed67643f6d4224564/infrastructure-for-deep-learning.jpg?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/31860186-a1ba-4d48-95900dc56c4d/f862844197c6d8bed67643f6d4224564/infrastructure-for-deep-learning.jpg?w=3840&q=90&fm=webp)

Illustration: Ludwig Pettersson

Deep learning is an empirical science, and the quality of a group’s infrastructure is a multiplier on progress. Fortunately, today’s open-source ecosystem makes it possible for anyone to build great deep learning infrastructure.

## Summary

In this post, we’ll share how deep learning research usually proceeds, describe the infrastructure choices we’ve made to support it, and open-source [kubernetes-ec2-autoscaler(opens in a new window)](https://github.com/openai/kubernetes-ec2-autoscaler), a batch-optimized scaling manager for Kubernetes. We hope you find this post useful in building your own deep learning infrastructure.

## The use case

A typical deep learning advance starts out as an idea, which you test on a small problem. At this stage, you want to run many ad-hoc experiments quickly. Ideally, you can just SSH into a machine, run a script in screen, and get a result in less than an hour.

Making the model really work usually requires seeing it fail in every conceivable way and finding ways to fix those limitations. (This is similar to building any new software system, where you’ll run your code many times to build an intuition for how it behaves.)

So deep learning infrastructure must allow users to flexibly introspect models, and it’s not enough to just expose summary statistics.

Once the model shows sufficient promise, you’ll scale it up to larger datasets and more GPUs. This requires long jobs that consume many cycles and last for multiple days. You’ll need careful experiment management, and to be extremely thoughtful about your chosen range of hyperparameters.

The early research process is unstructured and rapid; the latter is methodical and somewhat painful, but it’s all absolutely necessary to get a great result.

## An example

The paper [Improved Techniques for Training GANs(opens in a new window)](https://arxiv.org/abs/1606.03498) began with [Tim Salimans(opens in a new window)](http://timsalimans.com/) devising several ideas for improving [Generative Adversarial Network](https://openai.com/index/generative-models/#gan) training. We’ll describe the simplest of these ideas (which happened to produce the best-looking samples, though not the best semi-supervised learning).

GANs consist of a generator and a discriminator network. The generator tries to fool the discriminator, and the discriminator tries to distinguish between generated data and real data. Intuitively, a generator which can fool every discriminator is quite good. But there is a hard-to-fix failure mode: the generator can “collapse” by always outputting exactly the same (likely realistic-looking!) sample.

Tim had the idea to give discriminator an entire [minibatch(opens in a new window)](https://www.coursera.org/learn/machine-learning/lecture/9zJUs/mini-batch-gradient-descent) of samples as input, rather than just one sample. Thus the discriminator can tell whether the generator just constantly produces a single image. With the collapse discovered, gradients will be sent to the generator to correct the problem.

The next step was to prototype the idea on [MNIST(opens in a new window)](http://yann.lecun.com/exdb/mnist/) and [CIFAR-10(opens in a new window)](https://www.cs.toronto.edu/~kriz/cifar.html). This required prototyping a small model as quickly as possible, running it on real data, and inspecting the result. After some rapid iteration, Tim got very encouraging [CIFAR-10 samples(opens in a new window)](https://cdn.openai.com/infrastructure-for-deep-learning/cifar10samples-2.jpg)=—pretty much the best samples we’d seen on this dataset.

However, deep learning (and AI algorithms in general) must be scaled to be truly impressive—a small neural network is a proof of concept, but a big neural network actually solves the problem and is useful. So [Ian Goodfellow(opens in a new window)](https://www.linkedin.com/in/ian-goodfellow-b7187213) dug into scaling the model up to work on [ImageNet(opens in a new window)](http://image-net.org/).

![https://images.ctfassets.net/kftzwdyauwt9/a6d8998f-fcb9-4691-8f5b122c6c06/fb4e5828987bdd57cf6d7d640fa15f67/infra_img_1.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/a6d8998f-fcb9-4691-8f5b122c6c06/fb4e5828987bdd57cf6d7d640fa15f67/infra_img_1.png?w=3840&q=90&fm=webp)

Infra Img 1

Our model learning to generate ImageNet images

With a larger model and dataset, Ian needed to parallelize the model across multiple GPUs. Each job would push multiple machines to 90% CPU and GPU utilization, but even then the model took many days to train. In this regime, every experiment became precious, and he would meticulously log the results of each experiment.

Ultimately, while the results were good, they were not as good as we hoped. We’ve tested many hypotheses as to why, but still haven’t cracked it. Such is the nature of science.

## Infrastructure

### Software

![https://images.ctfassets.net/kftzwdyauwt9/e7938cea-0f8a-4722-050ef8024687/fe003fd9f59b4b4901c31fb8050c0557/infra_img_2.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/e7938cea-0f8a-4722-050ef8024687/fe003fd9f59b4b4901c31fb8050c0557/infra_img_2.png?w=3840&q=90&fm=webp)

A sample of our TensorFlow code

The vast majority of our research code is written in Python, as reflected in [our(opens in a new window)](https://github.com/openai/improved-gan) [open(opens in a new window)](https://github.com/openai/vime)-[source(opens in a new window)](https://github.com/openai/iaf) [projects(opens in a new window)](https://github.com/openai/imitation). We mostly use [TensorFlow(opens in a new window)](https://www.tensorflow.org/) (or [Theano(opens in a new window)](http://deeplearning.net/software/theano/) in special cases) for GPU computing; for CPU we use those or [Numpy(opens in a new window)](http://www.numpy.org/). Researchers also sometimes use higher-level frameworks like [Keras(opens in a new window)](https://keras.io/) on top of TensorFlow.

Like much of the deep learning community, we use Python 2.7. We generally use [Anaconda(opens in a new window)](https://www.continuum.io/anaconda-overview), which has convenient packaging for otherwise difficult packages such as [OpenCV(opens in a new window)](http://opencv.org/) and [performance optimizations(opens in a new window)](https://docs.continuum.io/anaconda/#high-performance) for some scientific libraries.

### Hardware

For an ideal batch job, doubling the number of nodes in your cluster will halve the job’s runtime. Unfortunately, in deep learning, people usually see very [sublinear(opens in a new window)](https://research.googleblog.com/2016/04/announcing-tensorflow-08-now-with.html) speedups from many GPUs. Top performance thus requires top-of-the-line GPUs. We also use quite a lot of CPU for [simulators(opens in a new window)](https://gym.openai.com/envs#box2d), [reinforcement learning environments(opens in a new window)](https://gym.openai.com/envs#atari), or small-scale models (which run no faster on a GPU).

![https://images.ctfassets.net/kftzwdyauwt9/fc705186-3c3d-40eb-a2f96b4d94d5/6f3d0e0703333fd51f9719225cea0632/infra_img_3.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/fc705186-3c3d-40eb-a2f96b4d94d5/6f3d0e0703333fd51f9719225cea0632/infra_img_3.png?w=3840&q=90&fm=webp)

nvidia-smi showing fully loaded Titan Xs

[AWS(opens in a new window)](https://aws.amazon.com/) generously agreed to donate a large amount of compute to us. We’re using them for CPU instances and for horizontally scaling up GPU jobs. We also run our own physical servers, primarily running [Titan X(opens in a new window)](http://www.geforce.com/hardware/10series/titan-x-pascal) GPUs. We expect to have a hybrid cloud for the long haul: it’s valuable to experiment with different GPUs, interconnects, and other techniques which may become important for the future of deep learning.

![https://images.ctfassets.net/kftzwdyauwt9/a52d26e1-f8c2-4ffa-7f4eff0762f5/5326f78c72a04f09816a670ec4dbfc05/infra_img_4.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/a52d26e1-f8c2-4ffa-7f4eff0762f5/5326f78c72a04f09816a670ec4dbfc05/infra_img_4.png?w=3840&q=90&fm=webp)

htop on the same physical box showing plenty of spare CPU. We generally run our CPU-intensive workloads separately from our GPU-intensive ones.

### Provisioning

We approach infrastructure like many companies treat product: it must present a simple interface, and usability is as important as functionality. We use a consistent set of tools to manage all of our servers and configure them as identically as possible.

![https://images.ctfassets.net/kftzwdyauwt9/d402e835-f111-40e6-28379f980e29/9914c96270cca97d124bee3faba1a0c9/infra_img_5.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/d402e835-f111-40e6-28379f980e29/9914c96270cca97d124bee3faba1a0c9/infra_img_5.png?w=3840&q=90&fm=webp)

Snippet of our Terraform config for managing Auto Scaling groups. Terraform creates, modifies, or destroys your running cloud resources to match your configuration files.

We use [Terraform(opens in a new window)](https://www.terraform.io/) to set up our AWS cloud resources (instances, network routes, DNS records, etc). Our cloud and physical nodes run [Ubuntu(opens in a new window)](http://www.ubuntu.com/) and are configured with [Chef(opens in a new window)](https://www.chef.io/chef/). For faster spinup times, we pre-bake our cluster AMIs using [Packer(opens in a new window)](https://www.packer.io/). All our clusters use non-overlapping IP ranges and are interconnected over the public internet with [OpenVPN(opens in a new window)](https://openvpn.net/) on user laptops, and [strongSwan(opens in a new window)](https://www.strongswan.org/) on physical nodes (which act as AWS [Customer Gateways(opens in a new window)](http://docs.aws.amazon.com/AmazonVPC/latest/NetworkAdminGuide/Introduction.html)).

We store people’s home directories, data sets, and results on [NFS(opens in a new window)](https://en.wikipedia.org/wiki/Network_File_System) (on physical hardware) and [EFS(opens in a new window)](https://aws.amazon.com/efs/)/[S3(opens in a new window)](https://aws.amazon.com/s3/) (on AWS).

### Orchestration

Scalable infrastructure often ends up making the simple cases harder. We put equal effort into our infrastructure for small- and large-scale jobs, and we’re actively solidifying our toolkit for making distributed use-cases as accessible as local ones.

We provide a cluster of SSH nodes (both with and without GPUs) for ad-hoc experimentation, and run [Kubernetes(opens in a new window)](http://kubernetes.io/) as our cluster scheduler for physical and AWS nodes. Our cluster spans 3 AWS regions—our jobs are bursty enough that we’ll sometimes hit capacity on individual regions.

Kubernetes requires each job to be a Docker container, which gives us dependency isolation and code snapshotting. However, building a new Docker container can add precious extra seconds to a researcher’s iteration cycle, so we also provide tooling to transparently ship code from a researcher’s laptop into a standard image.

![https://images.ctfassets.net/kftzwdyauwt9/77e54034-1413-47d5-6e792bc67141/de91b5a99163f399ce03e6b348a52415/infra_img_6.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/77e54034-1413-47d5-6e792bc67141/de91b5a99163f399ce03e6b348a52415/infra_img_6.png?w=3840&q=90&fm=webp)

Model learning curves in TensorBoard

We expose Kubernetes’s [flannel(opens in a new window)](https://coreos.com/flannel/docs/latest/) network directly to researchers’ laptops, allowing users seamless network access to their running jobs. This is especially useful for accessing monitoring services such as [TensorBoard(opens in a new window)](https://www.tensorflow.org/versions/r0.10/how_tos/summaries_and_tensorboard/index.html). (Our initial approach—which is cleaner from a strict isolation perspective—required people to create a Kubernetes [Service(opens in a new window)](http://kubernetes.io/docs/user-guide/services/) for each port they wanted to expose, but we found that it added too much friction.)

## kubernetes-ec2-autoscaler

Our workload is bursty and unpredictable: a line of research can go quickly from single-machine experimentation to needing 1,000 cores. For example, over a few weeks, one experiment went from an interactive phase on a single Titan X, to an experimental phase on 60 Titan Xs, to needing nearly 1600 AWS GPUs. Our cloud infrastructure thus needs to dynamically provision Kubernetes nodes.

It’s easy to run Kubernetes nodes in [Auto Scaling(opens in a new window)](https://aws.amazon.com/autoscaling/) groups, but it’s harder to correctly manage the size of those groups. After a batch job is submitted, the cluster knows exactly what resources it needs, and should allocate those directly. (In contrast, AWS’s [Scaling Policies(opens in a new window)](http://docs.aws.amazon.com/autoscaling/latest/userguide/policy_creating.html) will spin up new nodes piecemeal until resources are no longer exhausted, which can take multiple iterations.) Also, the cluster needs to [drain(opens in a new window)](http://kubernetes.io/docs/user-guide/kubectl/kubectl_drain/) nodes before terminating them to avoid losing in-flight jobs.

It’s tempting to just use raw EC2 for big batch jobs, and indeed that’s where we started. However, the Kubernetes ecosystem adds quite a lot of value: low-friction tooling, logging, monitoring, ability to manage physical nodes separately from the running instances, and the like. Making Kubernetes autoscale correctly was easier than rebuilding this ecosystem on raw EC2.

We’re releasing [kubernetes-ec2-autoscaler(opens in a new window)](https://github.com/openai/kubernetes-ec2-autoscaler), a batch-optimized scaling manager for Kubernetes. It runs as a normal [Pod(opens in a new window)](http://kubernetes.io/docs/user-guide/pods/) on Kubernetes and requires only that your worker nodes are in Auto Scaling groups.

![https://images.ctfassets.net/kftzwdyauwt9/626c3055-84f2-4a8f-bda6fee68f8f/f4546aa6e81d5aaa9e2ffb6e0dbc3351/infra_img_7.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/626c3055-84f2-4a8f-bda6fee68f8f/f4546aa6e81d5aaa9e2ffb6e0dbc3351/infra_img_7.png?w=3840&q=90&fm=webp)

The Launch Configurations for our Kubernetes cluster

The autoscaler works by polling the Kubernetes master’s state, which contains everything needed to calculate the cluster resource ask and capacity. If there’s excess capacity, it drains the relevant nodes and ultimately terminates them. If more resources are needed, it calculates what servers should be created and increases your Auto Scaling group sizes appropriately (or simply [uncordons(opens in a new window)](http://kubernetes.io/docs/user-guide/kubectl/kubectl_uncordon/) drained nodes, which avoids new node spinup time).

kubernetes-ec2-autoscaler handles multiple Auto Scaling groups, resources beyond CPU (memory and GPUs), and fine-grained constraints on your jobs such as AWS region and instance size. Additionally, bursty workloads can lead to Auto Scaling Groups timeouts and errors, since (surprisingly!) even AWS does not have infinite capacity. In these cases, kubernetes-ec2-autoscaler detects the error and overflows to a secondary AWS region.

Our infrastructure aims to maximize the productivity of deep learning researchers, allowing them to focus on the science. We’re building tools to further improve our infrastructure and workflow, and will share these in upcoming weeks and months. We [welcome help(opens in a new window)](https://jobs.lever.co/openai/f7801a92-1e2f-4656-a572-962b53ec34f6) to make this go even faster!

- [Join OpenAI](https://openai.com/careers/)
- [Chat with others(opens in a new window)](https://gitter.im/openai/infra)
- [Conclusion](https://openai.com/news/research/?tags=research-conclusion)
- [Compute](https://openai.com/news/research/?tags=topic-compute)
- [Open source](https://openai.com/news/research/?tags=topic-open-source)
- [Software engineering](https://openai.com/news/research/?tags=topic-software-engineering)

[Reasoning in GPT > cover image](https://openai.com/index/learning-to-reason-with-llms/)

![https://images.ctfassets.net/kftzwdyauwt9/bgJUZGtbvelVjCeoIjfUl/5e78175b7f7324d72f20927df2c3424d/o1-research-blogcard.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/bgJUZGtbvelVjCeoIjfUl/5e78175b7f7324d72f20927df2c3424d/o1-research-blogcard.png?w=3840&q=90&fm=webp)

[o1-mini research > cover image](https://openai.com/index/openai-o1-mini-advancing-cost-efficient-reasoning/)

![https://images.ctfassets.net/kftzwdyauwt9/1Q36rezJbyC7l7KEhDLm1D/8df88b51a23d7b2164f65cc1c9e3e8bb/o1-mini-research-blogcard.png?w=3840&q=90&fm=webp](https://images.ctfassets.net/kftzwdyauwt9/1Q36rezJbyC7l7KEhDLm1D/8df88b51a23d7b2164f65cc1c9e3e8bb/o1-mini-research-blogcard.png?w=3840&q=90&fm=webp)