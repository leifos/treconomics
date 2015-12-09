__author__ = 'leif'


#from ifind.common.autocomplete_trie import AutocompleteTrie
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.search import Query
import nltk

from bs4 import BeautifulSoup



# http://benjamindalton.com/extracting-nouns-with-python/

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names



def extract_nouns(text):

    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    all_words = []
    for ts in tokenized_sentences:
        for w in ts:
            all_words.append(w)

    tagged = nltk.pos_tag(all_words)
    nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns



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




def main():

    bm25 = Whooshtrec(
    whoosh_index_dir='fullindex/',
    stopwords_file='',
    model=1,
    newschema=True)


    query = Query('Sea Pirates')
    query.skip = 1
    query.top = 5

    bm25.snippet_size = 3


    response = bm25.search(query)
    i = 1
    for result in response.results:
        print i,len(result.summary)
        #print result.summary
        #print "--------------"
        soup = BeautifulSoup(result.summary,'html.parser')
        text = soup.getText()
        #print text


        print "--------------"

        n = extract_nouns(text)
        print set(n)
        print "--------------"

        sentences = nltk.sent_tokenize(text)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

        #print tokenized_sentences
        cat_sentences = []
        for ts in tokenized_sentences:
            for w in ts:
                cat_sentences.append(w)

        #print cat_sentences

        tagged =  nltk.pos_tag(cat_sentences)
        nouns = [word for word,pos in tagged if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        downcased = [x.lower() for x in nouns]
        joined = " ".join(downcased).encode('utf-8')
        into_string = str(nouns)
        print (into_string)

        #print tokenized_sentences

        print "--------------"
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.chunk.ne_chunk_sents(tagged_sentences, binary=True)
        entity_names = []
        for tree in chunked_sentences:
            # Print results per sentence
            # print extract_entity_names(tree)

            entity_names.extend(extract_entity_names(tree))

        print set(entity_names)

        i+=1



if __name__ == "__main__":
    main()




# Print all entity names
#print entity_names

# Print unique entity names
