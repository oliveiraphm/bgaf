from dotenv import load_dotenv 
import os 
from entities import Base
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Annotated
from database import engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_async_engine(database_url, echo=True) 

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False
)

async def get_db_session():
    try:
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]