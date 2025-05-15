Source: https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/edit

- Pages should be urgent, important, actionable, and real.
    
- They should represent either ongoing or imminent problems with your service.
    
- Err on the side of removing noisy alerts – over-monitoring is a harder problem to solve than under-monitoring.
    
- You should almost always be able to classify the problem into one of: availability & basic functionality; latency; correctness (completeness, freshness and durability of data); and feature-specific problems.
    
- Symptoms are a better way to capture more problems more comprehensively and robustly with less effort.
    
- Include cause-based information in symptom-based pages or on dashboards, but avoid alerting directly on causes.
    
- The further up your serving stack you go, the more distinct problems you catch in a single rule. But don't go so far you can't sufficiently distinguish what's going on.
    
- Every alert should be actionable.
    
- Every page should require intelligence to deal with, no robotic, scriptable responses.
    

Rules to follow when writing/reviewing a page:

1. Does it detect an **otherwise undetected condition** that is urgent, actionable, and actively or imminently user-visible?
2. Will I ever **be able to ignore this rule**, knowing it's benign?
3. Is it identifying a situation that is **definitely (going to be) hurting users**?
4. Can I take action to respond to this alert?
5. Are other people getting paged at the same time?

Monitor for symptoms and not for the cause - users don’t care if MySQL is failing, they care if their queries are failing

Users care about a small number of things:

1. Basic availability and correctness of data
2. Latency
3. Completeness/Freshness/Durability
4. Features of their service working

That's pretty much it.  There's a subtle but important difference between _database servers_ being unavailable and _user data_ being unavailable.  The former is a proximate cause, the latter is a symptom.  You can't always cleanly distinguish these things, particularly when you don't have a way to mimic the client's perspective (e.g. a blackbox probe or monitoring their perspective directly). But when you can, you should.

database servers that are unreachable results in user data unavailability

- Catch the symptom.
- Once you catch the symptom and the cause, you have redundant alerts.
- **The allegedly inevitable result is not always inevitable**: maybe your database servers are unavailable because you're turning up a new instance or turning down an old one.  Or maybe a feature was added to do fast-failover of requests, and so you don't care anymore about a single server's availability.  Sure, you can catch all these cases with increasingly complicated rules, but why bother?  The failure mode is more bogus pages, more confusion, and more tuning, with no gain, and _less time spent on fixing the alerts that matter_.

**Use these sparingly; don't write cause-based paging rules for symptoms you can catch otherwise.**

Alerting:

The best alerts in a layered client/server system come from the client's perspective:

- The **client sees the results of retries, and network latency between the client & server**, and has a better perspective on the user-facing latency and errors than the server
- the client (e.g. a mixer or application server) is **aggregating responses from many backends**, like caching services, databases, account management/authorization services, query shards, etc.  Your monitoring is more robust to changes in underlying infrastructure (and in application-level failover and retries) if you **see what the client _actually_ does.**
- the client can present a simpler view of the world than the backends.

Note that going too far can introduce agents that are beyond your control and responsibility.  If you can reliably capture a view of exactly what your users see (e.g. via browser-side instrumentation), that's great!  But remember that signal is full of noise—their ISP, browser, client-side load, and performance—so it probably shouldn't be the only way you see the world.  It may also be lossy if your external monitoring can't always contact you.  Taken to this kind of extreme, it's still a useful signal but maybe not one you want to page on.

Causes are still useful.

1. When you write (or discover) a rule that represents a cause, check that the symptom is also caught. If not, make it so.
    
2. Print a terse summary of _all_ of your cause-based rules that are firing on _every_ page that you send out. A quick skim by a human can identify whether the symptom they just got paged for has an already-identified cause. This might look like this:
    
    TooMany500StatusCodes
    
    Served 10.7% 5xx results in the last 3 minutes!
    
    Also firing:
    
    JanitorProcessNotKeepingUp
    
    UserDatabaseShardDown
    
    FreshnessIndexBehind
    

In this case, it's clear that the most likely source of 500s is a database problem; if instead, the firing symptom had been that a disk was getting full, or that result pages were coming back empty or stale, the other two causes might have been interesting.

1. Remove or tune cause-based rules that are noisy or persistent or otherwise low-value.

noisy rules have now been changed from a pager beep & ack (and investigation, and followup, and..) to a single line of text to be skimmed over.

Tickets/Reports/Email

Bugs/Tickets need follow-up.

The report can show all currently firing rules.

Every alert should be tracked through a workflow system

# Playbooks

Playbooks (or runbooks) are an important part of an alerting system; it's best to have an entry for each alert or family of alerts that catch a symptom, which can further explain what the alert means and how it might be addressed

**Tracking & Accountability**

Having a system in place (e.g. a **weekly review of all pages, and quarterly statistics**) can help keep a handle on the big picture of what's going on, and tease out patterns that are lost when the pager is handed from one human to the next.

Reasons to break these guidelines:

1. **You have a known cause that actually sits below the noise in your symptoms** - for example, if a service has 99.99% availability, but a common event causes 0.001% of requests to fail, you cannot alert on it as a symptom, because it is in the noise, but you can catch the causing event.
2. **You can't monitor at the spout, because you lose data resolution.** For example, maybe you tolerate some handlers/endpoints/backends/URLs being pretty slow (like a credit card validation compared to browsing items for sale) or low availability (like a background refresh of an inbox). At your load balancers, this distinction may be lost. Walk down the stack and alert from the highest place where you have the distinction.
3. **Your symptoms don't appear until it's too late like you've run out of quota.** Of course, you need to page before it's too late, and sometimes that means finding a cause to page on (e.g. usage > 80% and will run out in < 4h at the growth rate of the last 1h). But if you can do that, you should also be able to find a similar cause that's less urgent (e.g. quota > 90% and will run out in < 4d at the growth rate of the last 1d) that will catch most cases, and deal with that as a ticket or email alert or daily problem report, rather than the last-ditch escalation that a page represents.
4. **Your alert setup sounds more complex than the problems they're trying to detect.** Sometimes they will be. The goal should be to tend toward simple, robust, self-protecting systems (how did you not notice that you were running out of quota? Why can't that data go somewhere else?) In the long term, they should trend towards simplicity, but at any given time the local optimum may be relatively complex rules to keep things quiet and accurate.