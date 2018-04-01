# Tweet Scrapper

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5924d3402a2c43d0bf7affa6863872f6)](https://www.codacy.com/app/5hirish/tweet_scrapper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=5hirish/tweet_scrapper&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/5hirish/tweet_scrapper/branch/master/graph/badge.svg)](https://codecov.io/gh/5hirish/tweet_scrapper)
[![Build Status](https://travis-ci.org/5hirish/tweet_scrapper.svg?branch=master)](https://travis-ci.org/5hirish/tweet_scrapper)
[![Twitter](https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow)](https://twitter.com/intent/follow?screen_name=5hirish)


Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user's Tweets trivially. Follow the creator's blog at [shirishkadam.com](https://shirishkadam.com) for updates on progress.

> This project is inspired from Kenneth Reitz's similar project [kennethreitz/twitter-scraper](https://github.com/kennethreitz/twitter-scraper) which is limited to python 3.6 an above.

## Getting Started

```
$ git clone https://github.com/5hirish/tweet_scrapper.git
$ cd tweet_scrapper
$ pip install -r requirements.txt
$ python -m qas.twitter_scrape -u "@5hirish" -n 3
```

## Requirements

* [Python 3.X](https://docs.python.org/3/)

Python Package dependencies listed in [requirements.txt](requirements.txt)

### Features

* Extract user tweets with all meta-data
* Extracts external links, hashtags and mentions from a tweet
* Extracts reply, favorite and retweet counts of a tweet

### TODO

- [x] Extract tweets from a twitter user's profile
- [ ] Extract tweets from a twitter thread, given the thread link
- [ ] Extract the quoted tweet along with a tweet

### Contributions
Please see the [contributing documentation](docs/CONTRIBUTING.md) for some tips on getting started.

### Maintainers
* [@5hirish](https://github.com/5hirish) - Shirish Kadam