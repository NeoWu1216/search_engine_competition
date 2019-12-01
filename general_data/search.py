import sys
import metapy

# Path of parsed papers
path_parsed = "../Assignment_initial_datasets/General_data/"

def query(string):
    with open(path_parsed + 'doc_lines', "r", encoding='ISO-8859-1') as f:
        papers = f.read().split('\n')
    return lazy_query(string, papers)


def lazy_query(string, papers):
    # Create inverted index
    idx = metapy.index.make_inverted_index('main.toml')
    # Initialize ranker
    ranker = metapy.index.OkapiBM25()
    # Initialize query
    q = metapy.index.Document()
    q.content(string)
    # Get documents
    top_docs = ranker.score(idx, q, num_results=100)
    # Construct search results
    search_result = ""
    for d_id, _ in top_docs:
        search_result += papers[d_id].split(" ")[0]
        search_result += "\t" + str(_)
        search_result += "\n"

    return search_result

if __name__ == '__main__':
    print(query(sys.argv[1]))
