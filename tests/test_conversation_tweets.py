import pytest
import os
import csv
from tweetscrape.conversation_tweets import TweetScrapperConversation


@pytest.mark.parametrize("test_user,test_tweet,test_page", [
        ("naval", 1142596407460634624, 40),
        ("ewarren", 1146415363460141057, 30),
        ("ChrisEvans", 1138806658912702464, 100)
    ])
def test_user_tweets(test_user, test_tweet, test_page):
    ts = TweetScrapperConversation(test_user, test_tweet, test_page, 'twitter.csv', 'csv')
    tweet_count, tweet_id, tweet_time, dump_path = ts.get_thread_tweets(False)

    assert os.path.exists(dump_path)

    if test_page > 0:
        assert tweet_count > 20

    with open(dump_path, 'r') as csv_fp:
        csv_reader = csv.DictReader(csv_fp)
        for tweets in csv_reader:
            assert tweets.get('id') is not None
            assert tweets.get('text') is not None
            assert tweets.get('time') is not None

    os.remove(dump_path)