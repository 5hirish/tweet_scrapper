import logging

from tweetscrape.tweets_scrape import TweetScrapper
"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath
The '.' at the beginning means, that the current processing starts at the current node.
Your xpath starts with a slash '/' and is therefore absolute.
The '*' selects all element nodes descending from this current node with the @id-attribute-value or @class value'.
The '//' identifies any descendant designation element of element
"""

logger = logging.getLogger(__name__)


class TweetScrapperProfile(TweetScrapper):

    username = "5hirish"
    pages = 0

    __twitter_profile_url__ = None
    __twitter_profile_header__ = None
    __twitter_profile_params__ = None

    def __init__(self, username, pages=2, last_tweet_id=None):

        self.username = username
        if pages > 25:
            self.pages = 25
        else:
            self.pages = pages

        self.__twitter_profile_url__ = 'https://twitter.com/i/profiles/show/{username}/timeline/tweets' \
                                  '?include_available_features=1&include_entities=1&include_new_items_bar=true' \
            .format(username=self.username)

        self.__twitter_profile_header__ = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.8',
            'referer': 'https://twitter.com/{username}'.format(username=self.username),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/60.0.3112.78 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-twitter-active-user': 'yes',
            'x-twitter-polling': 'true',
        }

        if last_tweet_id is not None:
            self.__twitter_profile_params__ = {'max_position': last_tweet_id}
            super().__init__(twitter_request_url=self.__twitter_profile_url__,
                             twitter_request_header=self.__twitter_profile_header__,
                             twitter_request_params=self.__twitter_profile_params__)
        else:
            super().__init__(twitter_request_url=self.__twitter_profile_url__,
                             twitter_request_header=self.__twitter_profile_header__)

    def get_profile_tweets(self, save_output=False):
        output_file_name = '/'+self.username+'_profile'
        return self.execute_twitter_request(username=self.username, pages=self.pages,
                                     log_output=save_output, output_file=output_file_name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ts = TweetScrapperProfile("BarackObama", 2)
    l_extracted_tweets = ts.get_profile_tweets(True)
    for l_tweet in l_extracted_tweets:
        print(str(l_tweet))

