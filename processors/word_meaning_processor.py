import csv

data = []

with open('word-meaning-examples.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        word, meaning = row[0], row[1]
        data.append((word, meaning))

with open('res_wordmeaning.csv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"')
    for row in data:
        writer.writerow(row)

