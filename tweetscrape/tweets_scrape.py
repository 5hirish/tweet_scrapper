import re
import os
import requests
import logging
import csv
import json
import random
import time
from lxml import etree
from urllib import parse
from datetime import datetime
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

from tweetscrape.model.tweet_model import TweetInfo

logger = logging.getLogger(__name__)


"""
User-Agents: https://udger.com/resources/ua-list
"""


class TweetScrapper:
    __twitter_request_url__ = None
    __twitter_request_header__ = None
    __twitter_request_params__ = None

    _tweets_pattern_ = '''//li[contains(@class,"stream-item")]'''
    _tweet_stream_max_ = '''//*[@id="timeline"]/div'''

    _tweet_min_position = '''data-min-position'''
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

    __twitter_user_agent__ = [
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
    ]

    __twitter_request_header__ = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.8',
        'user-agent': random.choice(__twitter_user_agent__),
        'x-requested-with': 'XMLHttpRequest',
        'x-twitter-active-user': 'yes',
        'x-twitter-polling': 'true',
    }

    __twitter_request_delays__ = [2, 3, 4, 5, 6, 7]

    __twitter_search_url__ = 'https://twitter.com/i/search/timeline'

    twitter_date_format = '%Y-%m-%d'
    current_cursor = None
    scrape_pages = 2

    def __init__(self, twitter_request_url, twitter_request_header,
                 twitter_request_params=None, twitter_request_proxies=None, scrape_pages=2,
                 twitter_file_path=None, twitter_file_format='json'):

        self.__twitter_request_url__ = twitter_request_url
        if twitter_request_header is not None:
            self.__twitter_request_header__ = twitter_request_header
        self.__twitter_request_params__ = twitter_request_params
        self.__twitter_request_proxies__ = twitter_request_proxies
        self.scrape_pages = scrape_pages
        self.__twitter_tweet_persist_file_path__ = twitter_file_path
        self.__twitter_tweet_persist_file_format__ = twitter_file_format

        self.hashtag_capture = re.compile(self._tweet_hastag_pattern_)

        self.html_parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)

    def switch_user_agent(self):
        logger.info("Switching user-agent")
        self.__twitter_request_header__['user-agent'] = random.choice(self.__twitter_user_agent__)

    def update_request_params(self, twitter_request_url, twitter_request_params, update_refer=False):
        if twitter_request_params is not None:
            self.__twitter_request_params__ = twitter_request_params
            if update_refer and twitter_request_url != "":
                self.update_request_refer(twitter_request_url, self.__twitter_request_params__)

    def update_request_url(self, twitter_request_url):
        if twitter_request_url is not None:
            self.__twitter_request_url__ = twitter_request_url

    def update_request_refer(self, twitter_request_url, twitter_request_params):
        twitter_request_refer = twitter_request_url + '?' + parse.urlencode(twitter_request_params, quote_via=parse.quote)
        self.__twitter_request_header__['referer'] = twitter_request_refer

    def clear_old_cursor(self):
        self.current_cursor = None

    def execute_twitter_request(self, username=None, search_term=None, log_output=False, output_file=None,
                                add_delay=False, delay_tweet_count=100):
        tweet_count = 0
        last_tweet_id, last_tweet_time = '', ''

        if self.scrape_pages is None or self.scrape_pages < 0:
            is_stream = True
            self.scrape_pages = -1
        else:
            is_stream = False

        total_pages = self.scrape_pages

        if self.current_cursor is not None:
            self.__twitter_request_params__['reset_error_state'] = 'false'
            self.__twitter_request_params__['max_position'] = self.current_cursor

        while is_stream or self.scrape_pages > 0:
            current_tweet_count = 0
            min_position = None

            twitter_request_params_encoded = parse.urlencode(self.__twitter_request_params__, quote_via=parse.quote)

            response = requests.get(self.__twitter_request_url__,
                                    headers=self.__twitter_request_header__,
                                    params=twitter_request_params_encoded,
                                    proxies=self.__twitter_request_proxies__)

            if response.ok and response.status_code == 200:
                if search_term is not None:
                    self.__twitter_request_url__ = self.__twitter_search_url__

                logger.debug("Page {0} request: {1}".format(abs(self.scrape_pages), response.status_code))

                try:
                    tweet_json = response.json()

                    try:
                        if tweet_json.get('has_more_items'):
                            num_new_tweets = tweet_json.get('new_latent_count')
                            min_position = tweet_json.get('min_position')
                        else:
                            logger.info("No more items...!!!")

                        if 'items_html' in tweet_json:
                            tweets_html = tweet_json.get('items_html')
                        else:
                            tweets_html = tweet_json.get('page')

                    except KeyError:
                        if search_term is not None:
                            raise ValueError("Oops! Something went wrong while searching {0}.".format(search_term))
                        elif username is not None:
                            raise ValueError("Oops! Either {0} does not exist or is private.".format(username))
                        else:
                            raise ValueError("Received no arguments")

                except JSONDecodeError:
                    tweets_html = response.text

                if log_output:
                    save_output(output_file + '.html', tweets_html)

                html_tree = etree.fromstring(tweets_html, self.html_parser)

                if html_tree is not None:
                    tweet_stream = html_tree.xpath(self._tweet_stream_max_)
                    if tweet_stream is not None and len(tweet_stream) > 0:
                        min_position = tweet_stream[0].attrib['data-min-position']
                    tweet_list = html_tree.xpath(self._tweets_pattern_)

                    tweets_generator = self.extract_tweets_data(tweet_list)
                    tweet_id, tweet_time, current_tweet_count = self.persist_tweets(tweets_generator)

                    if tweet_time is not None and tweet_time != "":
                        last_tweet_time = tweet_time
                    if tweet_id is not None and tweet_id != "":
                        last_tweet_id = tweet_id
                    tweet_count += current_tweet_count

                    logger.debug(
                        "Extracting {0} tweets of {1} page...".format(len(tweet_list),
                                                                      total_pages - self.scrape_pages + 1))

                if not is_stream:
                    self.scrape_pages += -1

                self.current_cursor = min_position

                if current_tweet_count > 0 and min_position is not None:
                    # composed_count: 0
                    # interval: 30000
                    # latent_count: 0
                    # self.__twitter_request_params__['min_position'] = last_tweet_id
                    self.__twitter_request_params__['reset_error_state'] = 'false'
                    self.__twitter_request_params__['max_position'] = self.current_cursor

                    if add_delay and tweet_count % delay_tweet_count == 0:
                        delay = random.choice(self.__twitter_request_delays__)
                        time.sleep(delay)
                else:
                    logger.info("End of tweet stream...")
                    return tweet_count, last_tweet_id, last_tweet_time, self.__twitter_tweet_persist_file_path__

        logger.info("Total {0} tweets extracted.".format(tweet_count))
        return tweet_count, last_tweet_id, last_tweet_time, self.__twitter_tweet_persist_file_path__

    def extract_tweets_data(self, tweet_list):
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
                            tweet_time_ms = tweet_content[0].xpath(self._tweet_time_ms_pattern_)[0] \
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
                                    hash_tag_group = re.match(self.hashtag_capture, raw_url)
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

        with open(self.__twitter_tweet_persist_file_path__, dump_mode, encoding="utf-8") as tweet_fp:
            tweet_count = 0
            last_tweet_id = ''
            last_tweet_timestamp = ''

            tweet_csv_writer = csv.DictWriter(tweet_fp, fieldnames=TweetInfo.tweet_fields)

            if self.__twitter_tweet_persist_file_format__ != 'csv' and tweet_fp.tell() != 0:
                tweet_fp.seek(tweet_fp.tell() - 1, os.SEEK_SET)
                tweet_fp.truncate()
                tweet_fp.write(",")

            for tweet in tweets_generator:
                last_tweet_id = tweet.get_tweet_id()
                last_tweet_timestamp = tweet.get_tweet_time_ms()
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

            try:
                last_datetime = datetime.fromtimestamp(int(last_tweet_timestamp) // 1000)
                last_tweet_timestamp = datetime.strftime(last_datetime, self.twitter_date_format)
            except ValueError:
                last_tweet_timestamp = ""
                logger.warning("Unable to get last tweet timestamp")

            logger.debug("Batch written to file:{0}".format(self.__twitter_tweet_persist_file_path__))
            return last_tweet_id, last_tweet_timestamp, tweet_count


def save_output(filename, data):
    if filename is not None and data is not None:
        file_path = os.path.dirname(os.path.realpath(__file__))
        with open(file_path + filename, 'w') as fp:
            fp.write(data)
