#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/bot.py

from os import getenv
from json import load
from asyncio import sleep
from typing import Final
from collections import Counter
from dotenv import load_dotenv

from google.oauth2 import service_account
from googleapiclient.discovery import build
from discord.ext import commands
from discord import Embed, Activity, ActivityType, Color

from utils.app import alive
from utils.utils import format_row_data

COMMAND_PREFIX: Final[str] = "--"
bot: commands.AutoShardedBot = commands.AutoShardedBot(
    commands.when_mentioned_or(COMMAND_PREFIX), 
    help_command=None,      # ensures that we may use the 'help' command
    activity=Activity(
        type=ActivityType.listening, 
        name=f"{COMMAND_PREFIX}help"
    )
)

class Custom_commands:
    def embed_help_commands(path: str = 'data/help_cmd.md') -> Embed:
        help_data: list = [line.strip() for line in open(path)]

        EMBED: Embed = Embed(
            title="Help command",
            description='\n'.join(help_data[:-3]),
            url='https://github.com/michalspano',
            color=Color.from_rgb(255, 255, 0)
        )
        EMBED.add_field(
            name="Twitter profile",
            value=help_data[-2], inline=True
        )
        EMBED.add_field(
            name="Developed by",
            value=help_data[-1], 
            inline=True
        )
        EMBED.set_author(
            name=bot.user.display_name,
            icon_url=bot.user.avatar_url
        )
        return EMBED

    def embed_discord_message(tweet_data: dict, user: str) -> Embed:
        embed_title: str = f"@{tweet_data['user']} tweeted at {tweet_data['date']} [{tweet_data['lang'].upper()}]"

        EMBED: Embed = Embed(
            title=embed_title, 
            url=tweet_data['url'],
            description=tweet_data['data'], 
            color=Color.blue()
        )
        EMBED.add_field(
            name="Number of likes", 
            value=tweet_data['likes'], 
            inline=True
        )
        EMBED.add_field(
            name="Number of retweets", 
            value=tweet_data['retweets'], 
            inline=True
        )
        EMBED.set_footer(text=f"Requested by {user}")
        return EMBED

    def embed_status_message(path: str = 'data/stats_cmd.md', db: list = []) -> Embed:
        # read the message from the local `.md` file
        status_msg: list = [line.strip() for line in open(path)]

        # parse the latency of the bot and round to 3 decimal places
        latency: str = f"{round(bot.latency * (10 ** 3))}ms"

        # get the average length of the tweets in the database from the current entry
        avg_len: int = sum(len(format_row_data(tweet)['data']) for tweet in db) // len(db)

        # get the languages to a Counter object and get the most occuring language
        lang_dict: object = Counter([format_row_data(db[idx])['lang'] for idx in range(len(db))])
        max_lang: str = max(lang_dict, key=lang_dict.get)

        embed_message: Embed = Embed(
            title="Status command",
            description=f'\n'.join(status_msg) + 
                        f'\n📊 | Parsing the latest **{len(db)}** tweets.',
            url='https://github.com/michalspano',
            color=Color.dark_blue()
        )
        embed_message.set_author(
            name=bot.user.display_name,
            icon_url=bot.user.avatar_url
        )
        embed_message.add_field(
            name="🔊 | Ping: ",
            value=latency,
            inline=True
        )
        '''
        TODO: fix the number of tweets method
        the 'number of tweets' field is currently paused due to
        memory issues with the bot; the database has eventually become
        too large to be stored in memory, thus causing the bot to be 
        extremely slow.
        '''
        # embed_message.add_field(
        #     name="✍️ | Number of tweets: ",
        #     value=str(tweets_counter),
        #     inline=True
        # )
        embed_message.add_field(
            name=f"🗣 | Dominant language: ",
            value=max_lang,
            inline=True
        )
        embed_message.add_field(
            name="📈 | Average tweet length: ",
            value=f'{avg_len} characters',
            inline=True
        )
        return embed_message


# TODO: add valid type check for all the variables
def load_secrets(path: str = 'private/secrets.json', data_range: int = 1) -> list:
    secrets: object = load(open(path))

    SPREAD_SHEET_ID: Final[str] = secrets["sheet_id"]
    
    # load API credentials with valid scope
    credentials = service_account.Credentials.\
        from_service_account_file(secrets["creds"], scopes=secrets["scope"])

    # load the sheet service
    sheet = build(
        "sheets", "v4", 
        credentials=credentials
    ).spreadsheets()

    number_of_rows: int = len(sheet.values().get(
        spreadsheetId=SPREAD_SHEET_ID,
        range="A:A"
    ).execute().get("values", []))

    # parse the desired range of rows from the sheet
    RANGE: Final[str] = f"A{number_of_rows - data_range + 1}:G{number_of_rows}"

    # get the data from the sheet with the range and return the values 
    # as a list of lists
    result = sheet.values().get(
        spreadsheetId=SPREAD_SHEET_ID,
        range=f"Sheet1!{RANGE}"
    ).execute()
    return result.get("values", [])


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")


@bot.command(aliases=["h", "help", "Help"])
async def help_command(ctx) -> None:
    print(type(ctx))
    await ctx.channel.send(embed=Custom_commands.embed_help_commands())


@bot.command(aliases=["Status", "status", "st"])
async def bot_status(ctx, count: int = 100) -> None:
    final_em_status_msg: Embed = Custom_commands.embed_status_message(
        db=load_secrets(data_range=count) # default data range is 100
    )
    await ctx.send(embed=final_em_status_msg)


@bot.command(aliases=["Load", "load", "l"])
async def load_tweet_msg(ctx, operator: str = None, count: int = 5, time: float = 5.0) -> None:
    if operator is None:
        instance: dict = format_row_data(load_secrets()[0])
        embed_message: Embed = Custom_commands.\
            embed_discord_message(instance, ctx.author)
        await ctx.send(embed=embed_message)

    elif operator == "recent" or operator == "r":
        if count > 20:
            await ctx.reply(
                "The maximum number of tweets to load is 20."
            ), await ctx.message.add_reaction(emoji="\U0001F44E")   # :thumbsdown:
            return
        await ctx.message.add_reaction(emoji="\U0001F44D")          # :+1: emoji
        db_instance: list = load_secrets(data_range=count)
        for idx in range(count):
            instance: dict = format_row_data(db_instance[idx])
            embed_message: Embed = Custom_commands.\
                embed_discord_message(instance, ctx.author)
            await ctx.send(embed=embed_message), await sleep(time)


alive(), load_dotenv()
bot.run(getenv("TOKEN"))
