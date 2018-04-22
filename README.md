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

> This project is inspired from Kenneth Reitz's similar project [kennethreitz/twitter-scraper](https://github.com/kennethreitz/twitter-scraper) which is limited to python 3.6 and above.

## Getting Started

```bash
$ pip install tweetscrape
$ python -m tweetscrape.twitter_scrape -u "@5hirish" -p 3
$ python -m tweetscrape.twitter_scrape -s "#Python" -p 4
$ python -m tweetscrape.twitter_scrape -s "Avengers Infinity War" -p 2

```

## Usage

```python
from tweetscrape.profile_tweets import TweetScrapperProfile 

tweet_scrapper = TweetScrapperProfile("@5hirish", 1)
tweets = tweet_scrapper.get_profile_tweets()
for tweet in tweets:
    print(str(tweet))
```
Read more on `tweetscrape` usage [here](USAGE.md).
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

....
```

## Requirements

* [Python 3.X](https://docs.python.org/3/)

Python Package dependencies listed in [requirements.txt](requirements.txt)

### Features

* Extract user tweets with all meta-data
* Extracts external links, hashtags and mentions from a tweet
* Extracts reply, favorite and retweet counts of a tweet

### Cool stuff you try
I have added a few examples (Jupyter Notebooks) using this library to do some [cool stuff](tweetscrape/coolstuff).
- Tweet generator using Markov Chain
- Gensim Topic Modeling using Latent Dirichlet Allocation model

### TODO

- [x] Extract tweets from a twitter user's profile
- [x] Extract tweets from twitter search
- [ ] Extract tweets from a twitter thread, given the thread link
- [ ] Extract the quoted tweet along with a tweet

### Contributions
Please see the [contributing documentation](docs/CONTRIBUTING.md) for some tips on getting started.

### Maintainers
* [@5hirish](https://github.com/5hirish) - Shirish Kadam