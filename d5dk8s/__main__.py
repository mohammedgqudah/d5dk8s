import os
import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.load_extension("d5dk8s.cogs.pods")
bot.load_extension("d5dk8s.cogs.nodes")

print('Running the bot..')

bot.run(os.getenv('D5DK8S_BOT_TOKEN'))
