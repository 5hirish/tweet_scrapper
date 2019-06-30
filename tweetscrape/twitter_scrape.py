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
        '--all',
        dest="search_all",
        help="Search all of these words",
        type=str,
        metavar="")
    parser.add_argument(
        '--exact',
        dest="search_exact",
        help="Search this exact phrase",
        type=str,
        metavar="")
    parser.add_argument(
        '--any',
        dest="search_any",
        help="Search any of these words",
        type=str,
        metavar="")
    parser.add_argument(
        '--exclude',
        dest="search_excludes",
        help="Search excluding these words",
        type=str,
        metavar="")
    parser.add_argument(
        '--hashtag',
        dest="search_hashtags",
        help="Search these hashtags",
        type=str,
        metavar="")
    parser.add_argument(
        '--from',
        dest="search_from_accounts",
        help="Search tweets from these accounts",
        type=str,
        metavar="")
    parser.add_argument(
        '--to',
        dest="search_to_accounts",
        help="Search tweets to these accounts",
        type=str,
        metavar="")
    parser.add_argument(
        '--mention',
        dest="search_mentions",
        help="Search tweets mentioning these accounts",
        type=str,
        metavar="")
    parser.add_argument(
        '--near',
        dest="search_near_place",
        help="Search tweets near this place",
        type=str,
        metavar="")
    parser.add_argument(
        '--until',
        dest="search_till_date",
        help="Search tweets until this date: YYYY-MM-DD",
        type=str,
        metavar="")
    parser.add_argument(
        '--since',
        dest="search_since_date",
        help="Search tweets since this date: YYYY-MM-DD",
        type=str,
        metavar="")
    parser.add_argument(
        '-n',
        dest="num_tweets",
        help="Number of tweets to fetch",
        type=int,
        metavar="")
    parser.add_argument(
        '-l',
        dest="language",
        help="Search tweets in language from language codes",
        type=int,
        metavar="")
    parser.add_argument(
        '-d',
        dest="tweet_dump_path",
        help="Path of the file to export to",
        type=str,
        metavar="")
    parser.add_argument(
        '-f',
        dest="tweet_dump_format",
        help="File format to export to: json or csv",
        type=str,
        metavar="")
    parser.add_argument(
        '--proxy',
        dest="request_proxies",
        help="The proxies used for scraping. Use serialized dictionary.",
        type=str,
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
    _logger.info("Scrapping tweets")

    if args.username is not None:

        ts = TweetScrapperProfile(username=args.username, num_tweets=args.pages,
                                  tweet_dump_path=args.tweet_dump_path, tweet_dump_format=args.tweet_dump_format,
                                  request_proxies=args.request_proxies)

        l_tweet_count, l_tweet_id, l_tweet_time, l_dump_path = ts.get_profile_tweets()
        print("Extracted {0} tweets till {1} at {2}".format(l_tweet_count, l_tweet_time, l_dump_path))
        return "Extracted {0} tweets till {1} at {2}".format(l_tweet_count, l_tweet_time, l_dump_path)

    else:

        ts = TweetScrapperSearch(search_all=args.search_all, search_exact=args.search_exact, search_any=args.search_any,
                                 search_excludes=args.search_excludes, search_hashtags=args.search_hashtags,
                                 search_from_accounts=args.search_from_accounts,
                                 search_to_accounts=args.search_to_accounts, search_mentions=args.search_mentions,
                                 search_near_place=args.search_near_place,
                                 search_till_date=args.search_till_date, search_since_date=args.search_since_date,
                                 num_tweets=args.pages, language=args.language,
                                 tweet_dump_path=args.tweet_dump_path, tweet_dump_format=args.tweet_dump_format,
                                 request_proxies=args.request_proxies)

        l_tweet_count, l_tweet_id, l_tweet_time, l_dump_path = ts.get_search_tweets()
        print("Extracted {0} tweets till {1} at {2}".format(l_tweet_count, l_tweet_time, l_dump_path))
        return "Extracted {0} tweets till {1} at {2}".format(l_tweet_count, l_tweet_time, l_dump_path)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
