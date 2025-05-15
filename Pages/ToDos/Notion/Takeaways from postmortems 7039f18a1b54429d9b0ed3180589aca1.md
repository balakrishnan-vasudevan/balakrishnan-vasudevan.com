# Takeaways from postmortems

Tags: incident-mgmt
Category: Articles
Company: general
Status: Not started
URL: https://leaddev.com/team/5-takeaways-running-50-postmortems

You have **0** further articles remaining this month. [Join LeadDev.com for free](https://leaddev.com/register?s=dw) to read unlimited articles.

Learn how to create a blameless culture and ensure everyone can move on from an incident postmortem with confidence.

During my time at Etsy, I was involved in their renowned [blameless postmortem culture](https://www.etsy.com/codeascraft/blameless-postmortems). As a postmortem facilitator, I have seen it all, from small team process hiccups to full-site outages. For three years, I also taught their internal postmortem facilitation class.

The following insights from these experiences may be able to help if you’re eager to start a [postmortem practice](https://www.jeli.io/howie/welcome), or improve what you already run.

![https://leaddev.com/sites/default/files/inline-images/Screenshot%202024-03-19%20at%2014.20.32.png](https://leaddev.com/sites/default/files/inline-images/Screenshot%202024-03-19%20at%2014.20.32.png)

A blameless postmortem meeting taking place.

## 1. You don’t need to be an expert to lead a postmortem

While I was running my postmortem facilitation classes I often got asked, "Do I need to be a subject matter expert (SME) to lead a postmortem?" The assumption here is that dissecting an incident requires intimate knowledge of the systems involved. But my experience taught me that the key traits for being a great postmortem facilitator are [asking better questions](https://github.com/etsy/DebriefingFacilitationGuide/blob/master/guide/05-the-art-of-asking-questions.md) and [leading with empathy](https://leaddev.com/team/4-pillars-empathetic-leadership).

A key principle of modern accident investigation is that it’s the people within a complex system who bring the adaptability and creativity needed to keep it functioning. Since the resilience of the system relies on these people, we must approach the postmortem process from their perspective and empathize with their experience. Developing this empathy is an essential skill when it comes to being an effective facilitator.

Some of the best facilitators I've known weren't even engineers. Their lack of preconceived notions about how things should work empowered them to scrutinize seemingly routine processes contributing to an issue in a complex system. This works both ways. As an engineer, I have conducted postmortems for non-engineering situations such as interactions with vendors, or product planning that went awry. I may not have had direct experience with these situations before, but by grounding my analysis in empathy for the people at the center of the incident, I could always overcome any gaps in knowledge.

## 2. Pre-meetings are critical

Whether you’re assembling 50 engineers or five, you want to maximize the return on this precious time. To do this, a pre-meeting with key stakeholders is essential.

Invest just 30 minutes for a pre-meeting huddle with the main stakeholders. Use this time to review the incident timeline, clarify any jargon, and establish a narrative framework for the main postmortem event. This prep work yields immense benefits, allowing you to:

- **Identify subject matter experts** – You'll know exactly who to direct specific inquiries to, ensuring a smooth flow of information.
- **Boost efficiency** – By establishing a shared understanding of the incident beforehand, the postmortem can tackle deeper questions and solutions without getting bogged down in basics.
- **Empower participation** – Promoting a shared understanding *also* gives participants the right context, reducing pressure on engagement and encouraging broader team involvement with meaningful contributions.
- **Develop lines of inquiry** – I prompt participants to come up with three key aspects of the incident that they would like to focus on in the postmortem. This provides a signal to the facilitator on where they should direct the conversation and dig in.
- **Highlight sources of conflict** – Not all postmortems are by default blameless. In the pre-meeting, take note of potential hazardous topics that will arise in the postmortem. Doing so can help you plan ahead to route around more challenging conversations such as a [confrontation between peers](https://leaddev.com/culture-engagement-motivation/managing-conflict-engineering-teams) that should be handled elsewhere.

**Tip**: Make sure that you clarify organization-related acronyms as well as technical acronyms. I once had someone refer to “bird” in a postmortem and I had to pause the discussion to ask if “bird” is a person, a team, a technology, or a Slack channel.

## 3. Remediation is non-deterministic

Remediation is a constant point of tension between engineering and higher leadership positions. There's a common assumption that a postmortem or debrief should culminate in a checklist of tasks designed to prevent future recurrences. But the true value of a postmortem is its role in sharing knowledge across the organization.

I consider a postmortem successful when, six months down the road, a similar incident arises and someone recalls a vital detail – a shell command, a dashboard, the right expert to message on Slack – and resolves the issue before escalation. This shared knowledge, woven into the team's collective memory, is the heart of a postmortem's impact.

Leadership will often ask for a quantified value of a postmortem in meetings, and it's challenging to provide a concrete answer. Look for the value of postmortems in:

- **Long-term trends of incident occurrences**: Are similar issues becoming less frequent and severe?
- **Developer happiness**: Do engineers feel heard, supported, and equipped to handle challenges as a result of incident postmortems?
- **Confidence in action**: Are less-experienced engineers gaining confidence and responding to more incidents as a result of information shared in these meetings?

**Tip**: If you want to dive further into this topic then I recommend [this talk](https://www.adaptivecapacitylabs.com/blog/2020/05/06/how-learning-is-different-than-fixing/) by John Allspaw.

## 4. Celebrate the role of engineers in a complex system

Human experience plays a critical role in system resilience. At the heart of every robust engineering system lies an often-overlooked superpower: the human who "just happened to be."

“Just happened to be” are the words you see in a timeline when the right person happened to be in the right place at the right time. For instance, someone who just happened to be online at the time when the database hosts ran out of memory, or lurking in the team’s Slack channel when cascading configuration management failures caused a key service to go offline. I have seen these four words save millions of dollars in potential lost revenue.

It's tempting to chalk these interventions up to pure chance, however in reality they are anything but. They represent the unique flex and adaptive intelligence that humans provide, filling the gaps in even the most sophisticated systems. These moments should be celebrated to highlight the importance of engineer involvement. Plus, it is almost always a moment of levity that can brighten the mood and encourage people to contribute to the discussion.

**Tip**: When unpacking incidents in the postmortem, bring attention to situations in which someone intuitively knows how to navigate and solve an issue. Intuition might be subconscious reasoning, but it is always grounded in experience. Sharing how they handled the situation can [promote team learning and help with future incidents](https://leaddev.com/managing-time-crisis/how-turn-engineering-incident-opportunity).

## 5. Be mindful of self-blaming

At the beginning of every postmortem, we state that we’ll discuss an incident openly, “without fear of retribution or humiliation.” I have found that people are very willing to create a safe space free of retribution. The biggest challenge to overcome is the second part: humiliation.

Unlike their tolerance for others' missteps, individuals tend to be much more unforgiving toward themselves. They readily "fall on the sword," especially when an incident pivots on a single action like a code commit or clicking a checkbox. Publicly admitting fallibility before peers in these situations is difficult. In these moments be sure to pay close attention to people reflecting on their actions and describing what they “could have done” or “should have done.” When you hear this it is important to pause the postmortem and state emphatically that there is no need to be self-deprecating. Everyone comes to work to do a good job and accidents are a part of every complex system. It is how we react to them that is important.

**Tip**: For an incident that hinges on one principal actor it helps to ask them to walk through the entire incident in the pre-meeting. Having done it once in front of a small audience they will be less nervous when the postmortem begins.

## Final thoughts

My work with blameless postmortems, especially mentoring new facilitators, has been the most rewarding part of my 15-year career as an engineer. I encourage everyone to try facilitating a postmortem, no matter what your role. Beyond the surface-level benefits of developing a deeper understanding of how disparate services combine to create a complex system, you will also gain a unique perspective on how the people in that system collaborate with each other to keep it working.