import json
import math

total_doc = []
with open('Academic_papers/docs.json', 'r') as infile:
    for line in infile:
        document = json.loads(line)
        doc_content = ''
        try:
            doc_content += ' '.join(document['keyPhrases']) + ' '
            doc_content += ' '.join(document['keyPhrases']) + ' '
            doc_content += ' '.join(document['keyPhrases']) + ' '
            doc_content += ' '.join(document['keyPhrases']) + ' '
            doc_content += ' '.join(document['keyPhrases']) + ' '
        except:
            pass
        try:
            doc_content += ' '.join(document['title']) + ' '
            doc_content += ' '.join(document['title']) + ' '
            doc_content += ' '.join(document['title']) + ' '
            doc_content += ' '.join(document['title']) + ' '
            doc_content += ' '.join(document['title']) + ' '
        except:
            pass
        try:
            key_citations = document['numKeyCitations'][0] + 1
            weight = math.ceil(math.log(key_citations,2))
            doc_content = doc_content*weight
        except:
            pass
        try:
            doc_content += ' '.join(document['paperAbstract']) + ' '
        except:
            pass
        try:
            doc_content = document['docno'] + ' ' + doc_content
        except:
            pass
        total_doc.append(doc_content)

with open('Academic_papers/Academic_papers.dat', 'w', encoding="utf-8") as outfile:
    for line in total_doc:
        outfile.write(line)
        outfile.write("\n")
