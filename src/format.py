import csv


def csv_to_table(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=",")
