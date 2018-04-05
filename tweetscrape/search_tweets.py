import re
import os
import logging
import requests
from lxml import etree
from urllib import parse

from tweetscrape.tweets_scrape import TweetScrapper

logger = logging.getLogger(__name__)


class TweetScrapperSearch(TweetScrapper):

    search_term = None
    search_type = None
    pages = None

    __twitter_search_url__ = None
    __twitter_profile_header__ = None
    __twitter_profile_params__ = None

    def __init__(self, search_term, search_type, pages=2):
        super().__init__()

        self.search_term = parse.quote(search_term)
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

    def get_search_tweets(self, save_json=False):

        hastag_capture = re.compile(self._tweet_hastag_pattern_)
        total_pages = self.pages

        while self.pages > 0:

            if self.__twitter_profile_params__ is not None:
                response = requests.get(self.__twitter_search_url__,
                                        headers=self.__twitter_profile_header__,
                                        params=self.__twitter_profile_params__)
            else:
                response = requests.get(self.__twitter_search_url__, headers=self.__twitter_profile_header__)

            logger.debug("Page {0} request: {1}".format(self.pages, response.status_code))

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

                tweet_list = html_tree.xpath(self._tweets_pattern_)

                self.extract_tweets_data(tweet_list, hastag_capture)

                logger.debug("Extracting {0} tweets of {1} page...".format(len(tweet_list), total_pages - self.pages + 1))

            except KeyError:
                raise ValueError("Oops! Something went wrong when searching {0}.".format(self.search_term))

            self.pages += -1
            last_tweet_id = self.tweets_data_list[len(self.tweets_data_list) - 1].get_tweet_id()
            self.__twitter_profile_params__ = {'max_position': last_tweet_id}

        logger.info("Total {0} tweets extracted.".format(len(self.tweets_data_list)))
        return self.tweets_data_list


def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path+filename, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # ts = TweetScrapperSearch("avengers infinity war", "typd")
    ts = TweetScrapperSearch("#FakeNews", "hash", 3)
    l_extracted_tweets = ts.get_search_tweets(True)
    for l_tweet in l_extracted_tweets:
        print(str(l_tweet))
