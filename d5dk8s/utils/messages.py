from discord import Bot, Message


async def get_message(bot: Bot, guild_id: int, channel_id: int, message_id: int) -> Message:
    guild = await bot.fetch_guild(guild_id, with_counts=False)
    channel = await guild.fetch_channel(channel_id)
    return await channel.fetch_message(message_id)
