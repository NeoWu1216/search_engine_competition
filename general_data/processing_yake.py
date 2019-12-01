
import yake
import os
from time import time
from threading import Thread
from multiprocessing import Process
import pickle

with open('Dataset\Dataset.dat') as f:
    data = f.read()
lines = data.split('\n')

# %%


def build_dict(doc):
    max_ngram_size = 1
    numOfKeywords = 20
    kw_extractor = yake.KeywordExtractor(n=max_ngram_size, top=numOfKeywords)
    keywords = kw_extractor.extract_keywords(doc)

    res = {}
    for kw in keywords:
        k, v = kw
        res[k] = v
    return res


def get_features(lines, id):
    features = {}

    for i in range(len(lines)):
        docid = lines[i].split('<')[0]
        features[docid] = build_dict(lines[i])

    with open('saved_{}_{}.pickle'.format(id, time()), 'wb') as f:
        pickle.dump(features, f)

    print('Done')

if __name__ == '__main__':
    lines.pop()
    # print(len(lines))
    # lines = lines[3*len(lines) // 4 - 1: len(lines)]
    #
    start = time()
    total = 4
    processes = [None] * total
    for i in range(total):
        processes[i] = Process(target=get_features, args=(lines[i * len(lines) // total: (i + 1) * len(lines) // total], i))
        processes[i].start()

    for i in range(total):
        processes[i].join()

    print('{}s elapsed'.format(time() - start))