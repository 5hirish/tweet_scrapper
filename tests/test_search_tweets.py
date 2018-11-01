import pytest
from tweetscrape.search_tweets import TweetScrapperSearch


@pytest.mark.parametrize("test_term,test_page", [
        ("New York", 2),
        ("White House", 6),
        ("Avengers Infinity War", 5),
        ("Machine Learning", 10),
        ("The Rock", 15)
    ])
def test_search_tweets(test_term, test_page):

    ts = TweetScrapperSearch(test_term, test_page)
    extracted_tweets = ts.get_search_tweets(False)
    assert len(extracted_tweets) > 0
    for tweets in extracted_tweets:
        assert tweets.get_tweet_id() is not None
        assert tweets.get_tweet_text() is not None


@pytest.mark.parametrize("test_tag,test_page", [
        ("#StarWars", 3),
        ("#FakeNews", 6),
        ("#Hamilton", 5),
        ("#MarchForOurLives", 1),
        ("#CNN", 12)
    ])
def test_hashtag_tweets(test_tag, test_page):

    ts = TweetScrapperSearch(test_tag, test_page)
    extracted_tweets = ts.get_search_tweets(False)
    assert len(extracted_tweets) > 0
    for tweets in extracted_tweets:
        assert tweets.get_tweet_id() is not None
        assert tweets.get_tweet_text() is not None
        extracted_hastags = [ht.lower() for ht in tweets.get_tweet_hashtags()]
        assert test_tag.lower() in extracted_hastags
