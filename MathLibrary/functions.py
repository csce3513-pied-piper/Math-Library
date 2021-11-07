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

#Perform chi square goodness of fit test
def chi_square_gof(observed, expected):

    result = 0.0

    for i in range(0, len(observed) - 1):
         temp = (observed - expected) ** 2
         temp = temp/expected
         result = result + temp

    #Result is the test statistic of the Chi-Square test
    return result
        