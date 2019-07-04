## Usage

For bash command line interface help:
```bash
$ python -m tweetscrape.twitter_scrape -h
```

### Fetch User Profile Tweets

```python
from tweetscrape.profile_tweets import TweetScrapperProfile 

tweet_scrapper = TweetScrapperProfile("5hirish", 40, 'twitter.csv', 'csv')
tweet_count, tweet_id, tweet_time, dump_path = tweet_scrapper.get_profile_tweets()
print("Extracted {0} tweets till {1} at {2}".format(tweet_count, tweet_time, dump_path))
```

The `TweetScrapperProfile` class scrapes the tweets using Twitter frontend APIs with XPATH queries. 
It requires four parameters, the Twitter **username**, the **number of tweets** to scrape
 (default tweets scraped are 40), the **file path** to dump 
the data and the data **export format**, which can be JSON or CSV. 
You can even add proxy to the scraper via `request_proxies` parameter.
__NOTE__: To extract as much tweets as possible set the number of tweets to -1.

The `get_profile_tweets()` method returns the count of tweets, last extracted tweet id, last extracted tweet time and
 the file export path of extracted tweets. 

```csv
id,type,time,author,author_id,re_tweeter,associated_tweet,text,links,hashtags,mentions,reply_count,favorite_count,retweet_count
993872079274508289,tweet,1525792543000,5hirish,428808036,,993872079274508289,"Built @twitter #scrapper inspired by @kennethreitz similar project. Does a bunch of other cool stuff like extracting user tweets with all meta-data, hastags, images, likes, etc. extracting tweets based on keyword or hastag search #python @Github https://github.com/5hirish/tweet_scrapper …pic.twitter.com/bXdnrWXNwr","['https://t.co/ID5hJ6InIu', 'https://t.co/bXdnrWXNwr']","['#scrapper', '#python']","['@Twitter', '@kennethreitz', '@github']",1,14,7
1141791578970894338,tweet,1561059300000,gracecondition,127701253,5hirish,1141791578970894338,everyone else using word2vec:king – man + woman = queenme using word2vec:fish + music = bassfish + friend = chumfish + hair = mulletfish + struggle = flounderoink - pig + bro = wassupyeti – snow + economics = homo economicushttps://graceavery.com/word2vec-fish-music-bass/ …,['https://t.co/UAiViuEnM2'],[],[],17,939,227
1141849459342610437,tweet,1561073100000,Reuters,1652541,5hirish,1141849459342610437,WATCH: Elon Musk gives #E3 audience a preview of gaming in Tesla carspic.twitter.com/u7rVedhDyW,['https://t.co/u7rVedhDyW'],"['#E3', '#E3']",[],3,49,18
1141812196453699584,tweet,1561064216000,xamat,9316452,5hirish,1141812196453699584,"The annoying pop-up about cookies on websites is basically teaching me to click ""ok"" on anything that gets in my way asap, which seems very dangerous and exactly the opposite of what is intended.",[],[],[],1,23,3
1141897990627446784,tweet,1561084671000,data_mike_j,1053368990695706624,5hirish,1141897990627446784,Check out my newest blog post where I build a graph visualization of the #MuellerReport using @spacy_io and #Python including paragraph recommendation engine.https://minimizeuncertainty.com/post/graph-visualization-of-the-mueller-report-with-spacy-and-pyvis/ …,['https://t.co/Q5GGKqmbYv'],"['#MuellerReport', '#Python']",['@spacy_io'],0,31,13
1142137189775507456,tweet,1561141700000,5hirish,428808036,,1142137187783213056,"Share your weekend goals here, could be anything, like reading a book, writing a blog post, preparing your favorite dessert or anything that will give you a positive feeling of #accomplishment for the coming week. Let's check back on Monday.",[],['#accomplishment'],[],1,0,0
1142137187783213056,tweet,1561141700000,5hirish,428808036,,1142137187783213056,"Weekend Goal: Convert my Flask app into a RESTful Flask API app template with Unit tests, Travis CI and Swagger docs. #python Repo: https://github.com/5hirish/flask-restful-template … (Contributors Welcome!)#weekendgoal #accountability",['https://t.co/m7isdCd6cc'],"['#python', '#weekendgoal', '#accountability']",[],1,3,1
1141840676394434560,tweet,1561071006000,naval,745273,5hirish,1141840676394434560,"Lasting novels don’t come from literature departments. Successful businesses don’t come from business schools. Scientific revolutions don’t come from research universities.Get your education, then get moving. Find the loners tinkering at the edge.",[],[],[],149,10188,2562
1141740790542213121,tweet,1561047191000,WSJ,3108351,5hirish,1141740790542213121,"Slack shares open at $38.50 in their trading debut, above $26 reference price and giving the company a valuation of about $23.2 billionhttps://on.wsj.com/2Xmkitn",['https://t.co/uo7yCGqSmC'],[],[],3,76,48
1141511813709717504,tweet,1560992599000,quocleix,989251872107085824,5hirish,1141511813709717504,"XLNet: a new pretraining method for NLP that significantly improves upon BERT on 20 tasks (e.g., SQuAD, GLUE, RACE)arxiv: https://arxiv.org/abs/1906.08237 github (code + pretrained models): https://github.com/zihangdai/xlnet with Zhilin Yang, @ZihangDai, Yiming Yang, Jaime Carbonell, @rsalakhupic.twitter.com/JboOekUVPQ","['https://t.co/C1tFMwZvyW', 'https://t.co/kI4jsVzT1u', 'https://t.co/JboOekUVPQ']",[],"['@ZihangDai', '@rsalakhu']",21,1763,715
1141736965311569920,tweet,1561046279000,justinkan,28917111,5hirish,1141736965311569920,"One of the most important skills I’ve built is the ability to sit with discomfort. Being able to be uncomfortable (bored, on the receiving end of anger, in pain) and not needing to escape has changed my happiness and my life. It would have seemed impossible to me 12 months ago.",[],[],[],38,1578,242
....
```

