import logging
import argparse
import subprocess
import discord
from bot.config import load_config

logging.basicConfig(level=logging.INFO, format="%(levelname)s [%(name)s] %(message)s")
logging.getLogger("discord").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    prog="kube-inspector-bot",
    description="A discord bot that inspects your kubernetes cluster",
)
parser.add_argument("-c", "--config")  # yml configuration file
args = parser.parse_args()
if args.config:
    load_config(args.config)


from bot.config import config


def run_migrations():
    # I originally used the code below to run alembic, but env.py was messing
    # with the logging module, so i had to use a separate process.

    # alembic_config = ac_config.Config(
    #    pathlib.Path().joinpath("..").joinpath("alembic.ini")
    # )
    # db_url = config.database.url
    ## use the sync driver for running the migrations
    # db_url = db_url.replace("+asyncpg", "", 1)

    # alembic_config.set_main_option("sqlalchemy.url", db_url)
    # command.upgrade(alembic_config, "head")
    subprocess.run(["alembic", "upgrade", "head"], check=True)


def run_bot():
    bot = discord.Bot()

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user}")

    bot.load_extension("bot.cogs.pods")
    bot.load_extension("bot.cogs.nodes")
    if config.prometheus.enabled:
        bot.load_extension("bot.cogs.prometheus")

    bot.run(config.bot_token)


if config.database.url:
    run_migrations()

run_bot()
