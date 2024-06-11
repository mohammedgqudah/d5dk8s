from typing import Optional
import discord
from discord.ext import commands
from bot import prometheus as prom

class Prometheus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def temperature(self, ctx: discord.ApplicationContext, node: Optional[str] = None):
        """Returns the temperature for all nodes from the node exporter hwmonitor metrics"""
        resp = await prom.query('node_hwmon_temp_celsius')
        result = resp.get('data').get('result')

        # list all nodes or only the specified node
        nodes = {
            _node['metric']['node']
            for _node in result
            if node is None or _node['metric']['node'] == node
        }

        embed = discord.Embed(title="Temperature", color=0x447ceb)

        # for each _node, add a field for each sensor in this format: node/sensor
        for _node in nodes:
            for sensor in result:
                if sensor['metric']['node'] == _node:
                    temp = float(sensor['value'][1])
                    embed.add_field(name=_node + "/" + sensor['metric']['sensor'], value=f"{temp:.2f}")

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Prometheus(bot))
