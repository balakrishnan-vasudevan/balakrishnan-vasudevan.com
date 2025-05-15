#linux

|                                              |                                                                                                                                            |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Defining DNS lookup time                     | The DNS lookup time is measured from when your computer requests a DNS record until it gets the correct response.                          |
| What Does Slow DNS Mean?                     | DNS response is considered slow when DNS resolution increases overall time enough to have a negative impact on the user experience.        |
| Factors Involved in DNS Lookup Time          | DNS lookup time depends on Internet connectivity, latency from servers, configuration particulars, and DNS server performance.             |
| Troubleshooting Slow DNS Problems            | To troubleshoot slow DNS, use network latency tools (e.g., ping and traceroute) and DNS performance testing tools (e.g., dig and DNSPerf). |
| Best Practices Ensuring Fast DNS Performance | Use CDN for high availability, perform benchmark and performance tuning, increase DNS TTL values, and use CNAME (DNS aliases).             |
This reply follows the same layers in the opposite direction. 

![Internet layer communications architecture](https://assets-global.website-files.com/610d78d90f895fbe6aef8810/65bd13244349bc099d6abc2c_20240202T0406-e970ffce-97ea-491b-afce-7b5387b5f0e4.png)

_Internet layer communications architecture_

‍

When your computer initiates a DNS resolution request, the DNS client application in your computer creates a DNS query. This query passes through your computer’s networking stack, goes out via your Internet connection, is received by your designated DNS server network, and is passed to the DNS resolver application. The resolver performs the above-mentioned iterative resolution process and returns the IP address to the requesting client. Each step in this layered communication takes time. 

Here are some of the important factors contributing to total DNS resolution time:

- End-user Internet connection speed and congestion
- Geographical distance and network latency between the user and the DNS server
- Non-optimal routing between source and destination, regardless of geographic distance
- DNS server network performance, latency, and congestion
- The geographic distance between the resolver and the TLD and authoritative DNS servers
- The computational resources of the DNS servers for handling incoming requests
- DNS application optimization and tuning based on compute resources and the number of requests

Steps:
1. Use ping to check latency and drop in traffic
2. Use dig to look at query time, use "dig +trace"
3. Use "dnsperf" like this
   ```shell
$ dnsperf -d inputfile -s ns1.bighosting.co -l 30 -Q 100


exampleshop.com	A
exampleshop.com	AAAA
exampleshop.com	MX
exampleshop.com	NS

```

These network and DNS testing utilities provide good visibility but only at a specific time. It is highly recommended to utilize network and application monitoring platforms to have continuous visibility along with storing the performance history of your networks and applications.



How to make it better?
1. Manage your own DNS
2. Increase TTL. The TTL number determines how long the records will remain in the cache of DNS resolvers. Longer TTL values mean a more significant benefit of caching, resulting in quicker DNS responses for end users.
3. One common practice in DNS records is having multiple records point to the same address. For example, we may want to use _exampleshop.com_ and _www.exampleshop.com_ to point to the same website. For this, we configure the A record for _exampleshop.com_ and define _www.exampleshop.com_ to be a CNAME record. When a user tries to open _www.exampleshop.com,_ it results in two DNS lookups: the first getting the CNAME record and the second fetching the actual IP. The result is double the time for getting DNS records. Many DNS applications and DNS providers now support ALIAS record or CNAME “flattening.” The concept is that when you define a record as an ALIAS (www.exampleshop.com) pointing to another name (exampleshop.com) and a query comes for www.exampleshop.com, the DNS server itself will perform the A record lookup of the ALIAS and return the IP address to the client in one query. This achieves the benefits of CNAME without the double lookups.
4. DNS prefetch - As a website developer, you can add a small code snippet in the HEAD element of the web page, which will make the DNS resolution of all the listed external websites occur before the user opens or views the link.
