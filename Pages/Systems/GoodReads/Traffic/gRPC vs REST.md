

Tags: api, gRPC
Category: Articles
Company: general
Status: Not started
URL: https://itnext.io/why-is-grpc-so-much-faster-than-a-json-based-rest-api-df09cb69fae5

 Two primary reasons are HTTP/2 and Protobuf.

You’ll find many performance benchmarks for REST with JSON vs. gRPC if you look around. Some of these show that gRPC reduces the latency per request by half.

So why is it so fast? 🤔

#  The first reason is HTTP/2.

I recently posted about HTTP/2 and how the asynchronous request approach in HTTP/2 reduces request wait time and embraces connection reuse.

This is a significant factor for gRPC, as gRPC leverages the HTTP/2 protocol under the covers.

While it might seem like simple RPC calls as a user, it uses HTTP underneath all of that.

# The second reason is Protobuf.

HTTP/2 + JSON can be pretty fast by itself, but using Protobuf instead of JSON pushes the performance gains even more.

Like JSON, Protobuf is a structured messaging format for exchanging data, but the most significant difference is that Protobuf is binary-based.

Being binary-based makes Protobuf much more compact, which is handy when transferring data over a network.

But Protobuf is also a lot faster than JSON during serialization and deserialization.

So not only is it faster to transport, but it’s also faster to process.

##  But performance is not free.

While gRPC has a lot of advantages, even beyond performance, it also brings some complexities.

## Complexities: Load Distribution

As with HTTP/2, gRPC will reuse connections for multiple requests by default. This multiplexing can result in unbalanced load distribution if you primarily rely on connection-based load balancing.

A layer 7 load balancer or client-side load balancing can fix this, but it needs to be accounted for.

##  Complexities: Troubleshooting

While a growing set of tools is available to troubleshoot gRPC-based services, it’s still not as easy as REST + JSON.

gRPC makes it a bit harder to perform ad-hoc requests, capture and debug payloads, validate endpoints, etc.

##  Complexities: Contracts

One of Protobuf’s advantages is clear contracts. Everyone uses the same proto file to generate packages to serialize and deserialize.

This approach is great as it removes misinterpretation, but distributing and versioning that file can be complicated, especially when trying to distribute it to external users.

#  My advice:

It’s a great approach if you need performance gains or have an environment that can handle the complexities gRPC brings.