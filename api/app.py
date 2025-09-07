import os
import contextlib
import psycopg
from fastapi import FastAPI
from typing import List, Dict
from fastapi import Query

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app_pw@db:5432/appdb")

app = FastAPI(title="MyApp API")

def ensure_schema():
    # Safe if table already exists (init.sql also creates/seed on first boot)
    with contextlib.closing(psycopg.connect(DATABASE_URL)) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS samples (
                    id SERIAL PRIMARY KEY,
                    value DOUBLE PRECISION NOT NULL
                );
            """)
            conn.commit()

@app.on_event("startup")
def startup():
    ensure_schema()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/compute")
def compute_average():
    with contextlib.closing(psycopg.connect(DATABASE_URL)) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(value) FROM samples;")
            (avg,) = cur.fetchone()
    return {"average_value": float(avg) if avg is not None else None}

@app.post("/insert/{val}")
def insert_value(val: float):
    with contextlib.closing(psycopg.connect(DATABASE_URL)) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO samples(value) VALUES (%s) RETURNING id;", (val,))
            (new_id,) = cur.fetchone()
            conn.commit()
    return {"inserted_id": new_id, "value": val}

@app.get("/values")
def list_values(limit: int = Query(20, ge=1, le=1000)) -> List[Dict]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, value FROM samples ORDER BY id DESC LIMIT %s;", (limit,))
            rows = cur.fetchall()
    return [{"id": r[0], "value": float(r[1])} for r in rows]
