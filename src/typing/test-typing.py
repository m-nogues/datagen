import pandas as pd

csv = input("Enter path to csv")
df = pd.read_csv(csv, nrows=25)

with open('unsw-nb15.csv', 'w') as f:
    for name, dtype in df.dtypes.iteritems():
        line = str(name) + ", " + str(dtype) + "\n"
        f.write(line)