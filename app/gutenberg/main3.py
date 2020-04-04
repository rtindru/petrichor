import re
import csv

def convert_pos(pos):
    if "n." in pos:
        return "noun"
    elif "a." in pos:
        return "adjective"
    elif "v." in pos:
        return "verb"
    elif "adv." in pos:
        return "adv"
    return "unknown"

def process_row(row):
    row = row.strip()
    REGEXP = r"\"?(.*?)\s(\(.*?\))\s(.*)"
    prog = re.compile(REGEXP)
    match = prog.match(row)
    if not match:
        return None

    word = match.group(1)
    pos = convert_pos(match.group(2))
    meaning = match.group(3)
    return [word, pos, meaning]

def run():
    for i in range(65, 91):
        res = []
        alpha = chr(i)
        with open('{}.csv'.format(alpha), 'r') as csv_file:
            for row in csv_file:
                entry = process_row(row)
                if entry is not None:
                    res.append(entry)
        with open('gutenberg_meaning.{}.csv'.format(alpha), 'ab') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            for row in res:
                csv_writer.writerow(row)
run()