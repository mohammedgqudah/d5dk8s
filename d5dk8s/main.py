import discord
import os
import requests

bot = discord.Bot()
token = os.getenv('D5DK8S_BOT_TOKEN')
api_server = os.getenv('K8S_API_SERVER')

token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
ca_cert_path = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
with open(token_path, 'r') as f:
    token = f.read().strip()

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}


@bot.slash_command()
async def pods(ctx, name: str = None):
    name = name or ctx.author.name
    url = f"{api_server}/api/v1/namespaces/{name}/pods"
    r = requests.get(url, headers=headers, verify=ca_cert_path)
    print('response', r.text)
    pods = r.json()['items']
    embed = discord.Embed(title="Pods", color=0x00ff00)
    
    for pod in pods:
        pod_name = pod.get("metadata", {}).get("name")
        pod_status = pod.get("status", {}).get("phase")
        embed.add_field(name=pod_name, value=pod_status, inline=False)

    await ctx.respond(embed=embed)

print('Running the bot..')
bot.run(os.getenv('D5DK8S_BOT_TOKEN'))
