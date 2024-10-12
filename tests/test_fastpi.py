import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app, get_blockchain
from blockchain import Blockchain  # Импортируем блокчейн для тестирования

# Создаем тестовый экземпляр блокчейна
test_blockchain = Blockchain()

# Переопределяем зависимость на тестовый блокчейн
app.dependency_overrides[get_blockchain] = lambda: test_blockchain

@pytest.mark.asyncio
async def test_mine_block():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/mine_block/", json={"meter_id": "12345", "consumption": 100.0})
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Блок успешно замайнен!"
        assert data["block"]["meter_id"] == "12345"
        assert data["block"]["consumption"] == 100.0

@pytest.mark.asyncio
async def test_get_blockchain():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/blockchain/")
        assert response.status_code == 200
        data = response.json()
        assert "chain" in data
        assert isinstance(data["chain"], list)

@pytest.mark.asyncio
async def test_validate_chain():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/validate/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Цепочка блоков корректна!"
        assert data["valid"] == True

@pytest.mark.asyncio
async def test_get_meter_consumption():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/meter/12345/consumption/")
        assert response.status_code == 200
        data = response.json()
        assert data["meter_id"] == "12345"
        assert isinstance(data["consumption_history"], list)

@pytest.mark.asyncio
async def test_mine_block_invalid_chain():
    # Пример теста с симуляцией нарушения целостности цепочки
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Нарушаем цепочку
        test_blockchain.chain[-1].previous_hash = "invalid_hash"
        response = await ac.post("/mine_block/", json={"meter_id": "54321", "consumption": 200.0})
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Блокчейн недоступен или нарушена целостность"
