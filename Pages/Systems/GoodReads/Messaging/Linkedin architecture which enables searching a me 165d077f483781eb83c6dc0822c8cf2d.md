# Linkedin architecture which enables searching a message within 150ms

Status: Not started
URL: https://levelup.gitconnected.com/linkedin-architecture-which-enables-searching-a-message-within-150ms-83424aaa682a

You get a message on LinkedIn from an old colleague asking for a referral. You’re busy, so you just quickly acknowledge the message but forget to save the resume they sent. A few days later, you remember the conversation but you feel lazy to scroll so you just type in keyword. The message is right there. You can also read the free version [here](https://mayanksharmasharma77.substack.com/publish/posts/detail/152375873/share-center).

This simple action is exactly what LinkedIn’s messaging search system is all about. But what makes it so smooth? How does it work behind the scenes? Today, we’re going to dive into the architecture that powers LinkedIn’s search and the clever decisions that make it so fast and user-friendly. They crazy part is all this is done in 150ms.

# Search Service

One core idea for searching the message is that each message search is confined to the user which means user can only search in their inbox. This is important as we know that for searching we only need to search for a user, we can create index for search based on the user.

![https://miro.medium.com/v2/resize:fit:700/1*7V8IUZAYSVycf39hQHAX-w.png](https://miro.medium.com/v2/resize:fit:700/1*7V8IUZAYSVycf39hQHAX-w.png)

However one key observation that Linkedin had was that not all users use the search functionality. So instead of creating and updating the index for every user they only create index for the users who actively do the search. This was done to optimize both the cost and the write…