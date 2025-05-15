# Tweets From Command Line Magic

![rw-book-cover](https://pbs.twimg.com/profile_images/1322201332934156288/9CjMTKbb.jpg)

## Metadata
- Author: [[@climagic on Twitter]]
- Full Title: Tweets From Command Line Magic
- Category: #tweets
- URL: https://twitter.com/climagic

## Highlights
- List the top 30 404 generating URLs from your webserver log and order it by the number of requests for each.
  awk '$9 == "404" {print $7}' access.log |sort|uniq -c|sort -rn| head -n 30 ([View Tweet](https://twitter.com/climagic/status/1448297516571762691))
