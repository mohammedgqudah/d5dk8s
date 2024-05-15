import discord
from discord.ext import commands
from d5dk8s.kubernetes import get_pods


class Pods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def pods(self, ctx: discord.ApplicationContext, namespace: str = "default"):
        pods = await get_pods(namespace)
        embed = discord.Embed(title="Pods", color=0x447ceb)
        
        for pod in pods:
            pod_name = pod.get("metadata", {}).get("name")
            pod_status = pod.get("status", {}).get("phase")
            pod_status = pod_status if pod_status == 'Running' else f"~~{pod_status}~~"
            embed.add_field(name=pod_name, value=pod_status, inline=True)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Pods(bot))
