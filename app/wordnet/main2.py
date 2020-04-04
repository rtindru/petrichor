import multiprocessing as mp
import csv
from nltk.corpus import wordnet

POS_DICT = {
    'n': 'noun',
    'a': 'adjective',
    'v': 'verb',
    'r': 'adverb',
}

def convert_pos(pos):
    # Try to convert known POS, fallback to original
    return POS_DICT.get(pos, pos)

def get_meaning(word):
    syns = wordnet.synsets(word)
    res = []
    for syn in syns:
        row = encode_row(word, convert_pos(syn.pos()), syn.definition())
        res.append(row)
    return res

def yield_words():
    with open('/Users/rajtilakindrajit/Documents/Linux/codes/petrichor/words_alpha.txt') as f:
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
    row = None
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
    try:
        with open('wordnet.{}.csv'.format(alpha), 'r') as csv_file:
            start_at = get_last_word(csv_file)
        print 'Starting at :{}'.format(start_at)
    except IOError:
        pass

    with open('wordnet.{}.csv'.format(alpha), 'ab') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for meanings in get_all_meanings(alpha, start_at):
            csv_writer.writerows(meanings)
run()
