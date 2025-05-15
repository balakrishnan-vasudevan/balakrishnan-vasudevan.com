#auth-system


Link: https://medium.com/airbnb-engineering/himeji-a-scalable-centralized-system-for-authorization-at-airbnb-341664924574

## Why?
multiple presentation services that provided access to the same underlying data had duplicate code for authorization checks.
these authorization checks required calling into other services. This was slow, the load was difficult to maintain, and it impacted overall performance and reliability.
## The Solution

![](https://miro.medium.com/v2/resize:fit:1094/0*vLMmJuKbeDge1N5T)

## What was changed?
1. Moved authorization checks to data services (instead of performing them in presentation service).
2. Himeji (based on Zanzibar) was created - centralized authorization system - stores permissions data, performs the checks as central source of truth. Fan out the writes instead of the reads, given that authorization here is a read-heavy workload.

## API
// Can the principal do relation on entity?  
boolean check(entity, relation, principal)

## Storage
Basic unit of storage = Tuple = entity # relation @ principal
Entity = triple = (entity type : entity id : entity part) 
A **relation** describes the relationship, like `OWNER`,`READ`, or `WRITE` but can be specific to use cases; some examples include `HOST` for the host of a reservation and `DENY_VIEW` for denying access to a listing.
A **principal** is either an authenticated user identity like `User(123)`, or another entity like `Reference(LISTING:15)`.
##Config
If we had to write a tuple for each exact permission that is checked, the volume of data and denormalization would grow exponentially.
Himeji uses a YAML-based config language.
Suppose user 123 is the owner of listing 10. Then the database will have the tuple `LISTING : 10 # OWNER @ User(123)`.

When we request `check(entity: "LISTING : 10", relation: WRITE, userId: 123)`, Himeji interprets `LISTING # READ` as the union of `READ` & `WRITE`, and transitively `LISTING # WRITE` as the union of `WRITE` & `OWNER`. Therefore, it will fetch the following from its database, with any matches belonging to the set of `LISTING # WRITE`:

Query LISTING : 10 # WRITE @ User(123) => Empty  
Query LISTING : 10 # OWNER @ User(123) => Match User(123)

So for example, user 123 need only have `LISTING : 10 # OWNER @ User(123)` to be in the `LISTING : 10 # WRITE` set.

## Architecture & Performance

![](https://miro.medium.com/v2/resize:fit:2000/0*Mu6CzNQKbugA7iZu)


- The **orchestration layer** receives requests from clients and is responsible for issuing fetches for data, according to configuration logic, and parses the results. The orchestration layer routes to the caching layer with consistent hashing.
- The **caching layer**, which is sharded and replicated (one instance per AZ per shard), is responsible for filtering in-memory and deduplicating loads from the database on misses. Each shard is assigned a set of data to own via consistent hashing. We target a ~98% hit rate on the cache.
- The **data layer**, which consists of logically sharded databases.

## Changes from Zanzibar
1. Separate the request orchestration tier from the caching tier, so that the orchestration tier can be updated more easily without restarting the cache.
2. Invalidate the cache shards based on [published mutations from the databases](https://medium.com/airbnb-engineering/capturing-data-evolution-in-a-service-oriented-architecture-72f7c643ee6f).
3. Use Amazon [Aurora](https://aws.amazon.com/rds/aurora/?aurora-whats-new.sort-by=item.additionalFields.postDateTime&aurora-whats-new.sort-order=desc) for database storage as part of our [cloud journey](https://medium.com/airbnb-engineering/our-journey-towards-cloud-efficiency-9c02ba04ade8), which differs from Zanzibar’s usage of Spanner.

## Add-ons/Tooling

- **Configuration-based backfill:** Migrating the existing permission checks into Himeji required us to backfill the permission tuples for existing entities. Instead of each data service owner building their own backfill flow, we built a generic solution based on Apache Airflow and Apache Spark. Service owners have to only provide a small config which indicates how their tuple should be formed from their database exports.
- **Automatic code generation:** To make onboarding easier, we provided scripts to auto-generate Java and Scala code.
- **Thick client:** We provided a thick http client with logging, metrics, and migration rollout controls.
- **UI tool for debugging and one-off tasks:** Investigating one-off permission issues can get tedious and requires checking permission data written in the system, so we built a UI to analyze data and fix permissions issues.