import re
import os
import sys
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from utils import setup_django_env

SELECTED_TOPIC = 'ALL'
OUTPUT_KEYS = [
    'condition',
    'interface',
    'order',
    'topic',
    'query_count',
    'page_count',
    'page_count_per_query',
    'doc_count',
    'doc_count_per_query',
    'doc_depth_per_query',
    'hover_depth_per_query',
    'doc_relevant_depth_per_query',
    'docs_marked_relevant_count',
    'docs_trec_relevant_count',

    'time_total_query',
    'time_total_session',
    'time_total_system',
    'time_per_query',
    'time_total_doc',
    'time_per_doc',
    'time_total_serp',
    'time_serp_per_query',
    'time_total_serp_lag',
    'time_serp_lag_per_query', #

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
    'rprec'
]


def create_user_dict():
    '''
    Returns a new dictionary object, consisting with keys
    '''
    return_dict = {}

    for key in OUTPUT_KEYS:
        return_dict[key] = 0.0

    return_dict['doc_examined_depth'] = []
    return_dict['hover_depth'] = []

    return_dict['query_count'] = 0.0
    return_dict['page_count'] = 0.0
    return_dict['doc_count'] = 0.0
    return_dict['docs_marked_relevant_count'] = 0.0
    return_dict['doc_relevant_depth'] = []
    return_dict['doc_hover_count'] = 0.0
    return_dict['doc_hover_depth'] = []
    return_dict['docs_trec_relevant_count'] = 0.0

    return_dict['time_total_query'] = 0.0
    return_dict['time_total_system'] = 0.0
    return_dict['time_total_session'] = 0.0
    return_dict['time_total_doc'] = 0.0
    return_dict['time_total_serp'] = 0.0
    return_dict['time_total_serp_lag'] = 0.0


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
            #user_str = '{0}{1}'.format(map(int, re.findall('\d+', user))[0], separator)
            user_str = '{0}{1}'.format( user, separator)

            for key in OUTPUT_KEYS:
                val_to_disp = summaries[user][key]
                
                if type(val_to_disp) == float:
                    val_to_disp = '{0:3.2f}'.format(val_to_disp)
                
                user_str += '{0}{1}'.format(val_to_disp, separator)

            user_str = user_str[:-1]
            user_str += os.linesep
            output_str += user_str

    return output_str

def generate_user_summaries(input_file):
    '''
    Generates a list of user details with related information about each account from the given input file.
    '''
    summaries = {}

    for line in input_file:
        
        if line.startswith('userid'):
            continue
        
        split_line = line.split()
        user = split_line[0]
        condition = int(split_line[1])
        interface = int(split_line[2])
        topic = split_line[4]
        order = split_line[3]

        if user not in summaries:
            summaries[user] = create_user_dict()
            summaries[user]['condition'] = condition
            summaries[user]['order'] = order
            summaries[user]['topic'] = topic
            summaries[user]['interface'] = interface

        summaries[user]['query_count'] += 1
        summaries[user]['page_count'] += int(split_line[7])
        summaries[user]['doc_count'] += int(split_line[8])
        summaries[user]['doc_examined_depth'].append(int(split_line[9]))
        summaries[user]['docs_marked_relevant_count'] += int(split_line[10])
        summaries[user]['doc_relevant_depth'].append(int(split_line[11]))
        summaries[user]['doc_hover_count'] += int(split_line[12])
        summaries[user]['doc_hover_depth'].append(int(split_line[13]))
        summaries[user]['docs_trec_relevant_count'] += int(split_line[14])

        summaries[user]['time_total_query'] += float(split_line[15])
        summaries[user]['time_total_system'] += float(split_line[16])
        summaries[user]['time_total_session'] += float(split_line[17])
        summaries[user]['time_total_doc'] += float(split_line[18])
        summaries[user]['time_total_serp'] += float(split_line[20])
        summaries[user]['time_total_serp_lag'] += float(split_line[19])

        summaries[user]['p1'].append(float(split_line[21]))
        summaries[user]['p2'].append(float(split_line[22]))
        summaries[user]['p3'].append(float(split_line[23]))
        summaries[user]['p4'].append(float(split_line[24]))
        summaries[user]['p5'].append(float(split_line[25]))
        summaries[user]['p10'].append(float(split_line[26]))
        summaries[user]['p15'].append(float(split_line[27]))
        summaries[user]['p20'].append(float(split_line[28]))
        summaries[user]['p25'].append(float(split_line[29]))
        summaries[user]['p30'].append(float(split_line[30]))
        summaries[user]['p40'].append(float(split_line[31]))
        summaries[user]['p50'].append(float(split_line[32]))
        summaries[user]['rprec'].append(float(split_line[33]))

    for user in summaries:

        q = float(summaries[user]['query_count'])
        d = float(summaries[user]['doc_count'])
        if d < 1.0:
            d = 1.0
        if q < 1.0:
            q = 1.0

        summaries[user]['page_count_per_query'] = float(summaries[user]['page_count']) / q
        summaries[user]['doc_count_per_query'] = float(summaries[user]['doc_count']) / q
        summaries[user]['doc_depth_per_query'] = float(sum(summaries[user]['doc_examined_depth'])) / q
        summaries[user]['doc_relevant_depth_per_query'] = float(sum(summaries[user]['doc_relevant_depth'])) / q

        summaries[user]['hover_depth_per_query'] = float(sum(summaries[user]['doc_hover_depth']) ) / q
        summaries[user]['time_per_query'] = summaries[user]['time_total_query'] / q
        summaries[user]['time_per_doc'] = summaries[user]['time_total_doc'] / d
        summaries[user]['time_serp_per_query'] =summaries[user]['time_total_serp'] /q
        summaries[user]['time_serp_lag_per_query'] = summaries[user]['time_total_serp_lag'] / q

        summaries[user]['p1'] = sum(summaries[user]['p1']) / float(len(summaries[user]['p1']))
        summaries[user]['p2'] = sum(summaries[user]['p2']) / float(len(summaries[user]['p2']))
        summaries[user]['p3'] = sum(summaries[user]['p3']) / float(len(summaries[user]['p3']))
        summaries[user]['p4'] = sum(summaries[user]['p4']) / float(len(summaries[user]['p4']))
        summaries[user]['p5'] = sum(summaries[user]['p5']) / float(len(summaries[user]['p5']))
        summaries[user]['p10'] = sum(summaries[user]['p10']) / float(len(summaries[user]['p10']))
        summaries[user]['p15'] = sum(summaries[user]['p15']) / float(len(summaries[user]['p15']))
        summaries[user]['p20'] = sum(summaries[user]['p20']) / float(len(summaries[user]['p20']))
        summaries[user]['p25'] = sum(summaries[user]['p25']) / float(len(summaries[user]['p25']))
        summaries[user]['p30'] = sum(summaries[user]['p30']) / float(len(summaries[user]['p30']))
        summaries[user]['p40'] = sum(summaries[user]['p40']) / float(len(summaries[user]['p40']))
        summaries[user]['p50'] = sum(summaries[user]['p50']) / float(len(summaries[user]['p50']))
        summaries[user]['rprec'] = sum(summaries[user]['rprec']) / float(len(summaries[user]['rprec']))

    return summaries

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print 'Usage: {0} <query_summary_file>'.format(sys.argv[0])
    else:

        try:
            f = open(sys.argv[1], 'r')
        except IOError:
            print 'Input file \'{0}\' not found or could not be opened.'.format(sys.argv[1])
            sys.exit(1)

        user_summaries = generate_user_summaries(f)
        print generate_output(user_summaries, separator=',')