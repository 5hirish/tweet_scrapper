import markovify

from tweetscrape.coolstuff.db_helper import SQLiteHelper


def auto_generate_tweet():
    sqlite = SQLiteHelper()
    fetched_tweets = sqlite.get_all_tweets()
    tweets_text = ''
    for tweet in fetched_tweets:
        tweets_text = tweets_text+'\n'+tweet[5]
    # print(tweets_text)
    tweet_model = markovify.Text(tweets_text)
    for i in range(3):
        print("\nAuto-Generated Tweet {0}: {1}".format(i, tweet_model.make_short_sentence(140)))


if __name__ == '__main__':
    auto_generate_tweet()