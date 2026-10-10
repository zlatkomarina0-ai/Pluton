from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="PLUTON Core Engine")

# Вчитување на променливите од Docker-compose средината
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pluton_user:pluton_password@db:5432/pluton_db")

def get_db_connection():
    """Функција за сигурно поврзување со PostgreSQL базата во Docker"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# --- БИЗНИС МОДЕЛИ (Pydantic за внатрешна валидација без надворешни API) ---
class PredictionCreate(BaseModel):
    fixture_id: int
    home_score_guess: int
    away_score_guess: int
    user_id: int

# --- РУТИ И БИЗНИС ЛОГИКА ЗА PLUTON ---

@app.get("/api/health")
def health_check():
    """Главен статус чек за Docker и базата"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        return {
            "status": "ok",
            "database": "healthy",
            "engine": "PLUTON Python Core",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database System Failure: {str(e)}")

@app.get("/api/fixtures")
def get_internal_fixtures(sport: Optional[str] = None):
    """Ги враќа натпреварите и лигите генерирани директно од нашиот seed.sql"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if sport:
            query = """
                SELECT f.*, s.name as sport_name 
                FROM fixtures f 
                JOIN sports s ON f.sport_id = s.id 
                WHERE s.slug = %s;
            """
            cursor.execute(query, (sport,))
        else:
            query = "SELECT * FROM fixtures;"
            cursor.execute(query)
            
        fixtures = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"fixtures": fixtures}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predictions")
def create_internal_prediction(prediction: PredictionCreate):
    """
    Внесување на кориснички прогнози.
    Ја активира внатрешната SQL заштита (check_prediction_lock тригерот во базата)
    доколку натпреварот е веќе заклучен!
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Проверка за статус директно во базата пред вметнување
        cursor.execute("SELECT status FROM fixtures WHERE id = %s;", (prediction.fixture_id,))
        fixture = cursor.fetchone()
        
        if not fixture:
            raise HTTPException(status_code=404, detail="Натпреварот не е пронајден во базата.")
            
        if fixture['status'] == 'LOCKED':
            raise HTTPException(status_code=400, detail="Бизнис правило: Натпреварот е заклучен за прогнози!")

        # Вметнување на прогнозата
        insert_query = """
            INSERT INTO predictions (fixture_id, home_score_guess, away_score_guess, user_id, created_at)
            VALUES (%s, %s, %s, %s, NOW()) RETURNING id;
        """
        cursor.execute(insert_query, (
            prediction.fixture_id, 
            prediction.home_score_guess, 
            prediction.away_score_guess, 
            prediction.user_id
        ))
        prediction_id = cursor.fetchone()['id']
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"status": "success", "prediction_id": prediction_id, "message": "Прогнозата е успешно зачувана во PLUTON."}
        
    except psycopg2.Error as db_err:
        # Доколку тригерот во базата фрли EXCEPTION, FastAPI го фаќа тука
        raise HTTPException(status_code=400, detail=f"Database Restriction: {db_err.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
