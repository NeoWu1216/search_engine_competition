import json
import subprocess
import xml.etree.ElementTree as ET
import metapy
from sys import exit
from time import sleep
from web_analysis import get_info
import numpy as np



def experiment(k1=1.2, b=0.75, k3=500):

    outputcollection = []

    path_parsed = "../Assignment_initial_datasets/General_data/"
    with open(path_parsed + 'doc_lines', "r", encoding='ISO-8859-1') as f:
        papers = f.read().split('\n')
    print(len(papers))
    print('File loaded')

    idx = metapy.index.make_inverted_index('main.toml')
    print('Index processed')


    # Initialize ranker
    ranker = metapy.index.OkapiBM25(k1=k1, b=b, k3=k3)


    tree = ET.parse('../Assignment_initial_datasets/General_data/testqueries.xml')
    root = tree.getroot()


    num = None
    for query in root:
        for elem in query:
            if elem.tag != 'text':
                num = int(elem.text)
                continue

            query_string = elem.text
            query_string = query_string[query_string.index('(')+1: query_string.index(')')]
            print('Processing '+query_string)
            # Initialize query
            q = metapy.index.Document()
            q.content(query_string)
            # Get documents
            top_docs = ranker.score(idx, q, num_results=100)
            # Construct search results
            search_result = ""
            for d_id, _ in top_docs:
                search_result += papers[d_id].split("<")[0]
                search_result += "\t" + str(_)
                search_result += "\n"


            # output = subprocess.Popen(['python3' ,'search.py', query_string], stdout=subprocess.PIPE).stdout.read()
            # output = output.decode('utf8')
            output = search_result.split("\n")[:-2]
            for i in range(len(output)):
                output[i] = str(num) + "\t" + output[i]
            outputcollection.extend(output)

    with open("../submission/Search_engine_competition/results/General_domain_results.txt", "w") as outfile:
        for line in outputcollection:
            outfile.write(line)
            outfile.write("\n")

    subprocess.check_call("submit_git.bat")

    prev = get_info()
    max_iter = 36
    curr = prev

    while curr == prev and max_iter > 0:
        max_iter -= 1
        sleep(5)
        prev = curr
        curr = get_info()

    if max_iter == 0:
        return 0
    print(curr)
    return curr[2]

# b : 0.3-0.9
# k1: 0.5-2.0


if __name__ == '__main__':
    close = lambda a,b : abs(a-b) < 0.01


    with open('experiment.txt') as f:
        txt = f.read().strip()
    params = set(map(lambda line: tuple(map(float, line.split()[:-1])),txt.split('\n')[1:]))


    for k1 in np.arange(0.39, 2.01, 0.1):
        for b in np.arange(0.3, 1, 0.1):
            k3 = 500

            if any(close(k1, p[0]) and close(b, p[1]) and close(k3, p[2]) for p in params):
                continue


            score = experiment(k1=k1, b=b, k3=k3)
            with open('experiment.txt', 'a') as f:
                f.write('{:.2f} {:.2f} {} {}\n'.format(float(k1), float(b), k3, score))

            params.add((k1, b, k3))