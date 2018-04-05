import logging
from urllib import parse

from tweetscrape.tweets_scrape import TweetScrapper

logger = logging.getLogger(__name__)


class TweetScrapperSearch(TweetScrapper):

    search_term = None
    search_type = None
    pages = None

    __twitter_search_url__ = None
    __twitter_search_header__ = None
    __twitter_search_params__ = None

    def __init__(self, search_term, pages=2):
        self.search_term = parse.quote(search_term)

        if search_term.startswith("#"):
            self.search_type = "hash"
        else:
            self.search_type = "typd"

        if pages > 25:
            self.pages = 25
        else:
            self.pages = pages

        self.__twitter_search_url__ = 'https://twitter.com/i/search/timeline' \
                                 '?vertical=default&q={search_term}&src={search_type}' \
                                 '&include_available_features=1&include_entities=1' \
            .format(search_term=self.search_term, search_type=self.search_type)

        self.__twitter_search_header__ = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.8',
            'referer': 'https://twitter.com/search?q={search_term}&src={search_type}'
                .format(search_term=self.search_term, search_type=self.search_type),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/60.0.3112.78 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-twitter-active-user': 'yes'
        }

        super().__init__(twitter_request_url=self.__twitter_search_url__,
                         twitter_request_header=self.__twitter_search_header__)

    def get_search_tweets(self, save_output=False):
        output_file_name = '/' + self.search_term + '_search'
        return self.execute_twitter_request(search_term=self.search_term, pages=self.pages,
                                            log_output=save_output, output_file=output_file_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # ts = TweetScrapperSearch("avengers infinity war", "typd")
    ts = TweetScrapperSearch("#FakeNews", 3)
    l_extracted_tweets = ts.get_search_tweets(True)
    for l_tweet in l_extracted_tweets:
        print(str(l_tweet))
