import datetime as _dt
import hashlib as _hashlib
import json as _json
from decouple import config


class Block:
    """Класс блока."""
    def __init__(self, data: str, proof: int, previous_hash: str, index: int) -> None:
        self.index = index
        self.timestamp = str(_dt.datetime.now())
        self.data = data
        self.proof = proof
        self.previous_hash = previous_hash

class Blockchain:
    """Класс блокчейна."""
    def __init__(self) -> None:
        """Конструктор блокчейна."""
        self.chain = list()
        self.DIFFICLUTY = config("DIFFICULTY")
        genesis_block = self._create_block(data="first block", proof=1, previous_hash="0", index=0)
        self.chain.append(genesis_block)

    def mine_block(self, data: str) -> Block:
        """Майнинг блока."""
        previous_block = self.get_previous_block()
        previous_proof = previous_block.proof
        index = len(self.chain) + 1
        proof = self._proof_of_work(previous_proof=previous_proof,index=index,data=data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(data=data, proof=proof, previous_hash=previous_hash, index=index)
        self.chain.append(block)
        return block.__dict__

    def _hash(self, block: Block) -> str:
        """Хеширование блока."""
        encoded_block = _json.dumps(block.__dict__, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()


    def _to_digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        """Получение хеша."""
        to_digest = str(new_proof**2 - previous_proof**2 + index) + data
        return to_digest.encode()


    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        """Поиск подходящего proof."""
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_digest = self._to_digest(
                new_proof=new_proof,
                previous_proof=previous_proof,
                index=index,
                data=data
            )
            hash_value = _hashlib.sha256(to_digest).hexdigest()

            if hash_value[:len(self.DIFFICLUTY)] == self.DIFFICLUTY:
                check_proof = True
            else:
                new_proof += 1
        return new_proof


    def get_previous_block(self) -> Block:
        """Получение предыдущего блока."""
        return self.chain[-1]

    def _create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict():
        """Создание блока."""
        return Block(data, proof, previous_hash, index)

    def is_chain_valid(self) -> bool:
        """Проверка целостности цепочки."""
        current_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block.previous_hash != self._hash(current_block):
                return False
            current_proof = current_block.proof
            next_index, next_data, next_proof = next_block.index, next_block.data, next_block.proof
            hash_value = _hashlib.sha256(
                self._to_digest(
                    new_proof=next_proof,
                    previous_proof=current_proof,
                    index=next_index,
                    data=next_data
                )
            ).hexdigest()
            if hash_value[:len(self.DIFFICLUTY)] != self.DIFFICLUTY:
                return False
            current_block = next_block
            block_index += 1
        return True


