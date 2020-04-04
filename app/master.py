dirs = ['gutenberg/gutenberg_meaning', 'owl_bot/owl_bot_meanings', 'wordnet/wordnet']
import csv

def run():
    for i in range(65, 91):
        for dname in dirs:
            alpha = chr(i)
            with open('{}.{}.csv'.format(dname, alpha), 'rU') as csv_file:
                with open('master.csv'.format(alpha), 'ab') as csv_out:
                    csv_reader = csv.reader(csv_file)
                    csv_writer = csv.writer(csv_out, delimiter=',')
                    for row in csv_reader:               
                        csv_writer.writerow(row)

run()
