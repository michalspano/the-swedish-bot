#  Libs to be used
import tweepy
import time
import gspread
import discord
from config import export_API
from flaskProvider import keep_alive
from datetime import datetime as dt

client = discord.Client()


#  Custom Twitter model
class TwitterDataModel:
    def __init__(self, api, keyword, lang, tweet_range):
        self.api = api
        self.keyword, self.lang = keyword, lang
        self.tweet_range = tweet_range

    #  Loads tweets via tweepy.Cursor with specified settings
    def export_twitter_data(self):
        query = f"{self.keyword} -filter:retweets lang:{self.lang[0]} OR lang:{self.lang[1]}"
        tweets = [tweet for tweet in tweepy.Cursor(self.api.search,
                                                   q=query,
                                                   rpp=20,
                                                   result_type="recent",
                                                   tweet_mode="extended").items(self.tweet_range)]
        #  Loops through tweets from the scope
        for tweet in tweets:
            tweet_status = self.api.get_status(tweet.id)
            retweeted, liked = tweet_status.retweeted, tweet_status.favorited
            #  Likes and retweets a tweet if: no like and no retweet previously
            if not retweeted and not liked:

                #  Calls the Google spreadsheet module
                GoogleSpreadSheet(tweet).format_tweet()
                tweet.favorite(), tweet.retweet()
                print(f"{time_module()}; retweeted {tweet.id}")
                #  Breaks the loop if feasible tweet returned
                break


# Custom Google Spreadsheets API module
class GoogleSpreadSheet:
    def __init__(self, tweet):
        self.tweet = tweet
        self.gs = gspread.service_account(filename="credentials.json")
        self.sh = self.gs.open("@TheSwedishBot-spreadsheet").sheet1

    #  Appends selected data to a database via Google spreadsheets through credentials.json as gs
    def format_tweet(self):
        display_user_name = self.tweet.user.screen_name
        url_f = f"https://twitter.com/{display_user_name}/status/{self.tweet.id}"
        favorite_count, retweet_count = self.tweet.favorite_count, self.tweet.retweet_count
        sh_data = [url_f, str(self.tweet.created_at), self.tweet.full_text,
                   display_user_name, favorite_count,
                   retweet_count, self.tweet.lang]
        #  Appends a single row as a list
        self.sh.append_row(sh_data)
        return


#  Current time module function
def time_module():
    time_now = dt.now().strftime("%d. %m. (%A) - %H:%M:%S")
    return time_now


#  Main function looped in a time interval
def main(key_tags, lang, time_interval):
    api = export_API()
    while True:
        print("**Parsing tweets**\n")
        TwitterDataModel(api, key_tags, lang, 15).export_twitter_data()
        time.sleep(time_interval)


#  Main loop with keywords and time limit
if __name__ == "__main__":
    keep_alive()
    main("#Sweden OR #Sverige", ["en", "sv"], (60 * 60))
