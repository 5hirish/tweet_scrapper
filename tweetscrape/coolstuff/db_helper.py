import sqlite3


class SQLiteHelper:

	__connection__ = None
	__cursor__ = None
	
	def __init__(self):
		self.__connection__ = sqlite3.connect('tweets.db')
		self.create_table_if_exists()
	
	def get_cursor(self):
		if self.__cursor__ is None:
			self.__cursor__ = self.__connection__.cursor()
		return self.__cursor__
	
	def create_table_if_exists(self):
		create_table = '''CREATE TABLE IF NOT EXISTS tweets (
                tweet_id INTEGER PRIMARY KEY,
                tweet_type VARCHAR(10),
                tweet_author TEXT,
                tweet_author_id INTEGER,
                tweet_time_ms INTEGER,
                tweet_link TEXT,
                tweet_hastag TEXT,
                tweet_mentions TEXT,
                tweet_replies_count INTEGER,
                tweet_favorite_count INTEGER,
                tweet_retweet_count INTEGER
        	);'''
			
			self.__cursor__ = self.get_cursor()
			self.__cursor__.execute(create_table)
			self.__connection__.commit()
