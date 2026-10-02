from fastapi import FastAPI
from app.database import Base, engine
from app.routers.pluton import router

app = FastAPI(title="PLUTON", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "PLUTON API is running"}
