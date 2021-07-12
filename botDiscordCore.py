import json
import discord
import os

from discord.ext import commands
from asyncio import sleep as s
from googleapiclient.discovery import build
from google.oauth2 import service_account
from collections import Counter
#  from flaskProvider import keep_alive

bot = commands.AutoShardedBot(commands.when_mentioned_or("--"), help_command=None,
                              activity=discord.Activity(type=discord.ActivityType.listening, name="--help"))


#  Class to process and embed a message
class EmbedMessage:
    def __init__(self, data, user):
        self.data = data
        self.user = user

    def embed_discord_message(self):
        tweet_data = self.data
        embed_title = f"@{tweet_data[3]} tweeted at {tweet_data[1]} [{tweet_data[6].upper()}]"

        #  Creates an embedded message with all settings respectively
        embed_message = discord.Embed(title=embed_title, url=tweet_data[0],
                                      description=tweet_data[2], colour=discord.Colour.blue())
        embed_message.add_field(name="Number of likes", value=tweet_data[4], inline=True)
        embed_message.add_field(name="Number of retweets", value=tweet_data[5], inline=True)
        embed_message.set_footer(text=f"Requested by {self.user}")

        #  Returns an embedded discord object
        return embed_message


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

    #  Embed status command message, only default data from single path (local .txt command description)
    def embed_status_command(self, status=str()):

        #  Reads from a local .txt file with em. description
        for line in open(self.path, "r").readlines():
            status += line

        #  Latency var rounded in milliseconds
        latency = f"{round(bot.latency * (10 ** 3))}ms"

        #  Embed preferences including author, fields, etc
        embed_msg = discord.Embed(title="Status command",
                                  description=status,
                                  url=str(os.environ["GITHUB_LINK"]),
                                  color=discord.Color.dark_blue())

        #  Custom author header
        embed_msg.set_author(name=bot.user.display_name,
                             icon_url=bot.user.avatar_url)

        #  Custom subfield
        embed_msg.add_field(name="Ping: ",
                            value=latency,
                            inline=True)
        return embed_msg


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
@bot.command(aliases=["Status", "status"])
async def bot_status(ctx):
    db_instance = load_secrets("secrets.json")
    tweets_counter = len(db_instance)

    lang_dict = Counter([db_instance[i][-1] for i in range(tweets_counter - 100, tweets_counter)])
    print(lang_dict)

    lang_list = [[key, value] for key, value in lang_dict.items()]
    print(lang_list)

    embed_status_message = Commands("status_command.txt").embed_status_command()
    embed_status_message.add_field(name="Number of tweets",
                                   value=str(tweets_counter),
                                   inline=True)
    await ctx.send(embed=embed_status_message)


# To initialise the bot
@bot.command(aliases=["Start", "start"])
async def start_news_thread(ctx):
    global client_switch
    client_switch = True

    #  Initial thread-enabled message
    await ctx.channel.send(f"{ctx.author.mention} enabled the thread. "
                           f"Use `--stop` to terminate it or `--help`.")
    while client_switch:
        print("Tweeting...")
        #  Loads the returned em. object from the custom class
        tweet_values = load_secrets("secrets.json")
        specified_value = tweet_values[(len(tweet_values) - 1)]
        embed_object = EmbedMessage(specified_value,
                                    str(ctx.author)).embed_discord_message()
        await ctx.channel.send(embed=embed_object)
        await s(int(os.environ["TIME_INTERVAL"]))


# To terminate the bot
@bot.command(aliases=["Stop", "stop"])
async def stop_news_thread(ctx):
    global client_switch
    client_switch = False
    print("Terminating...")
    await ctx.channel.send(f"{ctx.author.mention} disabled the thread. "
                           f"Use `--start` to configure it or `--help`.")


# Help command to config.
@bot.command(aliases=["Help", "help", "h"])
async def help_command(ctx):
    embed_message = Commands(path="help_command.txt").embed_help_commands()
    await ctx.channel.send(embed=embed_message)


client_switch = False
#  keep_alive()
bot.run(os.environ["TOKEN"])
