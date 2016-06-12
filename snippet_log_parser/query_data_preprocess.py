import sys

class UserLog(object):
    """
    Basically a list of objects for an individual user.
    """
    def __init__(self, user):
        self.user = user
        self.obj_list = []
    
    def append(self, obj):
        self.obj_list.append(obj)
    
    def process(self):
        """
        Does the magic, on a per-user basis.
        Do what checks need to be done here. To take a line out, set its include attribute to False.
        """
        query_focii = []
        
        for line_obj in self.obj_list:
            if line_obj.get_action() == 'QUERY_FOCUS':
                query_focii.append(line_obj)
            
            if line_obj.get_action() == 'QUERY_ISSUED':
                if len(query_focii) > 1:
                    del query_focii[-1]  # The last QUERY_FOCUS is the one we wish to keep.
                    
                    for focus in query_focii:
                        focus.include = False
                
                query_focii = []
    
class LogEntry(object):
    """
    Represents a log entry (i.e. a line in the log file).
    """
    def __init__(self, line_text):
        self.line_text = line_text
        self.line_split = self.line_text.split(' ')
        self.include = True
    
    def get_user(self):
        return self.line_split[3]
    
    def get_action(self):
        return self.line_split[8]
    
    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.line_split[0], self.line_split[1], self.get_user(), self.get_action())

def main():
    if len(sys.argv) == 3:
        log_file = open(sys.argv[1], 'r')
        obj_list = []
        users = {}
        
        # Populate the data structures.
        for line in log_file:
            line = line.strip()
            line_obj = LogEntry(line)
            obj_list.append(line_obj)
            
            user = line_obj.get_user()
            
            if user not in users.keys():
                users[user] = UserLog(user)
            
            users[user].append(line_obj)
        
        log_file.close()
        
        # Process each user's log.
        for user in users.keys():
            users[user].process()
        
        # Now write the output to stdout. Omit lines that are flagged to be removed.
        if sys.argv[2] == '1':
            for line_obj in obj_list:
                if line_obj.include:
                    print ' '.join(line_obj.line_split)
        
    else:
        print "{0} <logfile> <stdout>"

if __name__ == "__main__":
    sys.exit(main())
