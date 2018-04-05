from unittest import TestCase

from tweetscrape.profile_tweets import TweetScrapperProfile


class UserTweetsTest(TestCase):
    
    test_users = ["@BarackObama", "@fchollet", "@Kasparov63", "@ShashiTharoor", "@EdwardSnowden", "@colbertlateshow", "@HamillHimself"]
    test_pages = 2
    
    def test_user_tweets(self):    
        for user in self.test_users:
            with self.subTest(i=user):
                ts = TweetScrapperProfile(user, self.test_pages)
                extracted_tweets = ts.get_profile_tweets(False)
                assert len(extracted_tweets) > 0
                for tweets in extracted_tweets:
                    assert tweets.get_tweet_id() is not None
                    assert tweets.get_tweet_text() is not None