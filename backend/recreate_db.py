import asyncio, asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.models.user import User
from app.models.company import Company, ServiceProduct, TargetCustomer, ValueProposition, SocialLink
from app.models.email_config import EmailConfiguration
from app.models.signature import EmailSignature
from app.models.preferences import EmailPreference
from app.models.email_history import EmailHistory

async def recreate():
    conn = await asyncpg.connect(user='postgres', password='Lucky123', database='email_agent', host='localhost')
    tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    for t in tables:
        name = t['tablename']
        await conn.execute(f'DROP TABLE IF EXISTS {name} CASCADE')
        print(f'Dropped {name}')
    await conn.close()
    print('All old tables dropped')

    engine = create_async_engine('postgresql+asyncpg://postgres:Lucky123@localhost:5432/email_agent')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('All new tables created successfully')
    await engine.dispose()

asyncio.run(recreate())
