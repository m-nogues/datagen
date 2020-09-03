import argparse
import os

from PyPDF2 import PdfFileMerger

from view.csv2tab import csv2bar


def merge_pdfs(pdfs):
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)
    merger.write('report.pdf')
    merger.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to create a report from different CSV file')
    parser.add_argument('csvs', nargs='+', help='CSVs to analyse')
    args = parser.parse_args()

    csvs = args.csvs

    for csv in csvs:
        csv2bar(csv)

    pdfs = [f for f in os.listdir(os.path.dirname(csvs[0])) if os.path.isfile(f) and f.endswith('.pdf')]
    merge_pdfs(pdfs)
