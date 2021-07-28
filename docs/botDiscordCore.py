import json
import discord
import os

from discord import Embed
from discord.ext import commands
from asyncio import sleep as s
from googleapiclient.discovery import build
from google.oauth2 import service_account
from collections import Counter

from flaskProvider import keep_alive

bot = commands.AutoShardedBot(commands.when_mentioned_or("--"), help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="--help"))


#  Universal class for respective commands (and their embeds)
class Commands:
    def __init__(self, path):
        self.path = path

    #  Returns the --help command content with discord.Embed()
    def embed_help_commands(self):
        help_commands_desc = str()

        #  Read from a local .txt with corresponding data
        help_data = [line for line in open(self.path, "r").readlines()]

        #  Description data without last 3 lines (redundant \n, 2 hyperlink profiles)
        description_data = help_data[:len(help_data) - 3]
        for data_char in description_data:
            help_commands_desc += data_char

        #  Configuration of discord.Embed() with respective properties
        embed_message = discord.Embed(title="Help command",
                                      description=help_commands_desc,
                                      url=str(os.environ["GITHUB_LINK"]),
                                      color=discord.Color.from_rgb(255, 255, 0))

        #  Additional fields with hyperlinked profiles
        embed_message.add_field(name="Twitter profile",
                                value=str(help_data[-2]), inline=True)
        embed_message.add_field(name="Developed by",
                                value=str(help_data[-1]), inline=True)

        #  Author and icon set via client's cred. data
        embed_message.set_author(name=bot.user.display_name,
                                 icon_url=bot.user.avatar_url)
        return embed_message

    def embed_discord_message(self, user):
        tweet_data = self.path
        embed_title = f"@{tweet_data[3]} tweeted at {tweet_data[1]} [{tweet_data[6].upper()}]"

        #  Creates an embedded message with all settings respectively
        embed_message = discord.Embed(title=embed_title, url=tweet_data[0],
                                      description=tweet_data[2], colour=discord.Colour.blue())
        embed_message.add_field(name="Number of likes", value=tweet_data[4], inline=True)
        embed_message.add_field(name="Number of retweets", value=tweet_data[5], inline=True)
        embed_message.set_footer(text=f"Requested by {user}")

        #  Returns an embedded discord object
        return embed_message

    #  Embed status command message, only default data from single path (local .txt command description)
    def embed_status_message(self, db, status=str()):

        #  Reads from a local .txt file with em. description
        for line in open(self.path, "r").readlines():
            status += line

        #  Latency var rounded in milliseconds
        latency = f"{round(bot.latency * (10 ** 3))}ms"

        #  Number of rows in the database
        tweets_counter = len(db)

        #  Lang. parameter from the latest 100 submissions ordered in a dict.
        lang_dict = Counter([db[i][-1] for i in range(tweets_counter - 100, tweets_counter)])

        #  Transformed dict. to a list
        lang_list = [[value, key] for key, value in lang_dict.items()]

        #  The most frequent lang value
        max_lang = max(lang_list)[1]

        def assign_values():
            #  Embed preferences including author, fields, etc
            embed_message: Embed = discord.Embed(title="Status command",
                                                 description=status,
                                                 url=str(os.environ["GITHUB_LINK"]),
                                                 color=discord.Color.dark_blue())

            #  Custom author header
            embed_message.set_author(name=bot.user.display_name,
                                     icon_url=bot.user.avatar_url)
            #  Embed message fields
            embed_message.add_field(name="🔊 | Ping: ",
                                    value=latency,
                                    inline=True)
            #  Custom message field with the number of tweets from the database
            embed_message.add_field(name="✍️ | Number of tweets",
                                    value=str(tweets_counter),
                                    inline=True)

            #  Custom message field with the dominant language from the parsed tweets
            embed_message.add_field(name="🗣 | Dominant language: ",
                                    value=max_lang,
                                    inline=True)
            return embed_message
        return assign_values()


#  Loads data from Google spreadsheet via Google API
def load_secrets(path):
    #  Loads from .json module
    with open(path, ) as secretsJSON:
        secrets = json.load(secretsJSON)

    #  Service credentials configuration
    SERVICE_ACCOUNT_FILE = secrets["creds"]
    SCOPES = secrets["scope"]

    #  API credentials with valid scope
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,
                                                                        scopes=SCOPES)
    #  Spread sheet ID number
    SAMPLE_SPREAD_SHEET_ID = secrets["sheet_id"]
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    #  Resulting output with specified ID and range selection
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREAD_SHEET_ID,
                                range="Sheet1!A:G").execute()

    #  Creates a list instance from result scope
    values = result.get("values", [])

    #  Returns the latest thread
    return values


#  Initial bot load status
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


#  Status latency command
@bot.command(aliases=["Status", "status", "s"])
async def bot_status(ctx):
    final_em_status_msg = Commands("data/status_command.txt").embed_status_message(db=load_secrets("secrets.json"))
    await ctx.send(embed=final_em_status_msg)


#  Load data method
@bot.command(aliases=["Load", "load", "l"])
async def load_tweet_msg(ctx, operator: str = None, count: int = 5, time: float = 5):
    db_instance = load_secrets("ignore/secrets.json")

    #  Primitive load
    if operator is None:
        instance = db_instance[-1]
        embed_message = Commands(instance).embed_discord_message(user=ctx.author)
        await ctx.send(embed=embed_message)

    #  Complex load
    elif operator == "recent" or operator == "r":
        for i in range(count):
            instance = db_instance[-1 - i]
            embed_message = Commands(instance).embed_discord_message(user=ctx.author)
            await ctx.send(embed=embed_message)
            await s(time)


# Help command to config.
@bot.command(aliases=["Help", "help", "h"])
async def help_command(ctx):
    embed_message = Commands(path="data/help_command.txt").embed_help_commands()
    await ctx.channel.send(embed=embed_message)


keep_alive()
bot.run(os.environ["TOKEN"])
