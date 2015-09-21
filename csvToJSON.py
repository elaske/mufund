import csvAtRow
import csv
import locale
import json
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--row', type=int, default=0, help='Specify the row to start converting.')
    parser.add_argument('infile', metavar='infile', nargs='+', type=str, help='The file(s) to convert.')
    parser.add_argument('-o','--outfile', default=sys.stdout, type=argparse.FileType('w'), help='Specify an output file.')
    args = parser.parse_args()

    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

    # Output structure separated for file
    if len(args.infile) > 1:
        output = {i.split('.')[0]:[] for i in args.infile}
    else:
        output = []

    for infile in args.infile:
        dataFile = csvAtRow.csvAtRow(infile, args.row)
        dataReader = csv.reader(csvAtRow.csvAtRow(infile, args.row))
        header = dataReader.next()

        # Get all the data from the csv file
        for row in dataReader:
            # Convert to dictionary
            row = { header[idx].lower():row[idx]  # Convert to lowercase
                    for idx in range(0,len(row))  # For all of the columns
                    if header[idx] and row[idx] } # Only if both are unempty

            # Pass on empty rows
            if not row: continue

            # Go through all the keys and convert / format as necessary
            for key in row.keys():
                # Strip all the whitespace out of any field
                row[key].strip()
                # If there's accounting formatting, remove and convert to negative
                if '(' in row[key]: # This should be fixed to not include being in numbers
                    row[key] = row[key].strip('()')
                    # Convert the numbers to numbers
                    try:
                        temp = locale.atof(row[key])
                        row[key] = -temp
                    except ValueError:
                        pass
                else:
                    # Convert the numbers to floats 
                    try:
                        temp = locale.atof(row[key])
                        row[key] = temp
                    except ValueError:
                        pass

            # Add to the output list
            if len(args.infile) > 1:
                output[infile.split('.')[0]].append(row)
            else:
                output.append(row)

    # Write the entire list to the output file
    args.outfile.write(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == '__main__':
    main()
