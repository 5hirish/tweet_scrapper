import sqlite3
import json


class SQLiteHelper:
    __connection__ = None
    __cursor__ = None
    __table_name__ = 'tweets'

    def __init__(self):
        self.__connection__ = sqlite3.connect('tweets.sqlite')
        self.create_table_if_exists()

    def get_cursor(self):
        if self.__cursor__ is None:
            self.__cursor__ = self.__connection__.cursor()
        return self.__cursor__

    def create_table_if_exists(self):
        create_table = '''CREATE TABLE IF NOT EXISTS ''' + self.__table_name__ + ''' (
				tweet_id INTEGER PRIMARY KEY, 
				tweet_type VARCHAR(10), 
				tweet_author TEXT, 
				tweet_author_id INTEGER, 
				tweet_time_ms BIGINT, 
				tweet_text TEXT,
				tweet_link TEXT, 
				tweet_hastag TEXT, 
				tweet_mentions TEXT, 
				tweet_replies_count INTEGER, 
				tweet_favorite_count INTEGER, 
				tweet_retweet_count INTEGER
			);'''

        self.get_cursor().execute(create_table)
        self.__connection__.commit()

    def insert_tweet(self, tweets):
        tweets_insert = []
        for tweet in tweets:
            tweet_tuple = (
                tweet.get_tweet_id(),
                tweet.get_tweet_type(),
                tweet.get_tweet_author(),
                tweet.get_tweet_author_id(),
                tweet.get_tweet_time_ms(),
                tweet.get_tweet_text(),
                json.dumps(tweet.get_tweet_links()),
                json.dumps(tweet.get_tweet_hashtags()),
                json.dumps(tweet.get_tweet_mentions()),
                tweet.get_tweet_replies_count(),
                tweet.get_tweet_favorite_count(),
                tweet.get_tweet_retweet_count()
            )
            tweets_insert.append(tweet_tuple)

        insert_tweet_query = '''INSERT OR IGNORE INTO ''' + self.__table_name__ + '''
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        self.get_cursor().executemany(insert_tweet_query, tweets_insert)
        self.__connection__.commit()

    def get_user_tweets(self, author=None, author_id=None):
        if author_id is not None:
            fetch_tweets_query = '''SELECT * FROM ''' + self.__table_name__ + '''
                        WHERE tweet_author_id = ?'''
            author_tup = (author_id,)
            self.get_cursor().execute(fetch_tweets_query, author_tup)
        else:
            fetch_tweets_query = '''SELECT * FROM ''' + self.__table_name__ + '''
                        WHERE tweet_author = ?'''
            author_tup = (author,)
            self.get_cursor().execute(fetch_tweets_query, author_tup)
        return self.get_cursor().fetchall()

    def get_all_tweets(self):
        fetch_tweets_query = '''SELECT * FROM ''' + self.__table_name__
        self.get_cursor().execute(fetch_tweets_query)
        return self.get_cursor().fetchall()
