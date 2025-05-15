# CrowdStrike: how did we get here?

Tags: incident-mgmt
Category: Articles
Company: general
Status: Not started
URL: https://surfingcomplexity.blog/2024/08/07/crowdstrike-how-did-we-get-here/

CrowdStrike has released their final (*sigh*) [External Root Cause Analysis doc](https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf). The writeup contains some more data on the specific failure mode. I’m not going to summarize it here, mostly because I don’t think I’d add any value in doing so: my knowledge of this system is no better than anyone else reading the report. I must admit, though, that I couldn’t helping thinking of number eleven in [Alan Perlis’s epigrams in programming](https://cs.yale.edu/homes/perlis-alan/quotes.html).

> 
> 
> 
> If you have a procedure with ten parameters, you probably missed some.
> 

What I wanted to do instead with this blog is call out the last two of the “findings and mitigations” in the doc:

- ***Template Instance validation should expand to include testing within the Content Interpreter***
- ***Template Instances should have staged deployment***

This echos the chorus of responses I heard online in the aftermath of the outage. “*Why didn’t they test these configs before deployment? How could they not stage their deploys*?”

And this is my biggest disappointment with this writeup: it doesn’t provide us with insight into how the system got to this point.

Here are the types of questions I like to ask to try to get at this.

*Had a rapid response content update ever triggered a crash before in the history of the company? If not, why do you think this type of failure (crash related to rapid response content) has never bitten the company before?* *If so, what happened last time?*

*Was there something novel about the IPC template type? (e.g., was this the first time the reading of one field was controlled by the value of another?)*

*How is generation of the test template instances typically done? Was the test template instance generation here a typical case or an exceptional one? If exceptional, what was different? If typical, how come it has never led to problems before?*

*Before the incident, had customers ever asked for the ability to do staged rollouts? If so, how was that ask prioritized relative to other work?*

*Was there any planned work to improve reliability* *before* *the incident happened?* *What type of work was planned? How far along was it? How did you prioritize this work*?

I know I’m a broken record here, but I’ll say it again. Systems reach the current state that they’re in because, in the past, people within the system made rational decisions based on the information they had at the time, and the constraints that they were operating under. The only way to understand how incidents happen is to try and reconstruct the path that the system took to get here, and that means trying to as best as you can to recreate the context that people were operating under when they made those decisions.

In particular, availability work tends to go to the areas where there was previously evidence of problems. That tends to be where I try to pick at things. Did we see problems in this area before? If we never had problems in this area before, what was different this time?

If we did see problems in the past, and those problems weren’t addressed, then that leads to a different set of questions. There are always more problems than resources, which means that orgs have to figure out what they’re going to prioritize (say “quarterly planning” to any software engineer and watch the light fade from their eyes). How does prioritization happen at the org?

It’s too much to hope for a public writeup to ever give that sort of insight, but I was hoping for something more about the story of “How we got here” in their final writeup. Unfortunately, it looks like this is all we get.

### Share this:

Loading...