#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/main.py

from discord import Client
from tweepy import Cursor, API, models
from gspread import service_account

from utils.app import alive
from config import export_API
from utils.utils import logger

from time import sleep
from typing import Final, List

client: Client = Client()

class DataScrapeModel:
    def __init__(self, api: API, keyword: str, lang: list, tweet_range: int):
        self.api: API = api
        self.keyword: str = keyword
        self.lang: list = lang
        self.tweet_range: int = tweet_range
    
    def export_twitter_data(self) -> None:
        query: str = f"{self.keyword} -filter:retweets lang:{self.lang[0]} OR lang:{self.lang[1]}"

        # a list of tweets with the Cursor
        tweets: list = [tweet for tweet in Cursor(
            self.api.search_tweets, # search replaced with search_tweets
            q=query,                # pass in the query
            count=20,               # rpp replaced with count; https://github.com/tweepy/tweepy/issues/858
            result_type="recent", 
            tweet_mode="extended"
        ).items(self.tweet_range)]

        for tweet in tweets:
            tweet_status: models.Status() = self.api.get_status(tweet.id)

            '''
            Parse the tweet if only these conditions are met:
            1. The tweet is not retweeted by the bot
            2. The tweet is not liked by the bot
            3. The tweet is doesn't contain any sensitive content
            Then, we append it to the DB, retweet & like, log it.
            '''

            if not tweet_status.retweeted and not tweet_status.favorited:

                GoogleSpreadSheet(tweet).format_tweet()
                tweet.favorite(), tweet.retweet()
                logger(tweet.id)
                break 


# Custom Google Spreadsheets API module
class GoogleSpreadSheet:
    def __init__(self, tweet: models.Status) -> None:
        self.tweet: models.Status = tweet
        self.gs = service_account(filename="private/credentials.json")
        self.sheet = self.gs.open("@TheSwedishBot-spreadsheet").sheet1

    # format data and write to spreadsheet
    def format_tweet(self) -> None:
        display_user_name: str = self.tweet.user.screen_name
        url_f: str = f"https://twitter.com/{display_user_name}/status/{self.tweet.id}"

        sh_data: list = [url_f, str(self.tweet.created_at), self.tweet.full_text,
                         display_user_name, self.tweet.favorite_count,
                         self.tweet.retweet_count, self.tweet.lang]
                         
        # append to the sheet
        self.sheet.append_row(sh_data)


def main(key_tags: list, lang: list, interval: int) -> None:
    api: API = export_API()
    while 1:
        print("\tParsing tweets")
        DataScrapeModel(api, key_tags, lang, 15).export_twitter_data()
        sleep(interval)


if __name__ == "__main__":
    LANG_SCOPE:     Final[List[str]] = ["en", "sv"]
    KEY_TAGS:       Final[List[str]] = ["#sweden", "#swedish"]
    TIME_INTERVAL:  Final[int]       = 60 ** 2 # an hour

    alive()
    main((" OR ").join(KEY_TAGS), LANG_SCOPE, TIME_INTERVAL)
