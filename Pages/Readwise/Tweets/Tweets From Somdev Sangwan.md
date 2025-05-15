# Tweets From Somdev Sangwan

![rw-book-cover](https://pbs.twimg.com/profile_images/1860768076335394816/BGpdXrEg.jpg)

## Metadata
- Author: [[@s0md3v on Twitter]]
- Full Title: Tweets From Somdev Sangwan
- Category: #tweets
- URL: https://twitter.com/s0md3v

## Highlights
- Look-aheads and Look-behinds
  cat(?=dog) matches cat in catdog not in catxyz
  cat(?!dog) matches cat in catxyz not in catdog
  (?<=cat)dog matches dog in catdog not in xyzdog
  (?<!cat)dog matches dog in xyzdog not in catdog ([View Tweet](https://twitter.com/s0md3v/status/1171796849478402051))
- ? also serves as OPTIONAL-MATCH operator
  cat(corn)?dog will match both catdog and catcorndog i.e. corn is optional. ([View Tweet](https://twitter.com/s0md3v/status/1171795522916499457))
- ^ is also a MATCH-EVERYTHING-EXCEPT-THESE-CHARS operator.
  [^pc]orn will match zorn, 7orn, $orn etc. but not porn or corn ([View Tweet](https://twitter.com/s0md3v/status/1171793074344747009))
- Groups can be referenced
  (ca+t)dog\1 matches caaaatdogcaaaat where \1 is obviously the second (arrays start with 0) group
  If you don't want to capture a group add ?: in the start e.g. (?:ca+t)dog ([View Tweet](https://twitter.com/s0md3v/status/1171793070741831681))
- Since it blew up, I am extending this cheatsheet :)
  Grouping
  () are capturing groups. (ca+t)(dog) will match caaatdog.
  Groups can be accessed in Python as follows:
  https://t.co/3Sl4nAQdcS(0) = caaatdog
  https://t.co/3Sl4nAQdcS(1) = caaat
  https://t.co/3Sl4nAQdcS(2) = dog ([View Tweet](https://twitter.com/s0md3v/status/1171793066719473664))
- Sorry guys, I made 4 typos. I forgot to add "t" in the end of these 3 patterns.
  > c[ea]t matches cat and cet
  > c[ea]+t matches caaat, ceeet (also caeeeaaeat)
  > c[A-C0-9]t matches cAt, cBt, cCt, c8t etc.
  > .*w and .*w? will match "xx" in the starting of xxsomethingnew.... as well ([View Tweet](https://twitter.com/s0md3v/status/1171434559038078976))
- \t for tabs, \r for carriage return and \n for newline
  Yes, c\d+t matches c2784t
  Yes, c\s+ matches c t
  Yes, c\D+ matches cxxxt ca2t 
  Using .*w vs .*?w on xxsomethingnew@1234wxx
  .*w returns somethingnew@1234w (longest match)
  .*w? returns somethingnew (shortest match) ([View Tweet](https://twitter.com/s0md3v/status/1171394414251429889))
- cat$ will match cat in aaacat but not in aaacats
  ^cat$ will match only and only this string i.e. cat
  \d is for digits, \w for alphanumeric chars, \s is for white space chars & line breaks
  \D is for non-digits, \W for non-alphamueric chars and \s is for non-white space chars ([View Tweet](https://twitter.com/s0md3v/status/1171394410283560961))
- c[A-C0-9] matches cAt, cBt, cCt, c8t etc.
  c.t matches cat, c&t, c2t (any char between c and t)
  c.+t matches c3%x4t (any number of any chars)
  c.*t matches c3%x4t and as well as ct
  ^ denotes start of a string, $ denotes the end
  ^a+cat will match aaacat in aaacat but not in bbaaacat ([View Tweet](https://twitter.com/s0md3v/status/1171394406512910336))
- Learn Regex in 4 tweets :)
  cat matches cat
  ca+t matches caaaaaaaaaaaat but not ct
  ca*t matches caaaaaaaaaaaat and also ct
  ca{2,4} matches caat, caaat and caaaat
  c(at)+ matches catatatatatat
  c(at|orn) matches cat and corn
  c[ea] matches cat and cet
  c[ea]+ matches caaaat and ceeet ([View Tweet](https://twitter.com/s0md3v/status/1171394403065155584))
