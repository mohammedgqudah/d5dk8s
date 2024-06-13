import logging
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio.engine import AsyncConnection
from bot.kubernetes import get_pods
from bot.database.database import engine
from bot.database.tables import ResourceType, watchers
from bot.config import config
from bot.utils.messages import get_message
from bot.utils.pods import pods_to_embeds

logging.basicConfig(level=logging.INFO)
logging.root.setLevel(logging.DEBUG)


async def list_watchers(connection: AsyncConnection):
    """List all watchers"""
    result = await connection.execute(watchers.select())
    return result.fetchall()


class Pods(commands.Cog):
    bot: discord.Bot

    def __init__(self, bot):
        self.bot = bot
        self.update_watchers.start()

    pods = discord.SlashCommandGroup(name="pods", guild_ids=config.guild_ids)

    @pods.command(name="list")
    async def _list(
        self, ctx: discord.ApplicationContext, namespace: str = "default"
    ) -> discord.Interaction | discord.WebhookMessage:
        pods = await get_pods(namespace)

        return await ctx.respond(embeds=pods_to_embeds(pods))

    @pods.command(
        name="watch",
        description="Monitor pods by sending a message that refreshes at the specified interval",
    )
    async def watch(
        self,
        ctx: discord.ApplicationContext,
        namespace: str,
        refresh_interval: discord.Option(int, description="In minutes"),
    ):
        """Register a new watcher for pods."""
        pods = await get_pods(namespace)

        # the interaction response cannot be edited, as a workaround, the interaction
        # will be acknowledged and another message will be sent containing a list of pods
        await ctx.respond(":white_check_mark: Watcher added.", ephemeral=True)
        message = await ctx.channel.send(embeds=pods_to_embeds(pods))

        async with engine.connect() as conn:
            # insert a new watcher, which will be periodically checked in `self.update_watchers`
            stmt = insert(watchers).values(
                message_id=message.id,
                channel_id=message.channel.id,
                guild_id=message.guild.id,
                refresh_interval_seconds=refresh_interval * 60,
                resource_type=ResourceType.pods,
                last_refresh_time=datetime.now(),
                namespace=namespace,
            )
            await conn.execute(stmt)
            await conn.commit()

    @tasks.loop(minutes=1)
    async def update_watchers(self):
        async with engine.connect() as conn:
            result = await list_watchers(conn)
            logging.info(f"found {len(result)} watchers")

            for watcher in result:
                time_since_last_refresh: timedelta = (
                    datetime.now() - watcher.last_refresh_time
                )
                if time_since_last_refresh.seconds > watcher.refresh_interval_seconds:
                    logging.info(
                        f"updating watcher #{watcher.id} for namespace {watcher.namespace}"
                    )
                    message = await get_message(
                        self.bot,
                        watcher.guild_id,
                        watcher.channel_id,
                        watcher.message_id,
                    )

                    pods = await get_pods(watcher.namespace)
                    await message.edit(embeds=pods_to_embeds(pods))

                    stmt = (
                        update(watchers)
                        .where(watchers.c.id == watcher.id)
                        .values(last_refresh_time=datetime.now())
                    )
                    await conn.execute(stmt)
                    await conn.commit()


def setup(bot):
    bot.add_cog(Pods(bot))
