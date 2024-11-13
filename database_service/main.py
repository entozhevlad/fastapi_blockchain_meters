# database_service/main.py
import fastapi as _fastapi
from sqlalchemy.orm import Session
from shared.database import SessionLocal
from shared import models

app = _fastapi.FastAPI()

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get_consumption/{meter_id}")
async def get_consumption(meter_id: str, db: Session = _fastapi.Depends(get_db)):
    """Получить историю потребления по ID счётчика"""
    data = db.query(models.MeterData).filter(models.MeterData.meter_id == meter_id).order_by(models.MeterData.timestamp.desc()).all()
    return {"meter_id": meter_id, "consumption_history": [d.__dict__ for d in data]}

@app.get("/get_blockchain/")
async def get_blockchain(db: Session = _fastapi.Depends(get_db)):
    """Получить полную цепочку блоков"""
    blockchain_data = db.query(models.Blockchain).order_by(models.Blockchain.index.asc()).all()
    return {"blockchain": [b.__dict__ for b in blockchain_data]}
