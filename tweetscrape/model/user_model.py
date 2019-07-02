
class UserInfo:
    __user_handle__ = None
    __user_name__ = None
    __user_bio__ = None
    __user_location__ = None
    __user_location_id__ = None
    __user_url__ = None
    __user_tweets__ = 0
    __user_following__ = 0
    __user_followers__ = 0
    __user_favorites__ = 0

    def __init__(self, user_handle, user_name, user_bio, user_location, user_location_id,
                 user_url, user_tweets, user_following, user_followers, user_favorites):
        self.__user_handle__ = user_handle
        self.__user_name__ = user_name
        self.__user_bio__ = user_bio
        self.__user_location__ = user_location
        self.__user_location_id__ = user_location_id
        self.__user_url__ = user_url
        self.__user_tweets__ = user_tweets
        self.__user_following__ = user_following
        self.__user_followers__ = user_followers
        self.__user_favorites__ = user_favorites

    def get_user_handle(self):
        return self.__user_handle__

    def get_user_name(self):
        return self.__user_name__

    def get_json(self):
        return {
            "username": self.__user_handle__,
            "name": self.__user_name__,
            "bio": self.__user_bio__,
            "location": self.__user_location__,
            "location_id": self.__user_location_id__,
            "url": self.__user_url__,
            "tweets": self.__user_tweets__,
            "following": self.__user_following__,
            "followers": self.__user_followers__,
            "favorites": self.__user_favorites__
        }
