import fastapi as _fastapi
import blockchain as _blockchain
from pydantic import BaseModel

# Инициализация блокчейна
blockchain = _blockchain.Blockchain()

# Создание приложения FastAPI
app = _fastapi.FastAPI()

# Модель данных для передачи информации о блоке при майнинге
class MineBlockRequest(BaseModel):
    meter_id: str  # Идентификатор умного счетчика
    consumption: float  # Потребление электроэнергии в кВт*ч


@app.post("/mine_block/")
def mine_block(request: MineBlockRequest):
    """API для майнинга нового блока с показаниями умного счетчика."""
    if not blockchain.is_chain_valid():
        raise _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен или нарушена целостность")

    # Майнинг нового блока с данными умного счетчика
    block = blockchain.mine_block(meter_id=request.meter_id, consumption=request.consumption)
    return {"message": "Блок успешно замайнен!", "block": block}


@app.get("/blockchain/")
def get_blockchain():
    """API для получения всей цепочки блоков."""
    if not blockchain.is_chain_valid():
        raise _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен или нарушена целостность")

    # Преобразуем блоки в читаемый формат
    chain = [block.to_dict() for block in blockchain.chain]
    return {"length": len(chain), "chain": chain}


@app.get("/validate/")
def validate():
    """API для проверки целостности цепочки блоков."""
    is_valid = blockchain.is_chain_valid()
    if not is_valid:
        raise _fastapi.HTTPException(status_code=400, detail="Цепочка блоков нарушена!")
    return {"message": "Цепочка блоков корректна!", "valid": is_valid}
