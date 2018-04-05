import re

from tweetscrape.model.tweet_model import TweetInfo


class TweetScrapper:

    tweets_data_list = []

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

    def extract_tweets_data(self, tweet_list, hastag_capture):
        if tweet_list is not None:
            for tweet in tweet_list:
                if 'data-item-type' in tweet.attrib and tweet.attrib['data-item-type'] == "tweet":
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
                            tweet_text = ''.join(tweet_text).replace('\n', '')
                            tweet_data.set_tweet_text(tweet_text)

                            tweet_links_raw = tweet_content[0].xpath(self._tweet_links_list_pattern_)

                            for raw_link in tweet_links_raw:
                                raw_url = raw_link.attrib['href']
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
                            tweet_replies_count = tweet_replies[0].attrib['data-tweet-stat-count']
                            tweet_likes = tweet_content[0].xpath(self._tweet_like_count_pattern_)
                            tweet_likes_count = tweet_likes[0].attrib['data-tweet-stat-count']
                            tweet_retweets = tweet_content[0].xpath(self._tweet_retweet_count_pattern_)
                            tweet_retweets_count = tweet_retweets[0].attrib['data-tweet-stat-count']

                            tweet_data.set_tweet_interactions(tweet_replies_count, tweet_likes_count, tweet_retweets_count)

                            self.tweets_data_list.append(tweet_data)
