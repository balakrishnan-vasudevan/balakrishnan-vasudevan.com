#auth-system , #authentication 
# Why do we need JSON Web Tokens (JWTs)?

I always believe that requirements come first. Understanding why we need JWTs rather than diving right into the explanation will surely help.

In the modern web, you will often have several parties communicating with each other. Certain features will naturally be restricted and require some sort of authorization mechanism.

## Your typical front-end to back-end usage

The most shallow example would be a front-end application communicating with an API via HTTP requests. Using a JWT, you will be able to authorize the user. You could then take it one step further and use JWTs to perform role checks (for example, when a certain API route should only be available to admin users).

## In distributed systems

JWTs are extremely useful in distributed systems and microservices architecture, utilising the Private-Public Key signing method. This method will save you a huge amount of requests and improve the overall scalability of your application. We will talk about that later on in this article.

![](https://miro.medium.com/v2/resize:fit:700/1*FO2c5S2osc1Aot0R_bMgig.png)

The three components of a JSON Web Token

# Part 1: The JWT Standard

JSON Web Token is a standard. A typical token will consist of a header, a payload and a signature. Let’s talk about each one of those and how they are utilised.

## Header

The header contains metadata information about the JSON Web Token.

- Algorithm (`alg`): The algorithm used to sign the token. This is useful for the attempted _reproduction_ of the signature (we will talk about that later).
- Type (`typ`): The type of the token. In the case of a JWT, this will always have the `JWT` value.

You will sometimes find extra headers that were added by the _issuer_. But the above two will most certainly always be there.

## Payload

That’s what you’ve been waiting for. The payload will contain the _claims_ of the token. There are several “recommended” [standard fields](https://tools.ietf.org/html/rfc7519#section-4.1) that are defined in the JWT standard. Let’s talk about the most used ones:

- Issuer (`iss`): The entity to generate and issue the JSON Web Token (for example, your authentication service or OAuth provider).
- Subject (`sub`): The entity identified by this token. For example, if the token is used to authorize a user, `sub` could be the user ID.
- Audience (`aud`): Target audience for this JWT. For example, if the token is intended to be used by your beta testers user pool, you could specify that as an audience. It is advised to **reject** tokens with no audience.
- Expiry (`exp`): Specifies the timestamp (Unix) after which the token should not be accepted. We will talk about short-lived JWTs later on.
- Issued at (`iat`): Specifies the date at which the token has been issued.

Now, these are the _recommended_ ones. On top of those, you can feel free to add whatever extra fields you need.

For example, this would be a totally valid JWT payload:

{  
  "sub": "1dfee8d8-98a5-4314-b4ae-fb55c4b18845",  
  "email": "ariel@codingly.io",  
  "name": "Ariel Weinberger",  
  "role": "ADMIN",  
  "iat": 1598607423,  
  "exp": 1598607723  
}

**IMPORTANT:** The payload of a JSON Web Token is, by default, decodable by anyone. In fact, you can paste any JWT into [https://jwt.io](https://jwt.io/) and immediately see the claims.

## Signature

Although we would like to believe that the magic of JWTs happens in the payload, it actually happens in the signature. **This is probably the most commonly misunderstood part about JWTs.**

Often times, people use the term “encrypt-decrypt” with JSON Web Tokens. You _cannot_ decrypt the signature of a token. That is the idea behind the signature.

The signature is created from the _encoded header, encoded payload, a secret_ (or private key, read further) _and a cryptographic algorithm_. All these four components allow the creation of a signature.

signature = Crypto(secret, base64(header), base64(payload))

And this is a sample signature:

jbcOUQ2bbiYlfVtprEkaT_S6Y6yQnBDOAKDHIHjvl7g

If you are thinking _“that looks like gibberish”_, you are absolutely correct. The signature looks like gibberish. But hey, **this gibberish is unique and reproducible**.

## “Everyone can read my tokens! They can change the claims and grant themselves admin access!”

The first part is true. The second part isn’t. JSON Web Tokens are decodable by anyone. In fact, feel free to copy the following token:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZGZlZThkOC05OGE1LTQzMTQtYjRhZS1mYjU1YzRiMTg4NDUiLCJlbWFpbCI6ImFyaWVsQGNvZGluZ2x5LmlvIiwibmFtZSI6IkFyaWVsIFdlaW5iZXJnZXIiLCJyb2xlIjoiVVNFUiIsImlhdCI6MTU5ODYwODg0OCwiZXhwIjoxNTk4NjA5MTQ4fQ.oa3ziIZAoVFdn-97rweJAjjFn6a4ZSw7ogIHA74mGq0

And paste it directly into [https://jwt.io](https://jwt.io/).

![](https://miro.medium.com/v2/resize:fit:700/1*mFzPnYwPVSnhjezLc6MUnw.png)

You can immediately see all the claims in this token. That is why you should **never** store sensitive information in the token (no, a user’s role is not sensitive — a password is).

Now you are probably wondering, what prevents people from tampering with the token? Well, the signature does!

When verifying a JSON Web Token, whatever client you use will take the headers and claims, then generate a signature. It will then compare the new signature with the old signature. **JWT signatures are not decrypted** **but rather reproduced and then compared** (JWT misconception #1). If you are familiar with the world of hashing, you should now feel at home.

So, somebody tampered with the claims and set their role to `ADMIN`. The JWT verification will fail as the signature does not match anymore (remember, the signature is generated using the original payload defined by the issuer — where the role is `USER`).

Generating and signing a new JSON Web Token won’t work for them either — as they (hopefully) don’t have access to the secret or private key you use to sign your tokens. If they do, you are in trouble.

# Part 2: Common Misconceptions, FAQs and Techniques

We’ve discussed how JSON Web Tokens work. The value I hope to provide in this article is far beyond that. I hope you will be able to learn something new from this section where I talk about practical use cases, techniques and common misconceptions when using JSON Web Tokens.

## JWTs as Passports

JWTs are often used as a user’s passport. All I need in order to send requests on your behalf is your JSON Web Token. Therefore, it is your (and the service provider’s) goal to ensure the token is kept safe from any impersonator.

Always make sure to serve your clients via a secure connection (HTTPS). This will protect you and your clients from man-in-the-middle attacks, as the connection is encrypted.

Note that this approach will not protect you from other types of attacks (XSRF, for example).

## **Short-lived JWTs and Invalidating Tokens**

Short-lived tokens (tokens that expire quickly after they are issued) are highly advised. Some services have their tokens expire as soon as 5 minutes after issuing them.

After the token has expired, the auth server will issue a new access token (this action is called “token refresh”, explanation below) with the most up-to-date claim. For example, if the user role has changed from `ADMIN` to `USER`, having short-lived tokens will ensure the user’s token contains the most recent user role.

So to sum it up, short-lived tokens are useful for two main reasons:

- If your token has been compromised, it will expire quickly after and that will limit the time window during which the attacker is able to use your token and perform operations on your behalf.
- JWTs are stateless. You _cannot_ invalidate such tokens (that is pretty much the only trade-off in using this type of token). Therefore, short-lived tokens are _closest we can get_ to keeping strong consistency over stuff like user permissions and roles.

## JWT Advantages and Should You Trust Your Tokens?

JWTs are stateless. That is a blessing and a curse. To my taste, mostly a blessing.

**Why JWTs being stateless is awesome**

JWTs are not meant to be stored in a database. In a distributed system, you might have several back-end services for different purposes and business domains. All these services need is a public key (more information on this below) and they can now verify tokens from incoming requests. There is no need to send a request to your auth server for every request **(you have no idea how frequently I see this being done)**. This is a massive performance, resilience and scalability gain.

_“But Ariel, why not introduce an API Gateway to check the tokens and route internal traffic to target services?”_

You might as well do that. I have no strong opinion about this subject. What I can say, though, is that I always prefer to avoid single points of failure and bottlenecks. However, there are technologies such as [KeyCloak](https://www.keycloak.org/) that handle this at an ingress level with almost zero overhead.

**Should I trust the claims in my token, at all times?**

I will leave this decision to you. In general, I put full trust in my JSON Web Tokens and I consider the claims in my tokens to be the source of truth unless the operation is potentially destructive (changing payment method, changing password or email, etcetera). In this case, you could ask the user for an extra factor such as their password.

If you find yourself involving your Auth Service frequently, ensuring permissions against the database for every single operation, you are using JSON Web Tokens wrong.

## Refresh Tokens

Nicely bridging from the above section. Refresh Tokens are pretty much a must in every system that uses JWTs.

The way Refresh Tokens work is fairly simple. Upon initial authentication, the user will receive two tokens (note that the names might differ per auth provider):

- **Access Token:** Your typical JSON Web Token that is sent with every request. Contains the user claim.
- **Refresh Token:** This special kind of token is _persisted in a database_, mostly owned by an Authentication Service of some sort. This is often _not_ a JWT — but rather a unique hash.

As we already know, the Access Token will be sent with every request (fetch blog posts, create blog post, add comment etcetera) and at some point the token will expired. Then, the front-end will send a refresh request with the refresh token. The auth server will generate a new Access Token (JWT) with the most up-to-date claims, and send it back to the user. The user will use this token until it’s expired, and then refresh again. Over and over.

Refresh tokens can be valid for months, and that is often the case. When the refresh token expires, the user will be signed out and need to authenticate again. Do you remember the last time you had to log into Facebook, Twitter etcetera?

## Secret VS Private-Public Key (Keypair)

There are two ways to sign JSON Web Tokens. Let’s consider a very common distributed system where we have several services (Auth Service, Warehouse Service, Order Service and Notification Service).

![](https://miro.medium.com/v2/resize:fit:491/1*tJW0VFhnAneEyan9D9Cnzw.png)

Common Microservices Architecture

**Secret**

You could use any string as a secret (for example, `dontUseThisSecret123##$%83`), and the same secret will be used to verify the signature. However, if you choose to do so, please use a non-trivial secret that is hard to brute-force.

That works okay for monolithic systems. But what if you have several services that serve users? For example; Auth Service, Warehouse Service, Invoice Service, Notification Service and Order Service.

In this case, the Secret approach is seriously risky. All services will need to have access to the secret in order to verify the token. Which means:

- All services will know the secret. That increases the risk of the secret being exposed or hijacked by an attacker. I mean, when you tell your friend a secret you don’t expect it to be spread around, right?
- All services technically have the ability to create new tokens — whose responsibility is it to generate tokens? This can introduce semantic problems of ownership.

**Key Pair (Public and Private Keys)**

This is my favorite approach when working with JWTs. This utilizes a pair of keys — private and public.

Following this approach, the issuer of our token (Auth Service) will use a **private key** to sign the tokens (using RSA or ECSA algorithms). As the name implies, this key will be private and won’t be shared with any other service.

Any other service interested in verifying incoming tokens will have the **public key**. Public keys are able to verify tokens but not sign new ones. Therefore, the risks mentioned above are eliminated. There is absolutely no risk in exposing the public keys.

Using this approach, you could even let external parties verify the identity of your users. Which, in some cases, can actually be useful.

## Where Should I Store The JSON Web Tokens?

This is probably the most common question you will see about JSON Web Tokens on Stackoverflow. I will try to touch it briefly, but would rather refer you to other external resources as I am no security expert.

You always have to remember that JWTs are passports. If somebody gets access to one of your user’s tokens, he/she can send requests on behalf of you. This is bad.

Storing tokens in Local Storage is incredibly popular because it’s comfortable. However, this is **not** the most secure way to do things. It’s very XSS (Cross-Site-Scripting) vulnerable.

==Storing your tokens in a HttpOnly cookie (not a regular cookie) would be preferable. It would be better against XSS attacks, but still vulnerable to CSRF attacks. This can of course introduce annoying challenges in terms of CORS policies, but hey — it is security we’re dealing with here.==

I advise you to learn more from this [Stackoverflow answer](https://stackoverflow.com/a/37427233/1786557).

## What If I Want to Encrypt My Tokens Anyway?

In some cases you might want to apply an encryption over your token, to prevent hijackers from reading your claims. This is mostly common in server-to-server communication.

That is totally fine — feel free to apply whatever encryption you prefer over your token, as long as the receiving end can securely decrypt and view the token.

Either way, remember that performing communication over HTTPS is a must and will dramatically increase communication security.