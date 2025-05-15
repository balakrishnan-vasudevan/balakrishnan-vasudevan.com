# How Discord Modernized MFA with WebAuthn

Tags: #authentication, #security, #mfa  
Company: Discord
URL: https://discord.com/blog/how-discord-modernized-mfa-with-webauthn
-
- WebAuthn is an API that supports public key cryptography and is implemented across all major browsers and devices. We’ll cover three major benefits of WebAuthn: it is non-phishable, non-guessable, and easy to use.
- WebAuthn is different from previous authentication methods because it is **domain-bound**. Effectively this means that ONLY discord.com can request you to login with WebAuthn with your Discord credentials. When you show up to an attacker-controlled site you will be unable to send your Discord-specific WebAuthn keys no matter how hard those fraudsters try. When an attacker tries to phish you, you will have nothing to send them since the private key is securely tucked away and unknown to even you.
- When logging in with password-based authentication, your password is static: it does not change on every login. If your password gets exposed in a data dump of some site, attackers obtain the value and can attempt to log in as you. If you happen to reuse the password on multiple sites (please don’t) then the attacker has a good chance of logging in as you in many places. On the other hand, when authenticating with WebAuthn the authentication response changes every time, meaning that even if an attacker dumps the WebAuthn database, they are still unable to login as you.
-
- ![image.png](Notes/assets/image_1740690554090_0.png)
- In this flow, the user first attempts to make the request without any MFA credentials attached. The backend determines whether the request should be allowed based on the route’s MFA setting and the user’s configured MFA options:
- If the route requires MFA and the user has it enabled, then the backend returns a payload to the frontend containing the MFA options that the user must take.
- If the backend decides MFA is not required then it continues executing the request.
-
- After the user supplies authentication data, the frontend sends a request for a token which represents a successfully-completed MFA. The token is implemented as an expiring HTTP cookie. The frontend then automatically resends the initial request to the protected route this time with the cookie attached, the route verifies the cookie, and if it is valid then continues to execute the request. In the case of an invalid cookie, then the backend returns the same ‘MFA required’ response and we re-enter the flow until a successful MFA can be performed or the user cancels their request.
-
- ## MFAv2 Backend
  
  Two services work in tandem for the backend handling of MFA actions: our Python API and our Rust authentication service. The Python API is responsible for determining whether an action requires MFA or not, and whether the user is capable of performing an MFA check. If the API decides that MFA must be performed then it requests an MFAv2 ‘ticket’ from our authentication service over gRPC.
  
  The authentication service is responsible for the creation of the MFA ticket and determining which factors the user can use to complete the challenge. For WebAuthn, this is where we create the server-side challenge and attach it to the ticket.
-
- ![image.png](Notes/assets/image_1740690656776_0.png)