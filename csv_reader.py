import csv

def csv_reader():
    f_name = input("Enter the file name: ")
    print(f_name)
    with open (f_name, newline = '') as f:
        reader = csv.reader(f)
        data = list(reader)
    print(data)
    return data

csv_reader()