from random import randint


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
