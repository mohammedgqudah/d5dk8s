import aiohttp
import ssl
from d5dk8s.config import Config

session = aiohttp.ClientSession(base_url=Config.get('api_server'))

token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
ca_cert_path = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'

try:
    with open(token_path, 'r') as f:
        token = f.read().strip()

    # if the bot is running inside a cluster.
    ssl_context = ssl.create_default_context(cafile=ca_cert_path)
    session = aiohttp.ClientSession(base_url=Config.get('api_server'), connector=aiohttp.TCPConnector(ssl=ssl_context))
    session.headers.update({
        'Authorization': f'Bearer {token}',
    })
except FileNotFoundError as e:
    # When running the bot locally through a proxy
    print("Couldn't find the service token");


async def get_pods(namespace: str):
    url = f"/api/v1/namespaces/{namespace}/pods"
    async with session.get(url) as r:
        json = await r.json()
        return json['items']

async def get_nodes():
    url = f"/api/v1/nodes"
    async with session.get(url) as r:
        json = await r.json()
        return json['items']

