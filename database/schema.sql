
-- Креирање на табела за спортови
CREATE TABLE IF NOT EXISTS sports (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

-- Креирање на табела за натпревари
CREATE TABLE IF NOT EXISTS fixtures (
    id SERIAL PRIMARY KEY,
    sport_id INT REFERENCES sports(id) ON DELETE CASCADE,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN', -- 'OPEN', 'LOCKED', 'SETTLED'
    home_score_actual INT DEFAULT NULL,
    away_score_actual INT DEFAULT NULL,
    match_date TIMESTAMP NOT NULL
);

-- Креирање на табела за кориснички прогнози
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    fixture_id INT REFERENCES fixtures(id) ON DELETE CASCADE,
    user_id INT NOT NULL,
    home_score_guess INT NOT NULL,
    away_score_guess INT NOT NULL,
    points_earned INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- БИЗНИС ЗАШТИТА: Тригер функција која не дозволува запис ако натпреварот е LOCKED
CREATE OR REPLACE FUNCTION check_fixture_lock()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT status FROM fixtures WHERE id = NEW.fixture_id) = 'LOCKED' THEN
        RAISE EXCEPTION 'Бизнис правило: Натпреварот е заклучен, прогнозата е одбиена!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_fixture_lock
BEFORE INSERT ON predictions
FOR EACH ROW
EXECUTE FUNCTION check_fixture_lock();
