#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging

from tweetscrape import __version__
from tweetscrape.profile_tweets import TweetScrapperProfile
from tweetscrape.search_tweets import TweetScrapperSearch

__author__ = "Shirish Kadam"
__copyright__ = "Copyright (C) 2018  Shirish Kadam"
__license__ = "GNU General Public License v3 (GPLv3)"

_logger = logging.getLogger(__name__)
    

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Effortlessly scrape tweets from twitter...")
    parser.add_argument(
        '--version',
        action='version',
        version='Tweet Scrapper v{ver}'.format(ver=__version__))
    parser.add_argument(
        '-u',
        dest="username",
        help="Username of the twitter profile eg. @5hirish",
        type=str,
        metavar="")
    parser.add_argument(
        '-s',
        dest="search_term",
        help="Search term or titter hashtag eg. #Python",
        type=str,
        metavar="")
    parser.add_argument(
        '-p',
        dest="pages",
        help="Number of pages to fetch, maximum is 25",
        type=int,
        metavar="")    
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="Sets loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="Sets loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Scrapping tweets for {0}".format(args.username))
    if args.username is not None and args.username.startswith("@"):
        if args.pages is not None:
            ts = TweetScrapperProfile(args.username, args.pages)
        else:
            ts = TweetScrapperProfile(args.username)
        tweets = ts.get_profile_tweets(False)
        for tweet in tweets:
            print(str(tweet))
        return tweets

    elif args.search_term is not None:
        if args.pages is not None:
            ts = TweetScrapperSearch(args.search_term, args.pages)
        else:
            ts = TweetScrapperSearch(args.search_term)
        tweets = ts.get_search_tweets(False)
        for tweet in tweets:
            print(str(tweet))
        return tweets

    else:
        raise ValueError("No matching argument. Provide a twitter username eg. -u @5hirish or"
                         " a twitter hashtag eg. -s #Python or any search term.")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
