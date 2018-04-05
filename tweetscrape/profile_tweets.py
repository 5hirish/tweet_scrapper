import re
import os
import logging
import requests
from lxml import etree

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

    def __init__(self, username, pages=2):
        super().__init__()

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

    def get_profile_tweets(self, save_json=False):

        hastag_capture = re.compile(self._tweet_hastag_pattern_)
        total_pages = self.pages

        while self.pages > 0:

            if self.__twitter_profile_params__ is not None:
                response = requests.get(self.__twitter_profile_url__,
                                        headers=self.__twitter_profile_header__,
                                        params=self.__twitter_profile_params__)
            else:
                response = requests.get(self.__twitter_profile_url__, headers=self.__twitter_profile_header__)
                
            logger.debug("Page {0} request: {1}".format(self.pages, response.status_code))

            tweet_json = response.json()

            try: 
                if tweet_json['has_more_items']:
                    num_new_tweets = tweet_json['new_latent_count']
                
                tweets_html = tweet_json['items_html']

                if save_json:
                    save_output('/'+self.username+'_profile.json', str(tweet_json))
                    save_output('/'+self.username+'_profile.html', tweets_html)

                parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)        
                html_tree = etree.fromstring(tweets_html, parser)

                tweet_list = html_tree.xpath(self._tweets_pattern_)

                self.extract_tweets_data(tweet_list, hastag_capture)

                logger.debug("Extracting {0} tweets of {1} page...".format(len(tweet_list), total_pages - self.pages + 1))

            except KeyError:
                raise ValueError("Oops! Either {0} does not exist or is private.".format(self.username))
            
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
    ts = TweetScrapperProfile("BarackObama", 2)
    l_extracted_tweets = ts.get_profile_tweets(True)
    for l_tweet in l_extracted_tweets:
        print(str(l_tweet))

