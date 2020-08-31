import argparse
import os

import matplotlib.pyplot as plt

import pandas as pd

# plt.rcParams.update({'text.usetex': True})


def csv2bar(csv):
    df = pd.read_csv(csv)
    file = '.'.join(os.path.basename(csv).split(".")[0:-1])
    name = df.columns[0]
    xy = name.split('\\')
    df.plot.bar(x=name)

    plt.title(file.replace('_', ' '))
    plt.xlabel(xy[0])
    plt.ylabel(xy[1])

    plt.tight_layout()

    plt.savefig(file + '.pdf')
    plt.show()

    # plt.savefig(file + '.pgf')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to create a graph from a CSV file')
    parser.add_argument('csv', help='CSV to graph')
    args = parser.parse_args()

    csv2bar(args.csv)
