#sdp


[[CDN]]

![[Pasted image 20250429210424.png]]
_[Source: DNS security presentation](http://www.slideshare.net/srikrupa5/dns-security-presentation-issa)_

A Domain Name System (DNS) translates a domain name such as [www.example.com](http://www.example.com/) to an IP address.

DNS is hierarchical, with a few authoritative servers at the top level. Your router or ISP provides information about which DNS server(s) to contact when doing a lookup. Lower level DNS servers cache mappings, which could become stale due to DNS propagation delays. DNS results can also be cached by your browser or OS for a certain period of time, determined by the [time to live (TTL)](https://en.wikipedia.org/wiki/Time_to_live).

- **NS record (name server)** - Specifies the DNS servers for your domain/subdomain.
- **MX record (mail exchange)** - Specifies the mail servers for accepting messages.
- **A record (address)** - Points a name to an IP address.
- **CNAME (canonical)** - Points a name to another name or `CNAME` (example.com to [www.example.com](http://www.example.com/)) or to an `A` record.

Services such as [CloudFlare](https://www.cloudflare.com/dns/) and [Route 53](https://aws.amazon.com/route53/) provide managed DNS services. Some DNS services can route traffic through various methods:

- [Weighted round robin](https://www.jscape.com/blog/load-balancing-algorithms)
    - Prevent traffic from going to servers under maintenance
    - Balance between varying cluster sizes
    - A/B testing
- [Latency-based](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-latency.html)
- [Geolocation-based](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geo.html)

### Disadvantage(s): DNS
- Accessing a DNS server introduces a slight delay, although mitigated by caching described above.
- DNS server management could be complex and is generally managed by [governments, ISPs, and large companies](http://superuser.com/questions/472695/who-controls-the-dns-servers/472729).
- DNS services have recently come under [DDoS attack](http://dyn.com/blog/dyn-analysis-summary-of-friday-october-21-attack/), preventing users from accessing websites such as Twitter without knowing Twitter's IP address(es).


#dns 

![[how-dns-works.pdf]]


![[Pasted image 20240609123744.png]]
![[Pasted image 20240609123451.png]]

## CNAME vs Alias

https://adil.medium.com/why-use-dns-alias-record-instead-of-cname-in-the-cloud-ca995b7a364d

Let’s say you’re five. Your family just moved into town and you went for a walk and got lost. All you know is that you want to go home. You find an adult and ask them “where’s my home?” Now this adult, they recognize you, because they helped your family move in yesterday, and know that you live in Oakwood Apartments.

If the adult treats your request for “where’s my home” as a CNAME, they respond with “it’s Oakwood Apartments” and then you ask them “where is Oakwood Apartments?” They then tell you “215 Main Street.” You know how to get there.

If the adult treats your request as a Route53 alias, and they know your home is Oakwood Apartments, they think up the address of it and respond “215 Main Street.”

Oh, and when you’re five,you shouldn’t wander off on your own in a strange town.


The chief difference between a CNAME record and an ALIAS record is not in the result—both point to another [DNS record](https://www.ibm.com/blog/dns-record-types/)—but in how they resolve the target DNS record when queried. As a result of this difference, one is safe to use at the zone apex (for example, naked domain such as example.com), while the other is not.

Let’s start with the CNAME record type. It simply points a DNS name, like www.example.com, at another DNS name, like lb.example.net.  This tells the resolver to look up the answer at the reference name for all DNS types (for example, A, AAAA, MX, NS, SOA, and others). This introduces a performance penalty, since at least one additional DNS lookup must be performed to resolve the target (lb.example.net). In the case of neither record ever having been queried before by your recursive resolver, it’s even more expensive timewise, as the full DNS hierarchy may be traversed for both records:

1. You as the DNS client (or stub resolver) query your recursive resolver for www.example.com.
2. Your recursive resolver queries the root name server for www.example.com.
3. The root name server refers your recursive resolver to the .com Top-Level Domain (TLD) authoritative server.
4. Your recursive resolver queries the .com TLD authoritative server for www.example.com.
5. The .com TLD authoritative server refers your recursive server to the authoritative servers for example.com.
6. Your recursive resolver queries the authoritative servers for www.example.com and receives lb.example.net as the answer.
7. Your recursive resolver caches the answer and returns it to you.
8. You now issue a second query to your recursive resolver for lb.example.net.
9. Your recursive resolver queries the root name server for lb.example.net.
10. The root name server refers your recursive resolver to the .net Top-Level Domain (TLD) authoritative server.
11. Your recursive resolver queries the .net TLD authoritative server for lb.example.net.
12. The .net TLD authoritative server refers your recursive server to the authoritative servers for example.net.
13. Your recursive resolver queries the authoritative servers for lb.example.net and receives an IP address as the answer.
14. Your recursive resolver caches the answer and returns it to you.

Each of these steps consumes at least several milliseconds, often more, depending on network conditions. This can add up to a considerable amount of time that you spend waiting for the final, actionable answer of an IP address.

In the case of an ALIAS record, all the same actions are taken as with the CNAME, except the authoritative server for example.com performs steps six through thirteen for you and returns the final answer as both an IPv4 and IPv6 address. This offers two advantages and one significant drawback:
## Advantages

### Faster final answer resolution speed

In most cases, the authoritative servers for example.com will have the answer cached and thus can return the answer very quickly.

The alias response will be A and AAAA records. Since an ALIAS record returns the answer that comprises one or more IP addresses, it can be used anywhere an A or AAAA record can be used—including the zone apex. This makes it more flexible than a CNAME, which cannot be used at the zone apex.  The flexibility of the Alias record is needed when your site is posted on some of the most popular CDNs that require the use of CNAME records if you want your users to be able to access it via the naked domain such as example.com.

## Disadvantages

### Geotargeting information is lost

Since it is the authoritative server for example.com that is issuing the queries for lb.example.net, then any intelligent routing functionality on the lb.example.net record will act upon the location of the authoritative server, not on your location. The **EDNS0** edns-client-subnet option does not apply here. This means that you may be potentially mis-routed: for example, if you are in New York and the authoritative server for example.com is in California, then lb.example.com will believe you to be in California and will return an answer that is distinctly sub-optimal for you in New York.  However, if you are using a DNS provider with worldwide pops, then it is likely that the authoritative DNS server will be located in your region, thus mitigating this issue.

One important thing to note is that NS1 collapses CNAME records, provided that they all fall within the NS1 system. NS1’s nameservers are authoritative for both the CNAME and the target record. Collapsing simply means that the NS1 nameserver will return the full chain of records, from CNAME to final answer, in a single response. This eliminates all the additional lookup steps and allows you to use CNAME records, even in a nested configuration, without any performance penalty.

And even better, NS1 supports a unique record type called a Linked Record. This is basically a symbolic link within our platform that acts as an ALIAS record might, except with sub-microsecond resolution speed. To use a Linked Record, simply create the target record as you usually would (it can be of any type) and then create a second record to point to it and select the Linked Record option. Note that Linked Records can cross domain (zone) boundaries and even account boundaries within NS1 and offer a powerful way to organize and optimize your DNS record structure.

## CNAME, ALIAS and Linked Record Reference Chart

![[Pasted image 20240609123735.png]]

![[Pasted image 20240609123451.png]]


![[Pasted image 20240609123717.png]]




![[DIG Notes.pdf]]

![[DNS.pdf]]

![[Udemy_DNS.pdf]]



### Source(s) and further reading
- [DNS architecture](https://technet.microsoft.com/en-us/library/dd197427\(v=ws.10\).aspx)
- [Wikipedia](https://en.wikipedia.org/wiki/Domain_Name_System)
- [DNS articles](https://support.dnsimple.com/categories/dns/)







[[Dropbox - DNS-based LB]]
[[DNS over TLS]]
[[Slack DNSSEC rollout issue]]


