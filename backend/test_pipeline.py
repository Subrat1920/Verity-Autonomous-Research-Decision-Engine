import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

sys.path.append(os.path.dirname(__file__))
from models import Query, SubQuestion, ResearchStep, FinalReport
from services.research_pipeline import run_research_pipeline
import uuid

async def create_query():
    engine = create_async_engine(
        'postgresql+asyncpg://neondb_owner:npg_Q0Fb6fCmZsHv@ep-raspy-glade-amnt8dqh.c-5.us-east-1.aws.neon.tech/neondb',
        connect_args={'ssl': True}
    )
    session_maker = async_sessionmaker(engine)
    async with session_maker() as session:
        # Get first user
        q = await session.execute(select(Query).limit(1))
        first_q = q.scalar_one_or_none()
        if not first_q:
            print("No users found")
            return
            
        new_query = Query(
            user_id=first_q.user_id,
            raw_query="What are the economic impacts of quantum computing in the next decade?",
            status="pending"
        )
        session.add(new_query)
        await session.commit()
        await session.refresh(new_query)
        
        query_id_str = str(new_query.id)
        
    await engine.dispose()
    print(f"Created query: {query_id_str}")
    run_research_pipeline(query_id_str)
    
if __name__ == "__main__":
    asyncio.run(create_query())
