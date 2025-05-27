import hashlib, time, json, os

class Block:
    def __init__(self, index, data, previous_hash, timestamp=None, hash_val=None):
        self.index = index
        self.timestamp = timestamp or time.ctime()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash_val or self.generate_hash()

    def generate_hash(self):
        return hashlib.sha256((str(self.index) + self.timestamp +
                               self.data + self.previous_hash).encode()).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

    @staticmethod
    def from_dict(block_data):
        return Block(
            index=block_data['index'],
            data=block_data['data'],
            previous_hash=block_data['previous_hash'],
            timestamp=block_data['timestamp'],
            hash_val=block_data['hash']
        )

class Blockchain:
    def __init__(self):
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), data, last_block.hash)
        self.chain.append(new_block)
        self.save_chain()

    def save_chain(self):
        with open("chain.json", "w") as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=4)

    def load_chain(self):
        if os.path.exists("chain.json"):
            with open("chain.json", "r") as f:
                data = json.load(f)
                return [Block.from_dict(b) for b in data]
        else:
            return [self.create_genesis_block()]

    def get_chain(self):
        return self.chain
