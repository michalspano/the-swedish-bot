import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} is ready.")


client.run(os.environ["TOKEN"])
