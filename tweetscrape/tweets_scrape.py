import re
import os
import requests
import logging
import csv
import json
from lxml import etree
from urllib import parse

from tweetscrape.model.tweet_model import TweetInfo

logger = logging.getLogger(__name__)


class TweetScrapper:

    __twitter_request_url__ = None
    __twitter_request_header__ = None
    __twitter_request_params__ = None

    _tweets_pattern_ = '''/html/body/li[contains(@class,"stream-item")]'''

    _tweet_content_pattern_ = '''./div[@class="content"]'''
    _tweet_time_ms_pattern_ = '''./div[@class="stream-item-header"]/
                                        small[@class="time"]/a[contains(@class,"tweet-timestamp")]/span'''
    _tweet_text_pattern_ = '''./div[@class="js-tweet-text-container"]//text()'''
    _tweet_links_list_pattern_ = '''./div[@class="js-tweet-text-container"]//a'''

    _tweet_reply_count_pattern_ = '''./div[@class="stream-item-footer"]/div/
                                            span[contains(@class, "ProfileTweet-action--reply")]/span'''
    _tweet_like_count_pattern_ = '''./div[@class="stream-item-footer"]/div/
                                            span[contains(@class, "ProfileTweet-action--favorite")]/span'''
    _tweet_retweet_count_pattern_ = '''./div[@class="stream-item-footer"]/div/
                                            span[contains(@class, "ProfileTweet-action--retweet")]/span'''

    _tweet_hastag_pattern_ = r'''/hashtag/([0-9a-zA-Z_]*)\?src=hash'''

    def __init__(self, twitter_request_url, twitter_request_header, twitter_request_params=None,
                 twitter_file_path=None, twitter_file_format='json'):

        self.__twitter_request_url__ = twitter_request_url
        self.__twitter_request_header__ = twitter_request_header
        self.__twitter_request_params__ = twitter_request_params
        self.__twitter_tweet_persist_file_path__ = twitter_file_path
        self.__twitter_tweet_persist_file_format__ = twitter_file_format

    def execute_twitter_request(self, username=None, search_term=None, pages=2, log_output=False, output_file=None):
        hastag_capture = re.compile(self._tweet_hastag_pattern_)
        total_pages = pages
        tweet_count = 0
        last_tweet_id = ''

        while pages > 0:
            current_tweet_count = 0

            twitter_request_params_encoded = parse.urlencode(self.__twitter_request_params__, quote_via=parse.quote)

            response = requests.get(self.__twitter_request_url__,
                                    headers=self.__twitter_request_header__,
                                    params=twitter_request_params_encoded)

            logger.debug("Page {0} request: {1}".format(pages, response.status_code))

            tweet_json = response.json()

            try:
                if tweet_json.get('has_more_items'):
                    num_new_tweets = tweet_json.get('new_latent_count')
                else:
                    logger.info("No more items...!!!")

                tweets_html = tweet_json.get('items_html')

                if log_output:
                    # save_output(output_file + '.json', str(tweet_json))
                    save_output(output_file + '.html', tweets_html)

                parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
                html_tree = etree.fromstring(tweets_html, parser)

                if html_tree is not None:
                    tweet_list = html_tree.xpath(self._tweets_pattern_)

                    tweets_generator = self.extract_tweets_data(tweet_list, hastag_capture)
                    last_tweet_id, current_tweet_count = self.persist_tweets(tweets_generator)
                    tweet_count += current_tweet_count

                    logger.debug(
                        "Extracting {0} tweets of {1} page...".format(len(tweet_list), total_pages - pages + 1))

            except KeyError:
                if search_term is not None:
                    raise ValueError("Oops! Something went wrong while searching {0}.".format(search_term))
                elif username is not None:
                    raise ValueError("Oops! Either {0} does not exist or is private.".format(username))
                else:
                    raise ValueError("Received no arguments")

            pages += -1
            if current_tweet_count > 0:
                # self.__twitter_request_params__['min_position'] = last_tweet_id
                self.__twitter_request_params__['max_position'] = last_tweet_id
            else:
                logger.info("End of tweet stream...")
                return tweet_count, self.__twitter_tweet_persist_file_path__

        logger.info("Total {0} tweets extracted.".format(tweet_count))
        return tweet_count, self.__twitter_tweet_persist_file_path__

    def extract_tweets_data(self, tweet_list, hastag_capture):
        if tweet_list is not None:
            for tweet in tweet_list:
                if 'data-item-type' in tweet.attrib and tweet.attrib.get('data-item-type') == "tweet":
                    item_id = tweet.attrib.get('data-item-id')
                    item_type = tweet.attrib.get('data-item-type')
                    tweet_data = TweetInfo(item_id, item_type)

                    if len(tweet.getchildren()) > 0:
                        tweet_meta = tweet.getchildren()[0]
                        tweet_id = tweet_meta.attrib.get('data-tweet-id')
                        tweet_author = tweet_meta.attrib.get('data-screen-name')
                        tweet_author_name = tweet_meta.attrib.get('data-name')
                        tweet_author_id = tweet_meta.attrib.get('data-user-id')
                        if "data-conversation-id" in tweet_meta.attrib:
                            tweet_has_parent = tweet_meta.attrib.get('data-has-parent-tweet', False)
                            tweet_conversation_id = tweet_meta.attrib.get('data-conversation-id', None)
                            tweet_data.set_tweet_conversation(tweet_conversation_id, tweet_has_parent)
                        if "data-retweet-id" in tweet_meta.attrib:
                            tweet_retweeter = tweet_meta.attrib.get('data-retweeter')
                            tweet_data.set_retweeter(tweet_retweeter)
                        tweet_data.set_tweet_author(tweet_author, tweet_author_name, tweet_author_id)

                        tweet_content = tweet_meta.xpath(self._tweet_content_pattern_)
                        if len(tweet_content) > 0:
                            tweet_time_ms = tweet_content[0].xpath(self._tweet_time_ms_pattern_)[0]\
                                .attrib.get('data-time-ms')
                            tweet_data.set_tweet_time_ms(tweet_time_ms)

                            tweet_text = tweet_content[0].xpath(self._tweet_text_pattern_)
                            tweet_text = ''.join(tweet_text).replace('\n', '')
                            tweet_text = tweet_text.strip()
                            tweet_data.set_tweet_text(tweet_text)

                            tweet_links_raw = tweet_content[0].xpath(self._tweet_links_list_pattern_)

                            for raw_link in tweet_links_raw:
                                raw_url = raw_link.attrib.get('href')
                                if raw_url.startswith('https://'):
                                    tweet_data.set_tweet_links(raw_url)
                                elif raw_url.startswith('/hashtag/'):
                                    hash_tag_group = re.match(hastag_capture, raw_url)
                                    if hash_tag_group is not None and hash_tag_group.group(1) is not None:
                                        hash_tag = "#" + hash_tag_group.group(1)
                                        tweet_data.set_tweet_hashtags(hash_tag)
                                else:
                                    mention = raw_url.replace('/', '@')
                                    tweet_data.set_tweet_mentions(mention)

                            tweet_replies = tweet_content[0].xpath(self._tweet_reply_count_pattern_)
                            tweet_replies_count = tweet_replies[0].attrib.get('data-tweet-stat-count')
                            tweet_likes = tweet_content[0].xpath(self._tweet_like_count_pattern_)
                            tweet_likes_count = tweet_likes[0].attrib.get('data-tweet-stat-count')
                            tweet_retweets = tweet_content[0].xpath(self._tweet_retweet_count_pattern_)
                            tweet_retweets_count = tweet_retweets[0].attrib.get('data-tweet-stat-count')

                            tweet_data.set_tweet_interactions(tweet_replies_count, tweet_likes_count,
                                                              tweet_retweets_count)

                            yield tweet_data

    def persist_tweets(self, tweets_generator, dump_mode='a'):
        if self.__twitter_tweet_persist_file_path__ is None or self.__twitter_tweet_persist_file_path__ == "":
            self.__twitter_tweet_persist_file_format__ = 'json'
            self.__twitter_tweet_persist_file_path__ = os.getcwd() + 'tweets_dump.' + \
                                                       self.__twitter_tweet_persist_file_format__

        with open(self.__twitter_tweet_persist_file_path__, dump_mode) as tweet_fp:
            tweet_count = 0
            last_tweet_id = ''

            tweet_csv_writer = csv.DictWriter(tweet_fp, fieldnames=TweetInfo.tweet_fields)

            if self.__twitter_tweet_persist_file_format__ != 'csv' and tweet_fp.tell() != 0:
                tweet_fp.seek(tweet_fp.tell() - 1, os.SEEK_SET)
                tweet_fp.truncate()
                tweet_fp.write(",")

            for tweet in tweets_generator:
                last_tweet_id = tweet.get_tweet_id()
                tweet_count += 1
                if self.__twitter_tweet_persist_file_format__ == 'csv':
                    if tweet_fp.tell() == 0:
                        tweet_csv_writer.writeheader()
                    tweet_csv_writer.writerow(tweet.get_json())
                else:
                    if tweet_fp.tell() == 0:
                        tweet_fp.write("[")
                    json.dump(tweet.get_json(), tweet_fp)
                    tweet_fp.write(",")
            if self.__twitter_tweet_persist_file_format__ != 'csv':
                tweet_fp.seek(tweet_fp.tell() - 1, os.SEEK_SET)
                tweet_fp.truncate()
                tweet_fp.write("]")
            return last_tweet_id, tweet_count


def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path+filename, 'w') as fp:
            fp.write(data)
