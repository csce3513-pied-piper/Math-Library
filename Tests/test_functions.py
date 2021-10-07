import sys

sys.path.insert(0, './MathLibrary')

import functions
import random

#One group t-test
def ogtt_test():
    data_set = []
    for i in range(0, 10):
        data_set.append(random.randrange(100))
        print("Data point " + str(i) + ": " + str(data_set[i]))
    h_mean = random.randrange(100)
    print("Hypothetical mean: " + str(h_mean))

    print("T-value: " + str(functions.one_group_t_test(data_set, h_mean)))


ogtt_test()
    