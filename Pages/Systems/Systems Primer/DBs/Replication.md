#replication , #databases
**Table of Contents**

- [Synchronous Replication](#Synchronous%20Replication)
- [Asynchronous Replication](#Asynchronous%20Replication)
- [Semi-synchronous](#Semi-synchronous)

Database replication is the process of copying and synchronizing data from one database to one or more additional databases. This is commonly used in distributed systems where multiple copies of the same data are required to ensure data availability, fault tolerance, and scalability.

# Synchronous Replication


![[Pasted image 20250324152732.png]]
### Pros and Cons

**Fault Tolerance:** Synchronous Replication is like having a spare tire in your car. If something goes wrong, you have a backup ready to go. Since all the copies of the data are the same, if one part fails, the others can take over. It's a way to make sure that the system is always reliable and ready for anything.

**Potential Blocking Issues:** But what if you had to ask permission every time you wanted to use your spare tire, and you had to wait for an answer? That could slow you down. In Synchronous Replication, waiting for all the confirmations can sometimes cause delays. It's like waiting for a green light; it ensures safety but might slow things down a bit.

# Asynchronous Replication


![[Pasted image 20250324152742.png]]

### Pros and Cons

**Maximizing Throughput:** Asynchronous Replication is like a fast-moving conveyor belt. It keeps things moving quickly, without stopping to check every little detail. It's great for systems that need to handle a lot of requests at once. It's all about getting things done as fast as possible, even if it means taking some chances.

**Possibility of Data Loss:** But what if your postcard gets lost in the mail? In Asynchronous Replication, there's a risk that some updates might get lost or delayed. It's like playing a game without saving your progress. Most of the time, it's fine, but sometimes, you might wish you had been more careful.


# Semi-synchronous 


![[Pasted image 20250324152759.png]]

## Pros and Cons

**Addressing Durability:** Semi-synchronous Replication is like building a bridge with some strong pillars and some weaker ones. The strong pillars make sure the bridge won't fall down, but the weaker ones allow for some flexibility. This method makes sure that the most important parts are safe, without slowing everything down. It's a way to be careful without being too cautious.

**Marginal Impact on Throughput:** But what if you want the bridge to be really strong, or really flexible? Semi-synchronous Replication might not be perfect for either. It's like a compromise in a negotiation. Everyone gets something, but no one gets everything. It might slow things down a little, or it might not be quite as safe as you'd like. It's a balanced approach, and that means making some trade-offs.




Synchronous Replication is like a sturdy pair of hiking boots, safe but sometimes slow. Asynchronous Replication is like running shoes, fast but maybe not as protective. Semi-synchronous Replication is like casual sneakers, a bit of both. Understanding these differences helps you pick the right pair for your journey.


**Criticality of Data:** Some data is like a precious family heirloom. You want to keep it safe no matter what. Other data might be less important, like a casual snapshot on your phone. Understanding how crucial your data is helps you choose the right strategy. It's like deciding whether to keep something in a safe deposit box or a drawer at home.

**Consistency Requirements:** Imagine trying to bake a cake with a recipe that keeps changing. It would be a disaster! In computer systems, consistency means making sure that all the copies of the data are the same. If you need high consistency, like following a precise recipe, you'll choose one strategy. If you can handle some variation, like tossing a salad, you might choose another.

**System Throughput:** Think of a busy highway. If you need to get somewhere fast, you'll choose the route with the fewest traffic jams. In computer terms, throughput means how quickly data can move through the system. If you need high speed, like a race car driver, you'll choose one strategy. If you can take a leisurely drive, you might choose another.


[[Leaderless Replication]]