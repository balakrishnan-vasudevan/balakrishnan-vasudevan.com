

Tags: authentication
Category: Articles
Company: general
Status: Not started
URL: https://markilott.medium.com/password-storage-basics-2aa9e1586f98



https://github.com/nextauthjs/next-auth/discussions/4883

https://www.reddit.com/r/programming/comments/dyhyh1/how_to_build_a_user_authentication_system_from/
Your task is now to create a user authentication system.

This document will guide you through all the features and implication of such system, so that you don't have to search them yourself.

We will focus on web/browser-technologies, however similar concept can be widely applied. This guide, is a work in progress, feel free to comment and provide feedbacks.

## Expected Workflows


The following are the actions that users expect to take in your platform, some are very simple, others are more complex and requires sophisticated implementations.

The workflows that any user expect in any web based application are:

1. Signup
2. Login
3. Logout
4. Recover password
5. Change contact information
6. Delete account

More complex applications may also implement:

7. Two-Factor authentication
8. Change Second Contact information

## Common Authentication Systems

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#common-authentication-systems)

The common authentication systems on which the above workflow are implemented are:

1. Email & Password
2. Email
3. Social Login (Login with: Facebook, Twitter, Instagram, LinkedIn, etc...)
4. SSO (Single Sign On)

Not all the workflow methods make sense with all the authentication systems. As an example, _in general_ if you use Social Login, you don't need to implement yourself the Recover Password workflow, since it would be done by the Social platform itself for you.

If you implement more than a single authentication system, you will need to harmonize them behind a single interface. Mostly this means having a way to unequivocally identify users that use different authentication systems, it is usually a bad idea to use the email address for this and you most likely want to associate an identifier to each user.

## How to keep users logged in

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#how-to-keep-users-logged-in)

Cookies! Cookies are used to keep user logged in your application. When a user login in your application, you send them a cookie that usually stores a session identifier. Each request that the user will now do to your webservice will now contain this cookie, so you can identify the session and with that the user. When the user logs out, you simply remove the cookie.

## Email & Password

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#email--password)

Email & Password is the most common way to implement an authentication system. In this section we will explore how to implement each workflow for this authentication system. We will always refer to emails, however this is not strictly true, whichever communication system can work, another common option is to use phone number.

### Signup

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#signup)

To signup the user needs to provide an email address and a password, only this information are strictly necessary. Some platforms may decide to ask for more fields, like "username/nickname" or to type the password twice for confirmation. None of that is necessary, you can ask the user a username after, if they want to or you can just assign a random username and let the user change it inside the application. Also typing the password twice is not necessary, since anyway you will provide a password recovery workflow. For paid product, it might be wise to ask upfront for the credit card information even if the product adopt a freemium model, this will immediately weeds out the freeloaders that have no intention to ever pay for the product, of course it will result in less overall users.

On the frontend of your application a simple HTML form will capture the email and the password, and this information will be sent to your backend. The connection should be a secure (hence HTTP**S**) connection, otherwise the browser will inform the user that your application is not following the basic security guidelines. A simple form to capture this information will look like the following:

```html
<form method="POST" action="/signup">
    <input type="email" name="email" required="true">
    <input type="password" name="password" required="true">
</form>
```

The method for the form **must** be `POST` otherwise the email and password will appears in the URL.

Once your application receives the data it must first verify that the email is not already registered, if it is, you should not give away this information, an attacker could be trying to understand if the target signed-up for a website. If the email is not already registered, now you can store those information. The email address can be stored in plain text, indeed you may want to send emails to your users. The password **must not** be stored in plain text, but you need to store its cryptographic secure hash, ideally with salt. Do not make the mistake of storing the password as plain text.

In order to store password securely the standard algorithm is:

1. Generate a random cryptographic salt
2. Hash the original, user provided, password with a fast hash function, usually something like HASH-512
3. Concatenate the salt (from point 1) and the insecure hash of the password (from point 2)
4. Hash the concatenation of the salt and password (from point 3) using a slow cryptographic secure function.
5. Store the salt (from point 1) and the cryptographic secure hash (from point 4) in the database, one next to the other.

The cryptographic secure functions to use are, in order:

