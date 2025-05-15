#kubernetes , #deployment
StatefulSets are naturally a good fit for distributed caches, databases, and other stateful services that rely on unique Pod identity and persistent external volumes.

Natively in Kubernetes, there are two ways of rolling out StatefulSets, two _update strategies,_ set via the `.spec.updateStrategy` field:

### OnDelete

- When a StatefulSet's .spec.updateStrategy.type is set to OnDelete, the StatefulSet controller will not automatically update the Pods in a StatefulSet. Users must manually delete Pods to cause the controller to create new Pods that reflect modifications made to a StatefulSet's .spec.template.

### RollingUpdate

- The RollingUpdate update strategy implements automated, rolling updates for the Pods in a StatefulSet. This is the default update strategy.


Bedrock Rollout Operator: a Kubernetes operator that manages StatefulSet rollouts.
The diagram below is a simplification showing how the pieces fit together:

![](https://slack.engineering/wp-content/uploads/sites/7/2024/05/rollout-op-arch.png)

1. Write intentions in bedrock.yaml
2. Effect a deployment from release UI
3. Release platform calls Bedrock API
4. Bedrock Rollout Operator takes over and converges the existing state of the cluster to the desired state defined in the StatefulsetRollout.
5. Do slack notifications
6. Once finished converging a StatefulsetRollout resource, the Operator calls back to the Bedrock API to inform it of the success or failure of the rollout. Bedrock API then sends a callback to Release for the status of rollout to be reflected in the UI.
Here’s a non-exhaustive flow chart illustrating how it works for our StatefulsetRollout (Sroll for short) custom resource:

![](https://slack.engineering/wp-content/uploads/sites/7/2024/05/re-enqueue.jpg)

Some of you might have picked up on a not-so-subtle detail related to the (ab-)use of the OnDelete strategy for StatefulSets: what we internally call the version leak issue. When a user decides to do a percent-based rollout, or pause an existing rollout, the StatefulSet is left with some Pods running the new version and some Pods running the previous version. But if a Pod running the previous version gets terminated for any other reason than being rolled out by the operator, it’ll get replaced by a Pod running the new version. Since we routinely terminate nodes for a number of reasons such as scaling clusters, rotating nodes for compliance as well as chaos engineering, a stopped rollout will, over time, tend to converge towards being fully rolled out. Fortunately, this is a well-understood limitation and Slack engineering teams deploy their services out to 100% in a timely manner before the version leak problem would arise.