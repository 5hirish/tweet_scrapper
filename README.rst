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
    `kennethreitz/twitter-scraper`_ which is limited to python 3.6 an
    above.

Getting Started
---------------

.. code:: bash

    $ git clone https://github.com/5hirish/tweet_scrapper.git
    $ cd tweet_scrapper
    $ pip install -r requirements.txt
    $ python -m tweetscrape.twitter_scrape -u "@5hirish" -p 3

Usage
-----

.. code:: python

    from tweetscrape.user_tweets import TweetScrapper 

    tweet_scrapper = TweetScrapper("@5hirish", 1)
    tweets = tweet_scrapper.get_user_tweets()
    for tweet in tweets:
        print(str(tweet))

Read more on ``tweetscrape`` usage `here`_.

::

    Id:973027095411437568   Type:tweet  Time:1520822712000
    Author:Reza_Zadeh   AuthorId:92839676
    Text:  There's a lot of computational power that goes into mining bitcoin, in particular to find little bits of data with certain SHA256 hashes. Instead, would've been great if that compute power were used to solve challenging NP-hard problems. Human progress becomes side-effect of hype
    Links:[]
    Hastags:[]
    Mentions:[]
    Replies:12  Favorites:187   Retweets:51

    Id:972778151796510721   Type:tweet  Time:1520763359000
    Author:gensim_py    AuthorId:3110758625
    Text:   Calling all #Gensim users! Please help improve Gensim by giving us your feedback in this short survey.https://radimrehurek.com/gensim/survey.html …
    Links:['https://t.co/sJsDTXv6QF']
    Hastags:['#Gensim']
    Mentions:[]
    Replies:8   Favorites:57    Retweets:46

    Id:953706491881680896   Type:tweet  Time:1516216321000
    Author:QCon AuthorId:14100646
    Text:  “ML for Question and Answer Understanding @Quora” #machinelearning @nikhilbd presentation is now live on @infoqhttp://bit.ly/2Da8WuX 
    Links:['https://t.co/buseQxF9mS']
    Hastags:['#machinelearning']
    Mentions:['@Quora', '@nikhilbd', '@InfoQ']
    Replies:0   Favorites:15    Retweets:5

    Id:970542118350462976   Type:tweet  Time:1520230247000
    Author:GabbbarSingh AuthorId:108391251
    Text:  Gary Oldman, playing Winston Churchill, wins the best actor for Darkest hour. Nothing wrong with awarding the craft of acting even though you play a murderer, but showing the cold blooded tyrant Churchill, in a positive light, deserves condemnation from Indians. #FuckChurchill
    Links:[]
    Hastags:['#FuckChurchill']
    Mentions:[]
    Replies:30  Favorites:581   Retweets:253

    Id:970008694783176704   Type:tweet  Time:1520103069000
    Author:maxmunnecke  AuthorId:201907594
    Text:  New Jupyter notebook on topic modelling with SpaCy, Gensim and Textacy. Combining 'Termite Plot' and 'pyLDAvis' visualizations makes sense when evaluating topic models. Try out the notebook: https://nbviewer.jupyter.org/github/repmax/topic-model/blob/master/topic-modelling.ipynb … #dataviz #nlp #digitalhumanities @gensim_py @stanfordnlp @uwdatapic.twitter.com/ngyGZopw7g
    Links:['https://t.co/0o0FEOAl20', 'https://t.co/ngyGZopw7g']
    Hastags:['#dataviz', '#nlp', '#digitalhumanities']
    Mentions:['@gensim_py', '@stanfordnlp', '@uwdata']
    Replies:0   Favorites:170   Retweets:61

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