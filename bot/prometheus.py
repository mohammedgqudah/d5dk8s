from bot.config import Config
import aiohttp


session = aiohttp.ClientSession(base_url=Config.get('prometheus.url'))

async def query(_query: str):
    """Performs a prometheus query"""
    resp =  await session.get('/api/v1/query', params={'query': _query})

    return await resp.json()
