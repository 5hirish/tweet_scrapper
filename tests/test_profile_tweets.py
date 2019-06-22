import pytest
import os
import csv
from tweetscrape.profile_tweets import TweetScrapperProfile


@pytest.mark.parametrize("test_user,test_page", [
        ("@BarackObama", 2),
        ("@fchollet", 6),
        ("@Kasparov63", 1),
        ("@ShashiTharoor", 10),
        # ("@EdwardSnowden", 15),
        # ("@colbertlateshow", 5),
        # ("@HamillHimself", 4)

    ])
def test_user_tweets(test_user, test_page):
    ts = TweetScrapperProfile(test_user, test_page, 'twitter.csv', 'csv')
    tweet_count, tweet_id, tweet_time, dump_path = ts.get_profile_tweets(False)

    assert os.path.exists(dump_path)

    if test_page > 0:
        assert tweet_count == pytest.approx(test_page * 20, abs=5)

    with open(dump_path, 'r') as csv_fp:
        csv_reader = csv.DictReader(csv_fp)
        for tweets in csv_reader:
            assert tweets.get('id') is not None
            assert tweets.get('text') is not None
            assert tweets.get('time') is not None

    os.remove(dump_path)