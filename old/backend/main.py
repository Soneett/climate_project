from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Social Climate Profile API",
    description="API для доступа к социально-климатическим данным по регионам РФ",
    version="1.0.0"
)

# Настройка CORS (если фронт будет обращаться с другого порта)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/indicators", response_model=list[schemas.IndicatorOut])
def get_indicators(db: Session = Depends(get_db)):
    indicators = db.query(models.Indicator).all()
    return indicators
