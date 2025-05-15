

Ref: https://stackoverflow.com/questions/549/the-definitive-guide-to-form-based-website-authentication

## PART I: How To Log In

We'll assume you already know how to build a login+password HTML form which POSTs the values to a script on the server side for authentication. The sections below will deal with patterns for sound practical auth, and how to avoid the most common security pitfalls.

**To HTTPS or not to HTTPS?**

Unless the connection is already secure (that is, tunneled through HTTPS using SSL/TLS), your login form values will be sent in cleartext, which allows anyone eavesdropping on the line between browser and web server will be able to read logins as they pass through. This type of wiretapping is done routinely by governments, but in general, we won't address 'owned' wires other than to say this: Just use HTTPS.

In essence, the only **practical** way to protect against wiretapping/packet sniffing during login is by using HTTPS or another certificate-based encryption scheme (for example, [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security)) or a proven & tested challenge-response scheme (for example, the [Diffie-Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)-based SRP). _Any other method can be easily circumvented_ by an eavesdropping attacker.

Of course, if you are willing to get a little bit impractical, you could also employ some form of two-factor authentication scheme (e.g. the Google Authenticator app, a physical 'cold war style' codebook, or an RSA key generator dongle). If applied correctly, this could work even with an unsecured connection, but it's hard to imagine that a dev would be willing to implement two-factor auth but not SSL.

[[TLS]]
[[SSL]]


**(Do not) Roll-your-own JavaScript encryption/hashing**

