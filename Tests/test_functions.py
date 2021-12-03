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

#Prime factorization test
def prime_factor_test():
    x = random.randrange(0, 1000000)
    print("x: " + str(x))
    print(functions.prime_factorization(x))

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

#Is sphenic number test
def sphenic_test():
    x = 105
    assert(functions.is_sphenic_number(x) == True), "Sphenic number test failed!"
    x = 12
    assert(functions.is_sphenic_number(x) == False), "Sphenic number test failed!"
    print("Sphenic number test succeeded!")

#Is hoax number test
def hoax_test():
    x = 12955
    assert(functions.is_hoax_number(x) == True), "Hoax number test failed!"
    x = 7
    assert(functions.is_hoax_number(x) == False), "Hoax number test failed!"
    print("Hoax number test succeeded!")

#Modular inverse test
def mod_inverse_test():
    n = random.randrange(0, 1000)
    m = random.randrange(1, 10000)
    print("n: " + str(n))
    print("m: " + str(m))
    print(functions.mod_inverse(n,m))

#Multiplicative order test
def mult_order_test():
    n = random.randrange(0, 1000)
    m = random.randrange(1, 10000)
    print("n: " + str(n))
    print("m: " + str(m))
    print(functions.mult_order(n,m))

#Is Smith number test
def smith_test():
    x = 666
    assert(functions.is_smith_number(x) == True), "Smith number test failed!"
    x = 13
    assert(functions.is_smith_number(x) == False), "Smith number test failed!"
    print("Smith number test succeeded!")

#Is Mersenne Prime test
def mersenne_test():
    x = 2147483647
    assert(functions.is_mersenne_prime(x) == True), "Mersenne Prime test failed!"
    x = 11
    assert(functions.is_mersenne_prime(x) == False), "Mersenne Prime test failed!"
    print("Mersenne prime test succeeded!")

#Is circular prime test
def circular_test():
    x = 197
    assert(functions.is_circular_prime(x) == True), "Circular Prime test failed!"
    x = 23
    assert(functions.is_circular_prime(x) == False), "Circular Prime test failed!"
    print("Circular Prime test succeeded!")

#Juggler sequence test
def juggler_test():
    n = random.randrange(0, 1000)
    print("n: " + str(n))
    print(functions.juggler_sequence(n))

#Power set test
def power_set_test():
    test_list = ["a", "b", "c"]
    print(functions.get_power_set(test_list))

#Max subset gcd test
def max_sub_test():
    test_list = [12, 15, 2]
    print(functions.max_sub_gcd(test_list))

#Padovan sequence test
def padovan_test():
    x = random.randrange(0, 50)
    print("x: " + str(x))
    print(functions.padovan(x))

#Aliquot sequence test
def aliquot_test():
    x = random.randrange(0, 50)
    print("x: " + str(x))
    print(functions.aliquot(x))

#Is abundant number test
def is_abundant_test():
    x = 18
    assert(functions.is_abundant(x) == True), "Abundant number test failed!"
    x = 23
    assert(functions.is_abundant(x) == False), "Abundant number test failed!"
    print("Abundant number test succeeded!")

#Get abundance test
def abundance_test():
    x = random.randrange(0, 50)
    print("x: " + str(x))
    print(functions.get_abundance(x))

#Is lucky test
def is_lucky_test():
    n = 18
    assert(functions.is_lucky(n) == True), "Lucky number test failed!"
    n = 22
    assert(functions.is_lucky(n) == False), "Lucky number test failed!"
    print("Lucky number test succeeded!")

#Is arithmetic test
def is_arithmetic_test():
    n = 1
    assert(functions.is_arithmetic(n) == True), "Arithmetic number test failed!"
    n = 2
    assert(functions.is_arithmetic(n) == False), "Arithmetic number test failed!"
    print("Arithmetic number test succeeded!")

#Is friendly pair test
def friendly_pair_test():
    n = 6
    m = 28
    assert(functions.is_friendly_pair(n, m) == True), "Friendly pair test failed!"
    n = 18
    m = 26
    assert(functions.is_friendly_pair(n, m) == False), "Friendly pair test failed!"
    print("Friendly pair test succeeded!")

#Is perfect number test
def perfect_number_test():
    n = 8128
    assert(functions.is_perfect_number(n) == True), "Perfect number test failed!"
    n = 54
    assert(functions.is_perfect_number(n) == False), "Perfect number test failed!"
    print("Perfect number test succeeded!")

#Is Sophie Germain prime test
def sg_prime_test():
    n = 509
    assert(functions.is_sg_prime(n) == True), "Sophie Germain prime test failed!"
    n = 54
    assert(functions.is_sg_prime(n) == False), "Sophie Germain prime test failed!"
    print("Sophie Germain prime test succeeded!")
    
#Is twisted prime test
def twisted_prime_test():
    n = 17
    assert(functions.is_twisted_prime(n) == True), "Twisted prime test failed!"
    n = 19
    assert(functions.is_twisted_prime(n) == False), "Twisted prime test failed!"
    print("Twisted prime test succeeded!")

#Quad discriminant test
def quad_discriminant_test():
    a = random.randrange(-50, 50)
    b = random.randrange(-50, 50)
    c = random.randrange(-50, 50)
    print("a: " + str(a))
    print("b: " + str(b))
    print("c: " + str(c))
    print(functions.quad_discriminant(a,b,c))

#Cubic discriminant test
def cubic_discriminant_test():
    a = random.randrange(-50, 50)
    b = random.randrange(-50, 50)
    c = random.randrange(-50, 50)
    d = random.randrange(-50, 50)
    print("a: " + str(a))
    print("b: " + str(b))
    print("c: " + str(c))
    print("d: " + str(d))
    print(functions.cubic_discriminant(a,b,c,d))
