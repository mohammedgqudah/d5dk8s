import discord
from discord.ext import commands
from d5dk8s.kubernetes import session


class Pods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def pods(self, ctx: discord.ApplicationContext, namespace: str = "default"):
        url = f"/api/v1/namespaces/{namespace}/pods"
        r = session.get(url)

        print('response', r.json())

        pods = r.json()['items']
        embed = discord.Embed(title="Pods", color=0x447ceb)
        
        for pod in pods:
            pod_name = pod.get("metadata", {}).get("name")
            pod_status = pod.get("status", {}).get("phase")
            pod_status = pod_status if pod_status == 'Running' else f"~~{pod_status}~~"
            embed.add_field(name=pod_name, value=pod_status, inline=True)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Pods(bot))
