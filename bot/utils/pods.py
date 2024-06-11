import discord

from bot.utils.helpers import chunk

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
