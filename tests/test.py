import pytest
import asyncio
from blockchain import Blockchain, Block

@pytest.fixture
def blockchain():
    return Blockchain()

@pytest.mark.asyncio
async def test_genesis_block(blockchain):
    assert len(blockchain.chain) == 1
    genesis_block = blockchain.chain[0]
    assert genesis_block.index == 0
    assert genesis_block.meter_id == "0"
    assert genesis_block.consumption == 0.0
    assert genesis_block.previous_hash == "0"

@pytest.mark.asyncio
async def test_mine_block(blockchain):
    new_block = await blockchain.mine_block(meter_id="12345", consumption=100.0)
    assert len(blockchain.chain) == 2
    assert new_block.index == 1
    assert new_block.meter_id == "12345"
    assert new_block.consumption == 100.0
    assert new_block.previous_hash != "0"

@pytest.mark.asyncio
async def test_is_chain_valid(blockchain):
    await blockchain.mine_block(meter_id="12345", consumption=100.0)
    is_valid = await blockchain.is_chain_valid()
    assert is_valid

@pytest.mark.asyncio
async def test_invalid_chain(blockchain):
    new_block = await blockchain.mine_block(meter_id="12345", consumption=100.0)
    new_block.previous_hash = "invalid_hash"
    is_valid = await blockchain.is_chain_valid()
    assert not is_valid

@pytest.mark.asyncio
async def test_proof_of_work(blockchain):
    new_block = await blockchain.mine_block(meter_id="54321", consumption=50.0)
    previous_block = blockchain.chain[-2]  # Берем предпоследний блок в цепочке
    assert new_block.proof != previous_block.proof
    assert len(blockchain.chain) == 2

