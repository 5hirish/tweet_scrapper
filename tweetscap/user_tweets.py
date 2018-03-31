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
        hastag_capture = re.compile(r'/hashtag/([0-9a-zA-Z_]*)\?src=hash')

        tweets_pattern = '''/html/body/li[contains(@class,"stream-item")]'''        

        tweet_content_pattern = '''./div[@class="content"]'''
        tweet_time_ms_pattern = '''./div[@class="stream-item-header"]/small[@class="time"]/a[contains(@class,"tweet-timestamp")]/span'''
        tweet_text_pattern = '''./div[@class="js-tweet-text-container"]//text()'''
        tweet_links_list_pattern = '''./div[@class="js-tweet-text-container"]//a'''
        
        tweet_reply_count_pattern = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--reply")]/span'''
        tweet_like_count_pattern = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--favorite")]/span'''
        tweet_retweet_count_pattern = '''./div[@class="stream-item-footer"]/div/span[contains(@class, "ProfileTweet-action--retweet")]/span'''

        tweet_list = html_tree.xpath(tweets_pattern)

        for tweet in tweet_list:
            item_id = tweet.attrib['data-item-id']
            item_type = tweet.attrib['data-item-type']
            
            if len(tweet.getchildren()) > 0:
                tweet_data = tweet.getchildren()[0]
                tweet_id = tweet_data.attrib['data-tweet-id']
                tweet_author = tweet_data.attrib['data-screen-name']
                tweet_author_id = tweet_data.attrib['data-user-id']
            
                tweet_content = tweet_data.xpath(tweet_content_pattern)
                tweet_time_span = tweet_content[0].xpath(tweet_time_ms_pattern)[0].attrib['data-time-ms']       # @data-time-ms     

                logger.debug("{0}:{1}:{2}-{3}:{4}-{5}".format(item_id, item_type, tweet_id, tweet_author, tweet_author_id, tweet_time_span))

                tweet_text = tweet_content[0].xpath(tweet_text_pattern)
                tweet_text = ''.join(tweet_text).replace('\n','')
                tweet_links_raw = tweet_content[0].xpath(tweet_links_list_pattern)
                tweet_links_ext = []
                tweet_hashtags = []
                tweet_mentions = []
                for raw_link in tweet_links_raw:
                    raw_url = raw_link.attrib['href']
                    if raw_url.startswith('https://'):
                        tweet_links_ext.append(raw_url)
                    elif raw_url.startswith('/hashtag/'):
                        hash_tag_group = re.match(hastag_capture, raw_url)
                        hash_tag = "#"+hash_tag_group.group(1)
                        tweet_hashtags.append(hash_tag)
                    else:
                        raw_url = raw_url.replace('/','@')
                        tweet_mentions.append(raw_url)

                logger.debug("{0}:\t{1}:{2}:{3}".format(tweet_text, tweet_links_ext, tweet_hashtags, tweet_mentions))

                tweet_replies = tweet_content[0].xpath(tweet_reply_count_pattern)
                tweet_replies_count = tweet_replies[0].attrib['data-tweet-stat-count']
                tweet_likes = tweet_content[0].xpath(tweet_like_count_pattern)
                tweet_likes_count = tweet_likes[0].attrib['data-tweet-stat-count']
                tweet_retweets = tweet_content[0].xpath(tweet_retweet_count_pattern)
                tweet_retweets_count = tweet_retweets[0].attrib['data-tweet-stat-count']

                logger.debug("Replies={0}:Retweets={1}:Likes={2}".format(tweet_replies_count, tweet_retweets_count, tweet_likes_count))


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