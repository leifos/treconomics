### For debugging purposes - takes a log file, and produces log files for each user.
### Makes it easier to see what is going on.
import os
import sys

def main():
    if len(sys.argv) == 3:
        l = open(sys.argv[1], 'r')
        users = {}
        
        for line in l:
            line = line.strip().split(' ')
            user = line[3]
            
            if user not in users.keys():
                users[user] = []
            
            users[user].append(' '.join(line))
        
        l.close()
        
        for user in users.keys():
            f = open(os.path.join(sys.argv[2], '{0}.log'.format(user)), 'w')
            
            for line in users[user]:
                f.write('{0}{1}'.format(line, os.linesep))
            
            f.close()
    else:
        print "{0} <logfile> <dir_for_output>"

if __name__ == "__main__":
    sys.exit(main())