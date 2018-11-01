import pytest
from tweetscrape.profile_tweets import TweetScrapperProfile


@pytest.mark.parametrize("test_user,test_page", [
        ("@BarackObama", 2),
        ("@fchollet", 6),
        ("@Kasparov63", 0),
        ("@ShashiTharoor", 10),
        ("@EdwardSnowden", 15),
        ("@colbertlateshow", 5),
        ("@HamillHimself", 4)

    ])
def test_user_tweets(test_user, test_page):
    ts = TweetScrapperProfile(test_user, test_page)
    extracted_tweets = ts.get_profile_tweets(False)
    if test_page > 0:
        assert len(extracted_tweets) > 0
    for tweets in extracted_tweets:
        assert tweets.get_tweet_id() is not None
        assert tweets.get_tweet_text() is not None
        if not tweets.get_is_retweeter():
            assert tweets.get_tweet_author() == test_user[1:]
        else:
            assert tweets.get_retweeter() == test_user[1:]
