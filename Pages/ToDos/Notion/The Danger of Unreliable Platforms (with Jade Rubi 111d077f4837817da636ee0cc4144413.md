# The Danger of Unreliable Platforms (with Jade Rubick) – Boost software reliability | SREpath

Tags: reliability
Category: Articles
Company: general
Status: Not started
URL: https://www.srepath.com/danger-of-unreliable-platform-engineering/

**Navigate this page**

[Podcast](https://www.srepath.com/category/podcast/)

Ash Patel

·

**Episode 23 [SREpath Podcast]**

## Show notes

Jade Rubick needs no introduction in the reliability and observability space. He was VP of Engineering at New Relic from 2010 to 2019.

It was my pleasure to have him talk about issues like managing expectations with teams, especially platform-based teams. We even had a spicy take on their role!

We touched on topics like enhancing engineering practices, DORA metrics, platform teamwork, and so much more. Be sure to listen all the way through to learn Jade’s amazing insights.

You can follow Jade and his engineering leadership insights via: https://www.linkedin.com/in/jaderubick/

## More about Jade

Jade Rubick is an advisor and fractional VP of Engineering having helped 20 startups improve their engineering function.

Before he stepped into this role, he was VP of Engineering at New Relic from 2010 to 2019.

In between, he advised the teams at Gremlin and Jeli, two highly respected companies in the cloud-native computing space.

Our conversation touched on fascinating areas like:

➡️ Dangers in building an unreliable platform that doesn’t hit company goals

➡️ Jade’s call for platform teams to bear the consequences when they deprecate APIs

➡️ Jade’s experience as an organizational fixer handling structural issues within struggling teams

Let’s unpack each of these:

## Dangers in building an unreliable platform

Jade and I spoke at length about how platform engineering is one of the hottest topics right now.

But platform engineering lacks clarity around one thing.

The issue is you can talk about having internal customers, **but getting to that point of driving internal customer focus is not straightforward.**

It has inherent challenges.

Without the internal customer focus,a platform can become a shoddy, unreliable experience for all but the most savvy developer.

Jade told me that the danger with platform teams is that it’s really fun to build a platform.

It can be work that feels like you’re doing something really valuable, but it’s very possible to get too disconnected from what the company needs.

Jade had this say: *“I want to see teams that are paying attention to the needs of the people that are using their work. I like to see engineers that go talk with people that are using their APIs and how to refine things by testing out new things that they’re delivering.”*

Jade suggests bolstering the platform-focused team’s outlook on how they can think like above rather than: “building [a platform] for its own sake.”

[Related article: How cloud infrastructure teams evolve – from start to maturity](https://www.srepath.com/evolution-of-cloud-infrastructure-teams/)

One trait that he suggests developing is a sense of pragmatism. Some of the best platform engineers Jade has worked with are people that:

- spend a lot of time showing their work to people that might use it
- create applications that will really exercise the things that they’re building
- don’t view building an API as a done thing

What gets built needs to be validated by a customer or multiple customers.

On top of that, the platform team can go beyond the traditional reliability mindset of “sight unseen aspects” like robust architecture, processes and monitoring.

They can also emphasize a feeling of platform reliability through minimizing steps and having effective documentation.

Jade spoke of a way of extending that even further:

> 
> 
> 
> “*Do you need some sort of way that people can extend your work or add plugins to it? Like, what is the model for extending it? Just saying it’s open source at times is enough. And if it is… do something very standard that is like the rest of engineering so that they can easily contribute to it.”*
> 

In essence, treat the platform like the product it is, and put all the stops out to make sure it’s a reliable product.

## **Platform teams should deprecate APIs with care**

Jade told me he had a spicy take on platform engineering, so I of course got curious and asked him to dish it out.

He threw a bowl of ghost peppers right in the middle of our conversation!

It started with: *“One of the challenges you’ll sometimes find in organizations is that **platform engineering teams can be the source of a lot of work for the rest of the organization.**“*

And then it just got spicier and spicier. At one point, I was hunting for my favorite sparkling passionfruit drink to cool thinks down.

[Related article: #14 Faster Incident Resolution through Data-Driven Notebooks (with Ivan Merrill)](https://www.srepath.com/faster-incident-resolution-data-driven-notebooks-ivan-merrill/)

But here’s the thing: Jade made a very valid point.

*“Every time you deprecate an API, you are creating work for the rest of the team, like all your consumers. **The purpose of a platform team is to drive efficiencies in the rest of engineering…**“*

To him, it seemed like sometimes platform teams don’t really think about the consequences of API deprecation. The other scenario he presented was forcing developes to migrate without a valid upgrade path.

Both scenarios create a lot of work for the rest of the organization.

His take is that platform teams should have to do with that work themselves as much as possible. The platform teams should – where feasible – migrate their internal teams to use the new APIs.

His rationale makes sense:

“Because if you’re not having to bear the cost of it, you’re not going to do the work to make it really easy.”

I put in my two cents once I pulled myself out of the swimming pool to cool down from that zinger.

I think a lot of platform engineers are used to developing a replacement API and then saying, “Here you go, go for it.”

Without a little handholding – at least in the beginning – you will risk developers sending API requests to nowhere or at least having a huge support burden. I’ve seen this happen in organizations.

## **Supporting reliability as an organizational fixer**

I learned from the grapevine that Jade has a reputation among engineers as an organizational fixer.

So we naturally had to deepdive into how this manifested…

Jade’s response was fascinating.

He estimates that **when he left New Relic,** **there were about 60 engineering teams.**

> 
> 
> 
> *“When you have that many teams, there’s always will be some teams that are really struggling.”*
> 

He’d work with his boss, Alex Kroman (GM and SVP of Engineering at New Relic), to work out which teams were in need of help. Jade’s next step was to go hands on with those teams.

Over time, he worked out a routine where he’d go in to investigate the situation and talk with everybody involved. Jade often found a few underlying structural issues.

Sometimes he found that:

- teams had unrealistic expectations set upon them
- relationships among colleagues were not functioning as expected
- roles were not defined so people could not communicate well
- team decisionmaking was flawed due to weak communication among different roles within

[Related article: #21 – Better SRE in 2024 is all we can hope for](https://www.srepath.com/better-sre-vs-incident-responder/)

This work became a regular fixture in Jade’s schedule. So much so that he learned a peculiar thing.

Leaders surrounding these affected teams *thought* they knew what the problems were. But **the actual problems that Jade uncovered were nothing like what the leaders told him**.

Deepdiving into these issues in a hands on way allowed Jade to turnaround many of the struggling teams into model teams in as little as 6 months.

I think the lesson from this is that we need to truly step back and listen rather than assume what’s going on. Sometimes it takes someone not as attached to the day-to-day to work out the true dysfunction.

As Jade put it,

> 
> 
> 
> *“I think what was significant about that to me is that a lot of times people would point at the people involved, but it usually was not the people. It was ways in which the people were being set up to fail. They weren’t getting time to fix their reliability problems.”*
> 

In [Episode #23 of the SREpath podcast, Jade gives me his take on how VPEs see platforms & reliability](https://open.spotify.com/episode/4O2QGSEx89lk19Wx76AWev?si=0b6e2b96036a45f2) [Spotify link]

I’m sure you will gain some interesting ideas to take back to your team. If anything the spicy take on platform teams will have you screaming for a cool drink. How fun!

- [Author](https://www.srepath.com/danger-of-unreliable-platform-engineering/#abh_about)
- [Recent Posts](https://www.srepath.com/danger-of-unreliable-platform-engineering/#abh_posts)

Ash Patel

![https://www.srepath.com/wp-content/uploads/gravatar/3.jpeg](https://www.srepath.com/wp-content/uploads/gravatar/3.jpeg)

Connect?

Reliability Nut at [SREpath](https://www.srepath.com/)

Ash has an unhealthy obsession with software reliability. Maybe it’s got to do with the trauma of working at a few companies where software kept slowing or went down while he worked to turn it around. His ma hopes that he can one day turn this passion into a respectable job or business. Still waiting…