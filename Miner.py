import hashing
from Mempool import get_mempool
from Block import Block
from Blockchain import get_blockchain
from Transaction import Coinbase, Transaction
import random
from CONFIG import *

class Miner:
    def __init__(self, own_public_key):
        self.public_key = own_public_key
        while True:
            self.mine()

    def check_agains_target(self, hash_string):
        hex = hashing.string_to_hex(hash_string)
        for i in range(1, mining_target+1):
            if not hex[i] == "0":
                return False
        return True

    def mine(self):
        topmost_block = get_blockchain().get_topmost_block()
        assert isinstance(topmost_block, Block)
        hash_prev = topmost_block.get_hash()
        txs = get_mempool().tx
        for i in txs:
            assert isinstance(i, Transaction) or isinstance(i, Coinbase)
            if not i.is_valid():
                txs.remove(i)
        coinbase = Coinbase(self.public_key)
        txs.insert(0, coinbase)
        while True:
            block = Block(hash_prev, txs, random.randint(0, 9999999999999999999999999999))
            hash = block.get_hash()
            check = self.check_agains_target(hash)
            if check:
                #FOUND NEW BLOCK; COINBASE$$$$
                success = get_blockchain().insert_block(block)
                if success:
                    print(get_blockchain().get_json())
                break
