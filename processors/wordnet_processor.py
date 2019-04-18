import csv

data = []

with open('wordnet20.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        word, meaning = row[2], row[7]
        data.append((word, meaning))

with open('res_wordnet20.csv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter=',', quotechar='"')
    for row in data:
        writer.writerow(row)


