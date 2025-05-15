# Quantum of deployment

Tags: CI/CD, deployment-system
Category: Articles
Company: Etsy
Status: Complete
URL: https://www.etsy.com/codeascraft/quantum-of-deployment

Using Deployinator we've brought a typical web push from 3 developers, 1 operations engineer, everyone else on standby and over an hour (when things went smoothly) down to 1 person and under 2 minutes.

### From the repo of truth

We&39;re deploying directly from trunk (that&39;s a whole other post!). So the first step of deploying is to update the code on the deploy host.

### Builda what now?

After the code is updated, we run "builda", an app we wrote to take our assets and bundle them up with lots of magic. We use a combination of javascript async loading, Google&39;s [closure](http://code.google.com/closure/) and versioned directories to make things like css, javascript and sprites as fast as possible.

### Rsync

At this point, we have a bunch of directories on our deploy host that represent our web tree. We then rsync to a staging area on each web box.

### Fanout

At some number of boxes, rsyncing back to a single push host stops working. We're employing a strategy called fan out. We rsync in chunks of 10 hosts at a time. This is one area where a lot of speed ups will be happening soon.

### First they came for our assets…

[Pop quiz, hotshot](http://www.youtube.com/watch?v=Ug2hLQv6WeY): Someone visits the site during a deployment and box 1 (the one they randomly get) has the new code. The html they&39;re returned refers to a new image. When they request that image, they end up on box 451.. which doesn&39;t have that asset yet. What do you do? WHAT DO YOU DO?

We've solved this with two steps. The first (mentioned above) is versioned asset directories. The next is to get those assets on ALL hosts before ANY host has the new code referring to it.

### Graceful

We&39;re using APC user caching, and expect it to have fresh data each deployment. Things like some application settings, database fields and routes are all cached for super fast lookups. However, if someone changes something in some code going out, we need to make sure that it&39;s fresh. We're currently issuing a graceful restart to our apaches on each deployment.

## Database DDLs aren&39;t code

An awesome feature of Capistrano is the ability to run schema migrations as part of your deployment. At a certain scale, however, database changes become more time consuming and dangerous. All of our schema changes go through a stringent process with several checks in place. However, not all schema is defined in the database. Whenever we have schema that&39;s defined in code, or inside the data itself, it&39;s just a normal code push.