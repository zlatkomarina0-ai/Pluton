
-- Вметнување на основните спортови
INSERT INTO sports (name, slug) VALUES 
('Фудбал', 'football'),
('Кошарка', 'basketball')
ON CONFLICT (slug) DO NOTHING;

-- Вметнување на тест натпревари (1 отворен, 1 заклучен за бизнис проверка)
INSERT INTO fixtures (sport_id, home_team, away_team, status, match_date) VALUES 
(1, 'Real Madrid', 'Barcelona', 'OPEN', NOW() + INTERVAL '2 days'),
(2, 'Lakers', 'Celtics', 'LOCKED', NOW() - INTERVAL '2 hours');
