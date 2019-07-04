import pytest
import os
import csv
from tweetscrape.users_scrape import TweetScrapperUser


@pytest.mark.parametrize("test_user", [
        ("naval"),
        ("ewarren"),
        ("ChrisEvans")
    ])
def test_user_tweets(test_user):
    ts = TweetScrapperUser(test_user)
    user_info = ts.get_profile_info(False)

    assert user_info.get("name") is not None
    assert user_info.get("tweets") is not None
    assert user_info.get("following") is not None
    assert user_info.get("followers") is not None
    # assert user_info.get("favorites") is not None
