from lxml import etree
from pprint import pprint
import logging
import sys
import re
import os
import requests

"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath
The '.' at the beginning means, that the current processing starts at the current node. 
Your xpath starts with a slash '/' and is therefore absolute.
The '*' selects all element nodes descending from this current node with the @id-attribute-value or @class value'.
The '//' identifies any descendant designation element of element 
"""

logger = logging.getLogger(__name__)

def get_tweet(save_json=False):

    twitter_profile_url = 'https://twitter.com/i/profiles/show/5hirish/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'
    twitter_profile_header = {
        'accept':'application/json, text/javascript, */*; q=0.01',
        'accept-language':'en-US,en;q=0.8',
        'referer':'https://twitter.com/5hirish',
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
        'x-twitter-active-user':'yes',
        'x-twitter-polling':'true',
    }

    response = requests.get(twitter_profile_url, headers=twitter_profile_header)
    logger.debug(response.status_code)

    tweet_json = response.json()

    """//*[@id="stream-item-tweet-881842062265647105"]"""

    try: 
        if tweet_json['has_more_items']:
            num_new_tweets = tweet_json['new_latent_count']
        
        tweets_html = tweet_json['items_html']

        if save_json:
            save_output('/output.json', str(tweet_json))
            save_output('/output.html', tweets_html)

        #parser = etree.XMLParser(ns_clean=True, remove_comments=True, attribute_defaults=True)
        parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)        
        html_tree = etree.fromstring(tweets_html, parser)

        tweets_pattern = '''/html/body/li[contains(@class,"stream-item")]'''
        tweet_list = html_tree.xpath(tweets_pattern)

        for tweet in tweet_list:
            print(tweet)


    except KeyError:
        raise ValueError("Oops! Either user does not exist or is private.")


        
def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path+filename, 'w') as fp:
            fp.write(data)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    get_tweet(True)