from unittest import TestCase

from tweetscrape.search_tweets import TweetScrapperSearch


class UserTweetsTest(TestCase):
    test_search = ["New York", "White House", "Avengers Infinity War", "Machine Learning", "The Rock"]
    test_hashtags = ["#StarWars", "#FakeNews", "#Hamilton", "#MarchForOurLives", "#CNN"]
    test_pages = 2

    def test_search_tweets(self):
        for search_term in self.test_search:
            with self.subTest(i=search_term):
                ts = TweetScrapperSearch(search_term, self.test_pages)
                extracted_tweets = ts.get_search_tweets(False)
                assert len(extracted_tweets) > 0
                for tweets in extracted_tweets:
                    assert tweets.get_tweet_id() is not None
                    assert tweets.get_tweet_text() is not None

    def test_hashtag_tweets(self):
        for hashtag in self.test_hashtags:
            with self.subTest(i=hashtag):
                ts = TweetScrapperSearch(hashtag, self.test_pages)
                extracted_tweets = ts.get_search_tweets(False)
                assert len(extracted_tweets) > 0
                for tweets in extracted_tweets:
                    assert tweets.get_tweet_id() is not None
                    assert tweets.get_tweet_text() is not None
                    # extracted_hastags = [ht.lower() for ht in tweets.get_tweet_hashtags()]
                    # assert hashtag.lower() in extracted_hastags
