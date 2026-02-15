import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

# Have to add to PATH so models is found
sys.path.append(os.path.dirname(__file__))
from models import Query

async def main():
    engine = create_async_engine(
        'postgresql+asyncpg://neondb_owner:npg_Q0Fb6fCmZsHv@ep-raspy-glade-amnt8dqh.c-5.us-east-1.aws.neon.tech/neondb',
        connect_args={'ssl': True}
    )
    session_maker = async_sessionmaker(engine)
    async with session_maker() as session:
        res = await session.execute(select(Query))
        queries = res.scalars().all()
        for q in queries:
            print(f"ID={q.id} | USER={q.user_id} | STATUS={q.status} | ERR={q.error_message}")
        
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
