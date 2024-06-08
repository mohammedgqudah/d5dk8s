import logging
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from sqlalchemy import Row, insert, update
from d5dk8s.kubernetes import get_pods
from d5dk8s.database.database import engine
from d5dk8s.database.tables import ResourceType, watchers
from d5dk8s.config import Config
from d5dk8s.utils.helpers import chunk

logging.basicConfig(level=logging.INFO)
logging.root.setLevel(logging.DEBUG)


async def list_watchers():
    async with engine.connect() as conn:
        result = await conn.execute(watchers.select())
    return result.fetchall()

def pods_to_embed(pods):
    """Create an embed containing a list of pods."""
    embed = discord.Embed(title="Pods", color=0x447ceb)
    
    for pod in pods:
        pod_name = pod['metadata']['name']
        pod_status = pod['status']['phase']
        pod_status = pod_status if pod_status == 'Running' else f"~~{pod_status}~~"
        embed.add_field(name=pod_name, value=pod_status, inline=True)
    return embed


def pods_to_embeds(pods):
    """Return a list of embeds containing all pods"""
    embeds = []
    # a single embed can only contain 25 fields
    for pods_chunk in chunk(pods, 25):
        embeds.append(pods_to_embed(pods_chunk))

    return embeds

class Pods(commands.Cog):
    bot: discord.Bot

    def __init__(self, bot):
        self.bot = bot
        self.update_watchers.start()

    pods = discord.SlashCommandGroup(name="pods", guild_ids=Config.get('guild_ids'))

    @pods.command(name="list")
    async def _list(self, ctx: discord.ApplicationContext, namespace: str = "default") -> discord.Interaction | discord.WebhookMessage:
        pods = await get_pods(namespace)

        return await ctx.respond(embeds=pods_to_embeds(pods))

    @pods.command(name="watch", description="Monitor pods by sending a message that refreshes at the specified interval")
    async def watch(self, ctx: discord.ApplicationContext, namespace: str, refresh_interval: discord.Option(int, description="In minutes")):
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

    @tasks.loop(seconds=10)
    async def update_watchers(self):
        result = await list_watchers()
        logging.info(f"found {len(result)} watchers")

        async with engine.connect() as conn:
            for watcher in result:
                time_since_last_refresh: timedelta = (datetime.now() - watcher.last_refresh_time)
                if time_since_last_refresh.seconds > watcher.refresh_interval_seconds:
                    logging.info(f"updating watcher #{watcher.id} for namespace {watcher.namespace}")

                    guild = await self.bot.fetch_guild(watcher.guild_id, with_counts=False)
                    channel = await guild.fetch_channel(watcher.channel_id)
                    message = await channel.fetch_message(watcher.message_id)

                    pods = await get_pods(watcher.namespace)
                    await message.edit(embeds=pods_to_embeds(pods))

                    # update the watcher
                    stmt = update(watchers).where(watchers.c.id == watcher.id).values(last_refresh_time=datetime.now())
                    await conn.execute(stmt)
                    await conn.commit()


def setup(bot):
    bot.add_cog(Pods(bot))
