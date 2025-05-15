**Table of Contents**

- [SRE](#SRE)
- [DevOps](#DevOps)
- [Platform Engineering](#Platform%20Engineering)
- [SRE vs DevOps](#SRE%20vs%20DevOps)


# SRE
[Site reliability engineering (SRE)](https://www.splunk.com/en_us/blog/learn/site-reliability-engineer-sre-role.html) is a practice that focuses on improving and maintaining the reliability of a software system. It utilizes software tools and automated tasks like application monitoring and reliability tasks to accomplish that.


The responsibilities of SRE teams include:

- [Application monitoring](https://www.splunk.com/en_us/data-insider/what-is-application-performance-monitoring.html)
- Emergency response
- [Change management](https://www.splunk.com/en_us/blog/learn/change-management.html)
- Ensuring the availability, efficiency and performance standards of applications

These teams work closely with development teams throughout the lifecycle and provide solutions for underlying system-related issues, such as bugs in software pipelines and automated jobs. They also help automate routine tasks to improve the productivity of developers.

![](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2022/06/sre1.png)

"SRE is an engineering approach to manage and maintain complex, large-scale systems by applying software engineering practices to operations tasks. It emphasizes automation, reliability, scalability, and the intersection of development and operations to ensure efficient and reliable service delivery."

Key tenets of SRE include:

1. **Reliability Engineering**: Prioritizing system reliability and uptime through proactive measures and automation.
    
2. **Automation and Tooling**: Utilizing automation and tooling to manage and scale systems efficiently.
    
3. **Metrics-Driven Practices**: Using quantitative measures and monitoring to inform decision-making and drive continuous improvement.
    
4. **Culture of Collaboration**: Fostering collaboration between development and operations teams to align goals and improve system reliability.
    
5. **Incident Response and Post-Incident Analysis**: Implementing structured incident response practices and conducting thorough post-incident analyses to prevent future failures.
## SRE - Socio-technical
The socio-technical side of Site Reliability Engineering (SRE) encompasses the human, social, and organizational aspects intertwined with the technical facets of maintaining reliable systems. Here's a breakdown:

### Collaboration and Communication:

- **Cross-Functional Teams**: SRE often involves collaboration between development, operations, and other teams. Effective communication and collaboration are crucial for aligning goals and resolving issues efficiently.

- **Transparency and Documentation**: Clear documentation and transparent communication about system changes, incidents, and resolutions are vital for shared understanding among team members.

### Culture and Mindset:

- **Blameless Culture**: Encouraging a blameless culture fosters an environment where individuals focus on problem-solving rather than attributing blame. It allows for open discussions and learnings from failures.

- **Learning and Continuous Improvement**: Emphasizing continuous learning and improvement encourages teams to adopt new technologies, processes, and methodologies to enhance system reliability.

### Leadership and Empowerment:

- **Empowered Teams**: Giving autonomy to SRE teams empowers them to make decisions and take ownership of system reliability. Empowerment fosters innovation and a sense of responsibility.

- **Leadership Support**: Support from leadership in prioritizing reliability goals, investing in resources, and promoting a culture of reliability is pivotal for SRE success.

### Incident Response and Post-Incident Analysis:

- **Incident Response Practices**: Structured incident response practices and post-incident analysis sessions help in understanding root causes, identifying preventive measures, and sharing learnings across the organization.

- **Continuous Feedback Loop**: Implementing feedback mechanisms from incidents ensures that the team learns from past experiences, improves processes, and prevents recurring issues.

### Metrics, Monitoring, and Automation:

- **Meaningful Metrics**: Choosing and tracking meaningful metrics is not only technical but also socio-technical. It involves understanding user impact and aligning technical metrics with business goals.

- **Monitoring for User Experience**: Monitoring should not only focus on technical aspects but also encompass user experience metrics, enabling teams to prioritize based on user impact.

### Human Factors in Reliability:

- **Resilience Engineering**: Considering human factors and cognitive aspects when designing systems helps in building resilient systems that accommodate human error and unexpected situations.

- **Workload Management**: Avoiding burnout and managing workload is crucial for sustained performance and creativity among team members.

### Conclusion:

Incorporating the socio-technical aspects into SRE practices is about recognizing that technology doesn't exist in isolation; it operates within a social context. Balancing technical excellence with effective communication, a supportive culture, and continuous improvement initiatives is fundamental for successful Site Reliability Engineering.

## SRE - Human Factors Engineering
Human factors engineering in Site Reliability Engineering (SRE) involves understanding how human capabilities, limitations, and behaviors interact with the design and operation of systems. Here's how it applies in the SRE context:

### Cognitive Load Management:

- **Complexity Reduction**: Design systems and processes to minimize cognitive overload by simplifying interfaces, reducing unnecessary information, and providing clear guidance.

- **Information Presentation**: Present information in a way that is intuitive and easy to process during incident response, monitoring, and decision-making processes.

### Incident Response and Decision Making:

- **Playbooks and Procedures**: Develop clear, concise, and easy-to-follow incident response playbooks and procedures to guide SREs during high-stress situations.

- **Decision Support Tools**: Implement decision support tools that aid SREs in making informed decisions during incidents, such as runbooks, checklists, and diagnostic tools.

### Automation and Tooling:

- **User-Friendly Interfaces**: Ensure that monitoring, automation, and debugging tools have user-friendly interfaces that reduce the cognitive load required to operate them effectively.

- **Automation Design**: Design automated processes that account for human intervention points and provide clear instructions or decision points for human involvement.

### Collaborative Environments:

- **Effective Communication**: Foster a culture of effective communication within SRE teams and across departments to facilitate collaboration, knowledge sharing, and incident resolution.

- **Collaboration Tools**: Utilize collaboration tools that enhance communication and teamwork, such as shared documentation platforms, incident management systems, and chat platforms.

### Resilience and Error Management:

- **Error Tolerance**: Design systems with error tolerance, acknowledging that human errors are inevitable, and build systems that can handle or recover from mistakes gracefully.

- **Feedback Loops**: Establish feedback loops where SREs can report usability issues, contribute improvements, and provide insights for continuous improvement.

### User Experience and Feedback:

- **User-Centric Monitoring**: Monitor systems not just for technical metrics but also for user experience metrics to understand the impact of technical issues on end-users.

- **User Feedback Channels**: Create channels for user feedback and incorporate this information into the SRE process to align technical objectives with user needs.

### Training and Support:

- **Training Programs**: Develop comprehensive training programs that focus not only on technical skills but also on stress management, incident handling, and decision-making skills.

- **Mental Health Support**: Recognize the potential stressors of SRE roles and provide support mechanisms, such as counseling or mental health resources, to promote well-being.

### Conclusion:

Human factors engineering in SRE revolves around creating systems, processes, and environments that account for human capabilities, limitations, and behaviors. It aims to optimize the interaction between people and technology, ultimately enhancing the reliability, efficiency, and well-being of SRE teams and the systems they manage.

# DevOps
Traditionally, development and [operations teams](https://www.splunk.com/en_us/blog/learn/it-operations-itops.html) functioned separately. This siloed culture often led to issues like low-quality software and delays in software delivery. DevOps culture breaks down this siloed nature of development and operations teams by combining the tasks of two teams.

[DevOps teams](https://www.splunk.com/en_us/blog/learn/devops-roles-responsibilities.html) work in collaboration to automate and streamline the software development process. DevOps greatly benefits teams by improving collaboration, communication, software delivery speed and quality. Responsibilities of DevOps engineers include:

- Prioritizing communication and collaboration.
- Automating processes.
- [System monitoring](https://www.splunk.com/en_us/data-insider/what-is-it-monitoring.html).
- Optimizing system performance.
- Troubleshooting issues.


![](https://www.splunk.com/content/dam/splunk-blogs/images/en_us/2022/06/devops1.png)

## DevOps - Human Factors
Human factors engineering in DevOps involves integrating principles of human-centered design and psychology into the development and operation of software systems. It emphasizes understanding human capabilities and limitations to optimize system design, usability, and overall performance. Here's how it's relevant:

### User-Centered Design:

- **Understanding User Needs**: Incorporate user perspectives and needs into the design and development process to create intuitive and user-friendly interfaces and workflows.

- **User Feedback Integration**: Collect and integrate user feedback iteratively to enhance the usability and functionality of software systems.

### Collaboration and Communication:

- **Cross-Functional Teams**: Encourage collaboration between developers, operations teams, and other stakeholders. Effective communication ensures shared understanding and alignment of goals.

- **Reducing Cognitive Load**: Simplify interfaces and processes to reduce cognitive load on users, enabling better decision-making and faster response times.

### Automation and Tooling:

- **Ease of Tooling**: Design tools and automation interfaces that are intuitive and easy to use, minimizing the learning curve for users.

- **Feedback Mechanisms**: Implement clear feedback mechanisms in automated systems, allowing users to understand system status and actions taken.

### Incident Response and Recovery:

- **Human-Friendly Incident Response**: Implement incident response procedures that consider human factors, ensuring clear communication and minimizing stress during critical incidents.

- **Documentation and Knowledge Sharing**: Maintain easily accessible and comprehensive documentation to aid in troubleshooting and recovery processes.

### Training and Skill Development:

- **Training Programs**: Offer training and skill development programs that cater to both technical and non-technical aspects, ensuring teams understand not just the tools but also their impact on system performance.

- **Cross-Training Opportunities**: Encourage cross-training between teams to broaden skill sets, foster empathy, and improve collaboration.

### Workload Management and Well-Being:

- **Balancing Workload**: Avoid overloading team members with excessive tasks or alerts, which can lead to burnout and reduced performance.

- **Promoting Well-Being**: Create a culture that prioritizes well-being, allowing for breaks, time off, and a supportive environment to foster creativity and innovation.

### Continuous Improvement:

- **Feedback Integration**: Emphasize the importance of feedback loops in both technical and human aspects to drive continuous improvement.

- **Learning from Incidents**: Focus on learning and improving processes based on post-incident analyses, incorporating human factors into prevention strategies.

### Conclusion:

Human factors engineering in DevOps acknowledges that successful software delivery isn't just about technology; it's about considering human aspects in system design, operation, and maintenance. By focusing on usability, collaboration, communication, and well-being, DevOps practices become more effective, resilient, and user-centric.


# Platform Engineering
[Platform engineering is a rising discipline](https://www.splunk.com/en_us/blog/learn/platform-engineering.html) in the cloud-native era. It aims to build toolchains and workflows covering the operational needs of the entire software development lifecycle, enabling self-service [infrastructure capabilities](https://www.splunk.com/en_us/blog/learn/it-infrastructure.html).

[Platform engineers & PE teams](https://www.splunk.com/en_us/blog/learn/platform-engineer-role-responsibilities.html) might focus on developing things like build tools, version control systems and automated testing frameworks. They also build some workflows, such as CI/CD, alerting, and deployment workflows. These processes help software developers build and deliver software more efficiently. Platform engineers are responsible for:

- Developing toolchains and workflows.
- [Ensuring the security and compliance of infrastructure.](https://www.splunk.com/en_us/blog/learn/infrastructure-security.html)
- Managing infrastructure reliability and scalability.
- Educating developers on best practices and platform usage.

Ultimately, platform engineering’s aim is to solve issues that arise from poorly adopted SRE and DevOps practices.

# SRE vs DevOps
## Similarities
-  Focus on automation. SRE and DevOps both encourage automation, communication and collaboration. Both teams bear responsibilities like monitoring, optimizing system performance and troubleshooting issues. 
- **Communication & collaboration**. Both DevOps and SRE encourage communication and collaboration between development and operations teams as a core principle. It helps them deliver high-quality and reliable software.
- **Tools.** SRE and DevOps teams are responsible for production monitoring and troubleshooting. They frequently use [log analysis and monitoring tools](https://www.splunk.com/en_us/blog/learn/log-analytics.html) like [Splunk](https://www.splunk.com/en_us/products/observability.html), Grafana and NewRelic to identify issues and improve the performance of software systems.
- **Metrics**. Both SRE and [DevOps teams](https://www.splunk.com/en_us/blog/learn/devops-roles-responsibilities.html) monitor metrics that reflect the behavior of applications and systems. Even if there are separate metrics, some metrics are useful for both teams. For example, response times, error rates and [other failure metrics](https://www.splunk.com/en_us/blog/learn/failure-metrics.html) help detect and resolve issues before they impact users.
## Differences
But how SRE and DevOps differ is quite illuminating:

### Primary focus

Of course, there are some primary differences between them, too. The first major difference is the breadth of the focus. DevOps focuses on the entire software development process, while SRE narrowly focuses on the reliability and scalability of a system. Of course, in SRE’s case, that narrow focus can have a significant berth in practice, as system reliability can touch a lot of disparate areas.

### Cultural changes

DevOps breaks down silos between the development and operations teams, facilitating a collaborative and non-siloed culture. The main focus of SRE is to establish a culture of reliability and accountability.

### Incident response

DevOps teams focus on preventing incidents from occurring in the first place through tasks such as automated software development, testing and proactive monitoring. In contrast, SREs focus on investigating [the root cause of incidents](https://www.splunk.com/en_us/blog/learn/root-cause-analysis.html) and implementing measures to prevent them from happening again.

### Metrics

DevOps teams focus on [DORA metrics](https://www.splunk.com/en_us/data-insider/devops-research-and-assessment-metrics.html) such as [deployment frequency](https://www.splunk.com/en_us/blog/learn/deployment-frequency.html), lead time for changes, [mean time to resolution](https://www.splunk.com/en_us/blog/learn/mttr-mean-time-to-repair.html) (MTTR), and change failure rate. In contrast SRE teams focus on metrics such as latency, traffic, uptime, error rates, and service level agreements (SLAs).