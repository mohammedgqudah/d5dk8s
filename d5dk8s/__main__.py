import pathlib
import argparse
import discord
from d5dk8s.config import Config
from alembic import config, command

parser = argparse.ArgumentParser(
    prog="d5dk8s",
    description="A discord bot that inspects your kubernetes cluster",
)
parser.add_argument('-c', '--config') # yml configuration file
args = parser.parse_args()
if args.config:
    Config.load_config(args.config)

def run_migrations():
    alembic_config = config.Config(pathlib.Path().joinpath('..').joinpath('alembic.ini'))
    db_url = Config.get('database.url')
    # use the sync driver for running the migrations
    db_url = db_url.replace("+asyncpg", "", 1)

    alembic_config.set_main_option('sqlalchemy.url', db_url)
    command.upgrade(alembic_config, 'head')

def run_bot():
    bot = discord.Bot()

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")


    bot.load_extension("d5dk8s.cogs.pods")
    bot.load_extension("d5dk8s.cogs.nodes")
    if Config.get('prometheus.enabled'):
        bot.load_extension("d5dk8s.cogs.prometheus")

    bot.run(Config.get('bot_token'))


run_migrations()
run_bot()
