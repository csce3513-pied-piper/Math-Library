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

#Kruskal Wallis test
def kw_test():
    L1 = [8.2, 10.3, 9.1, 12.6, 11.4, 13.2]
    L2 = [10.2, 9.1, 13.9, 14.5, 9.1, 16.4]
    L3 = [13.5, 8.4, 9.6, 13.8, 17.4, 15.3]
    groups = [L1, L2, L3]
    print(functions.kruskal_wallis(groups))

#Chi Square GOF Test
def csgof_test():
    observed = [180, 250, 120, 225, 225]
    expected = [200, 200, 200, 200, 200]
    print(functions.chi_square_gof(observed, expected))

#nth prime test
def nth_prime_test():
    x = random.randrange(0, 1000000)
    n = random.randrange(1, 10)
    print("x: " + str(x))
    print("n: " + str(n))
    print(functions.nth_prime(x,n))

#Get divisors test
def get_divisors_test():
    n = random.randrange(1,1000)
    print("n:" + str(n))
    print(functions.get_divisors(n))

#Is amicable pair test
def a_pair_test():
    x = 220
    y = 284
    assert(functions.is_amicable_pair(x,y) == True), "Amicable Pair test failed!"
    x = 15
    y = 100
    assert(functions.is_amicable_pair(x,y) == False), "Amicable Pair test failed!"
    print("Amicable Pair test succeeded!")


#ogtt_test()
#kw_test()
#csgof_test()
#nth_prime_test()
#get_divisors_test()
#a_pair_test()