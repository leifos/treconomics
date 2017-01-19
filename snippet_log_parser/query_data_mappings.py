# After query_data.py has been run, run this script on the output of query_data.py.
# This changes the userids with integers, so that the file can be processed by MATLAB.
# Easier to just write another script and pipe the output.

# Input: first arg is the output of query_data.py, second is the mappings file.

import sys

interface_mappings = {
    '1': '2',
    '2': '0',
    '3': '1',
    '4': '4'
}

def get_mappings(mappings_file):
    mappings = {}
    
    for line in mappings_file:
        line = line.strip().split(',')
        mappings[line[0]] = line[1]
    
    return mappings

output_file = open(sys.argv[1], 'r')
mappings_file = open(sys.argv[2], 'r')

user_mappings = get_mappings(mappings_file)

print 'userid condition interface order topic actions pages doc_count doc_depth doc_rel_count doc_rel_depth hover_count hover_trec_rel_count hover_trec_nonrel_count hover_depth doc_trec_rel_count doc_trec_nonrel_count doc_clicked_trec_rel_count doc_clicked_trec_nonrel_count query_time system_query_delay session_time document_time serp_lag serp_time p1 p2 p3 p4 p5 p10 p15 p20 p25 p30 p40 p50 rprec total_relevant_docs doc_trec_unjudged_count interface per_page_time'

for line in output_file:
    line = line.strip().split(' ')
    amtid = line[0]
    
    # Changing the AMTID to the mapped user ID integer.
    line[0] = user_mappings[amtid]
    line.append(interface_mappings[line[2]])
    
    # Adding in the per_page_time.
    if float(line[6]) == 0:
        line.append('0')
    else:
        per_page_time = float(line[24]) / float(line[6])
        line.append('{0:3.2f}'.format(per_page_time))
    
    print ' '.join(line)

output_file.close()
mappings_file.close()

