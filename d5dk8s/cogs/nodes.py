import discord
from discord.ext import commands
from d5dk8s.kubernetes import get_nodes


class Nodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def nodes(self, ctx: discord.ApplicationContext):
        nodes = await get_nodes()
        embeds = []
        for node in nodes:
            node_name = node.get("metadata", {}).get("name")
            node_arch = node.get("metadata", {}).get("labels").get('beta.kubernetes.io/arch')
            node_os = node.get("metadata", {}).get("labels").get('beta.kubernetes.io/os')
            node_cpu = node.get("status", {}).get("capacity", {}).get('cpu')
            node_memory = node.get("status", {}).get("capacity", {}).get('memory')
            embed = discord.Embed(title=node_name, color=0x447ceb)
            embed.add_field(name='OS', value=f"{node_os}/{node_arch}", inline=True)
            embed.add_field(name='CPU', value=node_cpu, inline=True)
            embed.add_field(name='Memory', value=node_memory)
            embeds.append(embed)

        await ctx.respond(embeds=embeds)

def setup(bot):
    bot.add_cog(Nodes(bot))
