#sdp
### Representational state transfer (REST)


REST is an architectural style enforcing a client/server model where the client acts on a set of resources managed by the server. The server provides a representation of resources and actions that can either manipulate or get a new representation of resources. All communication must be stateless and cacheable.

There are four qualities of a RESTful interface:

- **Identify resources (URI in HTTP)** - use the same URI regardless of any operation.
- **Change with representations (Verbs in HTTP)** - use verbs, headers, and body.
- **Self-descriptive error message (status response in HTTP)** - Use status codes, don't reinvent the wheel.
- **[HATEOAS](http://restcookbook.com/Basics/hateoas/) (HTML interface for HTTP)** - your web service should be fully accessible in a browser.

Sample REST calls:

```
GET /someresources/anId

PUT /someresources/anId
{"anotherdata": "another value"}
```

REST is focused on exposing data. It minimizes the coupling between client/server and is often used for public HTTP APIs. REST uses a more generic and uniform method of exposing resources through URIs, [representation through headers](https://github.com/for-GET/know-your-http-well/blob/master/headers.md), and actions through verbs such as GET, POST, PUT, DELETE, and PATCH. Being stateless, REST is great for horizontal scaling and partitioning.

#### Disadvantage(s): REST

- With REST being focused on exposing data, it might not be a good fit if resources are not naturally organized or accessed in a simple hierarchy. For example, returning all updated records from the past hour matching a particular set of events is not easily expressed as a path. With REST, it is likely to be implemented with a combination of URI path, query parameters, and possibly the request body.
- REST typically relies on a few verbs (GET, POST, PUT, DELETE, and PATCH) which sometimes doesn't fit your use case. For example, moving expired documents to the archive folder might not cleanly fit within these verbs.
- Fetching complicated resources with nested hierarchies requires multiple round trips between the client and server to render single views, e.g. fetching content of a blog entry and the comments on that entry. For mobile applications operating in variable network conditions, these multiple roundtrips are highly undesirable.
- Over time, more fields might be added to an API response and older clients will receive all new data fields, even those that they do not need, as a result, it bloats the payload size and leads to larger latencies.


[[gRPC vs REST]]
### RPC and REST calls comparison

|Operation|RPC|REST|
|---|---|---|
|Signup|**POST** /signup|**POST** /persons|
|Resign|**POST** /resign  <br>{  <br>"personid": "1234"  <br>}|**DELETE** /persons/1234|
|Read a person|**GET** /readPerson?personid=1234|**GET** /persons/1234|
|Read a person’s items list|**GET** /readUsersItemsList?personid=1234|**GET** /persons/1234/items|
|Add an item to a person’s items|**POST** /addItemToUsersItemsList  <br>{  <br>"personid": "1234";  <br>"itemid": "456"  <br>}|**POST** /persons/1234/items  <br>{  <br>"itemid": "456"  <br>}|
|Update an item|**POST** /modifyItem  <br>{  <br>"itemid": "456";  <br>"key": "value"  <br>}|**PUT** /items/456  <br>{  <br>"key": "value"  <br>}|
|Delete an item|**POST** /removeItem  <br>{  <br>"itemid": "456"  <br>}|**DELETE** /items/456|

_[Source: Do you really know why you prefer REST over RPC](https://apihandyman.io/do-you-really-know-why-you-prefer-rest-over-rpc/)_

#### Source(s) and further reading: REST and RPC



- [Do you really know why you prefer REST over RPC](https://apihandyman.io/do-you-really-know-why-you-prefer-rest-over-rpc/)
- [When are RPC-ish approaches more appropriate than REST?](http://programmers.stackexchange.com/a/181186)
- [REST vs JSON-RPC](http://stackoverflow.com/questions/15056878/rest-vs-json-rpc)
- [Debunking the myths of RPC and REST](https://web.archive.org/web/20170608193645/http://etherealbits.com/2012/12/debunking-the-myths-of-rpc-rest/)
- [What are the drawbacks of using REST](https://www.quora.com/What-are-the-drawbacks-of-using-RESTful-APIs)
- [Crack the system design interview](http://www.puncsky.com/blog/2016-02-13-crack-the-system-design-interview)
- [Thrift](https://code.facebook.com/posts/1468950976659943/)
- [Why REST for internal use and not RPC](http://arstechnica.com/civis/viewtopic.php?t=1190508)