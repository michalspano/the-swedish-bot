import pandas as pd
import random as r
import json
import discord
import os
import time

from flaskProvider import keep_alive

client = discord.Client()


#  Class to process and embed a message
class EmbedMessage:
    def __init__(self, data, row_count, user):
        self.data, self.row_count = data, row_count
        self.user = user

    def embed_discord_message(self):
        #  Chooses random row index
        random_index = r.randint(0, self.row_count)

        #  Transform all keys from the dict to a list
        keys_list = self.data.keys()

        #  Loads indexed data from dict to a list
        random_data = [self.data[key][random_index] for key in keys_list]
        embed_title = f"@{random_data[3]} tweeted at {random_data[1]} [{random_data[6]}]"

        #  Creates an embedded message with all settings respectively
        embed_message = discord.Embed(title=embed_title, url=random_data[0],
                                      description=random_data[2], colour=discord.Colour.blue())
        embed_message.add_field(name="Number of likes", value=random_data[4], inline=True)
        embed_message.add_field(name="Number of retweets", value=random_data[5], inline=True)
        embed_message.set_footer(text=f"Requested by {self.user}")

        #  Returns an embedded discord object
        return embed_message


class HelpCommands:
    def __init__(self, path):
        self.path = path

    #  Returns the --help command content with discord.Embed()
    def embed_help_commands(self):
        help_commands_desc = str()
        help_data = [line for line in open(self.path, "r").readlines()]
        description_data = help_data[:len(help_data) - 3]
        for data_char in description_data:
            help_commands_desc += data_char

        #  Configuration of discord.Embed() with respective properties
        embed_message = discord.Embed(title="--help command",
                                      description=help_commands_desc,
                                      url=str(os.environ["GITHUB_LINK"]),
                                      color=discord.Color.from_rgb(255, 255, 0))
        embed_message.add_field(name="Twitter profile",
                                value=str(help_data[-2]), inline=True)
        embed_message.add_field(name="Developed by",
                                value=str(help_data[-1]), inline=True)
        embed_message.set_author(name=client.user.display_name,
                                 icon_url=client.user.avatar_url)
        return embed_message


#  Loads data from Google spreadsheet via Google API
def load_secrets(path):
    with open(path, ) as secretsJSON:  # Opens a json file with cred. details
        secrets = json.load(secretsJSON)

    #  Processes the spreadsheet through .csv format and pandas onto a dataFrame
    df = pd.read_csv(f"{secrets['provider']}{secrets['sheet_id']}/export?format=csv")

    #  Returns df in dict() form and the number of rows (index)
    return [df.to_dict(), len(df.index) - 1]


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

    # To do if --start was prompted by a user
    while client_switch:
        #  Loads the returned em. object from the custom class
        obj_instance = load_secrets("secrets.json")
        embed_object = EmbedMessage(obj_instance[0], obj_instance[1],
                                    str(message.author)).embed_discord_message()
        await message.channel.send(embed=embed_object)
        #  Repeats periodically every hour
        time.sleep(int(os.environ["TIME_INTERVAL"]))


client_switch = False
keep_alive()
client.run(os.environ["TOKEN"])