Given the perceived (though now [avoidable](https://letsencrypt.org/)) cost and technical difficulty of setting up an SSL certificate on your website, some developers are tempted to roll their own in-browser hashing or encryption schemes in order to avoid passing cleartext logins over an unsecured wire.

While this is a noble thought, it is essentially useless (and can be a [security flaw](https://stackoverflow.com/questions/1380168/does-it-make-security-sense-to-hash-password-on-client-end)) unless it is combined with one of the above - that is, either securing the line with strong encryption or using a tried-and-tested challenge-response mechanism (if you don't know what that is, just know that it is one of the most difficult to prove, most difficult to design, and most difficult to implement concepts in digital security).

While it is true that hashing the password _can be_ effective against **password disclosure**, it is vulnerable to [[Replay Attacks]], [[Man-In-The-Middle attacks]] / hijackings (if an attacker can inject a few bytes into your unsecured HTML page before it reaches your browser, they can simply comment out the hashing in the JavaScript), or brute-force attacks (since you are handing the attacker both username, salt and hashed password).

**CAPTCHAS against humanity**

[CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) is meant to thwart one specific category of attack: automated dictionary/brute force trial-and-error with no human operator. There is no doubt that this is a real threat, however, there are ways of dealing with it seamlessly that don't require a CAPTCHA, specifically properly designed server-side login throttling schemes - we'll discuss those later.

Know that CAPTCHA implementations are not created alike; they often aren't human-solvable, most of them are actually ineffective against bots, all of them are ineffective against cheap third-world labor (according to [OWASP](https://en.wikipedia.org/wiki/OWASP), the current sweatshop rate is $12 per 500 tests), and some implementations may be technically illegal in some countries (see [OWASP Authentication Cheat Sheet](https://www.owasp.org/index.php/Authentication_Cheat_Sheet)). If you must use a CAPTCHA, use Google's [reCAPTCHA](https://en.wikipedia.org/wiki/ReCAPTCHA), since it is OCR-hard by definition (since it uses already OCR-misclassified book scans) and tries very hard to be user-friendly.

Personally, I tend to find CAPTCHAS annoying, and use them only as a last resort when a user has failed to log in a number of times and throttling delays are maxed out. This will happen rarely enough to be acceptable, and it strengthens the system as a whole.

**Storing Passwords / Verifying logins**

This may finally be common knowledge after all the highly-publicized hacks and user data leaks we've seen in recent years, but it has to be said: Do not store passwords in cleartext in your database. User databases are routinely hacked, leaked or gleaned through SQL injection, and if you are storing raw, plaintext passwords, that is instant game over for your login security.

So if you can't store the password, how do you check that the login+password combination POSTed from the login form is correct? The answer is hashing using a [key derivation function](https://en.wikipedia.org/wiki/Key_derivation_function). Whenever a new user is created or a password is changed, you take the password and run it through a KDF, such as Argon2, bcrypt, scrypt or PBKDF2, turning the cleartext password ("correcthorsebatterystaple") into a long, random-looking string, which is a lot safer to store in your database. To verify a login, you run the same hash function on the entered password, this time passing in the salt and compare the resulting hash string to the value stored in your database. Argon2, bcrypt and scrypt store the salt with the hash already. Check out this [article](https://security.stackexchange.com/a/31846/8340) on sec.stackexchange for more detailed information.

The reason a salt is used is that hashing in itself is not sufficient -- you'll want to add a so-called 'salt' to protect the hash against [rainbow tables](https://en.wikipedia.org/wiki/Rainbow_table). A salt effectively prevents two passwords that exactly match from being stored as the same hash value, preventing the whole database being scanned in one run if an attacker is executing a password guessing attack.

A cryptographic hash should not be used for password storage because user-selected passwords are not strong enough (i.e. do not usually contain enough entropy) and a password guessing attack could be completed in a relatively short time by an attacker with access to the hashes. This is why KDFs are used - these effectively ["stretch the key"](https://en.wikipedia.org/wiki/Key_stretching), which means that every password guess an attacker makes causes multiple repetitions of the hash algorithm, for example 10,000 times, which causes the attacker to guess the password 10,000 times slower.

**Session data - "You are logged in as Spiderman69"**

Once the server has verified the login and password against your user database and found a match, the system needs a way to remember that the browser has been authenticated. This fact should only ever be stored server side in the session data.

> If you are unfamiliar with session data, here's how it works: A single randomly-generated string is stored in an expiring cookie and used to reference a collection of data - the session data - which is stored on the server. If you are using an MVC framework, this is undoubtedly handled already.

If at all possible, make sure the session cookie has the secure and HTTP Only flags set when sent to the browser. The HttpOnly flag provides some protection against the cookie being read through XSS attack. The secure flag ensures that the cookie is only sent back via HTTPS, and therefore protects against network sniffing attacks. The value of the cookie should not be predictable. Where a cookie referencing a non-existent session is presented, its value should be replaced immediately to prevent [session fixation](https://owasp.org/www-community/attacks/Session_fixation).

Session state can also be maintained on the client side. This is achieved by using techniques like JWT (JSON Web Token).

## PART II: How To Remain Logged In - The Infamous "Remember Me" Checkbox

Persistent Login Cookies ("remember me" functionality) are a danger zone; on the one hand, they are entirely as safe as conventional logins when users understand how to handle them; and on the other hand, they are an enormous security risk in the hands of careless users, who may use them on public computers and forget to log out, and who may not know what browser cookies are or how to delete them.

Personally, I like persistent logins for the websites I visit on a regular basis, but I know how to handle them safely. If you are positive that your users know the same, you can use persistent logins with a clean conscience. If not - well, then you may subscribe to the philosophy that users who are careless with their login credentials brought it upon themselves if they get hacked. It's not like we go to our user's houses and tear off all those facepalm-inducing Post-It notes with passwords they have lined up on the edge of their monitors, either.

Of course, some systems can't afford to have _any_ accounts hacked; for such systems, there is no way you can justify having persistent logins.

**If you DO decide to implement persistent login cookies, this is how you do it:**

1. First, take some time to read [Paragon Initiative's article](https://paragonie.com/blog/2015/04/secure-authentication-php-with-long-term-persistence) on the subject. You'll need to get a bunch of elements right, and the article does a great job of explaining each.
    
2. And just to reiterate one of the most common pitfalls, **DO NOT STORE THE PERSISTENT LOGIN COOKIE (TOKEN) IN YOUR DATABASE, ONLY A HASH OF IT!** The login token is Password Equivalent, so if an attacker got their hands on your database, they could use the tokens to log in to any account, just as if they were cleartext login-password combinations. Therefore, use hashing (according to [https://security.stackexchange.com/a/63438/5002](https://security.stackexchange.com/a/63438/5002) a weak hash will do just fine for this purpose) when storing persistent login tokens.
    

## PART III: Using Secret Questions

**Don't implement 'secret questions'**. The 'secret questions' feature is a security anti-pattern. Read the paper from link number 4 from the MUST-READ list. You can ask Sarah Palin about that one, after her Yahoo! email account got hacked during a previous presidential campaign because the answer to her security question was... "Wasilla High School"!

Even with user-specified questions, it is highly likely that most users will choose either:

- A 'standard' secret question like mother's maiden name or favorite pet
    
- A simple piece of trivia that anyone could lift from their blog, LinkedIn profile, or similar
    
- Any question that is easier to answer than guessing their password. Which, for any decent password, is every question you can imagine
    

**In conclusion, security questions are inherently insecure in virtually all their forms and variations, and should not be employed in an authentication scheme for any reason.**

The true reason why security questions even exist in the wild is that they conveniently save the cost of a few support calls from users who can't access their email to get to a reactivation code. This at the expense of security and Sarah Palin's reputation. Worth it? Probably not.

## PART IV: Forgotten Password Functionality

I already mentioned why you should **never use security questions** for handling forgotten/lost user passwords; it also goes without saying that you should never e-mail users their actual passwords. There are at least two more all-too-common pitfalls to avoid in this field:

1. Don't _reset_ a forgotten password to an autogenerated strong password - such passwords are notoriously hard to remember, which means the user must either change it or write it down - say, on a bright yellow Post-It on the edge of their monitor. Instead of setting a new password, just let users pick a new one right away - which is what they want to do anyway. (An exception to this might be if the users are universally using a password manager to store/manage passwords that would normally be impossible to remember without writing it down).
    
2. Always hash the lost password code/token in the database. _**AGAIN**_, this code is another example of a Password Equivalent, so it MUST be hashed in case an attacker got their hands on your database. When a lost password code is requested, send the plaintext code to the user's email address, then hash it, save the hash in your database -- and _throw away the original_. Just like a password or a persistent login token.
    

A final note: always make sure your interface for entering the 'lost password code' is at least as secure as your login form itself, or an attacker will simply use this to gain access instead. Making sure you generate very long 'lost password codes' (for example, 16 case-sensitive alphanumeric characters) is a good start, but consider adding the same throttling scheme that you do for the login form itself.

## PART V: Checking Password Strength

First, you'll want to read this small article for a reality check: [The 500 most common passwords](http://www.whatsmypass.com/?p=415)

Okay, so maybe the list isn't the _canonical_ list of most common passwords on _any_ system _anywhere ever_, but it's a good indication of how poorly people will choose their passwords when there is no enforced policy in place. Plus, the list looks frighteningly close to home when you compare it to publicly available analyses of recently stolen passwords.

So: With no minimum password strength requirements, 2% of users use one of the top 20 most common passwords. Meaning: if an attacker gets just 20 attempts, 1 in 50 accounts on your website will be crackable.

Thwarting this requires calculating the entropy of a password and then applying a threshold. The National Institute of Standards and Technology (NIST) [Special Publication 800-63](https://en.wikipedia.org/wiki/Password_strength#NIST_Special_Publication_800-63) has a set of very good suggestions. That, when combined with a dictionary and keyboard layout analysis (for example, 'qwertyuiop' is a bad password), can [reject 99% of all poorly selected passwords](https://cubicspot.blogspot.com/2012/01/how-to-calculate-password-strength-part.html) at a level of 18 bits of entropy. Simply calculating password strength and [showing a visual strength meter](https://blogs.dropbox.com/tech/2012/04/zxcvbn-realistic-password-strength-estimation/) to a user is good, but insufficient. Unless it is enforced, a lot of users will most likely ignore it.

And for a refreshing take on user-friendliness of high-entropy passwords, Randall Munroe's [Password Strength xkcd](https://xkcd.com/936/) is highly recommended.

Utilize Troy Hunt's [Have I Been Pwned API](https://haveibeenpwned.com/API/) to check users passwords against passwords compromised in public data breaches.

## PART VI: Much More - Or: Preventing Rapid-Fire Login Attempts

First, have a look at the numbers: [Password Recovery Speeds - How long will your password stand up](https://www.lockdown.co.uk/?pg=combi&s=articles)

If you don't have the time to look through the tables in that link, here's the list of them:

1. It takes _virtually no time_ to crack a weak password, even if you're cracking it with an abacus
    
2. It takes _virtually no time_ to crack an alphanumeric 9-character password if it is **case insensitive**
    
3. It takes _virtually no time_ to crack an intricate, symbols-and-letters-and-numbers, upper-and-lowercase password if it is **less than 8 characters long** (a desktop PC can search the entire keyspace up to 7 characters in a matter of days or even hours)
    
4. **It would, however, take an inordinate amount of time to crack even a 6-character password, _if you were limited to one attempt per second!_**
    

So what can we learn from these numbers? Well, lots, but we can focus on the most important part: the fact that preventing large numbers of rapid-fire successive login attempts (ie. the _brute force_ attack) really isn't that difficult. But preventing it _right_ isn't as easy as it seems.

Generally speaking, you have three choices that are all effective against brute-force attacks _(and dictionary attacks, but since you are already employing a strong passwords policy, they shouldn't be an issue)_:

- Present a **CAPTCHA** after N failed attempts (annoying as hell and often ineffective -- but I'm repeating myself here)
    
- **Locking accounts** and requiring email verification after N failed attempts (this is a [DoS](https://en.wikipedia.org/wiki/Denial-of-service_attack) attack waiting to happen)
    
- And finally, **login throttling**: that is, setting a time delay between attempts after N failed attempts (yes, DoS attacks are still possible, but at least they are far less likely and a lot more complicated to pull off).
    

**Best practice #1:** A short time delay that increases with the number of failed attempts, like:

- 1 failed attempt = no delay
- 2 failed attempts = 2 sec delay
- 3 failed attempts = 4 sec delay
- 4 failed attempts = 8 sec delay
- 5 failed attempts = 16 sec delay
- etc.

DoS attacking this scheme would be very impractical, since the resulting lockout time is slightly larger than the sum of the previous lockout times.

> To clarify: The delay is _not_ a delay before returning the response to the browser. It is more like a timeout or refractory period during which login attempts to a specific account or from a specific IP address will not be accepted or evaluated at all. That is, correct credentials will not return in a successful login, and incorrect credentials will not trigger a delay increase.

**Best practice #2:** A medium length time delay that goes into effect after N failed attempts, like:

- 1-4 failed attempts = no delay
- 5 failed attempts = 15-30 min delay

DoS attacking this scheme would be quite impractical, but certainly doable. Also, it might be relevant to note that such a long delay can be very annoying for a legitimate user. Forgetful users will dislike you.

**Best practice #3:** Combining the two approaches - either a fixed, short time delay that goes into effect after N failed attempts, like:

- 1-4 failed attempts = no delay
- 5+ failed attempts = 20 sec delay

Or, an increasing delay with a fixed upper bound, like:

- 1 failed attempt = 5 sec delay
- 2 failed attempts = 15 sec delay
- 3+ failed attempts = 45 sec delay

This final scheme was taken from the OWASP best-practices suggestions (link 1 from the MUST-READ list) and should be considered best practice, even if it is admittedly on the restrictive side.

> _As a rule of thumb, however, I would say: the stronger your password policy is, the less you have to bug users with delays. If you require strong (case-sensitive alphanumerics + required numbers and symbols) 9+ character passwords, you could give the users 2-4 non-delayed password attempts before activating the throttling._

DoS attacking this final login throttling scheme would be _**very**_ impractical. And as a final touch, always allow persistent (cookie) logins (and/or a CAPTCHA-verified login form) to pass through, so legitimate users won't even be delayed _while the attack is in progress_. That way, the very impractical DoS attack becomes an _extremely_ impractical attack.

Additionally, it makes sense to do more aggressive throttling on admin accounts, since those are the most attractive entry points

## PART VII: Distributed Brute Force Attacks

Just as an aside, more advanced attackers will try to circumvent login throttling by 'spreading their activities':

- Distributing the attempts on a botnet to prevent IP address flagging
    
- Rather than picking one user and trying the 50.000 most common passwords (which they can't, because of our throttling), they will pick THE most common password and try it against 50.000 users instead. That way, not only do they get around maximum-attempts measures like CAPTCHAs and login throttling, their chance of success increases as well, since the number 1 most common password is far more likely than number 49.995
    
- Spacing the login requests for each user account, say, 30 seconds apart, to sneak under the radar
    

Here, the best practice would be **logging the number of failed logins, system-wide**, and using a running average of your site's bad-login frequency as the basis for an upper limit that you then impose on all users.

Too abstract? Let me rephrase:

Say your site has had an average of 120 bad logins per day over the past 3 months. Using that (running average), your system might set the global limit to 3 times that -- ie. 360 failed attempts over a 24 hour period. Then, if the total number of failed attempts across all accounts exceeds that number within one day (or even better, monitor the rate of acceleration and trigger on a calculated threshold), it activates system-wide login throttling - meaning short delays for ALL users (still, with the exception of cookie logins and/or backup CAPTCHA logins).

I also posted a question with [more details and a really good discussion of how to avoid tricky pitfals](https://stackoverflow.com/questions/479233/what-is-the-best-distributed-brute-force-countermeasure) in fending off distributed brute force attacks

## PART VIII: Two-Factor Authentication and Authentication Providers

Credentials can be compromised, whether by exploits, passwords being written down and lost, laptops with keys being stolen, or users entering logins into phishing sites. Logins can be further protected with two-factor authentication, which uses out-of-band factors such as single-use codes received from a phone call, SMS message, app, or dongle. Several providers offer two-factor authentication services.

Authentication can be completely delegated to a single-sign-on service, where another provider handles collecting credentials. This pushes the problem to a trusted third party. Google and Twitter both provide standards-based SSO services, while Facebook provides a similar proprietary solution.

## MUST-READ LINKS About Web Authentication

1. [OWASP Guide To Authentication](https://www.owasp.org/index.php/Authentication_Cheat_Sheet) / [OWASP Authentication Cheat Sheet](https://www.owasp.org/index.php/Authentication_Cheat_Sheet)
2. [Dos and Don’ts of Client Authentication on the Web (very readable MIT research paper)](https://pdos.csail.mit.edu/papers/webauth:sec10.pdf)
3. [Wikipedia: HTTP cookie](https://en.wikipedia.org/wiki/HTTP_cookie#Drawbacks_of_cookies)
4. [Personal knowledge questions for fallback authentication: Security questions in the era of Facebook (very readable Berkeley research paper)](https://cups.cs.cmu.edu/soups/2008/proceedings/p13Rabkin.pdf)



[[Architecture of Identity Systems]]
[[JWT]]
[[Kerberos]]
[[MFA]]
[[SSO]]
[[Password Hashing and Storage Basics]] 
[[Password Storage]]
[[Authentication and Authorization]]
[[Auth System Design]]
[[Forgot Password]]
- 
- [[pages/ToDos/Notion/Edge Authentication and Token-Agnostic Identity Propagation]]
- [[Tokens]]
-