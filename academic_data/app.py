import json
import subprocess

outputcollection = []

with open('Academic_papers/test_queries.json', 'r') as infile:
    for line in infile:
        query = json.loads(line)
        query_string = query["query"]
        output = subprocess.Popen(['python3' ,'search.py', query_string], stdout=subprocess.PIPE).stdout.read()
        output = output.decode('utf8')
        output = output.split("\n")[:-2]
        for i in range(len(output)):
            output[i] = str(query["qid"]) + "\t" + output[i]
        outputcollection.extend(output)

with open("Academic_domain_results.txt", "w") as outfile:
    for line in outputcollection:
        outfile.write(line)
        outfile.write("\n")
