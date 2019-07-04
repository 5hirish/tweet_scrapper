# Tweet Scrapper

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5924d3402a2c43d0bf7affa6863872f6)](https://www.codacy.com/app/5hirish/tweet_scrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=5hirish/tweet_scrapper&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/5hirish/tweet_scrapper/branch/master/graph/badge.svg)](https://codecov.io/gh/5hirish/tweet_scrapper)
[![Build Status](https://travis-ci.org/5hirish/tweet_scrapper.svg?branch=master)](https://travis-ci.org/5hirish/tweet_scrapper)
[![Current Release Version](https://img.shields.io/github/release/5hirish/tweet_scrapper.svg)](https://github.com/5hirish/tweet_scrapper/releases)
[![pypi Version](https://img.shields.io/pypi/v/tweetscrape.svg)](https://pypi.python.org/pypi/tweetscrape)
[![Twitter](https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=5hirish)


Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user's Tweets trivially. Follow the creator's blog at [shirishkadam.com](https://shirishkadam.com) for updates on progress.

## Installation
Built for Python 3.5.x, 3.6.x

```bash
$ pip install tweetscrape
$ python -m tweetscrape.twitter_scrape --help
```

## Getting Started
```bash
$ python -m tweetscrape.twitter_scrape -u "5hirish"  -n 60 -d "twitter.csv" -f "csv"
$ python -m tweetscrape.twitter_scrape --hashtag "#Python" -n 60 -d "twitter.csv" -f "csv"
$ python -m tweetscrape.twitter_scrape --all "Avengers" --mention "@Marvel" -n 20 -d "twitter.csv" -f "csv"
$ python -m tweetscrape.twitter_scrape --near "Brooklyn" -n 20 -d "twitter.csv" -f "csv"
$ python -m tweetscrape.twitter_scrape --from "@CNN" --since "2019-06-20" --until "2019-06-23" -n 20 -d "twitter.csv" -f "csv"
```

## Usage

```python
from tweetscrape.profile_tweets import TweetScrapperProfile 

tweet_scrapper = TweetScrapperProfile("5hirish", 40, 'twitter.csv', 'csv')
tweet_count, tweet_id, tweet_time, dump_path = tweet_scrapper.get_profile_tweets()
print("Extracted {0} tweets till {1} at {2}".format(tweet_count, tweet_time, dump_path))
```
#### Read more on `tweetscrape` usage here: [USAGE.md](USAGE.md)
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

## Requirements

* [Python 3.X](https://docs.python.org/3/)

Python Package dependencies listed in [requirements.txt](requirements.txt)

### Features

* Extract user tweets with all meta-data
* Extracts external links, hashtags and mentions from a tweet
* Extracts reply, favorite and retweet counts of a tweet
* Exports data to file in CSV or JSON with UTF-8 encoding
* Scraps tweets in a recursive and greedy approach
* Supports Proxy requests, request delays
* Extracts user information including bio, location and stats

### TODO

- [x] Extract tweets from a twitter user's profile
- [x] Extract tweets from twitter search with advance filters
- [x] Exports tweets to files
- [x] Supports infinite scroll
- [x] Extract tweets from a twitter thread, given the thread
- [ ] Extract the quoted tweet along with a tweet

### Contributions
Please see the [contributing documentation](docs/CONTRIBUTING.md) for some tips on getting started.

### Maintainers
* [@5hirish](https://github.com/5hirish) - Shirish Kadam
