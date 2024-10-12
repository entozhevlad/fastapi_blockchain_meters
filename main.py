import fastapi as _fastapi
from pydantic import BaseModel
import asyncio
import blockchain as _blockchain  # Импортируем асинхронный блокчейн

# Создание приложения FastAPI
app = _fastapi.FastAPI()

# Модель данных для передачи информации о блоке при майнинге
class MineBlockRequest(BaseModel):
    meter_id: str  # Идентификатор умного счетчика
    consumption: float  # Потребление электроэнергии в кВт*ч

# Зависимость для получения блокчейна
def get_blockchain():
    return _blockchain.Blockchain()

@app.post("/mine_block/")
async def mine_block(request: MineBlockRequest, blockchain = _fastapi.Depends(get_blockchain)):
    """Асинхронное API для майнинга нового блока с показаниями умного счетчика."""
    if not await blockchain.is_chain_valid():
        raise _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен или нарушена целостность")

    # Майнинг нового блока с показаниями счетчика
    block = await blockchain.mine_block(meter_id=request.meter_id, consumption=request.consumption)
    return {
        "message": "Блок успешно замайнен!",
        "block": block.to_dict()
    }

@app.get("/blockchain/")
async def get_blockchain_view(blockchain = _fastapi.Depends(get_blockchain)):
    """Асинхронное API для получения всей цепочки блоков."""
    if not await blockchain.is_chain_valid():
        raise _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен или нарушена целостность")

    # Преобразуем блоки в читаемый формат
    chain = [block.to_dict() for block in blockchain.chain]
    return {
        "length": len(chain),
        "chain": chain
    }

@app.get("/validate/")
async def validate(blockchain = _fastapi.Depends(get_blockchain)):
    """Асинхронное API для проверки целостности цепочки блоков."""
    is_valid = await blockchain.is_chain_valid()
    if not is_valid:
        raise _fastapi.HTTPException(status_code=400, detail="Цепочка блоков нарушена!")
    return {"message": "Цепочка блоков корректна!", "valid": is_valid}

@app.get("/meter/{meter_id}/consumption/")
async def get_meter_consumption(meter_id: str, blockchain = _fastapi.Depends(get_blockchain)):
    """Асинхронное API для получения истории потребления по конкретному счетчику."""
    # Поиск всех блоков, связанных с данным идентификатором счетчика
    consumption_data = [
        block.to_dict() for block in blockchain.chain if block.meter_id == meter_id
    ]
    return {
        "meter_id": meter_id,
        "consumption_history": consumption_data
    }
