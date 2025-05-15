# What is 'HTTP Caching'? Discover how to master HTTP Caching, with free examples and code snippets.

Tags: caching
Category: Articles
Company: general
Status: Not started

[https://search.app/yCPo58amFv9nAvMS9](https://search.app/yCPo58amFv9nAvMS9)



HTTP Caching is a technique used to improve website performance. HTTP Caching can be implemented by the client, server, an intermediate node such as a proxy, or any combination of these.

Table of Contents

- [Client-side caching](https://http.dev/caching#client-side-caching)
- [Server-side caching](https://http.dev/caching#server-side-caching)
- [Network-wide performance increase](https://http.dev/caching#network-wide-performance-increase)
- [HTTP cache operations](https://http.dev/caching#http-cache-operations)
    - [Freshness](https://http.dev/caching#freshness)
    - [Validation](https://http.dev/caching#validation)
    - [Invalidation](https://http.dev/caching#invalidation)
- [Cache-Control header and directives](https://http.dev/caching#cache-control-header-and-directives)
    - [HTTP request directives](https://http.dev/caching#http-request-directives)
    - [HTTP response directives](https://http.dev/caching#http-response-directives)
- [Takeaway](https://http.dev/caching#takeaway)
- [See also](https://http.dev/caching#see-also)

## Client-side caching

In the typical situation, the first time a browser retrieves cacheable resources, such as a web page, the resources will be stored in the local HTTP Cache. The next time the browser navigates to this page, resources will be loaded from the local storage, rather than re-downloaded from the [origin](https://http.dev/origins) server. The conservation of bandwidth and reduction in server-side processing is where the performance increase comes from.

A browser cache is an example of a forward cache, which sits outside of the web server’s network. Other examples of a forward cache implementation might be at the corporate network level or with an intermediate proxy server.

Client-Side caches that are running at the browser level are private, which means that the cache is available only to a single client. A corporate-level cache may be shared, which means that different clients within the same corporate network can rely on using this cache, rather than resubmit an identical HTTP request to the server.

## Server-side caching

The idea behind server-side caching is that an intermediate node or alternative server will be used to cache responses from the [origin](https://http.dev/origins) server. This is also known as a reverse cache. The goal is to reduce the load on the server, which in turn will reduce the overall latency of the request.

An example of a reverse cache is a content delivery network (*CDN*) that stores copies of resources for quicker delivery across different points of the network. A *CDN* might have nodes in many different countries and thus a lot of traffic in one locale will not have as much of an effect, if any, on other locations.

Similarly, this type of cache is normally shared. This means that different clients will be served copies of the same resource, making it unnecessary to contact the server with a HTTP request identical to one that another client has recently made.

## Network-wide performance increase

Performance improvements from HTTP caching are not isolated to individual clients and HTTP requests. Regardless of where HTTP caching is employed, there are network-wide benefits that follow. Consider that when a client uses a private cache, not only is the latency decreased but the bandwidth requirements for all nodes along the entire HTTP request/response chain are lessened. Similarly, if a shared cache is operating at, for example, the corporate level, then nodes outside the network will not be affected by internal HTTP requests.

## HTTP cache operations

HTTP caching is optional and not supported for all HTTP request methods and HTTP responses. For example, if a user navigates to a web page and the browser sends a simple HTTP [GET](https://http.dev/get) request, which the server responds to and returns a status code indicating success, such as [200 OK](https://http.dev/200), or with a long term response which is not expected to change anytime soon, such as [301 Moved Permanently](https://http.dev/301), [308 Permanent Redirect](https://http.dev/308), [404 Not Found](https://http.dev/404) or [401 Gone](https://http.dev/401), then it can normally be cached. Subsequent identical HTTP requests will, for at least a time, instead draw on the local cache instead of sending the identical request to the server.

To manage a cache, HTTP relies upon three primary concepts. These are *Freshness*, *Validation*, and *Invalidation*. Freshness is a relative measure between the time the resource was cached and its expiry date. Validation can be used to check to see whether a cached resource is still valid after it expires, or becomes stale. Invalidation is the intention of setting a cache to stale, and it normally happens as a side effect of executing an operation that is not safe.

### Freshness

A fresh HTTP response inside a cache has not yet reached the expiry date or maximum age. The expiry date `expiry` or maximum age `max-age` is sent as part of the response. If there is no direction from the server, under certain conditions, the client may choose an expiry date using a heuristic approach.

Note

Caches are automatically considered to be stale if the client is given invalid [Cache-Control](https://http.dev/cache-control) information. For example, receiving multiple directives from the server with different values for `expiry` is considered invalid, and thus, the cache will be stale.

A cached resource might also be marked stale, in advance of the expiry, through the process of invalidation. In any event, just because a HTTP response is stale, does not mean that it’s invalid and no longer useful. If the client is unable to reach the [origin](https://http.dev/origins) server then a stale HTTP response may be better than nothing.

Various [Cache-Control](https://http.dev/cache-control) mechanisms are available to govern behavior concerning a stale response. For example, a `must-revalidate` or `proxy-revalidate` directive will restrict the use of stale responses under the relevant circumstances.

### Validation

When a HTTP response is stale, it will normally not be used unless it is first validated. Validation involves checking to see if the resource has changed since it was stored in the cache, and then updating the local metadata accordingly.

Validation is done by sending conditional HTTP requests, such as an HTTP [GET](https://http.dev/get) that includes the header [If-Modified-Since](https://http.dev/if-modified-since). This value can be compared against the [Last-Modified](https://http.dev/last-modified) header that is stored with the resource. If the value has not changed then the cached version can be used and the freshness renewed. Other timestamp-related validation methods exist, as well as a facility using entity-tag values ([ETag](https://http.dev/etag)).

A successful HTTP response to a conditional HTTP request where the cache is still valid is normally the [304 Not Modified](https://http.dev/304) status code. When this is received, the client is responsible for selecting a stored HTTP response that has a [200 OK](https://http.dev/200) status, and updating it with the data included with the [304 Not Modified](https://http.dev/304) HTTP response.

### Invalidation

A cached HTTP response is no longer of use once it has changed and the reason for having a cache expire is to ensure that it is periodically verified. If instead, the client sends a HTTP request that is unsafe, knowing that the state of the server may change as a result, it is appropriate to mark the cache stale. More specifically, if a non-error status code is received as the result of sending an unsafe HTTP request, such as HTTP [POST](https://http.dev/post), then any locally stored version is marked stale.

Again, this does not necessarily mean that the stored version is of no use. Depending on how the client is implemented, all of the stored HTTP responses might be deleted or instead, be marked such that subsequent HTTP requests require validation.

Another thing to consider is that invalidation is not guaranteed for all HTTP responses because an unsafe method only invalidates caches that it travels through. Consider, for example, that several intermediate nodes each store a local cache. Any nodes that the state-changing HTTP request does not travel will have a HTTP response that must be marked stale, but may still appear valid.

## Cache-Control header and directives

The [Cache-Control](https://http.dev/cache-control) response header is used by either the client or server to specify the relevant directives. Importantly, intermediate nodes, whether they act on the directive or not, will pass it along in case it is relevant for any of the other nodes in the path.

### HTTP request directives

The following directives can be submitted as part of a client’s HTTP request.

- `max-age`
    
    Indicates the number of seconds before the client considers the HTTP response stale. If the *max-stale* directive is not included then HTTP responses older than this will not be returned.
    
- `max-stale`
    
    If no argument is supplied then the client will accept a stale HTTP response of any age. However, if *max-stale* is assigned a value then it will be the maximum number of seconds that a HTTP response can be stale for, and have the client still accept it.
    
- `min-fresh`
    
    Indicates that the client will only accept a HTTP response that will remain fresh for at least the specified number of seconds.
    
- `no-cache`
    
    Requires that the HTTP response cannot be retrieved from a cache unless it is first validated by the [origin](https://http.dev/origins) server.
    
- `no-store`
    
    Directs that no part of the HTTP request or HTTP response be stored in a cache. This applies to caches of any type, including private caches. In cases where the information is stored unintentionally in volatile storage, well-behaved systems will attempt to remove it as soon as possible.
    
    Note: if a HTTP request containing the *no-store* directive was retrieved from a cache, then the directive does not apply to the existing stored HTTP response.
    
- `no-transform`
    
    Directs that intermediaries cannot transform the message body, regardless of whether they support caching.
    
- `only-if-cached`
    
    This indicates that the client only wants to receive a stored HTTP response. A system that receives this directive will return a stored version of the HTTP response that meets all of the requirements specified by the HTTP request. If no such copy exists then it will respond with a [504 Gateway Timeout](https://http.dev/504) status code.
    

### HTTP response directives

The following directives are sent as part of the HTTP response from the server and direct the client on the requirements for caching the accompanying resources.

- `must-revalidate`
    
    This instructs the client that once a HTTP response is stale, the client cannot rely on the cached version before it is revalidated. With this directive present, if a client is unable to reach the [origin](https://http.dev/origins) server to revalidate the cache then a [504 Gateway Timeout](https://http.dev/504) status code will accompany the HTTP response.
    
- `no-cache`
    
    Directs client that new HTTP requests cannot rely on a cached version of the resource unless it is first validated, even if stale HTTP responses are allowed.
    
- `no-store`
    
    Directs client and intermediaries not to intentionally store any part of the HTTP response in a cache. This differs from the *no-cache* directive because HTTP response caching is allowed, but cannot be used unless first validated. The *no-store* directive implies that a definite effort is made to eliminate all traces of this HTTP response from non-volatile storage as soon as possible.
    
- `no-transform`
    
    This instructs intermediaries not to transform the message body, regardless of whether a cache is involved.
    
- `public`
    
    Informs clients and intermediaries that the HTTP response may be cached, even in cases where it is normally non-cacheable or is restricted to a private cache.
    
- `private`
    
    This directive implies that this HTTP response cannot be stored in a shared cache. Furthermore, storing the HTTP response in a private cache is allowed, even in cases where the HTTP response is not normally cacheable.
    
- `proxy-revalidate`
    
    The directive is the same as *must-revalidate* but it does not apply to HTTP responses stored in a private cache.
    
- `max-age`
    
    Indicates the number of seconds before the client considers the HTTP response stale.
    
- `s-maxage`
    
    This directive is the same as *max-age* although it only refers to HTTP responses that are stored in a shared cache.
    

## Takeaway

HTTP Caching is an important practice that is used to improve network performance. There are private caches used by a single client and public caches that can be shared by many. The concepts behind cache control are freshness, validation, and invalidation, and are in place to ensure that stored messages are up to date.

## See also

- [Cache-Control](https://http.dev/cache-control)
- [Pragma](https://http.dev/pragma)
- [RFC 7234](https://datatracker.ietf.org/doc/html/rfc7234?utm_source=localhost%3A8080)