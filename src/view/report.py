import argparse

from PyPDF2 import PdfFileMerger


def merge_pdfs(pdfs):
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(pdf)
    merger.write('report.pdf')
    merger.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to merge PDFs into one file')
    parser.add_argument('pdfs', nargs='+', help='PDFs to merge')
    args = parser.parse_args()

    merge_pdfs(args.pdfs)
