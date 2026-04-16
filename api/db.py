import psycopg2
import os
from datetime import datetime
import hashlib
from dotenv import load_dotenv

# Load local .env for development, Vercel will use dashboard env vars in production
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    # Use sslmode=require for secure Vercel-to-Railway connection
    if "railway.app" in DATABASE_URL or "rlwy.net" in DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Ledger Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ledger (
        id SERIAL PRIMARY KEY,
        claim TEXT NOT NULL,
        result TEXT NOT NULL,
        hash TEXT NOT NULL UNIQUE,
        risk_level TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Cache Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_cache (
        query_hash TEXT PRIMARY KEY,
        results JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.close()
    conn.close()

def save_record(data: dict):
    # Generate unique hash based on claim text
    hash_val = hashlib.sha256(data['claim'].encode()).hexdigest()
    
    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ledger (claim, result, hash, risk_level) VALUES (%s, %s, %s, %s) ON CONFLICT (hash) DO NOTHING",
            (data['claim'], data.get('result', ''), hash_val, data.get('risk_level', 'UNKNOWN'))
        )
    finally:
        cursor.close()
        conn.close()

def get_records():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, claim, result, hash, risk_level, timestamp FROM ledger ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "claim": r[1],
                "result": r[2],
                "hash": r[3],
                "risk_level": r[4],
                "timestamp": r[5].isoformat() if r[5] else None
            } for r in rows
        ]
    finally:
        cursor.close()
        conn.close()
