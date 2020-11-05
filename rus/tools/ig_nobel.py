import re
from random import uniform, choice
from collections import defaultdict
import numpy as np
from fuzzywuzzy import process
import pickle
import argparse


# generator - all lines to lower register
def gen_lines(corpus):
    data = open(corpus, encoding = 'utf-8')
    # lines = []
    # for line in data:
        # lines.append(line)
    # print(len(lines))
    # return lines
    for line in data:
        yield line.lower()

# generator - tokens out of lines
def gen_tokens(lines):

    # symbols to keep
    r_alphabet = re.compile(u'[a-zA-Z0-9-]+|[.,:;?!]+')
    r_filter = '(\w+)?[-]?\d+[-,.]?(\w+)?[\d+]?'

    exceptions = ['as', 'at', 'but', 'by', 'for', 'in', 'of', 'off', 'on', 'out', 'per', 'to', 'up', 'via', 'a', 'the', 'and',
    '.', ',', ':', ';', 'pi', 'new', 'bar', 'sum', 'sea', 'low', 'gas']

    for line in lines:
        tokens = r_alphabet.findall(line)
        for token in tokens:
            if re.match(r_filter, token):
                continue
            elif (len(token) <= 3) & (token not in exceptions):
                continue
            else:
                yield token

# generator - for each token      
def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$','$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1
    print('2')
    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model


# model fit
def fit(dataset):
    model = train(dataset)
    
    #dumping the fitted model to the file
    with open('model', 'wb') as f:
        pickle.dump(model, f)
    
    #tokens_set generation
    lines = list(gen_lines(dataset))
    tokens_set = set(gen_tokens(lines))
    
    with open('tokens_set', 'wb') as f:
        pickle.dump(tokens_set, f)



def unirand(seq):
    items = []
    for item, freq in seq:
        items.append(item)
    token = choice(items)
    return token


def generate_title(first_word, model, exception = '', query = ''):
    phrase = ''
    first_word = first_word.lower()
    t0, t1 = '$', first_word
    
    if len(exception) != 0:
        phrase += query + ' ' + exception
    else:
        phrase += first_word
    while len(phrase) < 100:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()



def run(keyword):
        
    with open('model', 'rb') as f:
        model = pickle.load(f)
            
    with open('tokens_set', 'rb') as f:
        tokens_set = pickle.load(f)
            
    try:
        print('\n', generate_title(keyword, model))
    except KeyError:
        print('Hmmmm... let me think...')
        extract = process.extract(keyword.lower(), tokens_set)
        exception = choice(extract)
        first_word = choice(['a', 'the'])
        print('\n', generate_title(first_word, model, exception[0], keyword.lower()))
    
            
      
# CLI
parser = argparse.ArgumentParser(description = 'Ig Nobel Prize Paper Titles Generator. Just insert any key word to generate title for scientific paper.')
parser.add_argument('mode', help = 'select the mode: fit or run. If fit, also insert dataset name; in case of run, insert keyword', type = str)
parser.add_argument('second_arg', help = 'For fit mode, insert dataset name; for run mode, insert keyword', type = str)
args = parser.parse_args()


if args.mode == 'fit':
    print('Fitting the model...')
    fit(args.second_arg)
elif args.mode == 'run':
    print('Handling your request...')
    run(args.second_arg)
else:
    print('Dear future Ig Nobel Prize Laureate, please insert either fit or run command :)')
