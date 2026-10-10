FROM python:3.10-slim

WORKDIR /app

# Прво ги копираме само зависностите за побрз кеш
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Го копираме целиот корен на проектот во /app
COPY . .

EXPOSE 3000

# Ја стартуваме апликацијата со експлицитен модул лоциран во работната папка
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
