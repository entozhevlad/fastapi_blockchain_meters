import datetime as _dt
import hashlib as _hashlib
import json as _json
import asyncio

class Block:
    """Класс блока для хранения данных умных счетчиков."""
    def __init__(self, meter_id: str, consumption: float, proof: int, previous_hash: str, index: int) -> None:
        self.index = index
        self.timestamp = str(_dt.datetime.now())
        self.meter_id = meter_id
        self.consumption = consumption
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        """Превращает объект блока в словарь для сериализации."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "meter_id": self.meter_id,
            "consumption": self.consumption,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }


class Blockchain:
    """Асинхронный блокчейн для хранения данных умных счетчиков."""
    def __init__(self) -> None:
        """Конструктор блокчейна."""
        self.chain = list()
        self.DIFFICULTY = 4  # Количество нулей в начале хеша для проверки сложности
        # Генерация начального блока
        genesis_block = Block(meter_id="0", consumption=0.0, proof=1, previous_hash="0", index=0)
        self.chain.append(genesis_block)

    async def mine_block(self, meter_id: str, consumption: float) -> Block:
        """Асинхронный майнинг блока с данными о потреблении."""
        previous_block = self.get_previous_block()
        previous_proof = previous_block.proof
        index = len(self.chain)
        proof = await self._proof_of_work(previous_proof=previous_proof, index=index, meter_id=meter_id, consumption=consumption)
        previous_hash = await self._hash(previous_block)
        block = Block(meter_id=meter_id, consumption=consumption, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block

    async def _hash(self, block: Block) -> str:
        """Асинхронное хеширование блока."""
        encoded_block = _json.dumps(block.to_dict(), sort_keys=True).encode()
        await asyncio.sleep(0)  # Эмуляция асинхронной работы
        return _hashlib.sha256(encoded_block).hexdigest()

    async def _proof_of_work(self, previous_proof: int, index: int, meter_id: str, consumption: float) -> int:
        """Асинхронный поиск подходящего proof."""
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_digest = f'{new_proof**2 - previous_proof**2 + index}{meter_id}{consumption}'.encode()
            hash_value = _hashlib.sha256(to_digest).hexdigest()
            if hash_value[:self.DIFFICULTY] == "0" * self.DIFFICULTY:
                check_proof = True
            else:
                new_proof += 1
            await asyncio.sleep(0)  # Эмуляция асинхронного выполнения, чтобы не блокировать
        return new_proof

    def get_previous_block(self) -> Block:
        """Получение предыдущего блока в цепочке."""
        return self.chain[-1]

    async def is_chain_valid(self) -> bool:
        """Асинхронная проверка целостности цепочки блоков."""
        current_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            # Проверка корректности ссылки на предыдущий блок
            if next_block.previous_hash != await self._hash(current_block):
                return False

            current_proof = current_block.proof
            next_proof = next_block.proof
            # Проверка корректности хеша
            to_digest = f'{next_proof**2 - current_proof**2 + next_block.index}{next_block.meter_id}{next_block.consumption}'.encode()
            hash_value = _hashlib.sha256(to_digest).hexdigest()
            if hash_value[:self.DIFFICULTY] != "0" * self.DIFFICULTY:
                return False

            current_block = next_block
            block_index += 1
            await asyncio.sleep(0)  # Эмуляция асинхронного выполнения для больших цепочек
        return True
