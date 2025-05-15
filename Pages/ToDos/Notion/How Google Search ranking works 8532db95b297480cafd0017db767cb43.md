# How Google Search ranking works

Tags: web-search
Category: Articles
Company: Google
Status: Not started
URL: https://searchengineland.com/how-google-search-ranking-works-445141

It should be clear to everyone that the [Google documentation leak](https://searchengineland.com/google-search-document-leak-ranking-442617) and the [public documents from antitrust hearings](https://searchengineland.com/google-search-ranking-documents-434141) do not really tell us exactly how the rankings work.

The structure of organic search results is now so complex – not least due to the use of machine learning – that even the Google employees who work on the ranking algorithms say they can no longer explain why a hit is at one or two. We do not know the weighting of the many signals and the exact interplay.

Nevertheless, it is important to familiarize yourself with the structure of the search engine to understand why well-optimized pages do not rank or, conversely, why seemingly short and non-optimized results sometimes appear at the top of the rankings. The most important aspect is that you need to broaden your view of what is really important.

All the information available clearly shows that. Anyone who is even marginally involved with ranking should incorporate these findings into their own mindset. You will see your websites from a completely different point of view and incorporate additional metrics into your analyses, planning and decisions.

**To be honest**, it is extremely difficult to draw a truly valid picture of the systems’ structure. The information on the web is quite different in its interpretation and sometimes differs in terms, although the same thing is meant.

An example: The system responsible for building a SERP (search results page) that optimizes space use is called Tangram. In some Google documents, however, it is also referred to as Tetris, which is probably a reference to the well-known game.

Over weeks of detailed work, I have viewed, analyzed, structured, discarded and restructured almost 100 documents many times.

This article is not intended to be exhaustive or strictly accurate. It represents my best effort (i.e., “to the best of my knowledge and belief”) and a bit of Inspector Columbo’s investigative spirit. The result is what you see here.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201380%20795'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201380%20795'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/A-graphical-overview-of-how-Google-ranking-works.jpg.webp](https://searchengineland.com/wp-content/seloads/2024/08/A-graphical-overview-of-how-Google-ranking-works.jpg.webp)

A graphical overview of how Google ranking works, created by the author

## A new document waiting for Googlebot’s visit

When you publish a new website, it is not indexed immediately. Google must first become aware of the URL. This usually happens either via an updated sitemap or via a link placed there from an already-known URL.

Frequently visited pages, such as the homepage, naturally bring this link information to Google’s attention more quickly.

The trawler system retrieves new content and keeps track of when to revisit the URL to check for updates. This is managed by a component called the scheduler. The store server decides whether the URL is forwarded or whether it is placed in the sandbox.

Google denies the existence of this box, but the recent leaks suggest that (suspected) spam sites and low-value sites are placed there. It should be mentioned that Google apparently forwards some of the spam, probably for further analysis to train its algorithms.

Our fictitious document passes this barrier. Outgoing links from our document are extracted and sorted according to internal or external outgoing. Other systems primarily use this information for link analysis and PageRank calculation. (More on this later.)

Links to images are transferred to the ImageBot, which calls them up, sometimes with a significant delay, and they are placed (together with identical or similar images) in an image container. Trawler apparently uses its own PageRank to adjust the crawl frequency. If a website has more traffic, this crawl frequency increases (*ClientTrafficFraction*).

## Alexandria: The great library

Google’s indexing system, called Alexandria, assigns a unique DocID to each piece of content. If the content is already known, such as in the case of duplicates, a new ID is not created; instead, the URL is linked to the existing DocID.

Important: Google differentiates between a URL and a document. A document can be made up of multiple URLs that contain similar content, including different language versions, if they are properly marked. URLs from other domains are also sorted here. All the signals from these URLs are applied via the common DocID.

For duplicate content, Google selects the canonical version, which appears in search rankings. This also explains why other URLs may sometimes rank similarly; the determination of the “original” (canonical) URL can change over time.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20621%20348'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20621%20348'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-1-Alexandria-collects-URLs-for-a-document.png.webp](https://searchengineland.com/wp-content/seloads/2024/08/Figure-1-Alexandria-collects-URLs-for-a-document.png.webp)

Figure 1: Alexandria collects URLs for a document.

As there is only this one version of our document on the web, it is given its own DocID.

Individual segments of our site are searched for relevant keyword phrases and pushed into the search index. There, the “hit list” (all the important words on the page) is first sent to the direct index, which summarizes the keywords that occur multiple times per page.

Now an important step takes place. The individual keyword phrases are integrated into the word catalog of the inverted index (word index). The word pencil and all important documents containing this word are already listed there.

In simple terms, as our document prominently contains the word pencil multiple times, it is now listed in the word index with its DocID under the entry “pencil.”

The DocID is assigned an algorithmically calculated IR (information retrieval) score for pencil, later used for inclusion in the Posting List. In our document, for example, the word pencil has been marked in bold in the text and is contained in H1 (stored in *AvrTermWeight*). Such and other signals increase the IR score.

Google moves documents considered important to the so-called HiveMind, i.e., the main memory. Google uses both fast SSDs and conventional HDDs (referred to as TeraGoogle) for long-term storage of information that doesn’t require quick access. Documents and signals are stored in the main memory.

Notably, experts estimate that before the recent AI boom, about half of the world’s web servers were housed at Google. A vast network of interconnected clusters allows millions of main memory units to work together. A Google engineer once noted at a conference that, in theory, Google’s main memory could store the entire web.

It’s interesting to note that links, including backlinks, stored in HiveMind seem to carry significantly more weight. For example, links from important documents are given much greater importance, while links from URLs in TeraGoogle (HDD) may be weighted less or possibly not considered at all.

- **Hint**: Provide your documents with plausible and consistent date values. *BylineDate* (date in the source code), *syntaticDate* (extracted date from URL and/or title) and *semanticDate* (taken from the readable content) are used, among others.
- Faking topicality by changing the date can certainly lead to downranking (demotion). The *lastSignificantUpdate* attribute records when the last significant change was made to a document. Fixing minor details or typos does not affect this counter.

Additional information and signals for each DocID are stored dynamically in the repository (*PerDocData*). Many systems access this later when it comes to fine-tuning relevance. It is useful to know that the last 20 versions of a document are stored there (via *CrawlerChangerateURLHistory*).

Google has the ability to evaluate and assess changes over time. If you want to completely change the content or topic of a document, you would theoretically need to create 20 intermediate versions to override the old content signals. This is why reviving an expired domain (a domain that was previously active but has since been abandoned or sold, perhaps due to insolvency) does not offer any ranking advantage.

If a domain’s Admin-C changes and its thematic content changes at the same time, a machine can easily recognize this at this point. Google then sets all signals to zero, and the supposedly valuable old domain no longer offers any advantages over a completely newly registered domain.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20961%20632'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20961%20632'%3E%3C/svg%3E)

