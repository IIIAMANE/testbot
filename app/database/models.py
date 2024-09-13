from sqlalchemy import BigInteger, Text
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

    day: Mapped[int] = mapped_column(default=0, nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
