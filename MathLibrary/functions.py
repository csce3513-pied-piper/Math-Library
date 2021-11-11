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