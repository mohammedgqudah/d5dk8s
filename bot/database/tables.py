import enum
from sqlalchemy import BigInteger, Column as Col, DateTime, Enum, Integer, String, Table
from .meta import meta


def Column(*args, **kwargs):
    kwargs.setdefault("nullable", False)
    return Col(*args, **kwargs)


class ResourceType(enum.Enum):
    pods = 1


watchers = Table(
    "watchers",
    meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("message_id", BigInteger),
    Column("channel_id", BigInteger),
    Column("guild_id", BigInteger),
    Column("refresh_interval_seconds", Integer),
    Column("last_refresh_time", DateTime, nullable=True),
    Column("resource_type", Enum(ResourceType)),
    Column("namespace", String),
)
