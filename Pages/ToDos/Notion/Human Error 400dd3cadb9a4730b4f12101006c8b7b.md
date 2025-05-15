# Human Error

Tags: incident-mgmt
Category: Articles
Company: general
Status: Not started
URL: https://www.philvenables.com/post/human-error-1

- 

Several years after writing the first version of this blog I still see a repeated pattern of problematic events attributed to human error. It seems like society has a block on thinking more deeply about this. So, this post is worth an update.

> Human error is not an explanation, rather it is something to be explained.
> 

In analyzing and learning from incidents, not just security incidents, you should never be satisfied with anyone closing out a post-mortem or issue as having a root cause of human error. In every incident or close-call I’ve ever worked on, where there was an assignment of root cause to human error it actually turned out, when you looked at it more deeply, to be a situation where the humans were in fact performing heroics. These were heroics in the face of a poorly designed environment, terrible user interface, system operation issues or other factors. In reality, what was amazing in all these cases was not that there was the occasional error but that there weren’t a lot more - a hell of a lot more. The humans weren’t the problem, in fact they were the saviors already working to mitigate broader root causes. Let’s look at some examples I’ve seen over the years.

### **1. Logical Circuit Breakers**

There are many types of processes where "circuit breakers" operate to reduce the risk of runaway algorithms or other automation. Some common examples include virtual or physical server re-provisioning, imaging or reboots as well as automation to revoke access when there are changes in HR records, like someone's employment status. There are myriad of circuit breakers in automated financial trading applications, medical procedures and now increasingly in guarding the actions of agentic AI systems.

I’ve seen an event where an HR system bug erroneously terminated a whole company and then the linked identity and access management system automatically tried to revoke 20,000+ employee id’s and privileges. This was only curtailed by a fast fingered production support person. Many organizations build in circuit breakers to provide protection against exactly this type of issue. These circuit breakers are configured to automatically stop activities that appear anomalous, for example >5% of employees terminated in any one day, but also have overrides in case the activity is genuine. The problem can be, and I’ve seen a few different examples of this, where the circuit breaker is mistuned and noisy so the human operators have built up muscle-memory to dismiss the alerts and to constantly reset it. On the day there is an activity that really does need stopping then the operators just keep reseting the circuit breaker and disaster happens. The incident report then asserts this was human error in incorrectly resetting the circuit breaker - as opposed to blaming the system design and tuning such that the humans were conditioned to keep reseting it.

### **2. Problems with Mental Models**

Many, so called, human errors stem from a difference in the mental models of different parties to a system. This diagram (from the book [Engineering a Safer World: Systems Thinking Applied to Safety Engineering Systems](https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/)) is a good reminder of the difference between actual systems, what the designer intended, and what the operator perceives as the way the system should behave.

