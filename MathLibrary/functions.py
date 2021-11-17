import csv
import math

def csv_reader():
    f_name = input("Enter the file name: ")
    print(f_name)
    try:
        with open(f_name, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            print(data)
            return data
    except FileNotFoundError:
        print("File not found")

#=================================== Statistics Tests ================================================

#Performs one group t-test and returns t-value.
def one_group_t_test(data_set, h_mean):

    #Calculate sample size, sample mean, sample stdev
    s_size = len(data_set)
    s_mean = sum(data_set) / s_size
    
    variance = 0
    for num in data_set:
       variance += (num - s_mean) ** 2 
    s_stdev = math.sqrt(variance / (len(data_set) - 1))

    #Calculate t-value
    t_value = (s_mean - h_mean) / (s_stdev / math.sqrt(s_size))

    return t_value

#Performs chi square goodness of fit test
def chi_square_gof(observed, expected):

    result = 0.0

    #Check that observed and expected have the same number of entries
    if not len(observed) == len(expected):
        print("The observed and expected lists must be of the same length!")
        return

    for i in range(0, len(observed)):
         temp = (observed[i] - expected[i]) ** 2
         temp = temp/expected[i]
         result = result + temp

    #Result is the test statistic of the Chi-Square test
    return result
        

#Performs McNemar's Test and returns the test statistic
def mcnemars(group_one, group_two):
    try:
        #Determine possible values of dichotomous variable
        values = {}
        length = len(group_one)
        for i in range(0, length):
            if (not values.contains(group_one(i))):
                cont_table.add(group_one(i), 0)
        if(len(values) != 2):
            print("McNemar's test must be performed on a dichotomous variable")
            return

        #Populate contingency table
        cont_table = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0
        }
        for i in range(0, length):
            if (group_one(i) == values[0]) and (group_two(i) == values[0]):
                cont_table["A"] = cont_table["A"] + 1
            elif (group_one(i) == values[1]) and (group_two(i) == values[0]):
                 cont_table["B"] = cont_table["B"] + 1
            elif (group_one(i) == values[0]) and (group_two(i) == values[1]):
                 cont_table["C"] = cont_table["C"] + 1
            elif (group_one(i) == values[1]) and (group_two(i) == values[1]):
                 cont_table["D"] = cont_table["D"] + 1

        #Calculate test statistic
        t_stat = ((cont_table["B"] - cont_table["C"]) ** 2) / (cont_table["B"] + cont_table["C"])
        t_stat = t_stat ** .5
        return t_stat
            
    except IndexError:
        print("Data sets must be of the same size!")


#Performs Kruskal-Wallis one way analysis of variance
def kruskal_wallis(groups):
    #Initialize variables
    num_groups = len(groups)
    all_data = []
    ranked_data = {}
    group_lengths = []
    group_rank_sums = []

    #Check that test is valid
    if num_groups < 2:
        print("This test requires at least two groups!")
        return

    #Combine all lists into one and sort data
    for group in groups:
        group_lengths.append(len(group))
        for entry in group:
            all_data.append(entry)
    all_data.sort()
    total_entries = len(all_data)

    #Assign rank to each entry. Ranks are stored in lists to handle ties.
    i = 1
    for entry in all_data:
        if entry in ranked_data:
            ranked_data[entry].append(i)
        else:
            ranked_data[entry] = [i]
        i = i + 1

    #Take the sum of the ranks for each group
    j = 0
    for group in groups:
        group_rank_sums.append(0)
        for entry in group:
            group_rank_sums[j] = group_rank_sums[j] + (sum(ranked_data[entry]) / len(ranked_data[entry]))
        j = j + 1

    #Calculate H Statistic
    q1 = 0
    for index in range(0, num_groups):
        q1 = q1 + ((group_rank_sums[index] ** 2) / group_lengths[index])

    q2 = 12 / (total_entries * (total_entries + 1))

    h_stat = (q1 * q2) - (3 * (total_entries + 1))

    return h_stat

#=================================== Miscellaneous Algorithms ================================================

