# data_collector_service/main.py
import fastapi as _fastapi
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.database import SessionLocal
from shared import models

app = _fastapi.FastAPI()

class MeterData(BaseModel):
    meter_id: str
    consumption: float

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit_data/")
async def submit_data(data: MeterData, db: Session = _fastapi.Depends(get_db)):
    new_data = models.MeterData(meter_id=data.meter_id, consumption=data.consumption)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"status": "Data submitted successfully", "data": new_data}
