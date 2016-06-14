__author__ = 'leif'
import os
import socket
import logging
import logging.config
import logging.handlers

from autocomplete_trie import AutocompleteTrie
from ifind.search.engines.whooshtrec import Whooshtrec
from experiment_setup import ExperimentSetup

work_dir = os.getcwd()
# when deployed this needs to match up with the hostname, and directory to where the project is


my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex/')
if 'local' not in socket.gethostname():
    my_whoosh_doc_index_dir = '/home/leifos/fullindex/'
    #my_whoosh_doc_index_dir = '/Users/david/Workspace/indexes/aquaint-whoosh-fullindex'

my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file = os.path.join(work_dir, "data/TREC2005.qrels.txt")
stopword_file = os.path.join(work_dir, "data/stopwords.txt")
data_dir = os.path.join(work_dir, "data")

print "Work DIR: " + work_dir
print "QRELS File: " + qrels_file
print "my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir
print "Stopword file: " + stopword_file

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with startexperiment/

exp_work_flows = [
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
     'anitatimeinstructions/TC/',
     'anitapretasksurvey/1/', 'search/1/', 'anitaposttask0survey/1/',
     'anitaposttask1survey/1/', 'anitaposttask2survey/1/',
     'anitaposttask3survey/1/', 'taskspacer/',
     'anitapretasksurvey/2/', 'search/2/', 'anitaposttask0survey/2/',
     'anitaposttask1survey/2/', 'anitaposttask2survey/2/',
     'anitaposttask3survey/2/', 'taskspacer/',
     'anitapretasksurvey/3/', 'search/3/', 'anitaposttask0survey/3/',
     'anitaposttask1survey/3/', 'anitaposttask2survey/3/',
     'anitaposttask3survey/3/', 'taskspacer/',
     'anitapretasksurvey/4/', 'search/4/', 'anitaposttask0survey/4/',
     'anitaposttask1survey/4/', 'anitaposttask2survey/4/',
     'anitaposttask3survey/4/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
     'anitatimeinstructions/NTC/',
     'anitapretasksurvey/1/', 'search/1/', 'anitaposttask0survey/1/',
     'anitaposttask1survey/1/', 'anitaposttask2survey/1/',
     'anitaposttask3survey/1/', 'taskspacer/',
     'anitapretasksurvey/2/', 'search/2/', 'anitaposttask0survey/2/',
     'anitaposttask1survey/2/', 'anitaposttask2survey/2/',
     'anitaposttask3survey/2/', 'taskspacer/',
     'anitapretasksurvey/3/', 'search/3/', 'anitaposttask0survey/3/',
     'anitaposttask1survey/3/', 'anitaposttask2survey/3/',
     'anitaposttask3survey/3/', 'taskspacer/',
     'anitapretasksurvey/4/', 'search/4/', 'anitaposttask0survey/4/',
     'anitaposttask1survey/4/', 'anitaposttask2survey/4/',
     'anitaposttask3survey/4/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
    ['startexperiment/', 'consent', 'preexperiment/AN/',
     'anitaexit1survey/', 'anitaexit2survey/', 'anitaexit3survey/',
     'anitademographicssurvey/', 'logout/'],
]

snippet_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'demographicssurvey/',
    'prepracticetask/0/','taskspacer2/0/', 'search/0/', 'postpracticetask/0/', 'taskspacer',
    'snippetpretask/1/','taskspacer2/1/', 'search/1/', 'snippetposttask/1/','systemsnippetposttask/1/',
        'taskspacer',
    'snippetpretask/2/', 'taskspacer2/2/','search/2/', 'snippetposttask/2/','systemsnippetposttask/2/',
        'taskspacer',
    'snippetpretask/3/','taskspacer2/3/', 'search/3/', 'snippetposttask/3/','systemsnippetposttask/3/',
     'taskspacer',
    'snippetpretask/4/','taskspacer2/4/', 'search/4/', 'snippetposttask/4/','systemsnippetposttask/4/',
    'taskspacer', 'snippetexitsurvey/', 'performance/', 'endexperiment/',
    'logout/'
]





test_flow = [
    'startexperiment/', 'snippetexitsurvey/','snippetpretask/1/', 'snippetposttask/1/','systemsnippetposttask/1/',
    'pretask/1/', 'search/1/','taskspacer',
    'pretask/2/', 'search/2/','taskspacer',
    'pretask/3/', 'search/3/',
    'pretask/4/', 'search/4/','endexperiment/',
    'logout/'
]

suggestion_trie = AutocompleteTrie(
    min_occurrences=3,
    suggestion_count=8,
    include_stopwords=False,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))

search_engine = Whooshtrec(
    whoosh_index_dir=my_whoosh_doc_index_dir,
    stopwords_file=stopword_file,
    model=1,
    newschema=True)

search_engine.key_name = 'bm25'
search_engine.set_fragmenter(frag_type=2, surround=30)

exp_test = ExperimentSetup(
    workflow=snippet_flow,
    engine=search_engine,
    practice_topic='367',
    topics=['347', '341', '435','408'],
    rpp=10,
    practice_interface=1,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='standard condition bm25 test',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=[150,600,600,600, 600])  # 300s = 5min; 600s = 10min; 1200s = 20min


# these correspond to conditions
experiment_setups = [exp_test]
