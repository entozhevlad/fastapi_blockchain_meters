import pytest
from httpx import AsyncClient
from main import app  # Импортируем приложение FastAPI


@pytest.mark.asyncio
async def test_mine_block():
    """Тестируем создание нового блока."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/mine_block/",
            json={"meter_id": "12345", "consumption": 100.5}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Блок успешно замайнен!"
    assert "block" in data


@pytest.mark.asyncio
async def test_get_blockchain():
    """Тестируем получение всей цепочки блоков."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/blockchain/")
    assert response.status_code == 200
    data = response.json()
    assert "length" in data
    assert isinstance(data["chain"], list)


@pytest.mark.asyncio
async def test_validate():
    """Тестируем валидацию цепочки блоков."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/validate/")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True


@pytest.mark.asyncio
async def test_get_meter_consumption():
    """Тестируем получение истории потребления для конкретного счётчика."""
    meter_id = "12345"
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(f"/meter/{meter_id}/consumption/")
    assert response.status_code == 200
    data = response.json()
    assert data["meter_id"] == meter_id
    assert isinstance(data["consumption_history"], list)
