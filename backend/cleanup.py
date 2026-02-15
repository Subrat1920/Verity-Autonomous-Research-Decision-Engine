import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import update

sys.path.append(os.path.dirname(__file__))
from models import Query, QueryStatus

async def main():
    engine = create_async_engine(
        'postgresql+asyncpg://neondb_owner:npg_Q0Fb6fCmZsHv@ep-raspy-glade-amnt8dqh.c-5.us-east-1.aws.neon.tech/neondb',
        connect_args={'ssl': True}
    )
    session_maker = async_sessionmaker(engine)
    async with session_maker() as session:
        await session.execute(
            update(Query)
            .where(Query.status.in_([QueryStatus.PENDING, QueryStatus.PROCESSING]))
            .values(status=QueryStatus.FAILED, error_message='Interrupted. Stuck query reset to FAILED.')
        )
        await session.commit()
    await engine.dispose()
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())
