import sys
import utils

def get_blank_dict():
    return {'lines': [], 'commenced_time': None, 'hit_limit': False}

def get_details_object(log_file, time_limit=360):
    """
    Given a log file path and a time limit (in seconds), parses the log, trimming user interactions up to the time limit.
    """
    time_limit = float(time_limit)
    f = open(log_file, 'r')
    details = {}
    
    for line in f:
        line = line.strip().split(' ')
        current_event_datetime = '{date} {time}'.format(date=line[0], time=line[1])
        userid = line[3]
        topic = line[7]
        event = line[8]
        rotation = line[5]
        interface = line[6]
        
        if userid not in details:
            details[userid] = {}
        
        if topic not in details[userid]:
            details[userid][topic] = get_blank_dict()
        
        if event == 'SEARCH_TASK_COMMENCED':
            details[userid][topic]['commenced_time'] = current_event_datetime
        
        if details[userid][topic]['commenced_time'] is not None and not details[userid][topic]['hit_limit']:
            time_difference = utils.get_time_diff(details[userid][topic]['commenced_time'], current_event_datetime)
            
            if time_difference > time_limit:
                # We've hit the time ceiling - so we fabricate an 'EXPERIMENT_TIMEOUT' event to trigger our processing scripts.
                details[userid][topic]['hit_limit'] = True
                
                # Fabricate the line.
                timeout_line = '{date} {time} INFO {userid} 0 {rotation} {interface} {topic} EXPERIMENT_TIMEOUT'.format(date=line[0],
                                                                                                                        time=line[1],
                                                                                                                        userid=userid,
                                                                                                                        rotation=rotation,
                                                                                                                        interface=interface,
                                                                                                                        topic=topic)
                details[userid][topic]['lines'].append(timeout_line.split(' '))
            else:
                details[userid][topic]['lines'].append(line)  # Append the line.
    
    f.close()
    return details

def print_trimmed_log(details):
    """
    Traverses the details object - and prints out the log entries to stdout.
    Does not guarantee the same ordering as the original log.
    """
    for userid in details:
        for topic in details[userid]:
            for line in details[userid][topic]['lines']:
                print ' '.join(line)

def usage(script_name):
    print "Simple script that takes a log file, and cuts off users after a specified time limit (in seconds)."
    print "Start time is from a search session commencing, to the point at which the elapsed time of the session reaches the specified cutoff."
    print "Usage:"
    print "    {0} <log_path> <timeout_limit>".format(script_name)
    print "Specify cutoff limit in seconds."
    print "Dumps the modified log to stdout."

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])
        sys.exit(1)
    
    log_path = sys.argv[1]
    time_limit = sys.argv[2]
    
    details = get_details_object(log_path, time_limit)
    print_trimmed_log(details)