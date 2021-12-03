import math
import mmh3
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, items_count, false_positive_probability):
        self.false_positive = false_positive_probability
        self.array_size = self.get_size(items_count, false_positive_probability)
        self.hash_count = self.get_hash_count(self.array_size, items_count)
        self.bit_array = bitarray(self.array_size)
        self.bit_array.setall(0)

    def add(self, item):
        digests = []
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.array_size
            digests.append(digest)
            self.bit_array[digest] = True

        return item

    def exists(self, item):
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.array_size
            if not self.bit_array[digest]:
                return False
        return True

    @classmethod
    def get_size(cls, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        k = (m / n) * math.log(2)
        return int(k)
