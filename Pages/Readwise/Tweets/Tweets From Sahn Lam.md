# Tweets From Sahn Lam

![rw-book-cover](https://pbs.twimg.com/profile_images/1343612688912371713/YFqzEFlp.jpg)

## Metadata
- Author: [[@sahnlam on Twitter]]
- Full Title: Tweets From Sahn Lam
- Category: #tweets
- URL: https://twitter.com/sahnlam

## Highlights
- System design interview tip #4: Tackling deep dive
  Deep dive is where we shine. Use this opportunity to demonstrate our ability to identify problems and develop solutions with well-justified trade-offs. 1/5 ([View Tweet](https://twitter.com/sahnlam/status/1528809514794745856))
- System design interview tip #3: Focus on the core design
  Interviews are short. There is little time to cover components unrelated to the core design.
  Skip common components not unique to the problem. 1/5 ([View Tweet](https://twitter.com/sahnlam/status/1516454280974110720))
- System design interview tip: Ask clarifying questions. 1/7 ([View Tweet](https://twitter.com/sahnlam/status/1514306963676401664))
- I did a mental exercise to try to gain an intuitive understanding of latency numbers, and just how slow some of these operations are compared to a CPU instruction. 1/5 ([View Tweet](https://twitter.com/sahnlam/status/1572628687438348289))
- How does video live streaming work on YouTube Live, TikTok Live, or Twitch?
  This is challenging because the video content is broadcast over the Internet in near real-time.
  This video explains how they achieve low "glass-to-glass" latency.
  Watch here: https://t.co/19bTFQvLCz https://t.co/VEao9A3qjf
  ![](https://pbs.twimg.com/media/Fdt-hwWVUAA9Xgf.jpg) ([View Tweet](https://twitter.com/sahnlam/status/1574995326766698497))
- HTTP/3 is hot off the press (published June 2022). It is already supported by many browsers, and a quarter of the top websites.
  This video explains the progression from HTTP/1 ➡️ HTTP/2 ➡️ HTTP/3, and its new UDP-based transport protocol called QUIC.
  https://t.co/ARZEtMvGRJ https://t.co/PhkhszHdN3
  ![](https://pbs.twimg.com/media/Fd4Mmh5VQAAz3BE.png) ([View Tweet](https://twitter.com/sahnlam/status/1575715452440887296))
- **Understanding OAuth**
  OAuth is an open standard that allows users to grant limited access to their data on one site to other sites or applications without exposing their passwords. It has become the backbone of secure authorization across the web and mobile apps.
  **The OAuth ecosystem**
  OAuth connects three main players:
  - The User who wants to grant access to their data without sharing login credentials
  - The Server that hosts the user's data and provides access tokens
  - The Identity Provider (IdP) that authenticates the user's identity and issues tokens
  **How OAuth works**
  When a user tries to access their data through a third-party app, they are redirected to log in through the IdP. The IdP sends an access token to the app, which presents it to the server. Recognizing the valid token, the server grants access.
  **The OAuth flows**
  OAuth 2.0 defines four flows for obtaining authorization tokens:
  - Authorization Code Flow - for server-side applications
  - Client Credentials Flow - when the app is the resource owner
  - Implicit Code Flow - not secure and no longer recommended
  - Resource Owner Flow - for trusted apps using owner credentials
  **Key benefits**
  - Enhances user experience by eliminating multiple passwords
  - Allows secure data access across platforms using tokens
  - Balances accessibility and security
  OAuth 2.0 has become the standard for authorization. It enables secure, convenient data sharing while protecting user accounts.
  –
  Subscribe to our weekly newsletter to get a Free System Design PDF (158 pages): https://t.co/kNfv0DVDdf<img src='https://pbs.twimg.com/media/F-ZAPVpasAAWqCL.jpg'/> ([View Tweet](https://twitter.com/sahnlam/status/1722134846661890533))
- Caching 101: The Must-Know Caching Strategies
  Fetching data is **slow**. Caching speeds things up by storing frequently accessed data for quick reads. But how do you populate and update the cache? That's where strategies come in.
  🔍 Read Strategies:
  C**ache Aside **(Lazy Loading)
  - How it works: Tries cache first, then fetches from DB on cache miss
  - Usage: When cache misses are rare or the latency of a cache miss + DB read is acceptable
  R**ead Through
  **- How it works: Cache handles DB reads, transparently fetching missing data on cache miss
  - Usage: Abstracts DB logic from app code. Keeps cache consistently populated by handling misses automatically
  📝 Write Strategies:
  Wr**ite Around
  -** How it works: Writes bypass the cache and go directly to the DB
  - Usage: When written data won't immediately be read back from cache
  Wr**ite Back (**Delayed Write)
  - How it works: Writes to cache first, async write to DB later
  - Usage: In write-heavy environments where slight data loss is tolerable
  Wr**ite Through
  -** How it works: Immediate write to both cache and DB
  - Usage: When data consistency is critical
  🚀 Real-Life Usage:
  Cac**he Aside + Write Through
  Th**is ensures consistent cache/DB sync while allowing fine-grained cache population control during reads. Immediate database writes might strain the DB.
  Rea**d Through + Write Back
  Th**is abstracts the DB and handles bursting write traffic well by delaying sync. However, it risks larger data loss if the cache goes down before syncing the buffered writes to the database.
  –
  Subscribe to our weekly newsletter to get a Free System Design PDF (158 pages): https://t.co/kNfv0DVDdf<img src='https://pbs.twimg.com/media/GCadHrRawAAc1CZ.jpg'/> ([View Tweet](https://twitter.com/sahnlam/status/1740251348669702281))
