1. I guess I'd cover the following:

- Module parameter routing and type declarations for module parameters
- for_each, count, and conditional resource creation
- map (de)referencing
- template files and template variables
- IP address helpers (`cidrsubnet()` and friends)
- `remote_state` references and basic `data` usage
- resource lifecycle and validation blocks

1. If I were getting extra clever I might add manual state intervention like `import` and `rm` so make sure you know generally how resources are identified for their cloud provider. Also make sure you have an understanding of the cloud provider's networking model and things like IAM/service accounts and role access definitions. this is arguably one of the most frustrating things i deal with in tf, and given real world provider documentation (looking at you aws) is also one of the most common.
2. flattening a nested list to be able to use dynamic segments when the variable passed in is a map that contains lists inside of it.
3. want a module that deploys N resources? great, make a storngly typed list of objects, yadda yadda, but of course one of your params is going to need to be a list or two for a nested sub-resource that you can have N of...Maybe have a broken one, with a syntax error and see if they know how to fix it by memory. This shows they do this work often.
4. It was a hypothetical "Hello World" type of application that was partially broken. The task was to launch it into the cloud and connect to a database. It actually had nothing to do with the position's main responsibilities that were discussed with the hiring manager, and thus I was not fully prepared for a timed activity. I studied all the wrong things. I know how to do all of it but I took my time crafting correct networking and structure and then Terraform debugging just ate up all the time.
5. I want to hear about your tf to CM tool flow. How you might go about resolving a big discrepancy between code and actual. How you complete the lifecycle... Tell me how Ansible, Terraform and puppet differ in 10 ways. To me I want to know you understand concepts, not know how to perform a state mv operation. I do not believe in tech-ing people out via 'code'. You do not get better hires.
6. Here's one of my (on-going) battle stories with terraform..Background: I work on a platform team in a heavily regulated industry, specifically in medical research.Based on past (unpleasant) experiences with customized environments for different studies, we've created a unified platform based on AWS EKS, provisioned through a lot of tf repos and chained GHA pipelines. The idea here is to not have custom infra polluting the platform, outside of established feature flags. No problem, TF is great for that. All working awesome.Then we need to scale back RDS because an abandoned replication slot in postgres causes the allocated storage to balloon to many terrabytes, costing lots of money. The only resolution paths all involve spinning up a new database with the reduced allocated storage, and copying data over by some means or another (DMS? Native tools? You have options).There is no clean way to do this via terraform that doesn't involve polluting the repos with custom, one-off shit and targeted applies.I ended up using boto and a GHA workflow to stand everything up, do the migration song and dance, and end up back in a state terraform won't complain about. This the kind of stuff I mean. You have to know what you're doing to know there are multiple paths to doing it, and some tools you rely on every day are going to just suck at addressing those problems. You'll come up with something to work around it, and that's where I get to see your creativity and problem solving skills in action. To me stories like that are all so much better than a test project could ever be. EDIT: The heavily regulated industry part is relevant because we can't have direct access to the data at any point in the process, and all actions need to be peer reviewed and auditable. So if its not done through a PR, it doesn't happen.
7. Most of the questions i got from panel interview was mostly on tfstate, migrating it to another accout or region, push/pull and reconfiguring backend to be centralized. Good luck!!!
8. Authenticating to the API, incorrectly configured Provider block, potential state lock, refresh, importing and removing of items,, referencing items that exist outside of state (data), using TF_LOG environment variable, format, validate and plan and of course apply.
9. I'm fairly comfortable with syntax, things like referencing variables from modules, maps, using for_each, count, using depends_on etc. Do you think this covers most bases?
10. Walk me through how you deploy your terraform. You get one point for all the buzzwords like pipeline, source control, modules, etc.


🔹 Question 1: What are workspaces in Terraform, and how do they help manage infrastructure? 
*Multiple environments in same directory. Streamline management of environment*

🔹 Question 2: Explain how to handle secrets or sensitive data in Terraform configurations. 
*Use environment variables, encrypted files, or tools like Vault, also there is support for secure storage in enterprise edition*

🔹 Question 3: What is the difference between Terraform's count and for_each meta-arguments? 
*Both can be used to create multiple instances of a resource
Count is based on integer value
For each uses maps or a set of strings, more flexible, dynamic resource creation based on complex data structures*

🔹 Question 4: How do you handle dependencies between resources in Terraform? 
*TF manages this automatically, takes care of order based on config file
You can also use depends_on meta argument, not encouraged*

🔹Question 5: Explain how Terraform handles state management and why it's important. 
*Current state is maintained in a jSON file, stores current state of system*

🔹Question 6: What are Terraform providers, and how do they facilitate infrastructure management? 
*Manage lifecycle of resources, abstract API interactions*

🔹 Question 7: How can you enable parallelism and improve performance in Terraform operations? 
*Allows to specify degrees of parallelism using "parallelism" flag or "parallelism" setting to reduce execution time*

🔹 Question 8: What are remote backends in Terraform, and why would you use them? 
*Important to manage and store state file securely, allows collaboration and locking of state file. Better security, ideal for prod environments*

🔹 Question 9: Explain how you can manage Terraform modules effectively in a large-scale infrastructure project. 
*organize hierarchically based on functionality or environment, makes it reusable*

🔹Question 10: How do you handle Terraform state locking to prevent concurrent modifications? 
*To prevent concurrent modifications, acquire locks. Use built in mechanisms. Use external solutions or S3 with Dynamo DB to apply locks*

🔹 Question 11: What are the differences between Terraform's local-exec and remote-exec provisioners? 
*Local exec - local machine, local tasks, remote exec - execute on remote instances or instances being created, post provisioning tasks*

🔹 Question 12: How can you manage Terraform state across multiple environments or teams securely? 
*Terraform enterprise of TF Cloud - get State locking, access control,, Integration with version control, audit logging*

🔹 Question 13: Explain the difference between Terraform's taint and import commands. 
*Taint - mark resource for recreation during next apply
Import - manage resources created outside TF*

🔹 Question 14: How do you handle drift detection and remediation in Terraform? 
*TF Plan command detects drift*

🔹 Question 15: What are some best practices for structuring Terraform configurations in a modular and reusable way?
*1. Organize configs into modules based on functionality or environment. 2. Parametrize modules for flexibility 3. Use input variables and outputs to define interfaces 4. Leverage version control and dependency management for collaboration and reuse*


Here's a streamlined workflow for managing Terraform remote state with AWS:  
  
=> Developer initiates Terraform commands  
=> Read and update state files stored in Amazon S3  
=> State files are encrypted and versioned  
=> Acquire a lock in DynamoDB before making changes  
=> Locking prevents conflicts and race conditions  
=> Each lock is identified by a unique lock ID (e.g., lock-abc-123)  
=> Execute Terraform plans to provision or update resources  
=> Release the lock in DynamoDB after updates  
  
[hashtag#devops](https://www.linkedin.com/feed/hashtag/?keywords=devops&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7201094112463187968) [hashtag#terraform](https://www.linkedin.com/feed/hashtag/?keywords=terraform&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7201094112463187968) [hashtag#interviewtips](https://www.linkedin.com/feed/hashtag/?keywords=interviewtips&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7201094112463187968) [hashtag#devopscommunity](https://www.linkedin.com/feed/hashtag/?keywords=devopscommunity&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A7201094112463187968)

Activate to view larger image,

![Image preview](https://media.licdn.com/dms/image/D4D22AQGM-e39ekPSsw/feedshare-shrink_2048_1536/0/1716874625772?e=1720051200&v=beta&t=Qo19isnel32xoDw-4Zg0sypyPdvtydGAROl0Bs_njVI)