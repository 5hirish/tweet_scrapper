import logging
from datetime import datetime
from math import ceil

from tweetscrape.tweets_scrape import TweetScrapper

logger = logging.getLogger(__name__)


class TweetScrapperSearch(TweetScrapper):
    """
    Search syntax for query, each filter is white space separated
    eg: Election India NDA "BJP" 2019 OR 2018 -Asia #India OR #BJP from:narendramodi to:NITIAayog @NDTV since:2017-08-01 until:2019-06-15

    1) All of these words: each white space separated
    2) This exact phrase: `""` term in quotation marks
    3) Any of these words: `OR` operator separated, each operator separated
    4) None of these words: `-` operator as prefix to the term, each white space separated
    5) These hash-tags: `#` operator as prefix to the term, each `OR` separated
    6) From these accounts: `from:` as prefix to the term, each `OR` separated
    7) To these accounts: `to:` as prefix to the term, each `OR` separated
    8) Mentioning these accounts: `@` as prefix to the term, each `OR` separated
    9) Near this place: `near:` as prefix to the term and `""` term in quotation marks
                        and `within:` as range with `mi` as suffix miles
    10) From this date: `since:` as prefix to from date and `until:` as prefix to till date. Date format as `YYYY-MM-DD`

    Can specify language. Use language codes. eg. English - `en`

    """

    search_term = None
    search_type = None
    pages = None

    twitter_from_date = "2006-03-21"
    previous_last_tweet_id = ""
    max_retry_count = 6
    retry_count = 0

    def __init__(self,
                 search_all="", search_exact="", search_any="", search_excludes="", search_hashtags="",
                 search_from_accounts="", search_to_accounts="", search_mentions="",
                 search_near_place="", search_near_distance="",
                 search_till_date="", search_since_date="",
                 num_tweets=2, language='',
                 tweet_dump_path="", tweet_dump_format="",
                 request_proxies=None):

        self.search_type = "typd"

        if num_tweets > 0:
            self.pages = ceil(num_tweets/20)
        else:
            self.pages = -1

        self.search_since_date = search_since_date

        self.intermediate_query = self.construct_query(search_all, search_exact, search_any,
                                                       search_excludes, search_hashtags,
                                                       search_from_accounts, search_to_accounts, search_mentions,
                                                       search_near_place, search_near_distance)

        self.time_query = self.update_time_interval(search_since_date, search_till_date)

        # self.search_term = parse.quote(constructed_search_query)

        # if search_all.startswith("#"):
        #     self.search_type = "hash"
        # else:
        #     self.search_type = "typd"

        self.__twitter_search_init_url__ = 'https://twitter.com/search'

        self.__twitter_search_init_params__ = {
            'vertical': 'default',
            'src': self.search_type,
        }

        self.__twitter_search_params_recursive__ = {
            'vertical': 'default',
            'src': self.search_type,
            'l': language,
            'include_available_features': 1,
            'include_entities': 1,
            'include_new_items_bar': 'true'
        }

        super().__init__(None, None, None, request_proxies,
                         self.pages, tweet_dump_path, tweet_dump_format)

    def get_search_tweets(self, latest_tweets=True, save_output=False):
        if self.time_query is not None and self.time_query != "":
            search_query = self.intermediate_query + " " + self.time_query
        else:
            search_query = self.intermediate_query

        logger.info("Search:|{0}|".format(search_query))

        if latest_tweets:
            self.__twitter_search_init_params__['f'] = 'tweets'
        self.__twitter_search_init_params__['q'] = search_query

        self.update_request_url(self.__twitter_search_init_url__)
        self.update_request_params(
            twitter_request_url=self.__twitter_search_init_url__,
            twitter_request_params=self.__twitter_search_init_params__,
            update_refer=True)

        output_file_name = '/' + search_query + '_search'
        tweet_count, last_tweet_id, last_tweet_time, dump_path = self.execute_twitter_request(search_term=search_query,
                                                                                              log_output=save_output,
                                                                                              log_file=output_file_name)
        # Stop Iteration ?
        if last_tweet_time != "" and (self.pages == -1 or (self.pages - 1) * 20 > tweet_count):
            logger.info("Recursive search. Profile Limit exhausted: Till:" + last_tweet_time)

            if latest_tweets:
                self.__twitter_search_params_recursive__['f'] = 'tweets'
            self.__twitter_search_params_recursive__['q'] = search_query
            self.__twitter_search_init_params__['q'] = search_query

            # self.update_request_url(self.__twitter_search_url__)
            self.update_request_params(
                twitter_request_url=self.__twitter_search_init_url__,
                twitter_request_params=self.__twitter_search_init_params__,
                update_refer=True)
            self.clear_old_cursor()

            if self.previous_last_tweet_id != "" and self.previous_last_tweet_id == last_tweet_id:
                logger.info("Circular search detected. Taking measures...")

                # Try changing user-agent (Best case)
                self.switch_request_user_agent()
                # Try changing request proxy
                self.switch_request_proxy()
                # Try adding a request delay (Works in front-end)
                # time.sleep(random.choice(self.__twitter_request_delays__))
                # Try stepping the date (Worst case)

                if self.retry_count > self.max_retry_count:
                    # Finally give up ...
                    logger.warning("Tried all measures giving up!")
                    return tweet_count, last_tweet_id, last_tweet_time, dump_path

                self.retry_count += 1

            else:
                self.previous_last_tweet_id = last_tweet_id

            if self.search_since_date is None or self.search_since_date == '':
                search_since = self.twitter_from_date
            else:
                search_since = self.search_since_date

            self.time_query = self.update_time_interval(search_since_date=search_since,
                                                        search_till_date=last_tweet_time)
            append_tweet_count, last_tweet_id, last_tweet_time, dump_path = self.get_search_tweets(save_output)
            tweet_count += append_tweet_count

        return tweet_count, last_tweet_id, last_tweet_time, dump_path

    def update_time_interval(self, search_since_date, search_till_date):

        if search_till_date is not None and search_till_date != "" and valid_date_format(search_till_date,
                                                                                         self.twitter_date_format):
            search_till_date = "until:" + search_till_date

            if search_since_date is not None and search_since_date != "" and valid_date_format(search_since_date,
                                                                                               self.twitter_date_format):
                if datetime.strptime(search_since_date, self.twitter_date_format) <= \
                        datetime.strptime(search_till_date.replace('until:', ''), self.twitter_date_format):

                    search_since_date = "since:" + search_since_date
                else:
                    search_since_date = "since:" + self.twitter_from_date
            else:
                search_since_date = "since:" + self.twitter_from_date
        logger.info(search_since_date)
        if (search_since_date is not None and search_since_date != "") and \
                (search_till_date is not None and search_till_date != ""):
            return search_since_date + " " + search_till_date
        return ""

    @staticmethod
    def construct_query(search_all, search_exact, search_any, search_excludes, search_hashtags,
                        search_from_accounts, search_to_accounts, search_mentions, search_near_place,
                        search_near_distance):

        search_query_filters = []

        if search_all is not None and search_all != "":
            search_query_filters.append(search_all)

        if search_exact is not None and search_exact != "":
            search_exact = "\"" + search_exact + "\""
            search_query_filters.append(search_exact)

        if search_any is not None and search_any != "" and " " in search_any:
            search_any = " OR ".join(search_any.split())
            search_query_filters.append(search_any)

        if search_excludes is not None and search_excludes != "":
            search_excludes = " -".join(search_excludes.split())
            search_excludes = "-" + search_excludes
            search_query_filters.append(search_excludes)

        if search_hashtags is not None and search_hashtags != "":
            search_hashtags = prefix_operator(search_hashtags, "#")
            search_query_filters.append(search_hashtags)

        if search_from_accounts is not None and search_from_accounts != "":
            search_from_accounts = prefix_operator(search_from_accounts, "from:")
            search_query_filters.append(search_from_accounts)

        if search_to_accounts is not None and search_to_accounts != "":
            search_to_accounts = prefix_operator(search_to_accounts, "to:")
            search_query_filters.append(search_to_accounts)

        if search_mentions is not None and search_mentions != "":
            search_mentions = prefix_operator(search_mentions, "@")
            search_query_filters.append(search_mentions)

        if search_near_place is not None and search_near_place != "":
            search_near_place = "near:" + search_near_place

            if search_near_distance is not None and search_near_distance != "":
                search_near_distance = "within:" + search_near_distance
            else:
                search_near_distance = "within:15mi"

            search_query_filters.append(search_near_place)
            search_query_filters.append(search_near_distance)

        search_query = ' '.join(search_query_filters)

        return search_query


