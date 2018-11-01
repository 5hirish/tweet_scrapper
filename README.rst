Tweet Scrapper
==============

|License: GPL v3| |Codacy Badge| |codecov| |Build Status| |pypi Version| |Current Release Version| |Twitter|

Twitter’s API is annoying to work with, and has lots of limitations —
luckily their frontend (JavaScript) has it’s own API, which I
reverse–engineered. No API rate limits. No restrictions. Extremely fast.

You can use this library to get the text of any user’s Tweets trivially.
Follow the creator’s blog at `shirishkadam.com`_ for updates on
progress.

    This project is inspired from Kenneth Reitz’s similar project
    `kennethreitz/twitter-scraper`_ which is limited to python 3.6 anc
    above.

Getting Started
---------------

.. code:: bash

    $ git clone https://github.com/5hirish/tweet_scrapper.git
    $ cd tweet_scrapper
    $ pip install -r requirements.txt
    $ python -m tweetscrape.twitter_scrape -u "@5hirish" -p 3
    $ python -m tweetscrape.twitter_scrape -s "#Python" -p 4
    $ python -m tweetscrape.twitter_scrape -s "Avengers Infinity War" -p 2

Usage
-----

.. code:: python

    from tweetscrape.profile_tweets import TweetScrapperProfile

    tweet_scrapper = TweetScrapperProfile("@5hirish", 1)
    tweets = tweet_scrapper.get_profile_tweets()
    for tweet in tweets:
        print(str(tweet))

Read more on ``tweetscrape`` usage `here`_.

::

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

    ....

Requirements
------------

-  `Python 3.X`_

Python Package dependencies listed in `requirements.txt`_

Features
~~~~~~~~

-  Extract user tweets with all meta-data
-  Extracts external links, hashtags and mentions from a tweet
-  Extracts reply, favorite and retweet counts of a tweet

TODO
~~~~

-  [x] Extract tweets from a twitter user’s profile
-  [x] Extract tweets from twitter search
-  [ ] Extract tweets from a twitter thread, given the thread link
-  [ ] Extract the quoted tweet along with a tweet

Contributions
~~~~~~~~~~~~~

Please see the `contributing documentation`_ for some tips on getting
started.

Maintainers
~~~~~~~~~~~

-  `@5hirish`_ - Shirish Kadam


.. _shirishkadam.com: https://shirishkadam.com
.. _kennethreitz/twitter-scraper: https://github.com/kennethreitz/twitter-scraper
.. _here: USAGE.md
.. _Python 3.X: https://docs.python.org/3/
.. _requirements.txt: requirements.txt
.. _contributing documentation: docs/CONTRIBUTING.md
.. _@5hirish: https://github.com/5hirish

.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/5924d3402a2c43d0bf7affa6863872f6
   :target: https://www.codacy.com/app/5hirish/tweet_scrapper?utm_source=github.com&utm_medium=referral&utm_content=5hirish/tweet_scrapper&utm_campaign=Badge_Grade
.. |codecov| image:: https://codecov.io/gh/5hirish/tweet_scrapper/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/5hirish/tweet_scrapper
.. |Build Status| image:: https://travis-ci.org/5hirish/tweet_scrapper.svg?branch=master
   :target: https://travis-ci.org/5hirish/tweet_scrapper
.. |Current Release Version| image:: https://img.shields.io/github/release/5hirish/tweet_scrapper.svg
    :target: https://github.com/5hirish/tweet_scrapper/releases
.. |pypi Version| image:: https://img.shields.io/pypi/v/tweetscrape.svg
    :target: https://pypi.python.org/pypi/tweetscrape
.. |Twitter| image:: https://img.shields.io/twitter/follow/openebs.svg?style=social&label=Follow
   :target: https://twitter.com/intent/follow?screen_name=5hirish