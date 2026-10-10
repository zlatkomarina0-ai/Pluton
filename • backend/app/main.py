from fastapi import FastAPI, HTTPException
import psycopg2
import os

app = FastAPI(title="PLUTON Core")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pluton_user:pluton_password@db:5432/pluton_db")

@app.get("/api/health")
def health_check():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        return {"status": "ok", "service": "PLUTON", "phase": "1"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
