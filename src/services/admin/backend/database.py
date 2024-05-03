from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

import env


DB_URL = f"postgresql+asyncpg://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:5432/{env.DB_NAME}"

engine = create_async_engine(DB_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
