__author__ = 'leif'
from whoosh.index import open_dir
import nltk


def tokenize_text(raw_text):
    """
    :return: list of terms that are normalize (i.e. lowercase, a-z, longer than 2)
    """
    tokens = nltk.wordpunct_tokenize(raw_text)
    text = nltk.Text(tokens)
    words = [w.lower() for w in text if w.isalpha() and len(w)>2]
    return words


def count_bigrams(bigrams_dict, word_list):
    l = len(word_list)
    for j in range(1,l):
        bigram = '{0} {1}'.format(word_list[j-1],word_list[j])
        if bigram in bigrams_dict:
            bigrams_dict[bigram] += 1
        else:
            bigrams_dict[bigram] = 1


def count_unigrams(unigrams_dict, word_list):
    for w in word_list:
        if w in unigrams_dict:
            unigrams_dict[w] += 1
        else:
            unigrams_dict[w] = 1

def main():

    whoosh_index_dir='fullindex/'
    ix = open_dir(whoosh_index_dir)
    ixr = ix.reader()

    id_list = ixr.all_doc_ids()

    i = 0
    grams = dict()

    for id in id_list:

        fields = ixr.stored_fields(int(id))
        title = fields["title"]
        content = fields["content"]

        words = tokenize_text(title)
        count_bigrams(grams,words)

        count_unigrams(grams,words)

        words = tokenize_text(content)
        count_bigrams(grams,words)



        i+=1

        if i==0:
            break


    for words in grams:
        if grams[words] > 50:
            print '{0}, {1}'.format(words, grams[words])


if __name__ == "__main__":
    main()