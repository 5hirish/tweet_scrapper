import re
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, stem_text, strip_punctuation
from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
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
    hashtag_pattern = re.compile('#([a-zA-Z0-9_]+)')

    for pos, tweets_text in enumerate(tweets_doc):
        tweets_text = regex_clean(links_pattern, tweets_text)
        tweets_text = regex_clean(pics_pattern, tweets_text)
        tweets_text = regex_clean(mention_pattern, tweets_text)
        tweets_text = regex_clean(hashtag_pattern, tweets_text)

        tweets_text = strip_punctuation(tweets_text)
        tweets_text = strip_multiple_whitespaces(tweets_text)
        # improve stopwords removal
        tweets_text = remove_stopwords(tweets_text)
        tweets_text = stem_text(tweets_text)
        tweets_tokens = simple_preprocess(tweets_text)
        tweets_doc[pos] = tweets_tokens

    # a mapping between words and their integer ids.
    id2word_tweet = Dictionary(tweets_doc)
    print(id2word_tweet)

    # ignore words that appear in less than 3 documents or more than 5% documents
    id2word_tweet.filter_extremes(no_below=3, no_above=0.05)
    print(id2word_tweet)

    # transform a document into a bag-of-word vector, using a dictionary
    tweet_vec = [id2word_tweet.doc2bow(td) for td in tweets_doc]

    tweet_lda = LdaModel(tweet_vec, num_topics=3, id2word=id2word_tweet, passes=50)

    print(tweet_lda.print_topics(num_topics=3, num_words=3))


def regex_clean(pattern, text):
    return pattern.sub(' ', text)


if __name__ == '__main__':
    tweet_topic_modeling()