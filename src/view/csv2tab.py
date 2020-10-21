import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


# plt.rcParams.update({'text.usetex': True})


def csv2bar(csv):
    df = pd.read_csv(csv)
    file = '.'.join(os.path.basename(csv).split(".")[0:-1])
    basedir = '/'.join(os.path.dirname(csv).split('/')[0:-1]) + '/'
    x_axis = df.columns[0]
    xy = x_axis.split('\\')
    df.plot.bar(x=x_axis)

    plt.title(file.replace('_', ' ').capitalize())
    plt.xlabel(xy[0])
    plt.ylabel(xy[1])

    plt.tight_layout()

    # plt.savefig(basedir + file + '.pgf')
    plt.savefig(basedir + file + '.pdf')
    # plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to create a graph from a CSV file')
    parser.add_argument('csv', help='CSV to graph')
    args = parser.parse_args()

    csv2bar(args.csv)