1. [Argon2](https://en.wikipedia.org/wiki/Argon2)
2. [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)
3. [Scrypt](https://en.wikipedia.org/wiki/Scrypt)
4. [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)

For more details please visit [the owasp cheatsheet.](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#leverage-an-adaptive-one-way-function)

Concerning security, the correct approach would be to first verify that the email is a valid email at which the user has access. So, immediately after you receive email and password, you mark the account as "not verified", store the password as mentioned above, and send a verification email with an activation link to the user. If the user visits the link, then you mark the account as verified and now, only now, you let the user login.

Business reasons will invite you to immediately log in the user if the email they provide is not already registered or to return an error if the email is already registered. This will provide valuable information to a possible attacker.

There is not a definitive answer here, and it depends on the nature of the business.

### Login

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#login)

In order to login, you can provide a form very similar to the one used for signing up.

```html
<form method="POST" action="/login">
    <input type="email" name="email" required="true">
    <input type="password" name="password" required="true">
</form>
```

Again, as all forms that require a password, this form should be served using a secure connection.

Once the backend receives the authentication data, it must verify that the information is correct. In your database you will query for the email and extract the salt and the hash of the password. Then you redo exactly the same operation you have done for generating the hash:

1. Get the salt from the database
2. Hash the original, user provided, password with a fast hash function, usually something like HASH-512
3. Concatenate the salt (from point 1 extracted from the database) and the insecure hash of the password (from point 2)
4. Hash the concatenation of the salt and password (from point 3) using a slow cryptographic secure function.
5. Verify that the result (from point 4) is exactly the same that is stored in the database

If the two results match, then the user successfully authenticates in your application, if they don't match you should not give away any information to the user, again it could be an attacker.

Do **not** say things like "The email does not exist" or "We found the email, but the password does not match". Just say things like, "Email and Password don't match" even if the email is not in the database.

After the authentication is successfully completed, you can login the user. The simplest, reliable, and most robust approach to login a user is to simply send them a cookie. The cookie should be a `Secure Cookie`.

Cookies are just a key value storage, the key can be anything and a good key can be something like `id` or `session` or `sessionId`. The value should be a cryptographic secure random string. In your backend, you map the cookie value to the specific user, this can be done in another table of your database or also in some in-memory data structure like Redis.

The cookie should expires in a reasonable amount of time, not as short to force the user to login again every time, not too long that allows attacker to access it. Some website use `Session Cookie` that are reset as soon as the browser quits.

When you receive a request from a client you can immediately understand if the request is from an authenticated user, or from somebody else. This will allow you to create different response for each user and for not authenticated users.

In order to check if the user is authenticated you can simply check if the cookie you would set is present, and if the value of the cookie actually matches one of the saved one. If there is a match, the user is authenticated, if there is not a match the user is not authenticated.

### Logout

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#logout)

As mentioned above, the user is logged in, if it sends -through cookies- a session id that you have previously recorded. In order to logout a user you can simply delete its session id from the list of logged in sessions, in this way, the next time the user sends a new request with an old cookie value, it won't match and you will know that the user logged out.

Another approach would be to also delete the cookie from the user’s browser, you can do this by setting the cookie value to the empty string. In this way, the next time the user sends you a request it will not contain the cookie used for authentication.

### Recover/Change password

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#recoverchange-password)

When the user asks to recover or change the password you simply send them (through email) a token that will allow them to reset and input a new password. Of course the token must be valid only for a limited amount of time and for a single use.

There are two main implementations at this stage.

1. You could send a deep-link that will land the user on a form where it is prompted to insert the new password
2. You can send a random few-digit token, that the user needs to insert into a form (along with the new password) in order to upgrade its credentials

Both approaches work fine and are similarly difficult to implement.

As always, it is important not to leak any information regarding the presence or absence of a set of credentials, if the user inputs an email that does not exist, **never** say something like "Email not found".  
Instead say something like: "If we recognize the email we are sending the appropriate steps in order to change password".

Of course, the new password must be safely saved following the procedure mentioned above of hashing and salting.

### Change contact information

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#change-contact-information)

If the user wishes to change its contact information, since the contact information is used to recover and change the password, you should verify that the user actually knows the password.

After the user was able to input the correct password, before actually changing the contact information, you must verify that the user has access to the new contact information. The procedure of the verification could be the same of the procedure used during the signup process.

In order to be safe, it is wise to send an email also to the old contact information, in this way, an intrusion can be detected promptly.

### Delete account

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#delete-account)

Different philosophies apply when deleting accounts.

The most straightforward and honest approach would be to actually delete all the data connected to the account, along with email, hashed password and other application data. This is what is generally expected from users and what I believe should be implemented for not breaking the trust of the users.

The second, more subtle, approach is to mark the user as deleted while keeping all its information (this is usually known as shallow-delete). During Login, a user with an account marked as deleted would not be authenticated, just like if it provided the wrong credentials.

Shallow-deletes provide the benefits that, if a user changes its mind, he can always come back.

A reasonable middle ground is to shallow-delete users for a short amount of time (few days) and then completely delete their information.

For account deletion you should ask confirmation, especially if it means to loose important data, moreover I would suggest to ask the user to provide its password again.

## Social Logins

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#social-logins)

Social logins allow you to identify people using another (generally big and reliable) service. Examples of services that provide this Social Login are Facebook, Twitter, Google, Github, Pinterest, etc... we will call these services Identity Providers.

The identity provider takes care of managing the direct contact with the users, so you don't have to manage emails, phone numbers, reset passwords, etc... And the user does not have to manage and remember, yet another set of credentials.

This advantage comes at some costs. First of all, it means that all your contact with the users are gatekeeped by the identity provider, generally they are benevolent, but it is always a risk to consider. Second, you may not have access to a direct contact for your user, you may not have access to the user's email address for example. Finally, some users are reluctant to login using social logins.

Another advantage is that Social Login is very personal, so different people will most likely not share the same account.

All the services that provide Social Login features use very similar implementation of OAuth (a protocol to share identities online), which means that what works for Twitter will need only minor modification to work for Facebook or Google. Moreover the underlying principles are very similar.

Finally, while you don't keep direct information of your user, you still need to maintain indirect information about the user, and to create and manage the cookies.

Let's now dive deep into what is necessary to create a User Management system that uses Social Logins.

### General structure

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#general-structure)

The first step is to register an application with the Identity Provider. You will need to provide a callback url, which is the URL that users will visit after the Login in your application through the identity provider.

After you register your application, the identity provider will return a couple of strings, the ClientID and the ClientSecret, despite the name, both of them should be kept private.

At this point, you registered your application with the Identity Provide, your provide a callback URL and they provided you two strings.

Those strings should be saved somewhere, not in the code, since the code will be checked-in git (or another Version Control System). The usual approach is to have them available to your code using Environment Variables, but those credentials could be passed as inputs to your application, or could be read from a database.

### Login

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#login-1)

Using Social Login the users, technically, don't signup to your service. They just Login. The process is quite complex, but its final goal is to let you have another set of credentials that are associated with the user. Hence, at the end of the process you will have two more strings, one that identifies the user (that we will call `UserID`) and a secret one (the `UserSecret`). The one that identifies the user can be shared (for example it can be used as value in the cookie) while the secret one should be kept secret.

The very first step of the process is to render the Social Login button in your application. In theory you could use whichever button, but usually it is a good idea to use the buttons provided by the Identity Provider. When the user clicks on the button, the Identity Provider receives a request, but it does not know that it is from you. To obviate, you send also your `ClientID` as `GET` parameter. Often, you can send also the `scope` parameter that indicates what kind of information from the user you will like to access, depending on your application this may change, but usually you always want at least the email.

When the user finally clicks on the Social Login button it gets redirected to a page from the Identity Provider, there it will Login in the Identity Provider service, and will analyze what information you are requesting from them. At this point the user can either authorize or dismiss your Login.

If the user authorizes the Login, the Identity Provider invokes the callback that we provided at the very beginning passing as parameter the `UserID`.

As a last step, you need to exchange the `UserID` with the `UserSecret`. Finally, with the `UserSecret` you can invoke the API at which you required access through the scope.

The `UserSecret` expires rather quickly, and you will need to continuously refresh it. Usually this can be done with the `UserID`.

Please note that while writing this article I researched implementations from different Identity Providers (Twitter, Github and Google) and none of them is equal to the other, nor they work exactly as I mentioned. However they follow the spirit of this flow.

To recap:

1. The user wants to Login
2. You redirect the user to the Identity Provider service, passing as parameter your identifier
3. The user logins, and it gets redirected to your callback with some sort of tokens
4. You exchange the token from the callback for a (set of) secret tokens
5. You store the token and the secret token to make requests to the identity provider
6. Eventually you refresh the secret token against the Identity Provider
7. Store the session cookie in the client browser

Again, please note that each Identity Provider implements these steps a little bit differently.

Also remember that you most likely want to store a session cookie in the client browser, just like we did in the Email & Password workflow.

### Signup

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#signup-1)

As we mentioned before there is not a real Signup, the user just logins. However, the first login is different from the others. As soon as the user logins, you want to store its information in your database. Most likely you will require some basic information to the Identity Provider (usually the email address) and other information that could be specific to your app and the integration with the Identity Provider. Also, it is important to store the credentials provided by the Identity Provider.

Some identity providers allows you to refresh the tokens for quite a bit of time (in the order of 2 or 3 months) but eventually the refreshing of the token fails, and the user will need to signup again. In such case you will need to identify the user only from the tokens provided by the Identity Provider.

### Logout

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#logout-1)

To Logout you simply remove the cookie from the client browser, just like in the Email & Password case. Eventually the user will Login again, and in such case you need to retrieve its account only from the tokens provided by the Identity Provider.

### Change Contact information

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#change-contact-information-1)

Eventually the user might decide to change its contact information. Maybe it stopped using Facebook but want to keep using your service, or maybe it used Twitter to Login only to try your service, but now he likes it and want to switch to using normal Email & Password. This case is analogous to the one in the Email & Password workflow, you verify the email and store the password in a secure way. It may also happen that users decide to link multiple social accounts to its profile, in general this should be allowed. Even further, a user that has linked multiple accounts to its profile should be able to Login with any of those accounts.

### Delete account

[](https://gist.github.com/siscia/5ed3277551370df3eb8b1063923621d4#delete-account-1)

To delete the account the same considerations of the Email & Password applies. The most straightforward and honest approach would be to actually delete all the data connected to the account, all the token that are associated with the user and all the data fetched from the Identity Provider.

Shallow delete is possible, but if the user removes the authorization to your application the Identity Provider will stop providing you any information.

The reasonable middle ground of shallow delete for a few days, and then completely deleting the information must be considered also in this case.
One of the things that is always missing from many of the "lets invent this again" is request throttling. This is quite important to not accidentally expose information about user accounts to an attacker.

Lets assume the following flow on your login approach:

1. lookup user by email (30 ms)
    
2. get current password from user (maybe in another table to keep history for things like ensuring a password is not reused - FYI this is another debate for another point) - another 30ms
    
3. Do whatever hashing algo you are going to use (10 ms)
    
4. General overhead during peak times low/times on DB performance (and indexes) especially on very large DBs can change step 1 and 2
    

So I attack with 1000 usernames/passwords. 950 of them return in 30ms, 50 of them return in 80ms. I just got info on those 50 being likely a valid username, now I can keep on attacking and iterating over those with common passwords of previously leaked DBs on said users.

We do dynamic request throttling of a minimum of 1 second. This is not noticeable for user when they do a login, but for an attacker we just capped his attempts at a max of 3600 per hour and inability to sniff usernames. Our systems is smart enough to look at failed averages on an hourly basis and increase throttling to up to 2.5 seconds maximum.

Lets go further, we apply this same mechanism for ANY action that either go from unauthenticated to authenticated (ie simple login, remember me token) OR any other action that represents an unauthenticated user dealing with a token or action that represents a user identity (think of reset password tokens etc, registers etc). Remember during register I can sniff out if user accounts exists or the same with password resets - (register: user already exists, reset password: we did not find a user with this email) - you just gave away authentication information.

For us, when a user resets their password, they receive an email whether or not they have an account with us or not, if valid email "here is your token", if not "looks like we do not have an account with this email, request was made with this User Agent from X IP).

Now on token management, generate something with high enough enthrophy,lets take reset password. Generate a token, include it via email, store the hash of the token in DB (db gets leaked no way to reset passwords or take ownership) - I know reset passwords expire quickly, are only one time use etc but still.

FINALLY, EVERY attempt that a user makes to interact with "getting authenticated or using a token representing user" gets logged in attempt tables. Here we store user agent, IP, tokens, etc so we can identify possible attack approaches or anyone trying to do some fishy stuff - I know you can use logs for this, but having it in a DB gives you some more granularity to identify what type of attack maybe occuring.



# How to handle user sessions without overwhelming database?
https://www.reddit.com/r/node/comments/150ycyg/how_to_handle_user_sessions_without_overwhelming/

I’ve managed to get a few solid answers regarding this from ChatGPT but I’d like to hear some of your thoughts:

What I’m using: (JavaScript, NodeJS, Express, MongoDB).

I want to validate on every page that the user is logged in and ideally get certain data fields, such as “name” which can be displayed throughout the website.

I’m toying with using a http only cookie, and keeping the users session data in a JWT. Then using a helper function to parse this data out, as I don’t really want to keep hitting my database needlessly for every user. But at this stage of it all, I’m a bit lost.

Thanks. Hope you can help.

Redis for sessions, DB for accounts.

You can simply stringify/parse the JSON data from the session and store as string in Redis.

If you want to really get performant and avoid the parsing/serializing cost, you can store Session data as a Hash data type. Although It's a bit harder to pull off as you have to restrict the types of data you will store in your properties, It is more performant and allows you to consume specific properties without having to serialize/parse the whole data each time.

Since Redis only allows you to store string values. You would have to encode/decode the value with the type char in the following manner:

1 -> "n1" (Number with value of 1)

"hello" -> "shello" (String with value of hello)

true -> "b1" -> (Boolean with value of 1 aka. true or you can also just store the word true)

Note! Hash will only give you up to 1 level of fine tuned access. If you have highly nested data then you will likely have to serialize/parse that at some point as well, so Ideally try to store only important data in your Session and keep it as flat as possible. There are more tricks to represent nested data in a flat manner and have it be two way reconstructible but you are approaching over-engineering territory at that point. Hope the above helps!

