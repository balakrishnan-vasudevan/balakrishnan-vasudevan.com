#search 
tl:dr
- The age of the message
- The Lucene score of the message with respect to the query
- The searcher’s _affinity_ to the author of the message (we defined _affinity_ of one user for another as the propensity of that user to read the other’s messages — a subject for another post!)
- The [priority score](https://slack.engineering/personalized-channel-recommendations-in-slack) of the searcher’s DM channel with the message author
- The searcher’s priority score for the channel the message appeared in
- Whether the message author is the same as the searcher
- Whether the message was pinned, starred or had emoji reactions
- The propensity of searchers to click on other messages from the channel the message appeared in
- Aspects of the content of the message, such as word count, presence of line breaks, emoji and formatting.
play a a big role in searching messages on Slack







Search inside Slack is very different from web search. Each Slack user has access to a unique set of documents, and what’s relevant at the time frequently changes. By contrast, in web search, queries for “Prince,” “Powerball” or “Pokémon Go,” can get millions of hits per day, whereas queries within a Slack team are rarely repeated.
Slack provides two strategies for searching: _Recent_ and _Relevant_. _Recent_ search finds the messages that match all terms, and presents them in reverse chronological order. If a user is trying to recall something that just happened, _Recent_ is a useful presentation of the results.

_Relevant_ search relaxes the age constraint and takes into account the [Lucene score](http://lucene.apache.org/core/3_0_3/api/core/org/apache/lucene/search/Similarity.html) of the document — how well it matches the query terms (Solr powers search at Slack). Used about 17% of the time, _Relevant_ search performed slightly worse than _Recent_ according to the search quality metrics

we would leverage Solr’s custom sorting functionality to retrieve a set of messages ranked by only the select few features that were easy for Solr to compute, and then re-rank those messages in the application layer according to the full set of features, weighted appropriately.
We also knew that the relevance of a document would drift over time. So we focused on a labeling strategy that judged the relative relevance of documents within a single search using clicks known as a [Pairwise Transform](http://www.cs.cornell.edu/people/tj/publications/joachims_02c.pdf). Here’s an example:

![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_UNe-6cQ07kQEG9c00DswFg.png)

Illustration of the pairwise transform

If a query shows messages M1, M2, and M3, and the searcher clicks M2, then there must have been something _different_ about M2 that made it better than M1. Since M2 was a better result than M1, the difference in the corresponding feature vectors, F2-F1, should capture the difference, and this difference in values is given a positive label. Inversely, F1-F2 is given a negative label. There are several strategies for picking the pairs for the pairwise transform, and we tried a few before settling on one. We ended up pairing each click at position _n_ with the message at position _n_-1 and the message at position _n_+1.
One issue we struggled with was people’s tendency to click on messages at the top of the search results list — a message at position _n_ is on average 30% more likely to be clicked than a message at position _n_+1. Because the position of a message is such a strong indicator of whether or not it was clicked, we found that our initial models were learning to reconstruct the original order of the list. To counteract this effect, we evened out the distribution of clicks by position by oversampling clicks on results lower down in the list.

Using this dataset, we trained a model using SparkML’s built-in SVM algorithm. The model determined that the following signals were the most significant:




Notably, aside from the Lucene “match” score, we have not yet incorporated any other semantic features of the message itself in our models.