import os
import argparse
import discord
from d5dk8s.config import Config

parser = argparse.ArgumentParser(
    prog="d5dk8s",
    description="A discord bot that inspect your kubernetes cluster",
)
parser.add_argument('-c', '--config') # yml configuration file
args = parser.parse_args()
if args.config:
    Config.load_config(args.config)

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.load_extension("d5dk8s.cogs.pods")
bot.load_extension("d5dk8s.cogs.nodes")
if Config.get('prometheus.enabled'):
    bot.load_extension("d5dk8s.cogs.prometheus")

print('Running the bot..')

bot.run(Config.get('bot_token'))
