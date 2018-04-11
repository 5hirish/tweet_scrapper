import re
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, stem_text, strip_punctuation
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from tweetscrape.coolstuff.db_helper import SQLiteHelper


def tweet_topic_modeling():
    sqlite = SQLiteHelper()
    fetched_tweets = sqlite.get_all_tweets()
    tweets_text = ''
    for tweet in fetched_tweets:
        tweets_text = tweets_text+'\n'+tweet[5]

    tweets_text = remove_stopwords(tweets_text)
    # Remove hastags, mentions, links using regex
    tweets_text = strip_multiple_whitespaces(tweets_text)
    tweets_text = strip_punctuation(tweets_text)    
    tweets_text = stem_text(tweets_text)
    print(tweets_text)
    
    tweets_tokens = simple_preprocess(tweets_text)
    print(tweets_tokens[:5])
    # a mapping between words and their integer ids.
    id2word_tweet = Dictionary(tweets_tokens)
    print(id2word_tweet)


if __name__ == '__main__':
    tweet_topic_modeling()