def prefix_operator(query_str, prefix_op):
    query_list = query_str.split()
    for i, tag in enumerate(query_list):
        if tag[0] != prefix_op:
            query_list[i] = prefix_op + tag

    return " OR ".join(query_list)


def valid_date_format(date_str, date_format='%Y-%m-%d'):
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        logger.warning("Incorrect data format, should be YYYY-MM-DD")
        return False
    return True


if __name__ == '__main__':
    # avengers%20infinity%20war%20%22avengers%22%20-asia%20%23avengers%20from%3Amarvel%20since%3A2019-06-01
    # avengers infinity war "avengers" -asia #avengers from:marvel since:2019-06-01

    logging.basicConfig(level=logging.DEBUG)

    # ts = TweetScrapperSearch(search_all="avengers infinity war", tweet_dump_path='twitter.json',
    #                          tweet_dump_format='json')
    #
    # ts = TweetScrapperSearch(search_from_accounts="BarackObama",
    #                          tweet_dump_path='twitter.csv',
    #                          num_tweets=-1,
    #                          tweet_dump_format='csv')

    ts = TweetScrapperSearch(search_all="trump",
                             tweet_dump_path='twitter.csv',
                             num_tweets=100,
                             search_since_date='2019-01-01',
                             search_till_date='2019-05-01',
                             tweet_dump_format='csv')

    # ts = TweetScrapperSearch(search_hashtags="FakeNews Trump", pages=1)
    #
    # # avengers endgame spiderman OR ironman -spoilers
    # ts = TweetScrapperSearch(search_all="avengers endgame",
    #                          search_any="spiderman ironman",
    #                          search_excludes="spoilers", num_tweets=2)
    #
    # ts = TweetScrapperSearch(search_all="avengers marvel",
    #                          search_hashtags="avengers",
    #                          search_from_accounts="marvel ",
    #                          num_tweets=2)
    #
    # ts = TweetScrapperSearch(search_all="raptors",
    #                          search_since_date="2019-03-01", search_till_date="2019-06-01",
    #                          num_tweets=1)
    #
    # ts = TweetScrapperSearch(search_hashtags="raptors", search_near_place="toronto", pages=1)
    l_tweet_count, l_tweet_id, l_last_time, l_dump_path = ts.get_search_tweets(latest_tweets=True, save_output=True)
    # for l_tweet in l_extracted_tweets:
    #     print(str(l_tweet))
    print(l_tweet_count)
