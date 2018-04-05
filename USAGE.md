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
Id:972778151796510721	Type:tweet	Time:1520763359000
Author:gensim_py	AuthorId:3110758625
Text:   Calling all #Gensim users! Please help improve Gensim by giving us your feedback in this short survey.https://radimrehurek.com/gensim/survey.html …
Links:['https://t.co/sJsDTXv6QF']
Hastags:['#Gensim']
Mentions:[]
Replies:8	Favorites:57	Retweets:46

Id:953706491881680896	Type:tweet	Time:1516216321000
Author:QCon	AuthorId:14100646
Text:  “ML for Question and Answer Understanding @Quora” #machinelearning @nikhilbd presentation is now live on @infoqhttp://bit.ly/2Da8WuX 
Links:['https://t.co/buseQxF9mS']
Hastags:['#machinelearning']
Mentions:['@Quora', '@nikhilbd', '@InfoQ']
Replies:0	Favorites:15	Retweets:5

Id:970008694783176704	Type:tweet	Time:1520103069000
Author:maxmunnecke	AuthorId:201907594
Text:  New Jupyter notebook on topic modelling with SpaCy, Gensim and Textacy. Combining 'Termite Plot' and 'pyLDAvis' visualizations makes sense when evaluating topic models. Try out the notebook: https://nbviewer.jupyter.org/github/repmax/topic-model/blob/master/topic-modelling.ipynb … #dataviz #nlp #digitalhumanities @gensim_py @stanfordnlp @uwdatapic.twitter.com/ngyGZopw7g
Links:['https://t.co/0o0FEOAl20', 'https://t.co/ngyGZopw7g']
Hastags:['#dataviz', '#nlp', '#digitalhumanities']
Mentions:['@gensim_py', '@stanfordnlp', '@uwdata']
Replies:0	Favorites:170	Retweets:61

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
