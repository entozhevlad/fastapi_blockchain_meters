# blockchain_service/main.py
"""Микросервис для обработки блокчейн-транзакций"""
"""Отвечает за создание новых блоков, майнинг и проверку целостности блокчейна."""

# blockchain_service/main.py
import fastapi as _fastapi
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.database import SessionLocal
from shared import models
import blockchain as _blockchain

app = _fastapi.FastAPI()
blockchain = _blockchain.Blockchain()


class MineBlockRequest(BaseModel):
    meter_id: str
    consumption: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/mine_block/")
async def mine_block(request: MineBlockRequest, db: Session = _fastapi.Depends(get_db)):
    if not await blockchain.is_chain_valid():
        raise _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен или нарушена целостность")

    block = await blockchain.mine_block(meter_id=request.meter_id, consumption=request.consumption)
    new_block = models.Blockchain(
        index=block.index,
        previous_hash=block.previous_hash,
        data=block.to_dict(),
        timestamp=block.timestamp,
    )
    db.add(new_block)
    db.commit()
    db.refresh(new_block)
    return {"message": "Блок успешно замайнен!", "block": new_block}
