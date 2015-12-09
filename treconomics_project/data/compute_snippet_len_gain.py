__author__ = 'leif'

from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.search import Query
from ifind.common.language_model import LanguageModel
import nltk
import math

from bs4 import BeautifulSoup


def read_in_query_file(query_filename):
    """
    :param query_filename: query number and query string
    :return: a list of query strings
    """
    query_list = []
    qfile = open(query_filename,'r')
    while qfile:
        line = qfile.readline()
        vals = line.split()

        if len(vals)>0:
            query = vals[1:]
            query_list.append(query)
        else:
            break

    qfile.close()
    return query_list



def compute_info_gain(word_list, language_model):

    word_dict = dict()
    for word in word_list:
        if word in word_dict:
            word_dict[word] +=1
        else:
            word_dict[word] = 1
    wlm = LanguageModel(term_dict = word_dict)

    ig = 0.0

    for word in word_dict:
        pw = wlm.get_term_prob(word)
        pwc = language_model.get_term_prob(word)
        g = 0.0
        if pwc > 0.0:
            g = pw * (math.log(pwc)- math.log(pw))
        ig += g


    return ig


def compute_length(word_list):
    num_words = len(word_list)
    num_chars = 0
    for word in word_list:
        num_chars += len(word)
    return (num_words, num_chars)



def make_query(query_string):

    q = Query(query_string)
    q.skip = 1
    q.top = 10

    return q


def get_words_from_snippet(summary):
    soup = BeautifulSoup(summary,'html.parser')
    text = soup.getText()
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    #print tokenized_sentences
    cat_sentences = []
    for ts in tokenized_sentences:
        for w in ts:
            cat_sentences.append(w)

    downcased = [x.lower() for x in cat_sentences]
    return downcased


pl2_search_engine = Whooshtrec(
    whoosh_index_dir='fullindex/',
    stopwords_file='',
    model=2,
    newschema=True)





def main():

    #print "Making Language Model"
    lm = LanguageModel(file='vocab.in')

    #print "Reading in queries:"
    query_list = read_in_query_file('query.in')

    # read in vocab, and make lm.

    #print "Queries read in: {0}".format(len(query_list))
    sizes = [0, 1,2,3,4,5,6,7,8,9,10]

    qno = 0

    print "qno rno snip_size num_words num_chars ig t_num_words t_num_chars t_ig"
    for query in query_list:
        # create Query object
        query_str = ' '.join(query)
        #print "running through: ", query_str
        q = make_query(query_str)


        for s in sizes:
            pl2_search_engine.snippet_size = s
            response = pl2_search_engine.search(q)
            qno += 1
            rno = 0
            for r in response:
                rno += 1

                #calc len

                words = get_words_from_snippet(r.summary)
                (nwords,nchars) = compute_length(words)
                ig = compute_info_gain(words,lm)

                words = get_words_from_snippet(r.title + ' ' + r.summary)
                (tnwords,tnchars) = compute_length(words)

                tig = compute_info_gain(words,lm)


                print qno,rno, s, nwords,nchars, ig, tnwords, tnchars, tig



        # run query
        #




if __name__ == "__main__":
    main()