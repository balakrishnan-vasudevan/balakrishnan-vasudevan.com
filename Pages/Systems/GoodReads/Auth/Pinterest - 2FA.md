- Tags: #authentication, #security, #mfa
  Category: Articles
  Company: Pintrest
  URL: https://medium.com/pinterest-engineering/two-factor-authentication-on-pinterest-238aa3dc92d1
-
- Enabling two-factor authentication means you confirm your identity with a combination of two factors each time you log in. In general, the first factor is a password, and the second is through a trusted device like a smartphone.* Enabling two-factor authentication means you confirm your identity with a combination of two factors each time you log in. In general, the first factor is a password, and the second is through a trusted device like a smartphone.
- Pinterest supports login with an email address, Facebook or Google across Android, iOS and web. If you enable 2FA, you’ll receive a seven digit verification code every time you log in.
- By default, we’ll send the verification code via SMS. If you’re an Authy user, we’ll send you a push notification through Authy instead of SMS.
-
- There are three main architectural components:
	- Pinterest API, which is the point of contact for web and mobile apps.
	- User service, which stores data.
	- Authy, the third party provider we use to generate, send and verify 2FA codes.
-
- Here’s how the enable flow works:
	- User verifies their password
	- User inputs their phone number
	- API sends phone number to Authy, receives Authy ID for future reference
	- API requests an SMS to Authy (or push notification, Authy handles that transparently)
	- Authy sends a verification code to user’s phone. Optionally, user can request another code (this time, we require sending an SMS)
	- User sends verification code
	- API forwards the verification code to Authy
	- If verification code is correct, API enables 2FA and generates a backup code
	- API stores phone number, 2FA enabled and backup code in User service, and returns to user

Note that user’s phone number is only saved after it’s verified.

![[Pasted image 20250316150948.png]]


- When 2FA is enabled, the login flow is slightly modified to send the user a verification code, in a similar fashion as during the enable flow above.