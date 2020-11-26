import argparse
import os

from PyPDF2 import PdfFileMerger
from model import score
# from model.score import *
from view import radar
from view.csv2tab import csv2bar


def merge_pdfs(pdfs, output):
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)
    merger.write(output + 'report.pdf')
    merger.close()


def scoring(indi):
    score_list = list()
    for key in indi.keys():
        try:
            score_list.append(getattr(score, key)(indi))
        except AttributeError:
            print("Method `{}` is not implemented".format(key))
    return score_list


def report(name, indi):
    data = [indi.keys(), ('Radar Score', [scoring(indi)])]
    fig = radar.graph(data, name + '/pdf/radar.pdf')

    return fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to create a report from different CSV file')
    parser.add_argument('csvs', nargs='+', help='CSVs to analyse')
    args = parser.parse_args()

    csvs = args.csvs

    for csv in csvs:
        csv2bar(csv)

    pdfs = [f for f in os.listdir(os.path.dirname(csvs[0])) if os.path.isfile(f) and f.endswith('.pdf')]
    merge_pdfs(pdfs, '/'.join(os.path.dirname(csvs[0]).split('/')[0:-1]) + '/pdf/')
