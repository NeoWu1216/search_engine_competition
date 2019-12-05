import sys
import metapy
import math

# Path of parsed papers
path_parsed = "./Academic_papers/"

class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
        # Q.count(t) * tfn / (tfn + c) * log_2((N+1)/(C.count(t)+0.5) where tfn = D.count(t)*log_2(1 + avgdl/len(D))
        # print("avg_dl: {}".format(sd.avg_dl))
        # print("num_docs: {}".format(sd.num_docs))
        # print("total_terms: {}".format(sd.total_terms))
        # print("query_length: {}".format(sd.query_length))
        # print("t_id: {}".format(sd.t_id))
        # print("query_term_weight: {}".format(sd.query_term_weight))
        # print("doc_count: {}".format(sd.doc_count))
        # print("corpus_term_count: {}".format(sd.corpus_term_count))
        # print("d_id: {}".format(sd.d_id))
        # print("doc_term_count: {}".format(sd.doc_term_count))
        # print("doc_size: {}".format(sd.doc_size))
        # print("doc_unique_terms: {}".format(sd.doc_unique_terms))
        # print("================================================================================")
        #return (self.param + sd.doc_term_count) / (self.param * sd.doc_unique_terms + sd.doc_size)

        c = self.param
        N = sd.num_docs
        tfn = sd.doc_term_count*math.log2(1 + sd.avg_dl/sd.doc_size)
        return sd.query_term_weight * tfn / (tfn + c) * math.log2((N+1)/(sd.corpus_term_count+0.5))

class PL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.param = some_param
        # You *must* call the base class constructor here!
        super(PL2Ranker, self).__init__()

    def score_one(self, sd):
        tfn = sd.doc_term_count*math.log(1.0+self.param*sd.avg_dl/float(sd.doc_size),2)
        lamb = float(sd.num_docs)/float(sd.corpus_term_count)
        frac = (tfn*1.0*math.log(tfn*lamb,2)+(math.log(math.e,2))*(1.0/lamb-tfn)+0.5*math.log(2*math.pi*tfn,2))/float(tfn+1.0)
        if lamb<1.0 or tfn<=0:
            return 0
        return sd.query_term_weight*frac*1.0

def query(string):
    with open(path_parsed + 'Academic_papers.dat', "r", encoding='utf-8') as f:
        papers = f.read().split('\n')
        
    # Create inverted index
    fwd_idx = metapy.index.make_forward_index('main.toml')
    idx = metapy.index.make_inverted_index('main.toml')
    # Initialize ranker
    ranker = metapy.index.JelinekMercer(0.87)
    # Initialize query
    q = metapy.index.Document()
    q.content(string)
    # Get documents
    top_docs = ranker.score(idx, q, num_results=100)
    rocchio = metapy.index.Rocchio(fwd_idx, ranker, 0.9, 0.9, 25, 100)    
    #rocchio = metapy.index.KLDivergencePRF(fwd_idx, ranker, 0.6, 0.5, 20)    
    top_docs = rocchio.score(idx, q, 30)
    # Construct search results
    search_result = ""
    for d_id, _ in top_docs:
        search_result += papers[d_id].split(" ")[0]
        search_result += "\t" + str(_)
        search_result += "\n"
        
    return search_result

if __name__ == '__main__':
    print(query(sys.argv[1]))
