import multiprocessing as mp
import requests
import csv

API_TOKEN = "bd08ade0ad1688c0caed2b814cac344deef3751f"

BASE_URL = "https://owlbot.info/api/v4/dictionary/{}"

def add_auth_header(header):
    key = "Authorization"
    value = "Token {}".format(API_TOKEN)
    header[key] = value

def get_url(word):
    return BASE_URL.format(word)

def get_meaning(word):
    print word
    res = []
    headers = {}
    add_auth_header(headers)
    url = get_url(word)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        for result in resp.json()['definitions']:
            row = encode_row(word, result['type'], result['definition'], )
            res.append(row)
    return res

def yield_words():
    with open('/Users/rajtilakindrajit/Documents/Linux/codes/petrichor/words_alpha_sorted.txt') as f:
        for word in f:
            clean_word = word.strip()
            yield clean_word

def get_all_meanings(alpha, start_at):
    pool = mp.Pool(mp.cpu_count())
    for word in yield_words():
        if word[0] == alpha:
            if start_at:
                if word > start_at:
                    yield pool.apply(get_meaning, args=(word, ))
            else:
                yield pool.apply(get_meaning, args=(word, ))
    pool.close()

def encode_row(*args):
    res = []
    for x in args:
        if x is None:
            res.append('')
        else:
            res.append(x.encode('utf-8'))
    return res

def get_last_word(csv_file):
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        pass
    if row is not None:
        return row[0]
    return ''

def run():
    import sys
    try:
        alpha = sys.argv[1]
    except IndexError:
        print "Mention the alphabet range suffix"
        sys.exit(1)
    print 'Getting meanings for words starting with: {}'.format(alpha)

    start_at = None
    with open('owl_bot_meanings.{}.csv'.format(alpha), 'r') as csv_file:
        start_at = get_last_word(csv_file)
    print 'Starting at :{}'.format(start_at)

    with open('owl_bot_meanings.{}.csv'.format(alpha), 'ab') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for meanings in get_all_meanings(alpha, start_at):
            csv_writer.writerows(meanings)
run()
