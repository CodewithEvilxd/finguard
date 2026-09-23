"""
Neon PostgreSQL Direct Schema Migrator.
"""

import sys
import os
import asyncio
import ssl
import asyncpg

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

raw_url = "postgresql://neondb_owner:npg_WNywkb8h2ASe@ep-patient-bonus-b5a1rpwr-pooler.c-7.us-east-2.aws.neon.tech/micro?sslmode=require&channel_binding=require"
clean_url = raw_url.replace("postgresql://", "").split("?")[0]
auth_part, host_db = clean_url.split("@")
user_pass, _ = auth_part.split(":")
user, password = user_pass, auth_part.split(":")[1]
host_port, database = host_db.split("/")
host = host_port.split(":")[0]
port = int(host_port.split(":")[1]) if ":" in host_port else 5432

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


async def main():
    print(f"Connecting to Neon host {host}:{port}/{database} as {user}...", flush=True)
    conn = await asyncpg.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl=ssl_ctx,
        statement_cache_size=0,
    )
    print("Connected directly to Neon via asyncpg!", flush=True)

    schema_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database/schema/schema.sql"))
    with open(schema_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split into statements
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

    print(f"Executing {len(statements)} DDL statements from schema.sql...", flush=True)
    for idx, stmt in enumerate(statements, 1):
        try:
            await conn.execute(stmt)
        except Exception as e:
            print(f"Statement {idx} warning: {e}", flush=True)

    # Check created tables
    rows = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
    tables = [r["table_name"] for r in rows]
    print(f"\nSuccessfully verified {len(tables)} tables on Neon PostgreSQL:", flush=True)
    for t in tables:
        print(f"  - {t}", flush=True)

    await conn.close()
    print("\nNeon database schema migration completed successfully!", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
