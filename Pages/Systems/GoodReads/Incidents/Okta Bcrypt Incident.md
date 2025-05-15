

# What Okta Bcrypt incident can teach us about designing better APIs
https://itnext.io/what-okta-bcrypt-incident-can-teach-us-about-designing-better-apis-b87efe2bb830

> The Bcrypt algorithm was used to generate the cache key where we hash a combined string of userId + username + password. Under a specific set of conditions, listed below, this could allow users to authenticate by providing the username with the stored cache key of a previous successful authentication.

This means that if the user had a username above 52 chars, any password would suffice to log in. Also, if the username is, let’s say, 50 chars long, it means that the bad actor needs to guess only 3 first chars to get in, which is quite a trivial task for the computers these days.
