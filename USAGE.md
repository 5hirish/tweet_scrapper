## Usage

### Fetch User Profile Tweets

```python
from tweetscrape.profile_tweets import TweetScrapperProfile

tweet_scrapper = TweetScrapperProfile("@5hirish", 1)
tweets = tweet_scrapper.get_profile_tweets()
for tweet in tweets:
    print(str(tweet))
```

The `TweetScrapperProfile` class scrapes the tweets using Twitter frontend APIs with XPATH queries. 
It requires two parameters, the Twitter **username** and the **number of pages** to scrape (At the moment, maximum pages you can scrape is 25).

The `get_profile_tweets()` method return a list of extracted tweets of the type `TweetInfo`. 
Iterating over this list and using proper getters can fetch you the required information of each tweet.

```
Id: 1056176020368191488	Type: tweet	Time: 1540646960000
Author: 5hirish	AuthorId: 428808036
ReTweeter: None
Associated Tweet: 1056176020368191488
Text:   I've completed 7 Pull Requests for #Hacktoberfest! https://hacktoberfest.digitalocean.com/stats/5hirish  Always wanted to contribute to #OpenSource, thanks to @digitalocean initiative #Hacktoberfest finally got around doing it. Will keep it up.
Links: ['https://t.co/J42KiNKGMG']
Hastags: ['#Hacktoberfest', '#OpenSource', '#Hacktoberfest']
Mentions: ['@digitalocean']
Replies: 0	Favorites: 3	Retweets: 1

Id: 1055883061513084928	Type: tweet	Time: 1540577113000
Author: wesmckinn	AuthorId: 115494880
ReTweeter: 5hirish
Associated Tweet: 1055883061513084928
Text:   TFW someone asks "Any update?" or "When is this feature going to be implemented?" on an open source issue tracker.
Links: []
Hastags: []
Mentions: []
Replies: 5	Favorites: 84	Retweets: 11

Id: 1055151881377406976	Type: tweet	Time: 1540402786000
Author: justinkan	AuthorId: 28917111
ReTweeter: 5hirish
Associated Tweet: 1055151881377406976
Text:   1/ Actually I’ve learned a lot from @ROWGHANI that’s worth sharing. First, your job as CEO is to: make sure there’s $ in the bank, define the company’s mission, hire the senior team, and do maybe one thing you enjoy (sales, product, etc)
Links: []
Hastags: []
Mentions: ['@ROWGHANI']
Replies: 43	Favorites: 2793	Retweets: 700
```

### Fetch Search/Hashtag Tweets

```python
from tweetscrape.search_tweets import TweetScrapperSearch

tweet_scrapper = TweetScrapperSearch("#python", 1)
tweets = tweet_scrapper.get_search_tweets()
for tweet in tweets:
    print(str(tweet))
```

The `TweetScrapperSearch` class scrapes the tweets based on the hashtags or a search term. It requires two parameters, 
the **search_term** which can be hashtag or the actual search term and the **number of pages** to scrape (At the moment, maximum pages you can scrape is 25).

The `get_search_tweets()` method return a list of extracted tweets of the type `TweetInfo`. Iterating over this list and using proper getters can fetch you the required information of each tweet.


### Extracted Tweets data model

Method | Description
--- | ---
`get_tweet_id()` | Fetches the item unique identifier
`get_tweet_type()` | The type of the item eg. `tweet`
`get_tweet_author()` | Twitter username of the author
`get_tweet_author_id()` | Unique identifier of the author
`get_tweet_time_ms()` | Tweet time in milliseconds
`get_tweet_text()` | Original tweet text
`get_tweet_links()` | Extracted external links from the tweet
`get_tweet_hashtags()` | Extracted hastags from the tweet
`get_tweet_mentions()` | Mentioned Twitter users in the tweet
`get_tweet_replies_count()` | Total count of replies on the tweet
`get_tweet_favorite_count()` | Total count of favorites on the tweet
`get_tweet_retweet_count()` | Total count of retweets of the tweet
