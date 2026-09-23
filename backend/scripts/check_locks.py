import psycopg2
import os

env_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
with open(env_file) as f:
    for line in f:
        if line.startswith("DATABASE_URL="):
            db_url = line.split("=", 1)[1].strip().strip("'\"")

conn = psycopg2.connect(db_url)
cur = conn.cursor()

tables = ["accounts", "transactions", "alerts", "investigations", "documents", "document_chunks", "model_predictions"]
for t in tables:
    cur.execute(f"SELECT count(*) FROM {t}")
    print(f"Table: {t:20} -> {cur.fetchone()[0]} rows")

cur.execute("SELECT risk_level, count(*) FROM alerts GROUP BY risk_level")
for r in cur.fetchall():
    print(f"Alert risk level {r[0]}: {r[1]}")

cur.close()
conn.close()
