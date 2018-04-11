
import logging

from tweetscrape.profile_tweets import TweetScrapperProfile
from tweetscrape.coolstuff.db_helper import SQLiteHelper

logger = logging.getLogger(__name__)


def fetch_insert_tweets(username, pages, last_tweet_id=None):
    tweet_scrapper = TweetScrapperProfile(username, pages, last_tweet_id)
    tweets = tweet_scrapper.get_profile_tweets()
    if len(tweets) > 0:
        last_fetched_tweet = tweets[len(tweets) - 1].get_tweet_id()
        print("Last tweet:", last_fetched_tweet)
        sqlt = SQLiteHelper()
        sqlt.insert_tweet(tweets)


if __name__ == '__main__':
    # Last extracted: 812662401480830976
    logging.basicConfig(level=logging.DEBUG)
    fetch_insert_tweets("@5hirish", 25)