![https://static.wixstatic.com/media/683b4b_0aeef25b89ab4ce084932a7c1462bd16~mv2.png/v1/fill/w_980,h_587,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/683b4b_0aeef25b89ab4ce084932a7c1462bd16~mv2.png](https://static.wixstatic.com/media/683b4b_0aeef25b89ab4ce084932a7c1462bd16~mv2.png/v1/fill/w_980,h_587,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/683b4b_0aeef25b89ab4ce084932a7c1462bd16~mv2.png)

There are plenty of real world examples here from assumptions about magnitudes of data being entered, for example a designer thinking data entry is in millions but users or operators thinking it’s thousands. My personal favorite, or rather nightmare, was when as a mainframe system programmer I mistakenly shut down a whole system because I assumed a reboot instruction applied to the VM I was working in rather than the whole system because of the designer’s assumed intent based on what privileges people were operating under. Intuitive for the designer but highly counter intuitive for the operator.

### **3. Alert Fatigue**

There are many situations that happen in security monitoring and other observability situations. In fact, this has been covered as a factor in a number of well-known security breaches. In these cases the security systems were flashing red, so to speak, but the security operations analysts missed it, tuned it out, or failed to connect the dots. In hindsight, the one big red alert that showed a successful attack, that was missed can be ascribed to human error. This is wrong, especially when there were, in parallel, hundreds of other seemingly big, but false positive or less critical, red alerts.

The real root cause here, among others, is the failure to absolutely prioritize significant events, and to effectively mask away non-critical events using automation or ideally[autonomic security operations](https://cloud.google.com/blog/products/identity-security/modernizing-soc-introducing-autonomic-security-operations). It is also worth thinking about the desire of teams to cast things into false positives vs. true positives which causes some issues to be missed. I’ve seen occasions when people assert a true positive, that is just not critical, as a false positive. The problem with this approach is that a series of these kinds of “false positives” (i.e. low priority true positives) together can represent the build up to a serious event. The trick here is to only have false positives be actual false positives. In other words, to distinguish between false positives, true positives and varying degrees of criticality of true positives. Then, one of the most important security operations metrics is the false positive rate simply because that is what creates the risk of noise which can crowd out the true positive signal. Another big part of this is to assure the integrity of the monitoring system so that there is confidence in not only its tuning but its overall reliability, fidelity and coverage (environment and event types).

### **4. Error Prone Business Workflows**

Every organization is full of business workflows that are some combination of application, e-mail, data re-entry or transcription. Well run organizations have less of these but most have some, and poorly run organizations have lots. Inside these patchwork workflows are numerous opportunities for sensitive data to be leaked, mishandled or for fraudulent transactions to slip through. Such issues may result in the specific targeting of that organization if it is known that it is structurally unprepared to handle them. Again, the post-mortems of incidents like a fraudulent payment being dispatched are often put down to human error. This is deemed human error just because the human made one mistake in the midst of a transcription between one system and other, had a confusing cue from another system about what was authorized or many other possible factors. The real root cause, of course, is the system design which had no in-built guardrails for what was authentic, authorized and approvable. When you look at situations like this, the amazing reality is that there aren’t even more problems. Incidentally, when these types of workflows are naively automated - perhaps with carelessly deployed AI - then that approach can paper over the myriad of cracks that should really be redesigned end to end. Without such care it effectively makes the automation become “human error as a service."

### **5. Poor Confirmation Dialogs**

This is a classic. Interfaces to critical systems where there are pop-up dialog boxes to confirm an action e.g. “Do you really want to approve a transaction for $1,000,000,000.00 hit Yes / No”. Again, occasional data entry issues or incorrect approval dismissals are blamed as human error until you see people have built muscle memory to keep clicking yes. There are some interesting innovations I’ve seen from simply randomizing the Yes / No box positions, to varying the relative mouse movement speed as you approach the visual element that would approve a critical transaction (so it feels like harder work to get to that), all the way through to some interesting experiments in sensory feedback like haptic mouse vibration and system alert sounds or other warnings.

There are other related issues, often in financial services where rates or exchange fields need to be entered and the underlying semantics of the numbers change in different systems e.g. in one system you enter a percentage, in another system you enter basis points (1/100th of a percent) - this is where significant user interface consistency work is needed with particular attention to incompatible data entry semantics that exist within specific work groups.

### **6. E-Mail Data Leakage**

Another common one is blaming people for misdirecting sensitive content in e-mail. But the underlying issue is that the organization has failed to take steps to protect employees from themselves. This could be by routinely tolerating workflows in which sensitive information lives in e-mail in the first place, to not having warnings (although see point 5) that you are about to e-mail something externally or that you have chosen to permit e-mail address book auto-complete without some type of flow restriction to protect employees from common misdirection errors.

### **7. Phishing**

I probably don’t need to discuss this. But for completeness, yes, blaming users for clicking on phishing links which subsequently cause security incidents in some way is just wrong. There’s a special place in hell for post-mortems that blame users for big security incidents because *they* clicked a link. If there is an issue where the cause was clicking on a link then the diagnosis should not be human error and the infliction of more training and phishing tests, rather it should be to question the lack of defense in depth and what needs to be improved such that clicking anything isn’t harmful.

### **8. Software Vulnerability**

Ironically, software development is accepted to be so hard that it’s rare that developers are maligned for vulnerabilities, although there has been a few cases where the software error was sufficiently naive or otherwise egregious that people blame them anyway. Again, if an incident is ascribed to a programming error then that isn’t enough. The real root cause could be a combination of a lack of tool / IDE automation to detect security or other issues when the software is developed, a need for improvements in the analysis (static, dynamic, fuzzing or otherwise) at build time all the way through to the provision of well-architected and reviewed [frameworks that eliminate common errors.](https://sre.google/books/building-secure-reliable-systems/)

### 9. Production Maintenance Errors

Many of us are familiar with events when developers, operators, admins issue the wrong command in production that drops a database or reboots a server. All of these incidents and outages are human error. But the real root cause is the environment the humans work in that made these errors possible. You shouldn’t need to be routinely tinkering in production in the first place and any necessary support access should be mediated through layers of access review and subject to menu driven interfaces to reduce the scope of command line error. If for some reason you can’t put in place those structural mitigations then other approaches can help. Some of this can be strange but effective, I saw one system reduce the scope for error by making people do a quick math problem (adding small numbers) to engage a different part of their brain to make them stop and think about what they are doing. Other techniques include coloring a system window border differently and in the physical world putting floor markers or barriers around sensitive areas.

### 10.Web Site Uploads

Related to business workflow and e-mail issues there’s another pattern of incident where people are blamed for sending data outside of organizations to external web sites to perform basic functions. There were a number of incidents in various organizations a few years ago where PDF to Microsoft Office converter web sites were used, and some of them weren’t particularly careful with the data that was sent to them. There are many different types of web sites/service and this is part of the whole “shadow IT” pattern. If there’s a security breach as a result of this then it is (or was) usual to blame the employee who was often just trying to get their job done. The real error was the lack of learning that when this situation was occurring to quickly provide internal tooling and to redirect those type of web sites to that tool or to the one reviewed and preferred web site - or even just go one step further and embed the web site’s capability more fundamentally into the employees workflow.

### 11. Connecting Compromised Devices

Another seemingly common pattern, thankfully less so with[zero trust user access](https://cloud.google.com/beyondcorp-enterprise) and other controlled/mediated remote access methods, was to blame employees for connecting a laptop to the corporate network when it was unpatched and/or compromised and to then ascribe human error for the consequent security incident. Of course, the reality here is that the root cause is the fact they could do this without the interdiction of the security system.

### 12. Excess Privilege

Finally, although I could probably list another 20 categories of human errors that really aren’t, is the security incident that stems from someone having excess privilege, or a break in separation of duties for critical approvals like high value payments. This can be seen as the human error on either the security privilege administrator or the manager / supervisor who is supposed to routinely review and re-certify privileges. In reality many of these systems have poor user interfaces or otherwise don’t give the right cues to the person doing the reviewing that shows the discrepancies. Even more fundamentally, they shouldn’t be doing such recertification in the first place and people’s access should be determined according to rules, roles and attributes and such enforcement applied automatically in the privilege management system.

_____________________________________________________________

So, let’s sum up what organizations can do to shift from having to tolerate or deal with as much human error:

- Conduct[blameless postmortems](https://sre.google/sre-book/postmortem-culture/) for incidents or close-calls and do not permit human error to be used as an explanation - except if it’s to illustrate, collective, human based decision errors in the design of the system overall.
- Focus on the design of end to end business processes including applying systems and design thinking to reduce the scope for human error.
- Put in place guardrails and automation.
- Examine where fail-safe or fail-closed controls need to be put in place.
- Establish protocols where alerts / circuit-breakers or other tunable logical controls are regularly reviewed for noise levels.
- Empower employees to raise red-flags if they feel they are working in an error-prone situation.
- Apply defense in depth so impact from human error is minimized and the blast radius reduced.
- Design-in separation of duties and/or dual control for critical activities e.g. two-person code review, critical transaction approval like payments creation and payments release.
- Finally, in physical safety critical systems look for analog complements to digital controls. For example, dual turning physical keys, removing physical firing pins before a computer controlled weapons system can activate. Even in regular environments it’s useful for periodic or activity driven touching of your FIDO U2F key. As a more extreme example, I once worked on a oil drilling platform that had an analog back-up to the digital control system that when manual strain was detected, that was in excess of what the digital system should have reacted to, it would physically cut power.

**Bottom line:**in any incident analysis do not permit there to be a root cause of *human error* and above all actually look to see how the humans are adapting to avoid errors in the face of poor system design. Often you will find heroics that are keeping at bay what likely should be the much higher natural incident rate. Then apply systems and design thinking to make the environment free from the potential of or otherwise less prone to human error.