#Finds prime factorization of a number
def prime_factorization(x):
    if x <= 0:
        print("X must be a positive integer!")
        return

    #Index starts at two because it is the first prime number
    index = 2
    factors = []
    test = x

    #Loop through all integers from 2 until the midway point of factorization.
    while index <= (int)(test ** .5):

        #Divide by index as many times as possible. Add factor to list of factors
        while x % index == 0:
            x = (int) (x / index)
            factors.append(index)

        index = index + 1

    #Check if remaining x is prime
    if x > 2:
        factors.append(x)

    return factors

#Finds the nth prime factor of x
def nth_prime(x:int, n:int):
    #Get the prime factorization
    factors = prime_factorization(x)

    #Check if nth factor exists
    if len(factors) >= n:
        return factors[n - 1]
    else:
        return -1

#Finds all divosors of a natural number 
def get_divisors(n:int):
    divisors = []

    #Go through integers up to the multiplicative midpoint, which is the square root. Add divisors in pairs
    for i in range(1, (int) (n ** .5 + 1)):
        if(n % i == 0):
            divisors.append(i)

            #Add paired divisor if it is not the square root
            if not (n / i == i):
                divisors.append((int)(n/i))

    return divisors

#Check if number is prime. If it has exactly two divisors, return true
def is_prime(x):
    if(len(get_divisors(x)) == 2):
        return True
    return False

#Check if two numbers are an amicable pair.
def is_amicable_pair(num1, num2):
    if(sum(get_divisors(num1)) == sum(get_divisors(num2))):
        return True
    else:
        return False

#Check if a number is a sphenic number
def is_sphenic_number(x):

    #All sphenic numbers have 8 divisors
    divisors = get_divisors(x)
    divisors.sort()
    if (len(divisors) == 8):
        #The second, third, and fourth divisors must all be prime.
        if is_prime(divisors[1]) and is_prime(divisors[2]) and is_prime(divisors[3]):
            return True
        else:
            return False
    else:
        return False

#Find the sum of digits of a number
def sum_digits(x):
    sum = 0
    while x > 0:
        sum = sum + (x % 10)
        x = (int) (x / 10)

    return sum

#Check if a number is a hoax number
def is_hoax_number(x):
    #Hoax numbers must be composite numbers
    if(is_prime(x) or x <= 0):
        return False

    #Find unique prime factors of x
    all_factors = get_divisors(x)
    prime_factors = []

    for factor in all_factors:
        if(is_prime(factor)):
            prime_factors.append(factor)

    #Get sum of digits of prime factors
    pdigits_sum = 0
    for prime in prime_factors:
        pdigits_sum = pdigits_sum + sum_digits(prime)

    #Get sum of digits of x
    xdigits_sum = sum_digits(x)

    if(xdigits_sum == pdigits_sum):
        return True
    return False

#Calculate modular inverse
def mod_inverse(n, m):
    #Check that n and m are positive integers
    if not (n > 0 and m > 0):
        print("n and m must be positive integers")
        return -1

    for i in range(0, m-1):
        if((n * i) % m) == 1:
            return i
    return -1

#Check if two numbers a coprime
def is_coprime(n, m):
    if (math.gcd(n,m) == 1):
        return True
    return False

#Caclulate multiplicative order
def mult_order(n, m):
    #If n and m are not coprime, there is no multiplicative order
    if not is_coprime(n,m):
        return -1

    #m and n must be positive
    if m <= 0 or n <= 0:
        return -1

    #Use modular arithmetic to find i where n^i % m equals 1
    result = 1
    for i in range(1, m):
        result = (n * result) % m
        if(result == 1):
            return i

    return -1

#Determines if a number is a smith number
def is_smith_number(x):
    #Check if smith number is positive and composite
    if(x <= 0) or is_prime(x):
        print("x must be a positive, composite integer!")
        return False

    #Get sum of digits of x and of x's prime factorization. If they are equal, return true.
    x_digits = sum_digits(x)
    prime_factors = prime_factorization(x)
    prime_digits = 0

    for factor in prime_factors:
        prime_digits = prime_digits + sum_digits(factor)

    if(prime_digits == x_digits):
        return True
    return False

#Determines if a number is a Mersenne Prime
def is_mersenne_prime(x):
    #First, check that x is prime
    if(is_prime(x)):
        #Now, check if x is of the form 2^k - 1, where k is an integer >= 2.
        k = math.log((x + 1), 2)
        k = round(k, 10)
        if(k.is_integer() and k >= 2):
            return True

    return False


