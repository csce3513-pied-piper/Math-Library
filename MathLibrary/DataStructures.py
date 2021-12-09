import math
import mmh3
from bitarray import bitarray
from random import randint, seed
import copy
import hashlib
import struct
import numpy as np


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


class CountMinSketch(object):

    def __init__(self, w, d):
        self.hash_width = w
        self.hash_functions_count = d
        self.p = 2 ** 31 - 1  # magic number from the original paper
        self.counts = [[0 for _ in range(w)] for _ in range(d)]
        self.total = 0

        self._init_hash_params()

    def __setitem__(self, element, c):
        self.total += c
        for i in range(self.hash_functions_count):
            h = self.hash(i, element)
            self.counts[i][h] += c

    update = __setitem__

    def __getitem__(self, element):
        estimates = [self.counts[i][self.hash(i, element)] for i in range(self.hash_functions_count)]
        return min(estimates)

    estimate = __getitem__

    def _init_hash_params(self):
        self.a_b = []
        for i in range(self.hash_functions_count):
            a = randint(1, self.p - 1)
            b = randint(1, self.p - 1)
            self.a_b.append((a, b))

    def hash(self, hash_i, e):
        """Apply the `i`th hash function to element `e`."""
        e_int = hash(e)
        a, b = self.a_b[hash_i]

        return CountMinSketch.hash_cw(self.p, self.hash_width, a, b, e_int)

    @staticmethod
    def hash_cw(p, w, a, b, e):
        """Auxillary hashing function for the CountMinSketch class.
        We use this parameterized hash function to obtain our
        pairwise-independent hash functions. `p` and `w` define the
        sub-family, `a` and `b` define the members.
        """
        # Universal hash functions from: Carter & Wegman "Universal
        # classes of hash functions" 1979
        #
        # a and b should be random integers in the range [1, p-1]
        return ((a * e + b) % p) % w


def sha1_hash32(data):
    return struct.unpack('<I', hashlib.sha1(data).digest()[:4])[0]


def sha1_hash64(data):
    return struct.unpack('<Q', hashlib.sha1(data).digest()[:8])[0]


# The size of a hash value in number of bytes
hash_value_byte_size = len(bytes(np.int64(42).data))

# http://en.wikipedia.org/wiki/Mersenne_prime
_mersenne_prime = np.uint64((1 << 61) - 1)
_max_hash = np.uint64((1 << 32) - 1)
_hash_range = (1 << 32)


def _init_hash_values(num_perm):
    return np.ones(num_perm, dtype=np.uint64) * _max_hash


def _parse_hash_values(hash_values):
    return np.array(hash_values, dtype=np.uint64)


