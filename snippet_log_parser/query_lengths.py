import re
import os
import sys
from datetime import datetime, timedelta
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from ifind.search.engines.whooshtrecnewsredis import WhooshTrecNewsRedis
from ifind.search import Query, Response

SELECTED_TOPIC = 'ALL'

qrels = TrecQrelHandler('/Users/david/Workspace/ifind/applications/treconomics_project/data/TREC2005.qrels.txt')
engine = WhooshTrecNewsRedis(whoosh_index_dir='/Users/david/Workspace/ifind/applications/treconomics_project/data/fullindex/')

OUTPUT_KEYS = ['user',
			   'condition',
			   'topic',
			   'query_len',
			   'query_time',
			   #'p1',
			   #'p2',
			   #'p3',
			   #'p4',
			   #'p5',
			   #'p10',
			   #'p15',
			   #'p20',
			   #'p30',
			   #'p40',
			   #'p50',
			   #'rprec',
			   #'total_rel',
			   'is_autocomplete',
			   'terms',]

def get_time_diff(past,present):
    FMT = "%H:%M:%S,%f"
    diff = ((datetime.strptime(present,FMT)-datetime.strptime(past,FMT)))
    return diff.seconds

def getQueryResultPerformance(results, topic_num):
    i = 0
    rels_found = 0
    for r in results:
        i = i + 1
        val = qrels.get_value(topic_num, r.docid)
        if val > 0:
            rels_found = rels_found + 1
    return [rels_found, i]


def get_topic_relevant_count(topic_num):
    """
    Returns the number of documents considered relevant for topic topic_num.
    """
    count = 0

    for document in qrels.get_doc_list(topic_num):
        if qrels.get_value(topic_num, document) > 0:
            count = count + 1

    return count


def is_relevant(topic_num, docid):
    if qrels.get_value(topic_num, docid) > 0:
        return 1
    else:
        return 0


def calculate_precision(results, topic_num, k):
    """
    Returns a float representing the precision @ k for a given topic, topic_num, and set of results, results.
    """
    results = results[0:k]
    no_relevant = getQueryResultPerformance(results, topic_num)[0]
    return no_relevant / float(k)


def get_query_performance_metrics(results, topic_num):
    """
    Returns performance metrics for a given list of results, results, and a TREC topic, topic_num.
    List returned is in the format [p@1, p@2, p@3, p@4, p@5, p@10, p@15, p@20, p@125, p@30, p@40, p@50, Rprec, total rel. docs]
    """

    total_relevant_docs = get_topic_relevant_count(topic_num)

    p_at_1 = str(calculate_precision(results, topic_num, 1))
    p_at_2 = str(calculate_precision(results, topic_num, 2))
    p_at_3 = str(calculate_precision(results, topic_num, 3))
    p_at_4 = str(calculate_precision(results, topic_num, 5))
    p_at_5 = str(calculate_precision(results, topic_num, 6))
    p_at_10 = str(calculate_precision(results, topic_num, 10))
    p_at_15 = str(calculate_precision(results, topic_num, 15))
    p_at_20 = str(calculate_precision(results, topic_num, 20))
    p_at_25 = str(calculate_precision(results, topic_num, 25))
    p_at_30 = str(calculate_precision(results, topic_num, 30))
    p_at_40 = str(calculate_precision(results, topic_num, 40))
    p_at_50 = str(calculate_precision(results, topic_num, 50))
    r_prec = str(calculate_precision(results, topic_num, total_relevant_docs))

    return [p_at_1, p_at_2, p_at_3, p_at_4, p_at_5, p_at_10, p_at_15, p_at_20, p_at_25, p_at_30, p_at_40, p_at_50, r_prec, str(total_relevant_docs)]

def get_query_dict():
	'''
	
	'''
	ret_dict = {}
	
	for key in OUTPUT_KEYS:
		ret_dict[key] = 0
	
	return ret_dict

def get_query_lengths(f):
	'''
	'''
	autocomplete = {}
	queries = []
	last_user_query_focus = {}
	
	for line in f:
		split_line = line.split()
		
		if (SELECTED_TOPIC == 'ALL' and split_line[6] != '367') or split_line[6] == SELECTED_TOPIC:
			if split_line[7] == 'AUTOCOMPLETE_QUERY_SELECTED':
				if user not in autocomplete:
					autocomplete[user] = ''
				
				autocomplete[user] = ' '.join(split_line[8:])
				
			if split_line[7] == 'QUERY_FOCUS':
				user = int(re.findall(r'\d+', split_line[3])[0])
				last_user_query_focus[user] = split_line[1]
			if split_line[7] == 'QUERY_ISSUED':
				user = int(re.findall(r'\d+', split_line[3])[0])
				condition = int(split_line[4])
			
				query_details = get_query_dict()
				query_details['user'] = user
				query_details['condition'] = condition
				query_details['topic'] = split_line[6]
				query_details['query_len'] = len(split_line[8:])
				query_details['terms'] = ' '.join(split_line[8:])
				query_details['query_time'] = get_time_diff(last_user_query_focus[user], split_line[1])
				
				if user in autocomplete and autocomplete[user] == ' '.join(split_line[8:]):
					query_details['is_autocomplete'] = 1
			
				# q = Query(' '.join(split_line[8:]))
				# 				q.skip = 1
				# 				q.top = 200
				# 				response = engine.search(q)
				# 				perf = get_query_performance_metrics(response.results, query_details['topic'])
			
				# query_details['p1'] = perf[0]
				# 				query_details['p2'] = perf[1]
				# 				query_details['p3'] = perf[2]
				# 				query_details['p4'] = perf[3]
				# 				query_details['p5'] = perf[4]
				# 				query_details['p10'] = perf[5]
				# 				query_details['p15'] = perf[6]
				# 				query_details['p20'] = perf[7]
				# 				query_details['p25'] = perf[8]
				# 				query_details['p30'] = perf[9]
				# 				query_details['p40'] = perf[10]
				# 				query_details['p50'] = perf[11]
				# 				query_details['rprec'] = perf[12]
				# 				query_details['total_rel'] = perf[13]
			
				queries.append(query_details)
			
				#print 'Query', ' '.join(split_line[8:]), 'executed', query_details['query_time']
				#print perf
				#print
	
	return queries

def get_output(queries):
	output_str = ''
	
	if len(queries) == 0:
		output_str = 'NO QUERIES'
	else:
		for key in OUTPUT_KEYS:
			output_str += '{0}{1}'.format(key, ',')
		
		output_str = output_str[:-1]
		output_str += os.linesep
		
		for query_details in queries:
			query_str = ''
			
			for key in OUTPUT_KEYS:
				query_str += '{0}{1}'.format(query_details[key], ',')
			
			query_str = query_str[:-1]
			query_str += os.linesep
			output_str += query_str
	
	return output_str

if __name__ == '__main__':
	if len(sys.argv) < 3 or len(sys.argv) > 3:
		print 'Usage: {0} <log_file> <topic>'.format(sys.argv[0])
	else:
		try:
			f = open(sys.argv[1], 'r')
		except IOError:
			print 'Input file \'{0}\' not found or could not be opened.'.format(sys.argv[1])
			sys.exit(1)
		
		SELECTED_TOPIC == sys.argv[2]
		queries = get_query_lengths(f)
		
		print get_output(queries)
