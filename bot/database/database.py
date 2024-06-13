from sqlalchemy.ext.asyncio import create_async_engine
from bot.config import config

engine = create_async_engine(config.database.url, echo=False)
