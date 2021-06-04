import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd


# plt.rcParams.update({'text.usetex': True})


def csv2bar(csv):
    df = pd.read_csv(csv)
    df = df.head(10)
    df = df.iloc[:, : 10]
    file = '.'.join(os.path.basename(csv).split(".")[0:-1])
    basedir = '/'.join(os.path.dirname(csv).split('/')[0:-1]) + '/pdf/'

    print("Starting graph on " + file)

    x_axis = df.columns[0]
    xy = x_axis.split('\\')
    ax = df.plot.bar(x=x_axis)

    plt.title(file.replace('_', ' ').capitalize())
    plt.xlabel(xy[0])
    plt.ylabel(xy[1])

    plt.legend(loc='center left', bbox_to_anchor=(1, .5))
    plt.tight_layout()

    print("Saving graph as PDF")

    os.makedirs(basedir, exist_ok=True)

    # plt.savefig(basedir + file + '.pgf')
    plt.savefig(basedir + file + '.pdf')
    # plt.show()

    return ax.get_figure()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Python script to create a graph from a CSV file')
    parser.add_argument('csv', help='CSV to graph')
    args = parser.parse_args()

    csv2bar(args.csv)
