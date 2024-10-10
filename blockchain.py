import datetime as _dt
import hashlib as _hashlib
import json as _json
from decouple import config


class Block:
    """Класс блока, содержащий данные об электроэнергии."""
    def __init__(self, meter_id: str, consumption: float, timestamp: str, proof: int, previous_hash: str, index: int) -> None:
        self.index = index
        self.timestamp = timestamp  # Временная метка добавления блока
        self.meter_id = meter_id     # Идентификатор умного счетчика
        self.consumption = consumption  # Потребление электроэнергии (например, в кВт*ч)
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self) -> dict:
        """Преобразование блока в словарь для хеширования."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "meter_id": self.meter_id,
            "consumption": self.consumption,
            "proof": self.proof,
            "previous_hash": self.previous_hash
        }


class Blockchain:
    """Класс блокчейна для учета потребления электроэнергии."""
    def __init__(self) -> None:
        """Конструктор блокчейна."""
        self.chain = list()
        self.DIFFICULTY = int(config("DIFFICULTY", default=2))  # Значение сложности
        # Создание первого блока (генезис-блок)
        genesis_block = self._create_block(meter_id="0", consumption=0.0, timestamp=str(_dt.datetime.now()), proof=1, previous_hash="0", index=0)
        self.chain.append(genesis_block)

    def mine_block(self, meter_id: str, consumption: float) -> dict:
        """Майнинг нового блока с показаниями."""
        previous_block = self.get_previous_block()
        previous_proof = previous_block.proof
        index = len(self.chain)
        timestamp = str(_dt.datetime.now())  # Создаем временную метку для нового блока
        proof = self._proof_of_work(previous_proof=previous_proof, index=index, meter_id=meter_id, consumption=consumption)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(meter_id=meter_id, consumption=consumption, timestamp=timestamp, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block.to_dict()

    def _hash(self, block: Block) -> str:
        """Хеширование блока."""
        encoded_block = _json.dumps(block.to_dict(), sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def _to_digest(self, new_proof: int, previous_proof: int, index: str, meter_id: str, consumption: float) -> bytes:
        """Получение данных для хеширования."""
        to_digest = f"{new_proof**2 - previous_proof**2 + int(index)}{meter_id}{consumption}"
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: int, index: int, meter_id: str, consumption: float) -> int:
        """Поиск подходящего proof для нового блока."""
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_digest = self._to_digest(
                new_proof=new_proof,
                previous_proof=previous_proof,
                index=str(index),
                meter_id=meter_id,
                consumption=consumption
            )
            hash_value = _hashlib.sha256(to_digest).hexdigest()
            if hash_value[:self.DIFFICULTY] == "0" * self.DIFFICULTY:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def get_previous_block(self) -> Block:
        """Получение предыдущего блока."""
        return self.chain[-1]

    def _create_block(self, meter_id: str, consumption: float, timestamp: str, proof: int, previous_hash: str, index: int) -> Block:
        """Создание нового блока с данными умного счетчика."""
        return Block(meter_id, consumption, timestamp, proof, previous_hash, index)

    def is_chain_valid(self) -> bool:
        """Проверка целостности цепочки блоков."""
        current_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block.previous_hash != self._hash(current_block):
                return False

            current_proof = current_block.proof
            next_index = next_block.index
            next_meter_id = next_block.meter_id
            next_consumption = next_block.consumption
            next_proof = next_block.proof
            hash_value = _hashlib.sha256(
                self._to_digest(
                    new_proof=next_proof,
                    previous_proof=current_proof,
                    index=str(next_index),
                    meter_id=next_meter_id,
                    consumption=next_consumption
                )
            ).hexdigest()
            if hash_value[:self.DIFFICULTY] != "0" * self.DIFFICULTY:
                return False

            current_block = next_block
            block_index += 1
        return True
