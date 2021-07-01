#  Libs to be used
import logging
import tweepy
import time
from config import export_API

logger = logging.getLogger()


# class TwitterMethods(tweepy.StreamListener):
#     def __init__(self, api):
#         super().__init__(api)
#         self.api = api
#         self.me = api.me()
#
#     def on_status(self, status):
#         print(f"Processing tweet id {status.id}")
#         if status.in_reply_to_status_id is not None or \
#                 status.user.id == self.me.id:
#             return
#         tweet_text = str(status.full_text.lower().encode('ascii', errors='ignore'))
#         if tweet_text.startswith("rt @"):
#             print("This is a retweet")
#         if not status.favorited:
#             # Mark it as Liked, since we have not done it yet
#             status.favorite()
#         if not status.retweeted:
#             status.retweet()
#
#     def on_error(self, status):
#         logger.error(status)

class TwitterDataModel:
    def __init__(self, api, keyword):
        self.api = api
        self.keyword = keyword

    def export_twitter_data(self):
        tweets = [tweet for tweet in tweepy.Cursor(self.api.search,
                                                   q=f"{self.keyword}-filter:retweets",
                                                   tweet_mode="extended").items(15)]
        i = 0
        while i < len(tweets):
            tweet = tweets[i]
            i += 1
            tweet_status_retweeted = self.api.get_status(tweet.id).retweeted
            if not tweet_status_retweeted:
                tweet.retweet()
                print(f"Retweeted at: {tweet.id}")
                break


def main(key_tags):
    api = export_API()
    while True:
        TwitterDataModel(api, key_tags).export_twitter_data()
        time.sleep(20)
    # tweet_handler = TwitterMethods(api)
    # stream = tweepy.Stream(api.auth, tweet_handler)
    # stream.filter(track=key_tags)


if __name__ == "__main__":
    main("#Sweden")
