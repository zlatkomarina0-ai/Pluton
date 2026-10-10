from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="PLUTON Intelligent Core Engine")

# Вчитување на променливите од Docker-compose средината
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pluton_user:pluton_password@db:5432/pluton_db")

def get_db_connection():
    """Функција за сигурно поврзување со PostgreSQL базата во Docker"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# --- БИЗНИС МОДЕЛИ СО НАПРЕДНА СПОРТСКА ВАЛИДАЦИЈА ---
class PredictionCreate(BaseModel):
    fixture_id: int
    sport_type: str  # 'football' или 'basketball'
    home_score_guess: int
    away_score_guess: int
    user_id: int

    @field_validator('sport_type')
    @classmethod
    def validate_sport(cls, v: str) -> str:
        supported = ['football', 'basketball']
        if v.lower() not in supported:
            raise ValueError(f"Неподдржан спорт во PLUTON. Поддржани се: {supported}")
        return v.lower()

    @field_validator('home_score_guess', 'away_score_guess')
    @classmethod
    def validate_scores(cls, v: int, info) -> int:
        sport = info.data.get('sport_type')
        if v < 0:
            raise ValueError("Резултатот не може да биде негативен број!")
        
        # Строго бизнис правило за фудбалски граници
        if sport == 'football' and v > 15:
            raise ValueError("Аномалија: Фудбалски резултат не може да биде поголем од 15 голови!")
            
        # Строго бизнис правило за кошаркарски граници
        if sport == 'basketball' and v > 200:
            raise ValueError("Аномалија: Кошаркарски поени не може да надминат 200 поени по тим!")
            
        return v

# --- СИСТЕМ ЗА АВТОМАТСКО БОДУВАЊЕ (SCORE CALCULATION ENGINE) ---
def calculate_prediction_points(sport: str, home_g: int, away_g: int, home_a: int, away_a: int) -> int:
    """
    Матрица за пресметка на поени во PLUTON:
    - Точен резултат = 5 поени (фудбал) / 8 поени (кошарка поради тежина)
    - Погодена разлика или нерешено = 3 поени
    - Погоден само победник (тип) = 1 поен
    - Промашување = 0 поени
    """
    # 1. Проверка за точен резултат
    if home_g == home_a and away_g == away_a:
        return 8 if sport == 'basketball' else 5

    # Логика за знаци (1, X, 2)
    guess_sign = 1 if home_g > away_g else (2 if home_g < away_g else 0)
    actual_sign = 1 if home_a > away_a else (2 if home_a < away_a else 0)

    # 2. Проверка за погоден исход (победник или нерешено)
    if guess_sign == actual_sign:
        # Дополнителен бонус за погодена иста гол-разлика (само кај фудбал)
        if sport == 'football' and (home_g - away_g) == (home_a - away_a):
            return 3
        return 1
        
    return 0

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
            "sports_active": ["football", "basketball"],
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database System Failure: {str(e)}")

@app.get("/api/fixtures")
def get_internal_fixtures(sport: Optional[str] = None):
    """Ги враќа натпреварите генерирани директно од базата"""
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
            cursor.execute(query, (sport.lower(),))
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
    """Внесување прогноза со спортска валидација и проверка на статус"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT status FROM fixtures WHERE id = %s;", (prediction.fixture_id,))
        fixture = cursor.fetchone()
        
        if not fixture:
            raise HTTPException(status_code=404, detail="Натпреварот не е пронајден.")
            
        if fixture['status'] == 'LOCKED':
            raise HTTPException(status_code=400, detail="Натпреварот е заклучен за прогнози!")

        insert_query = """
            INSERT INTO predictions (fixture_id, home_score_guess, away_score_guess, user_id, created_at, points_earned)
            VALUES (%s, %s, %s, %s, NOW(), 0) RETURNING id;
        """
        cursor.execute(insert_query, (
            prediction.fixture_id, prediction.home_score_guess, 
            prediction.away_score_guess, prediction.user_id
        ))
        prediction_id = cursor.fetchone()['id']
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"status": "success", "prediction_id": prediction_id, "sport": prediction.sport_type}
        
    except psycopg2.Error as db_err:
        raise HTTPException(status_code=400, detail=f"База грешка: {db_err.pgerror}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/settle/{fixture_id}")
def settle_fixture_predictions(fixture_id: int, home_actual: int, away_actual: int):
    """
    Админ рута за обработка на завршен натпревар. 
    Автоматски ги влече сите кориснички прогнози за тој натпревар, 
    ги пресметува освоените поени преку бодовната матрица и ја ажурира базата.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Извлечи ги деталите за натпреварот за да знаеме кој спорт е
        cursor.execute("""
            SELECT f.id, s.slug as sport_slug 
            FROM fixtures f 
            JOIN sports s ON f.sport_id = s.id 
            WHERE f.id = %s;
        """, (fixture_id,))
        fixture = cursor.fetchone()
        
        if not fixture:
            raise HTTPException(status_code=404, detail="Натпреварот не постои.")

        # 2. Ажурирај го статусот на натпреварот со реалниот резултат
        cursor.execute("""
            UPDATE fixtures 
            SET home_score_actual = %s, away_score_actual = %s, status = 'SETTLED' 
            WHERE id = %s;
        """, (home_actual, away_actual, fixture_id))

        # 3. Земи ги сите прогнози поднесени од корисниците за овој натпревар
        cursor.execute("SELECT id, home_score_guess, away_score_guess FROM predictions WHERE fixture_id = %s;", (fixture_id,))
        predictions = cursor.fetchall()

        processed_count = 0
        # 4. Пресметај поени за секоја прогноза посебно
        for pred in predictions:
            points = calculate_prediction_points(
                fixture['sport_slug'],
                pred['home_score_guess'], pred['away_score_guess'],
                home_actual, away_actual
            )
            
            # Сними ги бодовите во базата
            cursor.execute("UPDATE predictions SET points_earned = %s WHERE id = %s;", (points, pred['id']))
            processed_count += 1

        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "message": f"Успешно обработени {processed_count} прогнози за натпреварот {fixture_id}.",
            "result_settled": f"{home_actual}:{away_actual}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
