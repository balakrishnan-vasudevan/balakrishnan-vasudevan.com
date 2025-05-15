
Tags: caching
Category: Articles
Company: general
Status: Not started

# 

[https://search.app/yF8E8KStsjqoX2a29](https://search.app/yF8E8KStsjqoX2a29)

Browser Support

- 1
- 12
- 1
- 1

[Source](https://developer.mozilla.org/docs/Web/HTTP/Headers/Last-Modified)

## How the HTTP Cache works

All HTTP requests that the browser makes are first routed to the browser cache to check whether there is a valid cached response that can be used to fulfill the request. If there's a match, the response is read from the cache, which eliminates both the network latency and the data costs that the transfer incurs.

The HTTP Cache's behavior is controlled by a combination of [request headers](https://developer.mozilla.org/docs/Glossary/Request_header) and [response headers](https://developer.mozilla.org/docs/Glossary/Response_header). In an ideal scenario, you'll have control over both the code for your web application (which will determine the request headers) and your web server's configuration (which will determine the response headers).

Refer to MDN's [HTTP Caching](https://developer.mozilla.org/docs/Web/HTTP/Caching) article for a more in-depth conceptual overview.

## Request headers: stick with the defaults (usually)

There are a number of important headers that should be included in your web app's outgoing requests, but the browser almost always takes care of setting them on your behalf when it makes requests. Request headers that affect checking for freshness, like [`If-None-Match`](https://developer.mozilla.org/docs/Web/HTTP/Headers/If-None-Match) and [`If-Modified-Since`](https://developer.mozilla.org/docs/Web/HTTP/Headers/If-Modified-Since) appear based on the browser's understanding of the current values in the HTTP Cache.

This is good news—it means that you can continue including tags like `<img src="my-image.png">` in your HTML, and the browser automatically takes care of HTTP caching for you, without extra effort.

**Note:** Developers who do need more control over the HTTP Cache in their web application have an alternative—you can "drop down" a level, and manually use the [Fetch API](https://developer.mozilla.org/docs/Web/API/Fetch_API), passing it [`Request`](https://developer.mozilla.org/docs/Web/API/Request) objects with specific [`cache`](https://developer.mozilla.org/docs/Web/API/Request/cache) overrides set. That's beyond the scope of this guide, though!

## Response headers: configure your web server

The part of the HTTP caching setup that matters the most is the headers that your web server adds to each outgoing response. The following headers all factor into effective caching behavior:

- [`Cache-Control`](https://developer.mozilla.org/docs/Web/HTTP/Headers/Cache-Control). The server can return a `Cache-Control` directive to specify how, and for how long, the browser and other intermediate caches should cache the individual response.
- [`ETag`](https://developer.mozilla.org/docs/Web/HTTP/Headers/ETag). When the browser finds an expired cached response, it can send a small token (usually a hash of the file's contents) to the server to check if the file has changed. If the server returns the same token, then the file is the same, and there's no need to re-download it.
- [`Last-Modified`](https://developer.mozilla.org/docs/Web/HTTP/Headers/Last-Modified). This header serves the same purpose as `ETag`, but uses a time-based strategy to determine if a resource has changed, as opposed to the content-based strategy of `ETag`.

Some web servers have built-in support for setting those headers by default, while others leave the headers out entirely unless you explicitly configure them. The specific details of *how* to configure headers varies greatly depending on which web server you use, and you should consult your server's documentation to get the most accurate details.

To save you some searching, here are instructions on configuring a few popular web servers:

- [Express](https://expressjs.com/en/api.html#express.static)
- [Apache](https://httpd.apache.org/docs/2.4/caching.html)
- [nginx](http://nginx.org/en/docs/http/ngx_http_headers_module.html)
- [Firebase Hosting](https://firebase.google.com/docs/hosting/full-config)
- [Netlify](https://www.netlify.com/blog/2017/02/23/better-living-through-caching/)

Leaving out the `Cache-Control` response header does not disable HTTP caching! Instead, browsers [effectively guess](https://www.mnot.net/blog/2017/03/16/browser-caching#heuristic-freshness) what type of caching behavior makes the most sense for a given type of content. Chances are you want more control than that offers, so take the time to configure your response headers.

## Which response header values should you use?

There are two important scenarios that you should cover when configuring your web server's response headers.

### Long-lived caching for versioned URLs

How versioned URLs can help your caching strategy

Versioned URLs are a good practice because they make it easier to invalidate cached responses.

When responding to requests for URLs that contain "[fingerprint](https://en.wikipedia.org/wiki/Fingerprint_(computing))" or versioning information, and whose contents are never meant to change, add `Cache-Control: max-age=31536000` to your responses.

Setting this value tells the browser that when it needs to load the same URL anytime over the next one year (31,536,000 seconds; the maximum supported value), it can immediately use the value in the HTTP Cache, without having to make a network request to your web server at all. That's great—you've immediately gained the reliability and speed that comes from avoiding the network!

Build tools like webpack can [automate the process](https://webpack.js.org/guides/caching/#output-filenames) of assigning hash fingerprints to your asset URLs.

**Note:** You can also add the [`immutable` property](https://developer.mozilla.org/docs/Web/HTTP/Headers/Cache-Control#Revalidation_and_reloading) to your `Cache-Control` header as a further optimization, though it [will be ignored](https://www.keycdn.com/blog/cache-control-immutable#browser-support) in some browsers.

### Server revalidation for unversioned URLs

Unfortunately, not all of the URLs you load are versioned. Maybe you're not able to include a build step prior to deploying your web app, so you can't add hashes to your asset URLs. And every web application needs HTML files—those files are (almost!) never going to include versioning information, since no one will bother to use your web app if they need to remember that the URL to visit is `https://example.com/index.34def12.html`. So what can you do for those URLs?

This is one scenario in which you need to admit defeat. HTTP caching alone isn't powerful enough to avoid the network completely. (Don't worry—you'll soon learn about [service workers](https://web.dev/articles/service-workers-cache-storage), which will provide the support we need to swing the battle back in your favor.) But there are a few steps you can take to make sure that network requests are as quick and efficient as possible.

The following `Cache-Control` values can help you fine-tune where and how unversioned URLs are cached:

- `no-cache`. This instructs the browser that it must revalidate with the server every time before using a cached version of the URL.
- `no-store`. This instructs the browser and other intermediate caches (like CDNs) to never store any version of the file.
- `private`. Browsers can cache the file but intermediate caches cannot.
- `public`. The response can be stored by any cache.

See [Appendix: `Cache-Control` flowchart](https://web.dev/articles/http-cache#flowchart) to visualize the process of deciding which `Cache-Control` value(s) to use. `Cache-Control` can also accept a comma-separated list of directives. See [Appendix: `Cache-Control` examples](https://web.dev/articles/http-cache#examples).

Setting either [`ETag`](https://developer.mozilla.org/docs/Web/HTTP/Headers/ETag) or [`Last-Modified`](https://developer.mozilla.org/docs/Web/HTTP/Headers/Last-Modified) can also help. As mentioned in [Response headers](https://web.dev/articles/http-cache#response-headers), `ETag` and `Last-Modified` both serve the same purpose: determining whether the browser needs to re-download a cached file that has expired. We recommend using `ETag` because it's more accurate.

ETag example

Setting `ETag` or `Last-Modified`, makes the revalidation request much more efficient by letting it trigger the [`If-Modified-Since`](https://developer.mozilla.org/docs/Web/HTTP/Headers/If-Modified-Since) or [`If-None-Match`](https://developer.mozilla.org/docs/Web/HTTP/Headers/If-None-Match) request headers mentioned in [Request headers](https://web.dev/articles/http-cache#request-headers).

When a properly configured web server sees those incoming request headers, it can confirm whether the version of the resource that the browser already has in its HTTP Cache matches the latest version on the web server. If there's a match, then the server can respond with a [`304 Not Modified`](https://developer.mozilla.org/docs/Web/HTTP/Status/304) HTTP response, which is the equivalent of "Hey, keep using what you've already got!" There's very little data to transfer when sending this type of response, so it's usually much faster than having to actually send back a copy of the actual resource being requested.

![https://web.dev/static/articles/http-cache/image/a-diagram-a-client-reque-3e18455532e4e_2880.png](https://web.dev/static/articles/http-cache/image/a-diagram-a-client-reque-3e18455532e4e_2880.png)

A visualization of a client requesting a resource and the server responding with a 304 header.

## Summary

The HTTP Cache is an effective way to improve load performance because it reduces unnecessary network requests. It's supported in all browsers and doesn't take too much work to set up.

The following `Cache-Control` configurations are a good start:

- `Cache-Control: no-cache` for resources that should be revalidated with the server before every use.
- `Cache-Control: no-store` for resources that should never be cached.
- `Cache-Control: max-age=31536000` for versioned resources.

And the `ETag` or `Last-Modified` header can help you revalidate expired cache resources more efficiently.

**Try it:** Try the [HTTP Cache codelab](https://web.dev/articles/codelab-http-cache) to get first-hand experience with `Cache-Control` and `ETag` in Express.

## Learn more

If you're looking to go beyond the basics of using the `Cache-Control` header, check out Jake Archibald's [Caching best practices and max-age gotchas](https://jakearchibald.com/2016/caching-best-practices/) guide.

See [Love your cache](https://web.dev/articles/love-your-cache) for guidance on how to optimize your cache usage for return visitors.

## Appendix: More tips

If you have more time, here are further ways that you can optimize your usage of the HTTP Cache:

- Use consistent URLs. If you serve the same content on different URLs, then that content will be fetched and stored multiple times.
- Minimize churn. If part of a resource (such as a CSS file) updates frequently, whereas the rest of the file does not (such as library code), consider splitting the frequently updating code into a separate file and using a short duration caching strategy for the frequently updating code and a long caching duration strategy for the code that doesn't change often.
- Check out the new [`stale-while-revalidate`](https://web.dev/case-studies/ads-case-study-stale-while-revalidate) directive if some degree of staleness is acceptable in your `Cache-Control` policy.

## Appendix: `Cache-Control` flowchart

![https://web.dev/static/articles/http-cache/image/flowchart-8943547beafd6_2880.png](https://web.dev/static/articles/http-cache/image/flowchart-8943547beafd6_2880.png)

The decision process for setting your Cache-Control headers.

## Appendix: `Cache-Control` examples

| `Cache-Control` value | Explanation |
| --- | --- |
| `max-age=86400` | The response can be cached by browsers and intermediary caches for up to 1 day (60 seconds x 60 minutes x 24 hours). |
| `private, max-age=600` | The response can be cached by the browser (but not intermediary caches) for up to 10 minutes (60 seconds x 10 minutes). |
| `public, max-age=31536000` | The response can be stored by any cache for 1 year. |
| `no-store` | The response is not allowed to be cached and must be fetched in full on every request. |