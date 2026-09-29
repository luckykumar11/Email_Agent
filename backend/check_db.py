import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect(user='postgres', password='Lucky123', database='email_agent', host='localhost')
    tables = await conn.fetch("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    print(f"Found {len(tables)} tables:")
    for t in tables:
        print(f"  - {t['tablename']}")
    await conn.close()

asyncio.run(check())
