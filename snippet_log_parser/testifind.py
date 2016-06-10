import sys
from ifind.search import Query
from ifind.search.engines.whooshtrec import Whooshtrec

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

whoosh_path = sys.argv[1]
stopwords_path = sys.argv[2]

page = 3
page_len = 10

search_engine = Whooshtrec(whoosh_index_dir=whoosh_path,
                           stopwords_file=stopwords_path,
                           model=1,
                           newschema=True)

query = Query('wildlife extinction')
query.skip = page
query.top = page_len

response = search_engine.search(query)

for result in response:
    print '{0} {1}'.format(result.whooshid, result.rank)

print response.result_total
print response.results_on_page
print response.actual_page

########

print
print

index = open_dir(whoosh_path)

searcher = index.searcher()
parser = QueryParser('content', index.schema)

parsed_terms = parser.parse('wildlife extinction')

res_page = searcher.search_page(parsed_terms, page, pagelen=page_len)
print dir(res_page)
print res_page.offset

#offsetlist = res_page.results[res_page.offset:]

for res in res_page.results:
    print res.docnum, res.rank
