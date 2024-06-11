from sqlalchemy.ext.asyncio import create_async_engine
from bot.config import Config

engine = create_async_engine(Config.get('database.url'), echo=False)
