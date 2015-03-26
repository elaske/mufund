import csv
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--row', type=int, default=0, help='Specify the row to start converting.')
    parser.add_argument('infile', metavar='infile', nargs='+', type=str, help='The file(s) to convert.')
    parser.add_argument('outfile', nargs='?', default=sys.stdout, type=argparse.FileType('w'), help='Specify an output file.')
    args = parser.parse_args(['-r','8','Investment Returns - Escrow.csv'])

    for infile in args.infile:
        # rowList = [ row for row in csv.DictReader(csvAtRow(infile, args.row)) ]
        rowList = [ row for row in csv.reader(csvAtRow(infile, args.row)) ]
        # Exit if there's nothing in here.
        if not rowList:
            return

        # If there's a file, write out to it.
        if args.outfile:
            if type(rowList[0]) is dict:
                header = rowList[0].keys()
            if type(rowList[0]) is list:
                writer = csv.writer(args.outfile)
                for row in rowList:
                    writer.writerow(row)

        # Otherwise, print to the screen.
        else:
            if type(rowList[0]) is dict:
                for row in rowList:
                    print row
            if type(rowList[0]) is list:
                for row in rowList:
                    print ', '.join(row)

def csvAtRow(file, row=0):
    csvFile = open(file)
    while row > 0:
        csvFile.readline()
        row -= 1
    return csvFile

if __name__ == '__main__':
    main()
