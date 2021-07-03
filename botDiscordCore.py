import json
import discord
import os
import time

from googleapiclient.discovery import build
from google.oauth2 import service_account
from flaskProvider import keep_alive

client = discord.Client()


#  Class to process and embed a message
class EmbedMessage:
    def __init__(self, data, user, switch):
        self.data = data
        self.user = user
        self.switch = switch

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


class HelpCommands:
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
        embed_message = discord.Embed(title="--help command",
                                      description=help_commands_desc,
                                      url=str(os.environ["GITHUB_LINK"]),
                                      color=discord.Color.from_rgb(255, 255, 0))

        #  Additional fields with hyperlinked profiles
        embed_message.add_field(name="Twitter profile",
                                value=str(help_data[-2]), inline=True)
        embed_message.add_field(name="Developed by",
                                value=str(help_data[-1]), inline=True)

        #  Author and icon set via client's cred. data
        embed_message.set_author(name=client.user.display_name,
                                 icon_url=client.user.avatar_url)
        return embed_message


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
    last_index = len(values) - 1

    #  Returns the latest thread
    return values[last_index]


@client.event
async def on_ready():
    #  Bot log. detection
    await client.change_presence(activity=discord.Game(name="--help"))
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message, start_method="--"):
    global client_switch

    #  Stop to prevent bot replying to itself
    if message.author == client.user:
        return

    #  Detect if a message starts with the default intend
    if message.content.startswith(start_method):
        user_message = message.content[2:].replace(" ", "")

        # To initialise the bot
        if user_message == "start":
            client_switch = True

        # To terminate the bot
        elif user_message == "stop":
            client_switch = False

        # Help command to config.
        elif user_message == "help":
            embed_message = HelpCommands("help_command.txt").embed_help_commands()
            await message.channel.send(embed=embed_message)

        while client_switch:
            print("Tweeting...")
            #  Loads the returned em. object from the custom class
            embed_object = EmbedMessage(load_secrets("secrets.json"),
                                        str(message.author), client_switch).embed_discord_message()
            await message.channel.send(embed=embed_object)
            time.sleep(3600)


client_switch = False
keep_alive()
client.run(os.environ["TOKEN"])
