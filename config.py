import tweepy
import logging
import os

logger = logging.getLogger()


def export_API():
    consumer_key, consumer_secret = os.environ["API_KEY"], os.environ["API_SECRET_KEY"]
    access_token, access_secret = os.environ["ACCESS_TOKEN"], os.environ["ACCESS_SECRET_TOKEN"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if api.verify_credentials():
        return api
    else:
        logger.error("Error, no API was created.", exc_info=True)
