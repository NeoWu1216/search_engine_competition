import json

total_doc = []
with open('Academic_papers/docs.json', 'r') as infile:
    for line in infile:
        document = json.loads(line)
        doc_content = ''
        try:
            doc_content += document['docno'] + ' '
        except:
            pass
        try:
            doc_content += ' '.join(document['keyPhrases']) + ' '
        except:
            pass
        try:
            doc_content += ' '.join(document['title']) + ' '
        except:
            pass
        total_doc.append(doc_content)

# with open('Academic_papers/Academic_papers.dat', 'w', encoding="utf-8") as outfile:
#     for line in total_doc:
#         outfile.write(line)
#         outfile.write("\n")