### Fetch Advance Search Tweets

```python
from tweetscrape.search_tweets import TweetScrapperSearch

tweet_scrapper = TweetScrapperSearch(search_from_accounts="@CNN", search_till_date="2016-04-01", search_since_date="2015-11-01", num_tweets=40, tweet_dump_path='twitter.csv', tweet_dump_format='csv')
tweet_count, tweet_id, tweet_time, dump_path = tweet_scrapper.get_search_tweets()
print("Extracted {0} tweets till {1} at {2}".format(tweet_count, tweet_time, dump_path))
```

The `TweetScrapperSearch` class scrapes the tweets based on the hashtags or a search term or any of the 
advanced filters of Twitter search [Twitter Search Advance](https://twitter.com/search-advanced).
 It requires multiple parameters, based on the filters you might want to search with. Based on these filters a query is
 constructed and searched on Twitter. It also requires the **number of tweets** to scrape, the **file path** to dump 
the data and the data **export format**, which can be JSON or CSV.
You can even add proxy to the scraper via `request_proxies` parameter.

The `get_search_tweets()` method returns the count of tweets, last extracted tweet id, last extracted tweet time and
 the file export path of extracted tweets. 
 
Following are the supported search filters (parameters) for `TweetScrapperSearch` class.

```text
search_all: Search all of these words. eg. Avengers Infinity War
search_exact: Search this exact phrase. eg. Avengers
search_any: Search any of these words. eg. SpiderMan Thor Hulk
search_excludes: Search excluding these words. eg. AntMan
search_hashtags: Search these hashtags. eg. #avengers #endgame
search_from_accounts: Search tweets from these accounts. eg. @marvel @avengers
search_to_accounts: Search tweets to these accounts. eg. @marvel
search_mentions: Search tweets mentioning these accounts. eg. @avengers
search_near_place: Search tweets near this place. eg. New York
search_till_date: Search tweets until this date: YYYY-MM-DD eg. 2019-01-01
search_since_date: Search tweets since this date: YYYY-MM-DD. eg. 2018-11-01
language: Search tweets in language from language codes. eg. 'en' for English
```

### Fetch User Tweet thread Tweets

```python
from tweetscrape.conversation_tweets import TweetScrapperConversation

tweet_scrapper = TweetScrapperConversation("ewarren", 1146415363460141057, 40, 'twitter.csv', 'csv')
tweet_count, tweet_id, tweet_time, dump_path = tweet_scrapper.get_thread_tweets()
print("Extracted {0} tweets till {1} at {2}".format(tweet_count, tweet_time, dump_path))
```

The `TweetScrapperConversation` class scrapes the tweets from a tweet tread or conversation.
 It requires two parameters, the Twitter username of the user who tweeted the original tweet and
  the id of the tweet. It also requires the **number of tweets** to scrape, the **file path** to dump 
the data and the data **export format**, which can be JSON or CSV.
You can even add proxy to the scraper via `request_proxies` parameter.

The `get_thread_tweets()` method returns the count of tweets, last extracted tweet id, last extracted tweet time and
 the file export path of extracted tweets. 
 
 
### Fetch User stats

```python
from tweetscrape.users_scrape import TweetScrapperUser

ts = TweetScrapperUser("5hirish")
user_info = ts.get_profile_info()
```

The `TweetScrapperUser` class scrapes the stats of the user from Twitter.
 It requires one parameter, the Twitter username of the user.
You can even add proxy to the scraper via `request_proxies` parameter.

The `get_profile_info()` method returns the JSON with user information. 
 ```json
{
  "username": "@5hirish", 
  "name": "Shirish Kadam", 
  "bio": "Building @alleviate_hq #SaaS #NLProc  #MachineLearning #DataScience\nAutomating Automation\nhttp://5hirish.com",
  "location": "Bengaluru, India", 
  "location_id": "1b8680cd52a711cb", 
  "url": "http://www.shirishkadam.com", 
  "tweets": "2619", 
  "following": "694", 
  "followers": "243", 
  "favorites": "8112"
}
```

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
`get_tweet_hashtags()` | Extracted hashtags from the tweet
`get_tweet_mentions()` | Mentioned Twitter users in the tweet
`get_tweet_replies_count()` | Total count of replies on the tweet
`get_tweet_favorite_count()` | Total count of favorites on the tweet
`get_tweet_retweet_count()` | Total count of retweets of the tweet
