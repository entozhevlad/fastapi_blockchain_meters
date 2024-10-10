import fastapi as _fastapi
import blockchain as _blockchain

blockchain = _blockchain.Blockchain()

app = _fastapi.FastAPI()

@app.post("/mine_block/")
def mine_block(data: str):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен")
    block = blockchain.mine_block(data=data)
    return block

@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен")
    chain = blockchain.chain
    return chain
@app.get("/validate/")
def validate():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="Блокчейн недоступен")
    return blockchain.is_chain_valid()