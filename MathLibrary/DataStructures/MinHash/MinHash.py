import copy
import hashlib
import struct

import numpy as np


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
