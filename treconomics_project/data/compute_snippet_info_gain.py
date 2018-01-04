from ifind.common.language_model import LanguageModel
from compute_snippet_len_gain import make_query, get_words_from_snippet, compute_length, compute_info_gain
import sys
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.search import Query

bm25_search_engine = Whooshtrec(
    whoosh_index_dir='/Users/leif/Code/treconomics/treconomics_project/data/test500index',
    stopwords_file='',
    model=1,
    newschema=True)

bm25_search_engine.snippet_size = 40


def main():
	log_file = sys.argv[1]
	lm = LanguageModel(file='vocab.in')
	
	# Interface...      1   2   3   4
	snippet_sizes    = [2,  0,  1,  4]
	snippet_surround = [40, 40, 40, 40]
	
	with open(log_file) as f:
		
		for s in f:
			fields = s.strip().split()
			amtid = fields[3]
			interface = fields[5]
			order = fields[6]
			topic = fields[7]
			query_str = ' '.join(fields[9:])
			query_str = query_str[1:-1]
			
			#print("{0} {1} {2} {3} {4}".format(amtid, interface, order, topic, query_str))
			q = make_query(query_str)
			
			# Added by David (2016-12-04) - added snippet size and surround properties
			interface_list_index = int(interface) - 1
			bm25_search_engine.snippet_size = snippet_sizes[interface_list_index]
			bm25_search_engine.set_fragmenter(frag_type=2, surround=snippet_surround[interface_list_index])
			
			# Issue the query to the search engine.
			response = bm25_search_engine.search(q)
			
			rno = 0
			for r in response:
				rno += 1
				words = get_words_from_snippet(r.summary)
				(nwords,nchars) = compute_length(words)
				ig = compute_info_gain(words,lm)
				words = get_words_from_snippet(r.title + ' ' + r.summary)
				(tnwords,tnchars) = compute_length(words)
				tig = compute_info_gain(words,lm)
				print("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(amtid, interface, order, topic ,rno, nwords,nchars, ig, tnwords, tnchars, tig))
				

if __name__ == "__main__":
	main()