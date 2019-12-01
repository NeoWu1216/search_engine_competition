import json
import subprocess
import xml.etree.ElementTree as ET
import metapy
from sys import exit
from time import sleep


def single_experiment():

    outputcollection = []

    path_parsed = "../Assignment_initial_datasets/General_data/"
    with open(path_parsed + 'doc_lines', "r", encoding='ISO-8859-1') as f:
        papers = f.read().split('\n')
    print(len(papers))
    print('File loaded')

    idx = metapy.index.make_inverted_index('main.toml')
    forward_idx = metapy.index.make_forward_index('main.toml')
    print('Index processed')


    # Initialize ranker
    ranker = metapy.index.OkapiBM25(k1=0.8, b=0.5, k3=500)


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
            # top_docs = ranker.score(idx, q, num_results=100)
            rocchio = metapy.index.Rocchio(forward_idx, ranker, 0.8, 0.9, 20)
            top_docs = rocchio.score(idx, q, 30)
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


if __name__ == '__main__':
    single_experiment()