

class TweetInfo:

    __tweet_id__ = -1
    __tweet_type__ = None
    __tweet_author__ = None
    __tweet_author_id__ = None
    __tweet_text__ = None
    __tweet_time_ms__ = 0
    __tweet_links__ = []
    __tweet_hashtags__ = []
    __tweet_mentions__ = []
    __tweet_replies_count__ = 0
    __tweet_favorite_count__ = 0
    __tweet_retweet_count__ = 0

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
    
    def set_tweet_author(self, tweet_author, tweet_author_id):
        self.__tweet_author__ = tweet_author
        self.__tweet_author_id__ = tweet_author_id
    
    def get_tweet_author(self):
        return self.__tweet_author__

    def get_tweet_author_id(self):
        return self.__tweet_author_id__

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

    def __str__(self):
        return "Id:"+self.get_tweet_id()+"\tType:"+self.get_tweet_type()+"\tTime:"+self.get_tweet_time_ms()+\
        "\nAuthor:"+self.get_tweet_author()+"\tAuthorId:"+self.get_tweet_author_id()+\
        "\nText:"+self.get_tweet_text()+\
        "\nLinks:"+str(self.get_tweet_links())+\
        "\nHastags:"+str(self.get_tweet_hashtags())+\
        "\nMentions:"+str(self.get_tweet_mentions())+\
        "\nReplies:"+self.get_tweet_replies_count()+"\tFavorites:"+self.get_tweet_favorite_count()+"\tRetweets:"+self.get_tweet_retweet_count()+"\n"