import re
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, stem_text, strip_punctuation
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from tweetscrape.coolstuff.db_helper import SQLiteHelper


def tweet_topic_modeling():
    sqlite = SQLiteHelper()
    fetched_tweets = sqlite.get_all_tweets()
    tweets_doc = []
    for tweet in fetched_tweets:
        tweets_doc.append(tweet[5])

    links_pattern = re.compile('(http[^\s]+)')
    pics_pattern = re.compile('(pic.twitter.com/[^\s]+)')
    mention_pattern = re.compile('\@([a-zA-Z0-9_]+)')
    hastag_patter = re.compile('#([a-zA-Z0-9_]+)')

    for pos, tweets_text in enumerate(tweets_doc):
        tweets_text = regex_clean(links_pattern, tweets_text)
        tweets_text = regex_clean(pics_pattern, tweets_text)
        tweets_text = regex_clean(mention_pattern, tweets_text)
        tweets_text = regex_clean(hastag_patter, tweets_text)

        tweets_text = strip_punctuation(tweets_text)
        tweets_text = strip_multiple_whitespaces(tweets_text)
        tweets_text = remove_stopwords(tweets_text)
        tweets_text = stem_text(tweets_text)
        tweets_tokens = simple_preprocess(tweets_text)
        tweets_doc[pos] = tweets_tokens
    

    # print(tweets_tokens[:5])
    # print(type(tweets_tokens))
    # a mapping between words and their integer ids.
    id2word_tweet = Dictionary(tweets_doc)
    print(id2word_tweet)


def regex_clean(pattern, text):
    return pattern.sub(' ', text)


if __name__ == '__main__':
    tweet_topic_modeling()