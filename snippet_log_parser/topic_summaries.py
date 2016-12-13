import re
import os
import sys
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from utils import setup_django_env

SELECTED_TOPIC = 'ALL'
OUTPUT_KEYS = [
    'user_id',
    'interface',
    'snippet_len',
    'order',
    'topic',
    
    'query_count',
    
    'pages',
    'pages_per_query',
    'doc_count',
    'doc_count_per_query',
    'doc_depth_per_query',
    'doc_rel_count',
    'doc_rel_depth_per_query',
    'hover_count_per_query',
    'hover_depth_per_query',
    'hover_trec_rel_count',
    'hover_trec_nonrel_count',
    'rels_found',
    'nrels_found',
    'clicked_rel',
    'clicked_nrel',
    
    'total_query_time',
    'query_time',
    'query_system_time',
    'total_session_time',
    'doc_time',
    'serp_lag',
    'serp_time',
    
    'time_per_query',
    'time_per_doc',
    'time_serp_per_query',
    'time_per_snippet',
    
    'p1',
    'p2',
    'p3',
    'p4',
    'p5',
    'p10',
    'p15',
    'p20',
    'p25',
    'p30',
    'p40',
    'p50',
    'rprec',
    
    'pmr',
    'pmn',
    'pcr',
    'pcn',
]


def create_user_dict():
    '''
    Returns a new dictionary object, consisting with keys
    '''
    return_dict = {}

    for key in OUTPUT_KEYS:
        return_dict[key] = 0.0
    
    return_dict['user_id'] = 0
    return_dict['snippet_len'] = 0
    return_dict['query_count'] = 0.0
    return_dict['pages'] = 0.0
    return_dict['doc_count'] = 0.0
    return_dict['doc_depth'] = []
    return_dict['doc_rel_count'] = 0.0
    return_dict['doc_rel_depth'] = []
    return_dict['hover_count'] = 0.0
    return_dict['hover_trec_rel_count'] = 0.0
    return_dict['hover_trec_nonrel_count'] = 0.0
    return_dict['hover_depth'] = []
    return_dict['rels_found'] = 0.0
    return_dict['nrels_found'] = 0.0
    return_dict['clicked_rel'] = 0.0
    return_dict['clicked_nrel'] = 0.0
    
    return_dict['total_query_time'] = 0.0
    return_dict['query_time'] = 0.0
    return_dict['query_system_time'] = 0.0
    return_dict['total_session_time'] = 0.0
    return_dict['doc_time'] = 0.0
    return_dict['serp_lag'] = 0.0
    return_dict['serp_time'] = 0.0
    
    return_dict['p1'] = []
    return_dict['p2'] = []
    return_dict['p3'] = []
    return_dict['p4'] = []
    return_dict['p5'] = []
    return_dict['p10'] = []
    return_dict['p15'] = []
    return_dict['p20'] = []
    return_dict['p25'] = []
    return_dict['p30'] = []
    return_dict['p40'] = []
    return_dict['p50'] = []
    return_dict['rprec'] = []
    
    return return_dict

def generate_output(summaries, separator=' ', include_header=True):
    '''
    Creates an output string, consisting of the user account, followed by the values in the order or OUTPUT_KEYS.
    Each user's details are separated by a newline, courtesy of os.linesep.
    Optional parameter separator allows you to specify the separator - could be a comma, tab (\t) or simply a space.
    Can also specify whether to include a header line with the include_header parameter.
    '''
    output_str = ''

    if len(summaries) == 0:
        output_str = 'NO USERS FOUND'
    else:
        if include_header:
            output_str = 'user{0}'.format(separator)

            for key in OUTPUT_KEYS:
                output_str += '{0}{1}'.format(key, separator)

            output_str = output_str[:-1]
            output_str += os.linesep

        for user in summaries:
            for topic in summaries[user]:
                topic_str = '{0}{1}'.format(user, separator)
                
                for key in OUTPUT_KEYS:
                    val_to_disp = summaries[user][topic][key]
                
                    if type(val_to_disp) == float:
                        val_to_disp = '{0:3.2f}'.format(val_to_disp)
                
                    topic_str += '{0}{1}'.format(val_to_disp, separator)

                topic_str = topic_str[:-1]
                topic_str += os.linesep
                output_str += topic_str

    return output_str