Figure 2: In addition to the leaks, the evidence documents from hearings and trials of the U.S. judiciary against Google are a useful source for research. You can even find internal emails there.

## QBST: Someone is looking for ‘pencil’

When someone enters “pencil” as a search term in Google, QBST begins its work. The search phrase is analyzed, and if it contains multiple words, the relevant ones are sent to the word index for retrieval.

The process of term weighting is quite complex, involving systems like RankBrain, DeepRank (formerly BERT) and RankEmbeddedBERT. The relevant terms, such as “pencil,” are then passed on to the Ascorer for further processing.

## Ascorer: The ‘green ring’ is created

The Ascorer retrieves the top 1,000 DocIDs for “pencil” from the inverted index, ranked by IR score. According to internal documents, this list is referred to as a “green ring.” Within the industry, it is known as a posting list.

The Ascorer is part of a ranking system known as Mustang, where further filtering occurs through methods such as deduplication using SimHash (a type of document fingerprint), passage analysis, systems for recognizing original and helpful content, etc. The goal is to refine the 1,000 candidates down to the “10 blue links” or the “blue ring.”

Our document about pencils is on the posting list, currently ranked at 132. Without additional systems, this would be its final position.

## Superroot: Turn 1,000 into 10!

The Superroot system is responsible for re-ranking, carrying out the precision work of reducing the “green ring” (1,000 DocIDs) to the “blue ring” with only 10 results.

