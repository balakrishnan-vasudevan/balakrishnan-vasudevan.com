#auth-system , #authentication 
Figuring out who people are is hard on the internet. It's pretty tough to keep track of all that yourself. OAuth is basically the industry standard for web apps to vouch for each other. You're basically asking, Twitter, Facebook, Github, whoever to keep track of it for you in a few steps:

1. Someone walks up to your website and asks to come in. You have no idea who they are and have very little idea how to check. You ask Facebook (or whoever) to check for you since they have a whole system in place to do that.
2. They tell Facebook who they are (usually through a reroute to a login page or through a pop up and they supply their Facebook credentials) and then Facebook turns around and tells you, 'Yeah, they're who they say they are' and hand you a signed piece of paper with their seal of approval on it (Rerouted back to your application with an auth code).
3. Now that Facebook said it was okay and gave you the thumbs up, you can now tell Facebook that you're cool with letting them in if they're cool with it. Facebook says 'okay' tells the person what information Facebook is going to tell you, and then gives them a temporary key (passing the auth code for a web token).

This key is now good for whatever you set it up to be good for (at the registration of your app) and works for those approved parts of Facebook as well. Facebook told you that person is who they say they are and they're good at knowing these types of things.


OAuth stands for Open Authorization. It's a process through which an application or website can access private data from another website. It provides applications the ability to "secure designated access." For example, you can tell Google that it's OK for abc.com to access your Google account or contact without having to give abc.com your Google password.

OAuth never shares password data but instead uses authorization tokens to prove an identity between consumers and service providers. OAuth is an authentication protocol that allows you to approve one application interacting with another on your behalf without giving away your password.

To understand this, let's take the example of Facebook. When an app on Facebook asks you to share your profile and pictures, Facebook acts as a service provider: it has your data and image, and that app is a consumer. If you want to do something with your picture with the help of this app, you need to provide permission to this app to access your images, which the OAuth manages in the background.

How Does the OAuth2.0 Work

![[Screenshot 2025-05-11 at 5.05.50 PM.png]]

The following explains the working of the above sequence diagram of Oauth 2.0 implementation:

1. Let's assume the client requests authorization to access protected resources owned by the resource owner by redirecting the client to the authorization server.
2. The resource access request is authenticated and authorized by the resource owner from the web application, and the authorization grant is returned to the client by an authorized endpoint.
3. There are four types of Grant Protocol defined by OAuth 2.0: **Authorization Code**, **Client Credentials**, **Device Code**, and **Refresh Token**.
4. The client requests the access token from the authorization server by presenting the authorization grant returned from the authorized endpoint and authentication of its own identity to the token endpoint. A token endpoint is a URL such as [https://your_domain/oauth2/token](https://your_domain/oauth2/token).
5. The access token will be issued to the client for valid authentication and authorization grant by the authorization server or authentication provider.
6. By presenting the access token for authentication, the client can request the protected resources from the resource server.
7. The requested resources are returned to the application (client) with the valid access token from the resource server.

**Also Read: [Guide to Authorization Code Flow for OAuth 2.0](https://www.loginradius.com/blog/engineering/authorization-code-flow-oauth/)**

Why You Should be Using OAuth

OAuth provides applications the ability to secure designated access. In the traditional method, before OAuth, sites ask for the username and password combination for login and use the same credentials to access your data.

With OAuth flow, instead of sending the username and password to the server with each request, the consumer sends an API key ID and secret. In this scenario, the consumer communicates to their identity provider for access. The identity provider generates an encrypted, signed token that grants the application access by authenticating the consumer. This process works on trust between the Identity Provider and the application. It will create a better interface for web applications.

Working with OAuth Token & Scope

The authorization server authenticates the client and validates the authorization grant, and if valid, issues a token known as an **access token. **It must be kept confidential and in storage. This access token should only be seen by the application, authorization, and resource server. The application makes sure that the storage of the access token can not be readable to other applications on the same device.

The [OAuth 2.0 authorization protocol](https://www.loginradius.com/blog/blog/identity/oauth2-0-guide/) defines the following methods to receive the Access Token. These Flows are called grant types. So you can decide the grant types as per the use case or it is based mainly on the type of your application.

The following are the five types of grants described to perform authorizations tasks. Those are

- Authorization Code Grant
- Implicit Grant
- Resource Owner Credentials Grant
- Client Credentials Grant
- Refresh Token Grant \

**The scope** specifies the level of access that the application is requesting from the client. An application can request one or more scopes. This information is then presented to the consumer on the consent screen. The access token issued to the application will be limited to the scopes granted. **Consent** tells your consumers who is requesting access to their data and what kind of data you're asking to access.

[[Oauth Background]]
[[OAuth 2 Simplified]]