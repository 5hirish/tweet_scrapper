## Usage

```python
from tweetscrape.user_tweets import TweetScrapper 

tweet_scrapper = TweetScrapper("@5hirish", 1)
tweets = tweet_scrapper.get_user_tweets()
for tweet in tweets:
    print(str(tweet))
```

The `TweetScrapper` class scrapes the tweets using Twitter frontend APIs with XPATH queries. It requires two parameters, the Twitter **username** and the **number of pages** to scrape (At the moment, maximum pages you can scrape is 25). 

The `get_user_tweets()` method return a list of extracted tweets of the type `TweetInfo`. Iterating over this list and using proper getters can fetch you the required information of each tweet.

```
Id:973027095411437568	Type:tweet	Time:1520822712000
Author:Reza_Zadeh	AuthorId:92839676
Text:  There's a lot of computational power that goes into mining bitcoin, in particular to find little bits of data with certain SHA256 hashes. Instead, would've been great if that compute power were used to solve challenging NP-hard problems. Human progress becomes side-effect of hype
Links:[]
Hastags:[]
Mentions:[]
Replies:12	Favorites:187	Retweets:51

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

Id:970542118350462976	Type:tweet	Time:1520230247000
Author:GabbbarSingh	AuthorId:108391251
Text:  Gary Oldman, playing Winston Churchill, wins the best actor for Darkest hour. Nothing wrong with awarding the craft of acting even though you play a murderer, but showing the cold blooded tyrant Churchill, in a positive light, deserves condemnation from Indians. #FuckChurchill
Links:[]
Hastags:['#FuckChurchill']
Mentions:[]
Replies:30	Favorites:581	Retweets:253

Id:970008694783176704	Type:tweet	Time:1520103069000
Author:maxmunnecke	AuthorId:201907594
Text:  New Jupyter notebook on topic modelling with SpaCy, Gensim and Textacy. Combining 'Termite Plot' and 'pyLDAvis' visualizations makes sense when evaluating topic models. Try out the notebook: https://nbviewer.jupyter.org/github/repmax/topic-model/blob/master/topic-modelling.ipynb … #dataviz #nlp #digitalhumanities @gensim_py @stanfordnlp @uwdatapic.twitter.com/ngyGZopw7g
Links:['https://t.co/0o0FEOAl20', 'https://t.co/ngyGZopw7g']
Hastags:['#dataviz', '#nlp', '#digitalhumanities']
Mentions:['@gensim_py', '@stanfordnlp', '@uwdata']
Replies:0	Favorites:170	Retweets:61

```

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
