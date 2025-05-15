https://www.nslookup.io/learning/the-life-of-a-dns-query-in-kubernetes/?ref=architecture-notes
Service discovery in Kubernetes is a crucial component of the overall architecture. It allows incoming requests to be routed to the correct workloads running in the cluster. DNS plays a key role in this process.

When a pod performs a DNS lookup, the query is first sent to the DNS cache on the node where the pod is running. If the cache does not contain the IP address for the requested hostname, the query is forwarded to the cluster DNS server. This server handles service discovery in Kubernetes.

The cluster DNS server determines the IP address by consulting the Kubernetes service registry. This registry contains a mapping of service names to their corresponding IP addresses. This allows the cluster DNS server to return the correct IP address to the requesting pod.

Services:

A service has an IP that, when accessed, redirects connections to a healthy pod backing that service.

A new service in K8S, the cluster DNS server creates an A record for the service.

This allows pods to access the service using its DNS name.

DNS service updates A record whenever the IP addr of the service changes.

Example of a service definition:

```
apiVersion: v1
kind: Service
metadata:
  name: foo
  namespace: bar
spec:
  ports:
    - port: 80
      name: http
```

DNS records for this look like this:

```
foo.bar.svc.cluster.local                  30   A   10.129.1.26
_http._tcp.nginx.default.svc.cluster.local 3600 SRV 0 100 80 10-129-1-26.foo.bar.svc.cluster.local.
```

To create the fully qualified domain name for this service, we use the name of the service (**`foo`**), the namespace (**`bar`**), and the cluster domain (**`cluster.local`**).

How a service does a DNS lookup?

![https://www.nslookup.io/img/flow-of-a-dns-query-in-kubernetes.8671b839.png](https://www.nslookup.io/img/flow-of-a-dns-query-in-kubernetes.8671b839.png)

1. Pod needs to perform a DNS lookup.
2. Query sent from pod to local DNS resolver in the pod.
3. Resolver uses resolv.conf file. nodelocaldns server is set as default recursive DNS resolver in this file, that acts as the cache. This file is provisioned by kubelet.

```
search namespace.svc.cluster.local svc.cluster.local cluster.local  ==> specifies which domain suffixes should be searched when incomplete domains are given
nameserver 10.123.0.10 ===> Address to forward all queries to 
options ndots:5  ===> When a query for the absolute domain is made directly instead of first appending the search domains.
```

1. If resolv.conf does not have the IP address for the requested hostname, query is forwarded to cluster DNS server - Coredns.
2. Coredns determines IP address by checking the Kubernetes service registry.
3. Registry contains a mapping of service names and their corresponding IP addresses.
4. If a domain is not in the service registry, it is forwarded to an upstream DNS server.

ndots:

Suppose a pod named foo performs a DNS lookup for **`bar.other-ns`**. If the **`ndots`** option is set to 5 (the default value), the resolver will count the number of dots in the domain.

If there are fewer than 5 dots, the search domains will be appended before the DNS lookup is performed on the DNS server. If there are 5 or more dots, the domain will be queried as-is without appending the search domains. In this example, **`bar.other-ns`** has less than 5 dots, so the search domains will be appended before the DNS lookup is performed.

By default, the search domains are:

- <requester namespace>.svc.cluster.local
- svc.cluster.local
- cluster.local

Until a valid response is found, these search domains are appended to the domain and queried. The resolver will try the following queries one by one:

- bar.other-ns.<requester namespace>.svc.cluster.local
- bar.other-ns.svc.cluster.local (⇐ match found!)

The bar service will be listening on **`bar.other-ns.svc.cluster.local`**, so a match is found and the proper A-record is returned.

Sample config:

```
apiVersion: v1
kind: Pod
metadata:
  namespace: default
  name: dns-example
spec:
  containers:
    - name: test
      image: nginx
  dnsPolicy: "None"  =====> pod will not use default DNS settings provided by the cluster, it will instead use settings in dnsConfig 
  dnsConfig:
    nameservers:
      - 1.2.3.4
    searches:
      - ns1.svc.cluster-domain.example
      - my.dns.search.suffix
    options:
      - name: ndots
        value: "2"
      - name: edns0
```

Authoritative DNS server:

coredns replaced kube-dns as the default in k8s 1.13.

The DNS server adds all services to its authoritative **[DNS zone](https://www.nslookup.io/learning/what-is-a-dns-zone/)** , so that it can resolve domain names to IP addresses for Kubernetes services.

coredns sample config:

```
.:53 {
    errors ===> errors logged to stdout
    health { ==> health of coredns is reported to localhost:8080/health
        lameduck 5s ==> make the process unhealthy then wait for 5 seconds before the process is shut down.
    }
    ready  ==> An HTTP endpoint on port 8181 will return 200 OK, when all plugins that are able to signal readiness have done so.
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        fallthrough in-addr.arpa ip6.arpa
        ttl 30  ==> TTL of 0 will prevent records from being cached
    }
    forward . /etc/resolv.conf  ==> Any queries that are not within the Kubernetes cluster domain are forwarded to predefined resolvers (/etc/resolv.conf).
    cache 30  ==> Enables a frontend cache
}
```

Nodelocaldns:

To improve the performance of DNS queries in a Kubernetes cluster, a cache layer can be added on each node using the **[nodelocaldns](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/)** component. This component caches the responses to DNS queries.

If no response is found in the cache, the query is forwarded to the authoritative nameserver (coredns).

TTL:

By default, CoreDNS sets the TTL of DNS records to 30 seconds. This means that when a DNS query is resolved, the response will be cached for up to 30 seconds before it is considered stale. The TTL of DNS records can be modified using the **`ttl`** option in the CoreDNS configuration file.

Shorter TTL = Accurate DNS response = Increased load on DNS server

Longer TTL = Lower load on DNS server = Outdated DNS records


## SRV Records

Kubernetes also uses SRV (service) records to resolve the port numbers of named services. This allows clients to discover the port numbers of services by querying the DNS server for the appropriate SRV record.

```
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: default
spec:
  ports:
    - port: 80 ==> Port 80 is exposed and given the name http
      name: http
```

Because this port is named, K8S will generate a SRV record with the name = **_<port>._<proto>.<service>.<ns>.svc.<zone>**

In this case, the SRV record would be = **_http._tcp.nginx.default.svc.cluster.local**

```
dig +short SRV _http._tcp.nginx.default.svc.cluster.local
0 100 80 10-129-1-26.nginx.default.svc.cluster.local.
```

Some services, such as Kerberos, use SRV records for the discovery of the KDC (Key Distribution Center) servers.