# Himeji: A Scalable Centralized System for Authorization at Airbnb

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article3.5c705a01b476.png)

## Metadata
- Author: [[Alan Yao]]
- Full Title: Himeji: A Scalable Centralized System for Authorization at Airbnb
- Category: #articles
- URL: https://medium.com/p/341664924574

## Highlights
- The initial approach to moving the permission checks from monolith to SOA was to move these checks to presentation services. However this led to several problems:
- Duplicate and difficult to manage authorization checks: Often multiple presentation services that provided access to the same underlying data had duplicate code for authorization checks. In some cases these checks became out of sync and difficult to manage.
- Fan out to multiple services: Most of these authorization checks required calling into other services. This was slow, the load was difficult to maintain, and it impacted overall performance and reliability.
- We moved the authorization checks to data services, instead of performing authorization checks only in presentation services. This helped us alleviate duplicate and inconsistent check issues.
- We created Himeji, a centralized authorization system based on Zanzibar, which is called from the data layer. It stores permissions data and performs the checks as a central source of truth. Instead of fanning out at read time, we write all permissions data when resources are mutated. We fan out on the writes instead of the reads, given our read-heavy workload.
- Himeji exposes a check API for data services to perform authorization checks.
- A permissions check will look like the following, which states “can user 123 write to listing 10’s description?
- Similar to Zanzibar, the basic unit of storage for Himeji is a tuple in the form entity # relation @ principal.
- An entity is the triple (entity type : entity id : entity part); this comes from a natural language approach: LISTING : 10 : DESCRIPTION → “listing 10’s description”.
- An entity id is the corresponding id in the data source of truth.
- An entity type defines the data permissions apply to. Examples: LISTING, RESERVATION, USER
- An entity part is an optional component. Examples: DESCRIPTION, PRICING, WIFI_INFO
- A relation describes the relationship, like OWNER,READ, or WRITE but can be specific to use cases; some examples include HOST for the host of a reservation and DENY_VIEW for denying access to a listing.
- A principal is either an authenticated user identity like User(123), or another entity like Reference(LISTING:15).
