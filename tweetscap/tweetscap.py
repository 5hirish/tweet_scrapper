#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging

from tweetscap import __version__
from tweetscap.user_tweets import fetch_user_tweets

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
        help="Username of the twitter profile eg.@5hirish",
        type=str,
        metavar="@5hirish")
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
    _logger.debug("Scrapping tweets for {0}".format(user))
    fetch_user_tweets(args.username)
    # _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()