class MinHash(object):

    def __init__(self, num_perm=128, seed=1,
                 hash_func=sha1_hash32,
                 hash_values=None, permutations=None):
        if hash_values is not None:
            num_perm = len(hash_values)
        if num_perm > _hash_range:
            raise ValueError("Cannot have more than %d number of\
                    permutation functions" % _hash_range)
        self.seed = seed
        self.num_perm = num_perm

        if not callable(hash_func):
            raise ValueError("The hashfunc must be a callable.")
        self.hash_func = hash_func

        if hash_values is not None:
            self.hash_values = _parse_hash_values(hash_values)
        else:
            self.hash_values = _init_hash_values(num_perm)
        if permutations is not None:
            self.permutations = permutations
        else:
            self.permutations = self._init_permutations(num_perm)
        if len(self) != len(self.permutations[0]):
            raise ValueError("Numbers of hash values and permutations mismatch")

    def _init_permutations(self, num_perm):
        gen = np.random.RandomState(self.seed)
        return np.array([
            (gen.randint(1, _mersenne_prime, dtype=np.uint64), gen.randint(0, _mersenne_prime, dtype=np.uint64)) for _
            in range(num_perm)
        ], dtype=np.uint64).T

    def update(self, b):
        hv = self.hash_func(b)
        a, b = self.permutations
        phv = np.bitwise_and((a * hv + b) % _mersenne_prime, _max_hash)
        self.hash_values = np.minimum(phv, self.hash_values)

    def update_batch(self, b):
        hv = np.array([self.hash_func(_b) for _b in b], dtype=np.uint64)
        a, b = self.permutations
        phv = np.bitwise_and(((hv * np.tile(a, (len(hv), 1)).T).T + b) % _mersenne_prime, _max_hash)
        self.hash_values = np.vstack([phv, self.hash_values]).min(axis=0)

    def jaccard(self, other):
        if other.seed != self.seed:
            raise ValueError("Cannot compute Jaccard given MinHash with\
                    different seeds")
        if len(self) != len(other):
            raise ValueError("Cannot compute Jaccard given MinHash with\
                    different numbers of permutation functions")
        return float(np.count_nonzero(self.hash_values == other.hash_values)) / float(len(self))

    def count(self):
        k = len(self)
        return float(k) / np.sum(self.hash_values / float(_max_hash)) - 1.0

    def merge(self, other):
        if other.seed != self.seed:
            raise ValueError("Cannot merge MinHash with\
                    different seeds")
        if len(self) != len(other):
            raise ValueError("Cannot merge MinHash with\
                    different numbers of permutation functions")
        self.hash_values = np.minimum(other.hash_values, self.hash_values)

    def digest(self):
        return copy.copy(self.hash_values)

    def is_empty(self):
        if np.any(self.hash_values != _max_hash):
            return False
        return True

    def clear(self):
        self.hash_values = _init_hash_values(len(self))

    def copy(self):
        return MinHash(seed=self.seed, hash_func=self.hash_func,
                       hash_values=self.digest(),
                       permutations=self.permutations)

    def __len__(self):
        return len(self.hash_values)

    def __eq__(self, other):
        return type(self) is type(other) and \
               self.seed == other.seed and \
               np.array_equal(self.hash_values, other.hash_values)

    @classmethod
    def union(cls, *mhs):
        if len(mhs) < 2:
            raise ValueError("Cannot union less than 2 MinHash")
        num_perm = len(mhs[0])
        seed = mhs[0].seed
        if any((seed != m.seed or num_perm != len(m)) for m in mhs):
            raise ValueError("The unioning MinHash must have the\
                    same seed and number of permutation functions")
        np.minimum.reduce([m.hash_values for m in mhs])
        permutations = mhs[0].permutations
        return cls(num_perm=num_perm, seed=seed, permutations=permutations)

    @classmethod
    def bulk(cls, b, **minhash_kwargs):
        return list(cls.generator(b, **minhash_kwargs))

    @classmethod
    def generator(cls, b, **minhash_kwargs):
        m = cls(**minhash_kwargs)
        for _b in b:
            _m = m.copy()
            _m.update_batch(_b)
            yield _m

class Node:
    def __init__(self, height=0, elem=None):
        self.elem = elem
        self.next = [None] * height


def random_height():
    height = 1
    while randint(1, 2) != 1:
        height += 1
    return height


class SkipList:

    def __init__(self):
        self.head = Node()
        self.len = 0
        self.maxHeight = 0

    def __len__(self):
        return self.len

    def find(self, elem, update=None):
        if update is None:
            self.update_list(elem)
        elif len(update) > 0:
            item = update[0].next[0]
            if item is not None and item.elem == elem:
                return item
        return None

    def contains(self, elem, update=None):
        return self.find(elem, update) is not None

    def update_list(self, elem):
        update = [None] * self.maxHeight
        x = self.head
        for i in reversed(range(self.maxHeight)):
            while x.next[i] is not None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        return update

    def insert(self, elem):

        _node = Node(random_height(), elem)

        self.maxHeight = max(self.maxHeight, len(_node.next))
        while len(self.head.next) < len(_node.next):
            self.head.next.append(None)

        update = self.update_list(elem)
        if self.find(elem, update) is None:
            for i in range(len(_node.next)):
                _node.next[i] = update[i].next[i]
                update[i].next[i] = _node
            self.len += 1

    def remove(self, elem):

        update = self.update_list(elem)
        x = self.find(elem, update)
        if x is not None:
            for i in reversed(range(len(x.next))):
                update[i].next[i] = x.next[i]
                if self.head.next[i] is None:
                    self.maxHeight -= 1
            self.len -= 1

    def print_list(self):
        for i in range(len(self.head.next) - 1, -1, -1):
            x = self.head
            while x.next[i] is not None:
                print(x.next[i].elem)
                x = x.next[i]
            print('')