def generate_user_summaries(input_file):
    '''
    Generates a list of user details with related information about each account from the given input file.
    '''
    summaries = {}
    user_id_index = 0
    user_id_mappings = {}
    snippet_len_mappings = [2, 0, 1, 4]
    
    for line in input_file:
        
        if line.startswith('userid'):
            continue
        
        split_line = line.split()
        user = split_line[0]
        
        if user not in user_id_mappings:
            user_id_mappings[user] = user_id_index
            user_id_index = user_id_index + 1
        
        user_id = user_id_mappings[user]
        condition = int(split_line[1])
        interface = int(split_line[2])
        snippet_len = snippet_len_mappings[interface - 1]
        topic = split_line[4]
        order = split_line[3]
        
        if user not in summaries:
            summaries[user] = {}
        
        if topic not in summaries[user]:
            summaries[user][topic] = create_user_dict()
            summaries[user][topic]['condition'] = condition
            summaries[user][topic]['order'] = order
            summaries[user][topic]['topic'] = topic
            summaries[user][topic]['interface'] = interface
        
        summaries[user][topic]['user_id'] = user_id
        summaries[user][topic]['snippet_len'] = snippet_len
        summaries[user][topic]['query_count'] += 1
        summaries[user][topic]['pages'] += int(split_line[7])
        summaries[user][topic]['doc_count'] += int(split_line[8])
        summaries[user][topic]['doc_depth'].append(int(split_line[9]))
        summaries[user][topic]['doc_rel_count'] += int(split_line[10])
        summaries[user][topic]['doc_rel_depth'].append(int(split_line[11]))
        summaries[user][topic]['hover_count'] += int(split_line[12])
        summaries[user][topic]['hover_trec_rel_count'] += int(split_line[13])
        summaries[user][topic]['hover_trec_nonrel_count'] += int(split_line[14])
        
        summaries[user][topic]['hover_depth'].append(int(split_line[15]))
        summaries[user][topic]['rels_found'] += int(split_line[16])
        summaries[user][topic]['nrels_found'] += int(split_line[17])
        summaries[user][topic]['clicked_rel'] += int(split_line[18])
        summaries[user][topic]['clicked_nrel'] += int(split_line[19])
        
        summaries[user][topic]['total_query_time'] += (float(split_line[20]) + float(split_line[21]) + float(split_line[24]))
        summaries[user][topic]['query_time'] += float(split_line[20])
        summaries[user][topic]['query_system_time'] += float(split_line[21])
        summaries[user][topic]['total_session_time'] += float(split_line[22])
        summaries[user][topic]['doc_time'] += float(split_line[23])
        summaries[user][topic]['serp_lag'] += float(split_line[24])
        summaries[user][topic]['serp_time'] += float(split_line[25])
    
        summaries[user][topic]['p1'].append(float(split_line[26]))
        summaries[user][topic]['p2'].append(float(split_line[27]))
        summaries[user][topic]['p3'].append(float(split_line[28]))
        summaries[user][topic]['p4'].append(float(split_line[29]))
        summaries[user][topic]['p5'].append(float(split_line[30]))
        summaries[user][topic]['p10'].append(float(split_line[31]))
        summaries[user][topic]['p15'].append(float(split_line[32]))
        summaries[user][topic]['p20'].append(float(split_line[33]))
        summaries[user][topic]['p25'].append(float(split_line[34]))
        summaries[user][topic]['p30'].append(float(split_line[35]))
        summaries[user][topic]['p40'].append(float(split_line[36]))
        summaries[user][topic]['p50'].append(float(split_line[37]))
        summaries[user][topic]['rprec'].append(float(split_line[38]))
        
    for user in summaries:
        for topic in summaries[user]:
            q = float(summaries[user][topic]['query_count'])
            d = float(summaries[user][topic]['doc_count'])
        
            if d < 1.0:
                d = 1.0
            if q < 1.0:
                q = 1.0
            
            summaries[user][topic]['pages_per_query'] = float(summaries[user][topic]['pages']) / q
            summaries[user][topic]['doc_count_per_query'] = float(summaries[user][topic]['doc_count']) / q
            summaries[user][topic]['doc_depth_per_query'] = float(sum(summaries[user][topic]['doc_depth'])) / q
            summaries[user][topic]['doc_rel_depth_per_query'] = float(sum(summaries[user][topic]['doc_rel_depth'])) / q
            
            summaries[user][topic]['hover_count_per_query'] = float(summaries[user][topic]['hover_count']) / q
            summaries[user][topic]['hover_depth_per_query'] = float(sum(summaries[user][topic]['hover_depth']) ) / q
            summaries[user][topic]['time_per_query'] = summaries[user][topic]['query_time'] / q
            summaries[user][topic]['time_per_doc'] = summaries[user][topic]['doc_time'] / d
            summaries[user][topic]['time_serp_per_query'] = summaries[user][topic]['serp_time'] / q
            summaries[user][topic]['time_serp_lag_per_query'] = summaries[user][topic]['serp_lag'] / q
            # Time per snippet - not too sure about this.
            # We take the total number of recorded hover events for the given user/topic combination, and divide the SERP time spent by that value.
            summaries[user][topic]['time_per_snippet'] = summaries[user][topic]['serp_time'] / summaries[user][topic]['hover_count']
            
            summaries[user][topic]['p1'] = sum(summaries[user][topic]['p1']) / float(len(summaries[user][topic]['p1']))
            summaries[user][topic]['p2'] = sum(summaries[user][topic]['p2']) / float(len(summaries[user][topic]['p2']))
            summaries[user][topic]['p3'] = sum(summaries[user][topic]['p3']) / float(len(summaries[user][topic]['p3']))
            summaries[user][topic]['p4'] = sum(summaries[user][topic]['p4']) / float(len(summaries[user][topic]['p4']))
            summaries[user][topic]['p5'] = sum(summaries[user][topic]['p5']) / float(len(summaries[user][topic]['p5']))
            summaries[user][topic]['p10'] = sum(summaries[user][topic]['p10']) / float(len(summaries[user][topic]['p10']))
            summaries[user][topic]['p15'] = sum(summaries[user][topic]['p15']) / float(len(summaries[user][topic]['p15']))
            summaries[user][topic]['p20'] = sum(summaries[user][topic]['p20']) / float(len(summaries[user][topic]['p20']))
            summaries[user][topic]['p25'] = sum(summaries[user][topic]['p25']) / float(len(summaries[user][topic]['p25']))
            summaries[user][topic]['p30'] = sum(summaries[user][topic]['p30']) / float(len(summaries[user][topic]['p30']))
            summaries[user][topic]['p40'] = sum(summaries[user][topic]['p40']) / float(len(summaries[user][topic]['p40']))
            summaries[user][topic]['p50'] = sum(summaries[user][topic]['p50']) / float(len(summaries[user][topic]['p50']))
            summaries[user][topic]['rprec'] = sum(summaries[user][topic]['rprec']) / float(len(summaries[user][topic]['rprec']))
            
            summaries[user][topic]['pmr'] = 0.0
            summaries[user][topic]['pmn'] = 0.0
            summaries[user][topic]['pcr'] = 0.0
            summaries[user][topic]['pcn'] = 0.0
            
            if summaries[user][topic]['clicked_rel'] > 0:
                summaries[user][topic]['pmr'] = summaries[user][topic]['rels_found'] / summaries[user][topic]['clicked_rel']
            
            if summaries[user][topic]['clicked_nrel'] > 0:
                summaries[user][topic]['pmn'] = summaries[user][topic]['nrels_found'] / summaries[user][topic]['clicked_nrel']
            
            if summaries[user][topic]['hover_trec_rel_count'] > 0:
                summaries[user][topic]['pcr'] = summaries[user][topic]['clicked_rel'] / summaries[user][topic]['hover_trec_rel_count']
            
            if summaries[user][topic]['hover_trec_nonrel_count'] > 0:
                summaries[user][topic]['pcn'] = summaries[user][topic]['clicked_nrel'] / summaries[user][topic]['hover_trec_nonrel_count']
            
    return summaries

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: {0} <query_summary_file>'.format(sys.argv[0])
    else:
        try:
            f = open(sys.argv[1], 'r')
        except IOError:
            print 'Input file \'{0}\' not found or could not be opened.'.format(sys.argv[1])
            sys.exit(1)
        
        user_summaries = generate_user_summaries(f)
        print generate_output(user_summaries, separator=',')