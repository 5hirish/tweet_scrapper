import logging
from math import ceil

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


class TweetScrapperConversation(TweetScrapper):
    username = "5hirish"
    pages = 0

    def __init__(self, username, parent_tweet_id, num_tweets=40,
                 tweet_dump_path="", tweet_dump_format="",
                 request_proxies=None):
        self.username = username
        self.parent_tweet_id = parent_tweet_id

        if num_tweets > 0:
            self.pages = ceil(num_tweets / 20)
        else:
            self.pages = -1

        self.__twitter_init_conversation_url__ = 'https://twitter.com/{username}/status/{parent_tweet_id}' \
            .format(username=self.username, parent_tweet_id=self.parent_tweet_id)

        self.__twitter_init_conversation_params__ = {
            'conversation_id': self.parent_tweet_id
        }

        self.__twitter_conversation_params__ = {
            'include_available_features': 1,
            'include_entities': 1
        }

        self.__twitter_conversation_header__ = {
            'referer': 'https://twitter.com/{username}/status/{parent_tweet_id}'
                .format(username=self.username, parent_tweet_id=self.parent_tweet_id)
        }

        super().__init__(self.__twitter_init_conversation_url__,
                         self.__twitter_conversation_header__,
                         self.__twitter_init_conversation_params__,
                         request_proxies,
                         self.pages, tweet_dump_path, tweet_dump_format)

    def get_thread_tweets(self, save_output=False):
        output_file_name = '/' + self.username + '_conversation'
        # Search Profile since: until: from:
        # conversation_id
        if self.username is not None and self.username != "":
            self.username = self.username.replace("@", "")
            tweet_count, last_tweet_id, last_tweet_time, dump_path = \
                self.execute_twitter_request(username=self.username,
                                             conversation_id=self.parent_tweet_id,
                                             log_output=save_output,
                                             log_file=output_file_name)

            # if self.pages == -1 or (self.pages - 1 * 20) > tweet_count:
            #     logger.info("Switching to search mode. Profile Limit exhausted")
            #     ts = TweetScrapperSearch(search_from_accounts=self.username,
            #                              search_since_date=TweetScrapperSearch.twitter_from_date,
            #                              search_till_date=last_tweet_time)
            #     append_tweet_count, last_tweet_id, last_tweet_time, dump_path = ts.get_search_tweets(save_output)
            #     tweet_count += append_tweet_count

            return tweet_count, last_tweet_id, last_tweet_time, dump_path
        return 0, 0, 0, output_file_name


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # https://twitter.com/ewarren/status/1146132929065738246?conversation_id=1146132929065738246
    l_ts = TweetScrapperConversation("ewarren", 1146415363460141057, 40, 'twitter_conv.csv', 'csv')
    l_tweet_count, l_tweet_id, l_tweet_time, l_dump_path = l_ts.get_thread_tweets(True)
    # for l_tweet in l_extracted_tweets:
    #     print(str(l_tweet))
    print(l_tweet_count)
