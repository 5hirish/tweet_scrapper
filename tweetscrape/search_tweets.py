import re
import os
import logging
import requests
from lxml import etree

from tweetscrape.model.tweet_model import TweetInfo

logger = logging.getLogger(__name__)


class TweetScrapperSearch:

    search_term = None
    search_type = None
    pages = None

    __twitter_search_url__ = None
    ____twitter_profile_header__ = None

    def __init__(self, search_term, search_type, pages=2):
        self.search_term = search_term
        self.search_type = search_type
        self.pages = pages

        self.__twitter_search_url__ = 'https://twitter.com/i/search/timeline' \
                                 '?vertical=default&q={search_term}&src={search_type}' \
                                 '&include_available_features=1&include_entities=1' \
            .format(search_term=self.search_term, search_type=self.search_type)

        self.__twitter_profile_header__ = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.8',
            'referer': 'https://twitter.com/search?q={search_term}&src={search_type}'
                .format(search_term=self.search_term, search_type=self.search_type),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/60.0.3112.78 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-twitter-active-user': 'yes'
        }

    def get_result_tweets(self, save_json=False):

        response = requests.get(self.__twitter_search_url__,
                                headers=self.__twitter_profile_header__)

        logger.debug("Page {0} request: {1}".format(response.status_code, self.pages))

        tweet_json = response.json()

        try:
            if tweet_json['has_more_items']:
                num_new_tweets = tweet_json['new_latent_count']

            tweets_html = tweet_json['items_html']

            if save_json:
                save_output('/' + self.search_term + '_search.json', str(tweet_json))
                save_output('/' + self.search_term + '_search.html', tweets_html)

            parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
            html_tree = etree.fromstring(tweets_html, parser)

            # tweet_list = html_tree.xpath(self._tweets_pattern_)

            # self.extract_tweets_data(tweet_list, hastag_capture)

            # logger.debug("Extracting {0} tweets of {1} page...".format(len(tweet_list), self.pages))

        except KeyError:
            raise ValueError("Oops! Either {0} does not exist or is private.".format(self.username))


def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path+filename, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    ts = TweetScrapperSearch("avengers", "typd")
    ts.get_result_tweets(True)