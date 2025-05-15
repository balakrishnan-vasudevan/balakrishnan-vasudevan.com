

Tags: #live-streaming
Category: Video
Company: Jio
Status: Not started
URL: https://blog.jiocinema.com/behind-the-stream-jiocinemas-workflow-for-major-events/

![https://blog.jiocinema.com/content/images/size/w1920/2024/06/aksh-yadav-bY4cqxp7vos-unsplash--1-.jpg](https://blog.jiocinema.com/content/images/size/w1920/2024/06/aksh-yadav-bY4cqxp7vos-unsplash--1-.jpg)

Preparation Meets Opportunity

Streaming video content at scale to millions of customers simultaneously is not the same as shooting a video on your phone and uploading it to a social network, nor is it as convenient as just handing off to a CDN. We'll cover at a 100K view some of the things that go into bringing that precious moment when your team wins without a stutter.

## Is it really different?

Most of us have shot video. Some of us even regularly share videos from our lives and don't even blink. How different can streaming a live event be? The short answer is - very.

Hundreds of cameras, hundreds of personnel on ground, in the studios, at the playout and hundreds of eyes before it reaches yours.

As the song goes, lets start at the very beginning.

### Production - Shoot it, Send it

How many cameras are enough? This is a complex question to answer. Depending on the event - the production team has to figure field of play, span of each camera person and ultimately what the directors vision is for the event. Most marquee events end up having close to hundred cameras on field including aerial, manned, un-manned cameras with a variety of lenses , views and all of them ultimately tied to how to "story-tell" the event.

How do you take a 100+ video feeds and make sense of them. Enter a whole bunch of fiber and networking that all bring the camera feeds back to the on ground production team that deals with ensuring that they can bundle all that video and then send either all the raw video forward or in some cases, send selected raw footage forward to the central production facilities. Do this math times venues times number of streams times video quality per stream and oh don't forget multiple redundancies, because you know, things fail.

This is also a live event, so, there is constant communication between the central team and the on-ground team to make multiple editorial decisions on the fly. This paragraph does not do justice to the complexities that nobody ever sees.

Every unique video stream that is created, whether its unique due to the way the story telling works, or the commentary language, or the graphics, every little deviation from the "master" feed needs to be produced. This requires studios, crews and individual directors to control what goes out in that version of the content. These individually are called Production Control Rooms (PCRs).

> The PCR is responsible for creating the videos we as end users consume by incorporating camera angle changes, overlays, metrics, audio mixing, and quick replays as directed.
> 

### Beam it up, Scotty - Live Streaming & Operations

After what is a series of complex hand-offs, there are a number of unique live feeds that includes the main event, any additional camera angles and any additional commentary feeds that the creative team wants to provide.

The work to now "beam/stream it" digitally begins. The block diagram below is a vastly simplified version of the next sequence of complex moves that must be executed to get this to you, our customer. After the product team has generated the distinct video feeds, the only content alteration that "downstream" teams can do, is to manage the placement of advertisements.

![https://blog.jiocinema.com/content/images/2024/06/video-flow-1.png](https://blog.jiocinema.com/content/images/2024/06/video-flow-1.png)

Following are the steps involved before the video is ready for devices to consume.

### Playout - Decide when to insert an advertisement (ad)

This step involves a human operator who listens to the director's audio and inserts ad markers, ensuring no game moment is missed by the user. Many times you might notice that an ad abruptly ends and the event resumes, this is the work of a playout operator acting on the commands of the event or stream director to rush back to the primary event.

### Encoding

The video we receive from our PCR's needs to be converted to one of the formats that are suitable for internet streaming. Notably, the most compatible and oldest format is [HLS (HTTP Live Streaming)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming?ref=blog.jiocinema.com) amongst others articulated in the graphic below. Each format is targeted to a specific device since it is most suited for it.

![https://blog.jiocinema.com/content/images/2024/06/Ashutosh-Playground-1-1.png](https://blog.jiocinema.com/content/images/2024/06/Ashutosh-Playground-1-1.png)

Streaming formats targeted to devices

The number of combinations wildly amplifies once we start to consider devices x formats x quality levels and when we add ad-targeting to the mix, we are potentially dealing with hundreds of thousands of streams. It's impossible to manage this without automation.

### Distribution - CDN's

Video streams must be distributed by a CDN, if are to guarantee a good quality customer experience. For the scale of our events, we require multiple CDN's purely because no one CDN has the capacity to handle "Bharat" scale. While a certain degree of redundancy is generated, the sheer scale of an IPL cricket match or an India men's cricket game requires massive CDN capacity.

Just in this phase alone, we have to deal with varying security options, how to handle fail-overs and ensuring that there is high fidelity in pushing the video streams into the CDN's without failures. Media streaming requires tuning of the full CDN stack to ensure that we can avoid the dreaded "rotor" for our customers.

### Operational Rigour - The "war-room"

Given the sheer number of blocks and participants required in the act of streaming video, it is imperative to keep an eye on this entire operation through the event, so that every group while it focuses on performing it's functions is able to get support and escalate across the board when there are problems.

Live sports are time-sensitive events where every second counts. The team needs to act responsibly – anticipating, identifying, and solving problems to minimise impact and ensure the best experience possible.

This is made possible by falling back to good old operational rigour. Each team has a rotating set of people "on-call". There is an over-arching leader, the game-marshal, of the whole event - who interacts with all the "on-calls" and has an overall view of what is happening - she is responsible for any decisions to be made whether in peace time or war-time (when there is an incident). She is responsible for the event going smoothly.

Live events define the word "rigour" - consider that an IPL runs for two months, with daily events. All the team members primarily from the **on-call** roster (which include all clients, backends, product, operational, and third party vendor teams) are the soldiers of this war. Each event has a war-room, lasting from 8 hours on single-match days to 14 hours on weekends with back-to-back matches. This is just ONE event. It's very common to have concurrent live events happening.

![https://blog.jiocinema.com/content/images/2024/06/img3.jpeg](https://blog.jiocinema.com/content/images/2024/06/img3.jpeg)

Coordination trumps chaos

## Event Readiness: Recon, Strategise, and Engage

For successful live streaming of an event, strict prerequisites and runtime action items must be executed. We maintain a checklist with the relative time stamps for all the major events.

The agenda of the daily pre-event checks is to ensure the entire cohesion of the feed from the source, studio, and our applications is correctly established and the features built on top of it are working perfectly.

The source team starts as early as 24 hours before the live event for '**rigging the stadium**', which means setting up all the cameras and their networking. War-room preparation begins at least 6 hours before the commencement of the match.

Once the initial setup of configuring the streams on private internet addressess is done, we start with our checks.

### Configuration Sanity (T-4 hours)

Configs are everywhere: client applications, backend services, feature toggles depending on the platform, operating system, user state, etc. These configs are crucial and shape our platform the way it works and interacts with the user.

Our on-calls and QA teams verify thoroughly these config values again (intentionally) to avoid any experience loss to the user.

Strict change control is enforced. All the deployments, and configuration are frozen by this point of time. No changes are allowed after this or during the live event - unless required to mitigate a burning fire, with the approval of the game-marshal.

### Playability Checks (T-3 hours)

The **LIVE CQC** (Content Quality Check) team run deep checks to validate the playback - audio, video and their variations across languages, platforms, operating systems, player types and the supported advertisement types. And are tested in close co-ordination with the video engineering team.

### Infrastructure Scaling (T-2 hours)

Our entire infrastructure scaling works around the estimated number of concurrent users on the platform. The peak concurrency is estimated by various factors including the teams, the week day, importance of the match, star players, etc.

We usually scale up with a buffer while scaling for these matches. These are some of the crucial questions that we ask ourselves before the match.

> Are we correctly scaled for the expected traffic? Are all the running services and their instances healthy? Are the monitoring dashboards updated and working correctly for today’s event? Do we need to give special focus on some services due to a release of a new feature?
> 

### Feature Setup & Sanity (T - 1.5 hours)

Now comes the P1 set of features (second highest priority after playback) - for example the Key Moments (realtime highlights) on the live stream, watch party, scorecard, lineups, etc.

Agenda here is to corroborate the features configured for the day’s event are correctly setup, showing appropriate data, and are working as per the specifications.

### Panic (Failure Readiness) Setup (T-1 hours)

Our systems are designed to go into a panic mode, which is a mode to ensure that when a service fails, we're able to "hide" it to varying degrees from the rest of the systems, so that there is no cascading failure leading to a complete failure.

A state where only the P0 features (features of the highest priority) are supposed to work - which include video playback, ads, login, and home page in the case of any inevitable downtime.

In case of a prolonged failure (more than a couple of minutes) panics are triggered (judiciously) to unblock users from accessing the platform. Which also buys us time to recover from the system failures and get back up quickly.

Once the above checks are passed, we make the event searchable and discoverable to the public users.

### Why not automate these checks?

All the automation - including live stream validators (playback URL reachability checks), feature validations, clients tests, API validations are in place. But they are not sufficient to reach all the corners and edges of the platform (JioBharat, old smart TVs, etc).

Given the **sensitivity of the event** (brand image, scale, accountability to rights provider, etc), the **number of teams involved** (engineering, operations - content, sports, marketing, advertisers) and the **number of components** (clients, backend services, cloud providers, telecom infra, internet backbone, etc). There is always a chance of failure or a miss which could not have been anticipated in the automation.

We periodically review the checklist, and move items to automation as and when they become feasible.

What's most important is the end user's experience, and prioritising that above all else drives our platform forward.

## On Guard: Seamless Vigilance during the event

While the event is live, there are numerous possible reasons our platform and the stream may go wrong, leading the experience to compromise. Active monitoring, being extra vigilant and keeping a check on issues are the best ways to avoid downtimes.

The Customer Support team also closely monitors social media platforms, news, and user complaints to help us identify issues and their severity. Not all users might complain, so the impact measured from these complaints is manifold. We magnify every customer complaint by 10K, since that might be the real number of customers experiencing the issue.

Engineering teams constantly monitor our technical systems and actively track the match's progress (e.g. Dhoni walking in) to forecast any potential impact on our system's functionality. They take actions such as scaling up platforms, notifying vendors, and toggling features.

Game marshals have the context of all ongoing live issues that are not yet resolved. They coordinate with all on-call folks to act swiftly and ensure a smooth experience for the users.

Consequently, being immersed in the ups and downs of the event combined with tech truly uniquely adds to the thrill and enjoyment.

## Reflect, Refine, Repeat: Post-Event Evaluation

Teams will perform the post event procedures which include removal of the live stream from the forefronts of our applications, curating and publishing clips/highlights within a minute, scale-down the infrastructure to avoid wasting the resources.

Each event is a lesson. We review stumbles, identify patterns to avoid them, and learn from what worked well. At the end of the event, we conduct root cause analyses (RCAs) for the issues and take corrective actions such as:

- to fix the problem before the next match (<24 hours)
- to mitigate the problem by either turning off or degrading the feature
- to update our checklist and test cases to avoid the problems to repeat

![https://blog.jiocinema.com/content/images/2024/06/Nothing-Changes-1.png](https://blog.jiocinema.com/content/images/2024/06/Nothing-Changes-1.png)

In conclusion, the behind-the-scenes journey at JioCinema to bring high-scale events like the FIFA World Cup and TATA IPL 2024 to our screens showcases the intricate blend of coordination, technology, and dedication involved.

From the careful preparation by the production teams to the smooth execution by the war-room and game marshals, every step ensures a great real-time experience for millions of users.

Pre-event checks make sure the platform is ready, while active monitoring during the event allows for quick responses to any issues.

While automation is crucial, manual tests and verifications are equally important to maintain a robust platform.

Post-event evaluations offer valuable insights, helping the team refine their processes and ensure continuous improvement. Ultimately, JioCinema's commitment to providing the best possible user experience drives the platform forward, making each event a lesson in innovation and excellence.

## Breathe

If you got this far, and are out of breath, spare a thought for the host of people involved in this activity on a daily basis. What we describe here is the rigour for one marquee event. On peak days we might have close to 60 concurrent live events - where similar rigour must be applied. This is a complex, multi-disciplinary exercise and requires not just technical skill, but a strong dose of empathy, on-your-feet-thinking and trusting experts in each area while forming a view of your own, so that if issues arise, one is able to contribute to recovery.

Want to widen your operational and technical muscle. We're hiring across the board. Head on over to our [JioCinema job listings](https://jobs.lever.co/viacom18/?department=Software+Engineering&ref=blog.jiocinema.com), we love working with other smart folks!