Twiddlers and NavBoost perform this task. Other systems are probably in use here, but their exact details are unclear due to vague information.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201071%20512'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201071%20512'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-3-Mustang-generates-1000-potential-results-and-Superroot-filters-them-down-to-10-results.png.webp](https://searchengineland.com/wp-content/seloads/2024/08/Figure-3-Mustang-generates-1000-potential-results-and-Superroot-filters-them-down-to-10-results.png.webp)

Figure 3: Mustang generates 1,000 potential results and Superroot filters them down to 10 results.

- [Google Caffeine](https://searchengineland.com/googles-new-indexing-infrastructure-caffeine-now-live-43891) no longer exists in this form. Only the name has remained.
- Google now works with countless micro-services that communicate with each other and generate attributes for documents that are used as signals by a wide variety of ranking and re-ranking systems and with which the neural networks are trained to make predictions.

## Filter after filter: The Twiddlers

Various documents indicate that several hundred Twiddler systems are in use. Think of a Twiddler as a plug-in similar to those in WordPress.

Each Twiddler has its own specific filter target. They are designed this way because they are relatively easy to create and don’t require changes to the complex ranking algorithms in Ascorer.

Modifying these algorithms is challenging and would involve extensive planning and programming due to potential side effects. In contrast, Twiddlers operate in parallel or sequentially and are unaware of the activities of other Twiddlers.

There are basically two types of Twiddlers.

- PreDoc Twiddlers can work with the entire set of several hundred DocIDs because they require little or no additional information.
- In contrast, Twiddlers of the “Lazy” type require more information, for example, from the *PerDocData* database. This takes correspondingly longer and is more complex.

For this reason, the PreDocs first reduce the posting list to significantly fewer entries and then start with slower filters. This saves an enormous amount of computing capacity and time.

Some Twiddlers adjust the IR score, either positively or negatively, while others modify the ranking position directly. Since our document is new to the index, a Twiddler designed to give recent documents a better chance of ranking might, for instance, multiply the IR score by a factor of 1.7. This adjustment could move our document from the 132nd place to the 81st place.

Another Twiddler enhances diversity (*strideCategory*) in the SERPs by devaluing documents with similar content. As a result, several documents ahead of us lose their positions, allowing our pencil document to move up 12 spots to 69. Additionally, a Twiddler that limits the number of blog pages to three for specific queries boosts our ranking to 61.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20545%20333'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20545%20333'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-4-Two-types-of-Twiddlers-–-over-100-of-them-reduce-the-potential-search-results-and-re-sort-them.png](https://searchengineland.com/wp-content/seloads/2024/08/Figure-4-Two-types-of-Twiddlers-–-over-100-of-them-reduce-the-potential-search-results-and-re-sort-them.png)

Figure 4: Two types of Twiddlers – over 100 of them reduce the potential search results and re-sort them.

Our page received a zero (for “Yes”) for the *CommercialScore* attribute. The Mustang system identified a sales intention during analysis. Google likely knows that searches for “pencil” are frequently followed by refined searches like “buy pencil,” indicating a commercial or transactional intent. A Twiddler designed to account for this search intent adds relevant results and boosts our page by 20 positions, moving us up to 41.

Another Twiddler comes into play, enforcing a “page three penalty” that limits pages suspected of being spam to a maximum rank of 31 (Page 3). The best position for a document is defined by the *BadURL-demoteindex* attribute, which prevents ranking above this threshold. Attributes like *DemoteForContent*, *DemoteForForwardlinks* and *DemoteForBacklinks* are used for this purpose. As a result, three documents above us are demoted, allowing our page to move up to Position 38.

Our document could have been devalued, but to keep things simple, we’ll assume it remains unaffected. Let’s consider one last Twiddler that assesses how relevant our pencil page is to our domain based on embeddings. Since our site focuses exclusively on writing instruments, this works to our advantage and negatively impacts 24 other documents.

For instance, imagine a price comparison site with a diverse range of topics but with one “good” page about pencils. Because this page’s topic differs significantly from the site’s overall focus, it would be devalued by this Twiddler.

Attributes like *siteFocusScore* and *siteRadius* reflect this thematic distance. As a result, our IR score is boosted once more, and other results are downgraded, moving us up to Position 14.

As mentioned, Twiddlers serve a wide range of purposes. Developers can experiment with new filters, multipliers or specific position restrictions. It’s even possible to rank a result specifically either in front of or behind another result.

One of [Google’s leaked internal documents](https://www.zachvorhies.com/google_leaks/Fake%20News/Twiddler%20Quick%20Start%20Guide%20-%20Superroot.pdf) warns that certain Twiddler features should only be used by experts and after consulting with the core search team.

> 
> 
> 
> “If you think you understand how they work, trust us: you don’t. We’re not sure that we do either.”
> 
> [Leaked “Twiddler Quick Start Guide – Superroot” document](https://www.zachvorhies.com/google_leaks/Fake%20News/Twiddler%20Quick%20Start%20Guide%20-%20Superroot.pdf)
> 

There are also Twiddlers that only create annotations and add these to the DocID on the way to the SERP. An image then appears in the snippet, for example, or the title and/or description are dynamically rewritten later.

If you wondered during the pandemic why your country’s national health authority (such as the Department of Health and Human Services in the U.S.) consistently ranked first in COVID-19 searches, it was due to a Twiddler that boosts official resources based on language and country using *queriesForWhichOfficial*.

You have little control over how Twiddler reorders your results, but understanding its mechanisms can help you better interpret ranking fluctuations or “inexplicable rankings.” It’s valuable to regularly review SERPs and note the types of results.

For example, do you consistently see only a certain number of forum or blog posts, even with different search phrases? How many results are transactional, informational, or navigational? Are the same domains repeatedly appearing, or do they vary with slight changes in the search phrase?

If you notice that only a few online stores are included in the results, it might be less effective to try ranking with a similar site. Instead, consider focusing on more information-oriented content. However, don’t jump to conclusions just yet, as the NavBoost system will be discussed later.

## Google’s quality raters and RankLab

Several thousand quality raters work for Google worldwide to evaluate certain search results and test new algorithms and/or filters before they go “live.”

Google [explains](https://developers.google.com/search/blog/2023/11/search-quality-rater-guidelines-update?hl=en), “Their ratings don’t directly influence ranking.”

This is essentially correct, but these votes do have a significant indirect impact on rankings.

Here’s how it works: Raters receive URLs or search phrases (search results) from the system and answer predetermined questions, typically assessed on mobile devices.

For example, they might be asked, “Is it clear who wrote this content and when? Does the author have professional expertise on this topic?” The answers to these questions are stored and used to train machine learning algorithms. These algorithms analyze the characteristics of good and trustworthy pages versus less reliable ones.

This approach means that instead of relying on Google search team members to create criteria for ranking, algorithms use deep learning to identify patterns based on the training provided by human evaluators.

Let’s consider a thought experiment to illustrate this. Imagine people intuitively rate a piece of content as trustworthy if it includes an author’s picture, full name, and a LinkedIn biography link. Pages lacking these features are perceived as less trustworthy.

If a neural network is trained on various page features alongside these “Yes” or “No” ratings, it will identify this characteristic as a key factor. After several positive test runs, which typically last at least 30 days, the network might start using this feature as a ranking signal. As a result, pages with an author image, full name, and LinkedIn link might receive a ranking boost, potentially through a Twiddler, while pages without these features could be devalued.

Google’s official stance of not focusing on authors could align with this scenario. However, leaked information reveals attributes like isAuthor and concepts such as “author fingerprinting” through the *AuthorVectors* attribute, which makes the idiolect (the individual use of terms and formulations) of an author distinguishable or identifiable – again via embeddings.

Raters’ evaluations are compiled into an “information satisfaction” (IS) score. Although many raters contribute, an IS score is only available for a small fraction of URLs. For other pages with similar patterns, this score is extrapolated for ranking purposes.

Google notes, “A lot of documents have no clicks but can be important.” When extrapolation isn’t possible, the system automatically sends the document to raters to generate a score.

The term “golden” is mentioned in relation to quality raters, suggesting there might be a gold standard for certain documents or document types. It can be inferred that aligning with the expectations of human testers could help your document meet this gold standard. Additionally, it’s likely that one or more Twiddlers might provide a significant boost to DocIDs deemed “golden,” potentially pushing them into the top 10.

Quality raters are typically not full-time Google employees and may work through external companies. In contrast, Google’s own experts operate within the RankLab, where they conduct experiments, develop new Twiddlers and evaluate whether these or refined Twiddlers improve result quality or merely filter out spam.

Proven and effective Twiddlers are then integrated into the Mustang system, where complex, computationally intensive and interconnected algorithms are used.

Get the [newsletter](https://searchengineland.com/newsletters) search marketers rely on.

Business email address

[See terms.](https://searchengineland.com/termsofuse)

## But what do users want? NavBoost can fix that!

Our pencil document hasn’t fully succeeded yet. Within Superroot, another core system, [NavBoost](https://searchengineland.com/how-google-search-ranking-works-pandu-nayak-435395), plays a significant role in determining the order of search results. NavBoost uses “slices” to manage different data sets for mobile, desktop, and local searches.

Although Google has officially denied using user clicks for ranking purposes, FTC documents reveal an internal email instructing that the handling of click data must remain confidential.

This shouldn’t be held against Google, as the denial of using click data involves two key aspects. Firstly, acknowledging the use of click data could provoke media outrage over privacy concerns, portraying Google as a “data octopus” tracking our online activity. However, the intent behind using click data is to obtain statistically relevant metrics, not to monitor individual users. While data protection advocates might view this differently, this perspective helps explain the denial.

FTC documents confirm that click data is used for ranking purposes and frequently mention the NavBoost system in this context (54 times in the April 18, 2023 hearing). An official hearing in 2012 also revealed that click data influences rankings.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201600%20678'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201600%20678'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-5-Since-August-2012-it-was-officially-clear-that-click-data-changes-the-ranking.png.webp](https://searchengineland.com/wp-content/seloads/2024/08/Figure-5-Since-August-2012-it-was-officially-clear-that-click-data-changes-the-ranking.png.webp)

Figure 5: Since August 2012 (!), it was officially clear that click data changes the ranking.

It has been established that both click behavior on search results and traffic on websites or webpages impact rankings. Google can easily evaluate search behavior, including searches, clicks, repeat searches and repeat clicks, directly within the SERPs.

There has been speculation that Google could infer domain movement data from Google Analytics, leading some to avoid using this system. However, this theory has limitations.

First, Google Analytics does not provide access to all transaction data for a domain. More importantly, with over 60% of people using the Google Chrome browser (over three billion users), Google collects data on a substantial portion of web activity.

This makes Chrome a crucial component in analyzing web movements, as highlighted in hearings. Additionally, Core Web Vitals signals are officially collected through Chrome and aggregated into the “chromeInTotal” value.

The negative publicity associated with “monitoring” is one reason for the denial, while another is the concern that evaluating click and movement data could encourage spammers and tricksters to fabricate traffic using bot systems to manipulate rankings. While the denial might be frustrating, the underlying reasons are at least understandable.

- Some of the metrics that are stored include *badClicks* and *goodClicks*. The length of time a searcher stays on the target page and the information on how many other pages they view there and at what time (Chrome data) are most likely included in this evaluation.
- A short detour to a search result and a quick return to the search results and further clicks on other results can increase the number of bad clicks. The search result that had the last “good” click in a search session is recorded as the *lastLongestClick*.
- The data is squashed (i.e., condensed), so that it is statistically normalized and less susceptible to manipulation.
- If a page, a cluster of pages or the start page of a domain generally has good visitor metrics (Chrome data), this has a positive effect via NavBoost. By analyzing movement patterns within a domain or across domains, it is even possible to determine how good the user guidance is via the navigation.
- Since Google measures entire search sessions, it is theoretically even possible in extreme cases to recognize that a completely different document is considered suitable for a search query. If a searcher leaves the domain that they clicked on in the search result within a search and goes to another domain (because it may even have been linked from there) and remains there as the recognizable end of the search, this “end” document could be flushed to the front via NavBoost in the future, provided it is available in the selection ring set. However, this would require a strong statistically relevant signal from many searchers.

Let’s first examine clicks in search results. Each ranking position in the SERPs has an average expected click-through rate (CTR), serving as a performance benchmark. For example, according to an analysis by Johannes Beus presented at this year’s CAMPIXX in Berlin, the organic Position 1 receives an average of 26.2% of clicks, while Position 2 gets 15.5%.

If a snippet’s actual CTR significantly falls short of the expected rate, the NavBoost system registers this discrepancy and adjusts the ranking of the DocIDs accordingly. If a result historically generates significantly more or fewer clicks than expected, NavBoost will move the document up or down in the rankings as needed (see Figure 6).

This approach makes sense because clicks essentially represent a vote from users on the relevance of a result based on the title, description and domain. This concept is even detailed in official documents, as illustrated in Figure 7.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201131%20956'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201131%20956'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-6-If-the-22expected_CRT-deviates-significantly-from-the-actual-value-the-rankings-are-adjusted-accordingly.-Datasource-J.-Beus-SISTRIX-with-editorial-overlays.png.webp](https://searchengineland.com/wp-content/seloads/2024/08/Figure-6-If-the-22expected_CRT-deviates-significantly-from-the-actual-value-the-rankings-are-adjusted-accordingly.-Datasource-J.-Beus-SISTRIX-with-editorial-overlays.png.webp)

Figure 6: If the “expected_CRT deviates significantly from the actual value, the rankings are adjusted accordingly. (Datasource: J. Beus, SISTRIX, with editorial overlays)

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201134%20653'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201134%20653'%3E%3C/svg%3E)

Figure 7: Slide from a Google presentation (Source: Trial Exhibit – UPX0228, U.S. and Plaintiff States v. Google LLC)

Since our pencil document is still new, there are no available CTR values yet. It’s unclear whether CTR deviations are ignored for documents with no data, but this seems likely, as the goal is to incorporate user feedback. Alternatively, the CTR might initially be estimated based on other values, similar to how the quality factor is handled in Google Ads.

- SEO experts and data analysts have long reported that they have noticed the following phenomenon when comprehensively monitoring their own click-through rates: If a document for a search query newly appears in the top 10 and the CTR falls significantly short of expectations, you can observe a drop in ranking within a few days (depending on the search volume).
- Conversely, the ranking often rises if the CTR is significantly higher in relation to the rank. You only have a short time to react and adjust the snippet if the CTR is poor (usually by optimizing the title and description) so that more clicks are collected. Otherwise, the position deteriorates and is subsequently not so easy to regain. Tests are thought to be behind this phenomenon. If a document proves itself, it can stay. If searchers don’t like it, it disappears again. Whether this is actually related to NavBoost is neither clear nor conclusively provable.

Based on the leaked information, it appears that Google uses extensive data from a page’s “environment” to estimate signals for new, unknown pages.

For instance, *NearestSeedversion* suggests that the PageRank of the home page *HomePageRank_NS* is transferred to new pages until they develop their own PageRank. Additionally, *pnavClicks* seems to be used to estimate and assign the probability of clicks through navigation.

Calculating and updating PageRank is time-consuming and computationally intensive, which is why the *PageRank_NS* metric is likely used instead. “NS” stands for “nearest seed,” meaning that a set of related pages shares a PageRank value, which is temporarily or permanently applied to new pages.

It’s probable that values from neighboring pages are also used for other critical signals, helping new pages climb the rankings despite lacking significant traffic or backlinks. Many signals are not attributed in real-time but may involve a notable delay.

- Google itself set a good example of freshness during a hearing. For example, if you search for “Stanley Cup,” the search results typically feature the famous mug. However, when the Stanley Cup ice hockey games are actively taking place, NavBoost adjusts the results to prioritize information about the games, reflecting changes in search and click behavior.
- Freshness does not refer to new (i.e., “fresh”) documents but to changes in search behavior. According to Google, there are over a billion (that’s not a typo) new behaviors in the SERPs every day! So every search and every click contributes to Google’s learning. The assumption that Google knows everything about seasonality is probably not correct. Google recognizes fine-grained changes in search intentions and constantly adapts the system – which creates the illusion that Google actually “understands” what searchers want.

The click metrics for documents are apparently stored and evaluated over a period of 13 months (one month overlap in the year for comparisons with the previous year), according to the latest findings.

Since our hypothetical domain has strong visitor metrics and substantial direct traffic from advertising, as a well-known brand (which is a positive signal), our new pencil document benefits from the favorable signals of older, successful pages.

As a result, NavBoost elevates our ranking from 14th to 5th place, placing us in the “blue ring” or top 10. This top 10 list, including our document, is then forwarded to the Google Web Server along with the other nine organic results.

- Contrary to expectations, Google does not actually deliver many personalized search results. Tests have probably shown that modeling user behavior and making changes to it delivers better results than evaluating the personal preferences of individual users.
- This is remarkable. The prediction via neural networks is now better suited to us than our own surfing and clicking history. However, individual preferences, such as a preference for video content, are still included in the personal results.

## The GWS: Where everything comes to an end and a new beginning

The Google Web Server (GWS) is responsible for assembling and delivering the search results page (SERP). This includes 10 blue links, along with ads, images, Google Maps views, “People also ask” sections and other elements.

The Tangram system handles geometric space optimization, calculating how much space each element requires and how many results fit into the available “boxes.” The Glue system then arranges these elements in their proper places.

Our pencil document, currently in 5th place, is part of the organic results. However, the CookBook system can intervene at the last moment. This system includes *FreshnessNode*, *InstantGlue* (reacts in periods of 24 hours with a delay of around 10 minutes) and *InstantNavBoost*. These components generate additional signals related to topicality and can adjust rankings in the final moments before the page is displayed.

Let’s say a German TV program about 250 years of Faber-Castell and the myths surrounding the word “pencil” begins to air. Within minutes, thousands of viewers grab their smartphones or tablets to search online. This is a typical scenario. *FreshnessNode* detects the surge in searches for “pencil” and, noting that users are seeking information rather than making purchases, adjusts the rankings accordingly.

In this exceptional situation, *InstantNavBoost* removes all transactional results and replaces them with informational ones in real time. *InstantGlue* then updates the “blue ring,” causing our previously sales-oriented document to drop out of the top rankings and be replaced by more relevant results.

[data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20703%20288'%3E%3C/svg%3E](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20703%20288'%3E%3C/svg%3E)

![https://searchengineland.com/wp-content/seloads/2024/08/Figure-8-A-television-program-on-the-origins-of-the-word-22pencil22-to-celebrate-250-years-of-Faber-Castell-a-well-known-German-pencil-manufacturer.png.webp](https://searchengineland.com/wp-content/seloads/2024/08/Figure-8-A-television-program-on-the-origins-of-the-word-22pencil22-to-celebrate-250-years-of-Faber-Castell-a-well-known-German-pencil-manufacturer.png.webp)

Figure 8: A television program on the origins of the word “pencil” to celebrate 250 years of Faber-Castell, a well-known German pencil manufacturer.

Unfortunate as it may be, this hypothetical end to our ranking journey illustrates an important point: achieving a high ranking isn’t solely about having a great document or implementing the right SEO measures with high-quality content.

Rankings can be influenced by a variety of factors, including changes in search behavior, new signals for other documents and evolving circumstances. Therefore, it’s crucial to recognize that having an excellent document and doing a good job with SEO is just one part of a broader and more dynamic ranking landscape.

The process of compiling search results is extremely complex, influenced by thousands of signals. With numerous tests conducted live by SearchLab using Twiddler, even backlinks to your documents can be affected.

These documents might be moved from HiveMind to less critical levels, such as SSDs or even TeraGoogle, which can weaken or eliminate their impact on rankings. This can shift ranking scales even if nothing has changed with your own document.

Google’s John Mueller has emphasized that a drop in ranking often doesn’t mean you’ve done anything wrong. Changes in user behavior or other factors can alter how results perform.

For instance, if searchers start preferring more detailed information and shorter texts over time, NavBoost will automatically adjust rankings accordingly. However, the IR score in the Alexandria system or Ascorer remains unchanged.

One key takeaway is that SEO must be understood in a broader context. Optimizing titles or content won’t be effective if a document and its search intent don’t align.

The impact of Twiddlers and NavBoost on rankings can often outweigh traditional on-page, on-site or off-site optimizations. If these systems limit a document’s visibility, additional on-page improvements will have minimal effect.

However, our journey doesn’t end on a low note. The impact of the TV program about pencils is temporary. Once the search surge subsides, *FreshnessNode* will no longer affect our ranking, and we’ll settle back at 5th place.

As we restart the cycle of collecting click data, a CTR of around 4% is expected for Position 5 (based on Johannes Beus from SISTRIX). If we can maintain this CTR, we can anticipate staying in the top ten. All will be well.

## Key SEO takeaways

- **Diversify traffic sources**: Ensure you receive traffic from various sources, not just search engines. Traffic from less obvious channels, like social media platforms, is also valuable. Even if Google’s crawler can’t access certain pages, Google can still track how many visitors come to your site through platforms like Chrome or direct URLs.
- **Build brand and domain awareness**: Always work on strengthening your brand or domain name recognition. The more familiar people are with your name, the more likely they are to click on your site in search results. Ranking for many long-tail keywords can also boost your domain’s visibility. Leaks suggest that “site authority” is a ranking signal, so building your brand’s reputation can help improve your search rankings.
- **Understand search intent**: To better meet your visitors’ needs, try to understand their search intent and journey. Use tools like Semrush or SimilarWeb to see where your visitors come from and where they go after visiting your site. Analyze these domains – do they offer information that your landing pages lack? Gradually add this missing content to become the “final destination” in your visitors’ search journey. Remember, Google tracks related search sessions and knows precisely what searchers are looking for and where they’ve been searching.
- **Optimize your titles and descriptions to improve CTR**: Start by reviewing your current CTR and making adjustments to enhance click appeal. Capitalizing a few important words can help them stand out visually, potentially boosting CTR; test this approach to see if it works for you. The title plays a critical role in determining whether your page ranks well for a search phrase, so optimizing it should be a top priority.
- **Evaluate hidden content**: If you use accordions to “hide” important content that requires a click to reveal, check if these pages have a higher-than-average bounce rate. When searchers can’t immediately see they’re in the right place and need to click multiple times, the likelihood of negative click signals increases.
- **Remove underperforming pages**: Pages that nobody visits (web analytics) or that do not achieve a good ranking over longer periods of time should be removed if necessary. Bad signals are also passed on to neighboring pages! If you publish a new document in a “bad” page cluster, the new page has few chances. “deltaPageQuality” apparently actually measures the qualitative difference between individual documents in a domain or cluster.
- **Enhance page structure**: A clear page structure, easy navigation and a strong first impression are essential for achieving top rankings, often thanks to NavBoost.
- **Maximize engagement**: The longer visitors stay on your site, the better the signals your domain sends, which benefits all of your subpages. Aim to be the final destination by providing all the information they need so visitors won’t have to search elsewhere.
- **Expand existing content rather than constantly creating new ones**: Updating and enhancing your current content can be more effective. *ContentEffortScore* measures the effort put into creating a document, with factors like high-quality images, videos, tools and unique content all contributing to this important signal.
- **Align your headings with the content they introduce**: Ensure that (intermediate) headings accurately reflect the text blocks that follow. Thematic analysis, using techniques like embeddings (text vectorization), is more effective at identifying whether headings and content match correctly compared to purely lexical methods.
- **Utilize web analytics**: Tools like Google Analytics lets you track visitor engagement effectively and identify and address any gaps. Pay particular attention to the bounce rate of your landing pages. If it’s too high, investigate potential causes and take corrective actions. Remember, Google can access this data through the Chrome browser.
- **Target less competitive keywords**: You can also focus on ranking well for less competitive keywords first and thus more easily build up positive user signals.
- **Cultivate quality backlinks**: Focus on links from recent or high-traffic pages stored in HiveMind, as these provide more valuable signals. Links from pages with little traffic or engagement are less effective. Additionally, backlinks from pages within the same country and those with thematic relevance to your content are more beneficial. Be aware that “toxic” backlinks, which negatively impact your score, do exist and should be avoided.
- **Pay attention to the context surrounding links:** The text before and after a link, not just the anchor text itself, are considered for ranking. Make sure the text naturally flows around the link. Avoid using generic phrases like “click here,” which has been ineffective for over twenty years.
- **Take note of the Disavow tool’s limitations:** The Disavow tool, used to invalidate bad links, is not mentioned in the leak at all. It seems that algorithms do not consider it, and it serves mainly a documentary purpose for spam fighters.
- **Consider author expertise**: If you use author references, ensure they are also recognized on other websites and demonstrate relevant expertise. Having fewer but highly qualified authors is better than having many less credible ones. According to a patent, Google can assess content based on the author’s expertise, distinguishing between experts and laypeople.
- **Create exclusive, helpful, comprehensive and well-structured content**: This is especially important for key pages. Demonstrate your genuine expertise on the topic and, if possible, provide evidence of it. While it’s easy to have someone write content just to have something on the page, setting high ranking expectations without real quality and expertise may not be realistic.

*A version of this article was originally published in German in August 2024 in Website Boosting, Issue 87.*

[*Add Search Engine Land to your Google News feed.*](https://news.google.com/publications/CAAqBggKMLXKIzD8vAQ?hl=en-US&gl=US&ceid=US%3Aen) 

Related stories

[The latest jobs in search marketing](https://searchengineland.com/latest-jobs-in-search-marketing-378959)

[Unraveling Google Navboost and building user trust through UX](https://searchengineland.com/navboost-user-trust-ux-445240)

[How Google ending continuous scroll could impact ORM](https://searchengineland.com/google-continuous-scroll-orm-445239)

[Google Search ranking bug unrelated to the core update](https://searchengineland.com/google-search-ranking-bug-unrelated-to-the-core-update-445246)

[Publishers report ‘negligible’ traffic impact of Google AI Overviews](https://searchengineland.com/google-ai-overviews-publisher-traffic-impact-445238)

New on Search Engine Land