from lxml import etree
from pprint import pprint
import logging
import sys
import re
import os
import requests

from tweetscrape.model.tweet_model import TweetInfo

"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath
The '.' at the beginning means, that the current processing starts at the current node. 
Your xpath starts with a slash '/' and is therefore absolute.
The '*' selects all element nodes descending from this current node with the @id-attribute-value or @class value'.
The '//' identifies any descendant designation element of element 
"""

logger = logging.getLogger(__name__)

class TweetScrapper:

    username = "5hirish"
    pages = 0
    tweets_data_list = []

    __twitter_profile_url__ = 'https://twitter.com/i/profiles/show/{username}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'.format(username=username)
    __twitter_profile_header__ = {
        'accept':'application/json, text/javascript, */*; q=0.01',
        'accept-language':'en-US,en;q=0.8',
        'referer':'https://twitter.com/{username}'.format(username=username),
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
        'x-twitter-active-user':'yes',
        'x-twitter-polling':'true',
    }
    __twitter_profile_params__ = None

    _tweets_pattern_ = '''/html/body/li[contains(@class,"stream-item")]'''        

    _tweet_content_pattern_ = '''./div[@class="content"]'''
    _tweet_time_ms_pattern_ = '''./div[@class="stream-item-header"]/small[@class="time"]/a[contains(@class,"tweet-timestamp")]/span'''
    _tweet_text_pattern_ = '''./div[@class="js-tweet-text-container"]//text()'''
    _tweet_links_list_pattern_ = '''./div[@class="js-tweet-text-container"]//a'''
                
    _tweet_reply_count_pattern_ = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--reply")]/span'''
    _tweet_like_count_pattern_ = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--favorite")]/span'''
    _tweet_retweet_count_pattern_ = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--retweet")]/span'''

    _tweet_hastag_pattern_ = r'''/hashtag/([0-9a-zA-Z_]*)\?src=hash'''

    def __init__(self, username, pages=2):
        self.username = username
        if pages > 25:
            self.pages = 25
        else:
            self.pages = pages

    def get_user_tweets(self, save_json=False):

        hastag_capture = re.compile(self._tweet_hastag_pattern_)        

        while self.pages > 0:

            if self.__twitter_profile_params__ is not None:
                response = requests.get(self.__twitter_profile_url__, headers=self.__twitter_profile_header__, params=self.__twitter_profile_params__)
            else:
                response = requests.get(self.__twitter_profile_url__, headers=self.__twitter_profile_header__)
                
            logger.debug("Page {0} request: {1}".format(self.pages, response.status_code))

            tweet_json = response.json()

            try: 
                if tweet_json['has_more_items']:
                    num_new_tweets = tweet_json['new_latent_count']
                
                tweets_html = tweet_json['items_html']

                if save_json:
                    save_output('/output.json', str(tweet_json))
                    save_output('/output.html', tweets_html)

                parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)        
                html_tree = etree.fromstring(tweets_html, parser)

                tweet_list = html_tree.xpath(self._tweets_pattern_)

                self.extract_tweets_data(tweet_list, hastag_capture)

                logger.debug("Extracting {0} tweets of {1} page...".format(len(tweet_list), self.pages))

                
            except KeyError:
                raise ValueError("Oops! Either {0} does not exist or is private.".format(self.username))
            
            self.pages += -1
            last_tweet_id = self.tweets_data_list[len(self.tweets_data_list) - 1].get_tweet_id()
            self.__twitter_profile_params__ = {'max_position': last_tweet_id}

        logger.info("Total {0} tweets extracted.".format(len(self.tweets_data_list)))   
        return self.tweets_data_list     


    def extract_tweets_data(self, tweet_list, hastag_capture):
        if tweet_list is not None:
            for tweet in tweet_list:
                item_id = tweet.attrib['data-item-id']
                item_type = tweet.attrib['data-item-type']
                tweet_data = TweetInfo(item_id, item_type)
                    
                if len(tweet.getchildren()) > 0:
                    tweet_meta = tweet.getchildren()[0]
                    tweet_id = tweet_meta.attrib['data-tweet-id']
                    tweet_author = tweet_meta.attrib['data-screen-name']
                    tweet_author_id = tweet_meta.attrib['data-user-id']
                    tweet_data.set_tweet_author(tweet_author, tweet_author_id)
                    
                    tweet_content = tweet_meta.xpath(self._tweet_content_pattern_)
                    if len(tweet_content) > 0:
                        tweet_time_ms = tweet_content[0].xpath(self._tweet_time_ms_pattern_)[0].attrib['data-time-ms']
                        tweet_data.set_tweet_time_ms(tweet_time_ms)    

                        tweet_text = tweet_content[0].xpath(self._tweet_text_pattern_)
                        tweet_text = ''.join(tweet_text).replace('\n','')
                        tweet_data.set_tweet_text(tweet_text)

                        tweet_links_raw = tweet_content[0].xpath(self._tweet_links_list_pattern_)
                        
                        for raw_link in tweet_links_raw:
                            raw_url = raw_link.attrib['href']
                            if raw_url.startswith('https://'):
                                tweet_data.set_tweet_links(raw_url)
                            elif raw_url.startswith('/hashtag/'):
                                hash_tag_group = re.match(hastag_capture, raw_url)
                                hash_tag = "#"+hash_tag_group.group(1)
                                tweet_data.set_tweet_hashtags(hash_tag)
                            else:
                                mention = raw_url.replace('/','@')
                                tweet_data.set_tweet_mentions(mention)

                        tweet_replies = tweet_content[0].xpath(self._tweet_reply_count_pattern_)
                        tweet_replies_count = tweet_replies[0].attrib['data-tweet-stat-count']
                        tweet_likes = tweet_content[0].xpath(self._tweet_like_count_pattern_)
                        tweet_likes_count = tweet_likes[0].attrib['data-tweet-stat-count']
                        tweet_retweets = tweet_content[0].xpath(self._tweet_retweet_count_pattern_)
                        tweet_retweets_count = tweet_retweets[0].attrib['data-tweet-stat-count']

                        tweet_data.set_tweet_interactions(tweet_replies_count, tweet_likes_count, tweet_retweets_count)

                        self.tweets_data_list.append(tweet_data)
                        
        
def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path+filename, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ts = TweetScrapper("5hirish", 2)
    l_extracted_tweets = ts.get_user_tweets(True)
    for l_tweet in l_extracted_tweets:
        print(str(l_tweet))

