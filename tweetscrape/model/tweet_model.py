
class TweetInfo:
    __tweet_id__ = -1
    __tweet_type__ = None
    __tweet_author__ = None
    __tweet_author_name__ = None
    __tweet_author_id__ = None
    __tweet_is_retweet__ = False
    __tweet_has_parent__ = False
    __tweet_conversation_id__ = None
    __tweet_retweetwer__ = None
    __tweet_text__ = None
    __tweet_time_ms__ = 0
    __tweet_links__ = []
    __tweet_hashtags__ = []
    __tweet_mentions__ = []
    __tweet_replies_count__ = 0
    __tweet_favorite_count__ = 0
    __tweet_retweet_count__ = 0

    tweet_fields = ["id", "type", "time", "author", "author_id", "re_tweeter", "associated_tweet",
                    "text", "links", "hashtags", "mentions", "reply_count", "favorite_count", "retweet_count"]

    def __init__(self, tweet_id, tweet_type):
        self.__tweet_id__ = tweet_id
        self.__tweet_type__ = tweet_type
        self.__tweet_links__ = []
        self.__tweet_hashtags__ = []
        self.__tweet_mentions__ = []

    def get_tweet_id(self):
        return self.__tweet_id__

    def get_tweet_type(self):
        return self.__tweet_type__

    def set_tweet_author(self, tweet_author, tweet_author_name, tweet_author_id):
        self.__tweet_author__ = tweet_author
        self.__tweet_author_name__ = tweet_author_name
        self.__tweet_author_id__ = tweet_author_id

    def get_tweet_author(self):
        return self.__tweet_author__

    def get_tweet_author_name(self):
        return self.__tweet_author_name__

    def get_tweet_author_id(self):
        return self.__tweet_author_id__

    def set_retweeter(self, retweeter):
        self.__tweet_retweetwer__ = retweeter
        self.__tweet_is_retweet__ = True

    def get_retweeter(self):
        return self.__tweet_retweetwer__

    def get_is_retweeter(self):
        return self.__tweet_is_retweet__

    def set_tweet_conversation(self, tweet_conversation_id, tweet_has_parent):
        self.__tweet_conversation_id__ = tweet_conversation_id
        self.__tweet_has_parent__ = tweet_has_parent

    def get_conversation_id(self):
        return self.__tweet_conversation_id__

    def get_has_parent(self):
        return self.__tweet_has_parent__

    def set_tweet_text(self, tweet_text):
        self.__tweet_text__ = tweet_text

    def get_tweet_text(self):
        return self.__tweet_text__

    def set_tweet_time_ms(self, tweet_time_ms):
        self.__tweet_time_ms__ = tweet_time_ms

    def get_tweet_time_ms(self):
        return self.__tweet_time_ms__

    def set_tweet_links(self, tweet_link):
        self.__tweet_links__.append(tweet_link)

    def get_tweet_links(self):
        return self.__tweet_links__

    def set_tweet_hashtags(self, tweet_hashtag):
        self.__tweet_hashtags__.append(tweet_hashtag)

    def get_tweet_hashtags(self):
        return self.__tweet_hashtags__

    def set_tweet_mentions(self, tweet_mention):
        self.__tweet_mentions__.append(tweet_mention)

    def get_tweet_mentions(self):
        return self.__tweet_mentions__

    def set_tweet_interactions(self, tweet_replies_count, tweet_favorite_count, tweet_retweet_count):
        self.__tweet_replies_count__ = tweet_replies_count
        self.__tweet_favorite_count__ = tweet_favorite_count
        self.__tweet_retweet_count__ = tweet_retweet_count

    def get_tweet_replies_count(self):
        return self.__tweet_replies_count__

    def get_tweet_favorite_count(self):
        return self.__tweet_favorite_count__

    def get_tweet_retweet_count(self):
        return self.__tweet_retweet_count__

    def get_json(self):
        return {
            "id": self.get_tweet_id(),
            "type": self.get_tweet_type(),
            "time": self.get_tweet_time_ms(),
            "author": self.get_tweet_author(),
            "author_id": self.get_tweet_author_id(),
            "re_tweeter": self.get_retweeter(),
            "associated_tweet": self.get_conversation_id(),
            "text": self.get_tweet_text(),
            "links": self.get_tweet_links(),
            "hashtags": self.get_tweet_hashtags(),
            "mentions": self.get_tweet_mentions(),
            "reply_count": self.get_tweet_replies_count(),
            "favorite_count": self.get_tweet_favorite_count(),
            "retweet_count": self.get_tweet_retweet_count()
        }

    def __str__(self):
        return "Id: " + self.get_tweet_id() + "\tType: " + self.get_tweet_type() + "\tTime: " + self.get_tweet_time_ms() + \
               "\nAuthor: " + self.get_tweet_author() + "\tAuthorId: " + self.get_tweet_author_id() + \
               "\nReTweeter: " + str(self.get_retweeter()) + \
               "\nAssociated Tweet: " + str(self.get_conversation_id()) + \
               "\nText: " + self.get_tweet_text() + \
               "\nLinks: " + str(self.get_tweet_links()) + \
               "\nHashtags: " + str(self.get_tweet_hashtags()) + \
               "\nMentions: " + str(self.get_tweet_mentions()) + \
               "\nReplies: " + self.get_tweet_replies_count() + \
               "\tFavorites: " + self.get_tweet_favorite_count() + \
               "\tRetweets: " + self.get_tweet_retweet_count() + "\n"
