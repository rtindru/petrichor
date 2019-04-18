import glob
import csv
import re

data = []

def process_csv(csvfile):
    for row in csvfile:
        if not row.strip():
            continue
        try:
            w, m = process_row(row)
        except Exception as e:
            print(row)
        else:
            data.append((w, m))

def process_row(row):
    fmt = r'\"?([a-zA-Z-\s\d\'\.]+)\s\(.*?\)(.*)\"?'
    match = re.match(fmt, row)
    word, meaning = match.group(1).strip(), match.group(2).strip()
    return word, meaning

def write_out():
    with open('res_gutenberg.csv', 'w') as outfile:
         writer = csv.writer(outfile, delimiter=',', quotechar='"')
         for row in data:
             writer.writerow(row)

for filename in glob.glob('gutenberg_csv/*.csv'):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        try:
            process_csv(csvfile)
        except Exception as e:
            print("exception processing: {}\n{}".format(filename, e))

    write_out()
