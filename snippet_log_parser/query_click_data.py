import os
import sys

def process(filename):

    current_key = ""
    clicks = [0]*31
    queries = 0

    if os.path.exists( filename ):
        infile = open( filename, 'r' )

        while infile:
            line = infile.readline()
            vals = line.split()
            if len(vals) == 0:
                click_str = " ".join(str(x) for x in clicks )

                print("{0} {1} {2}".format(current_key, queries, click_str))
                break  #end of file??? clean up???
            else:
                username = vals[3]
                condition = vals[4]
                interface = vals[5]
                order = vals[6]
                topic = vals[7]
                key = "%s %s %s %s %s" % (username,condition,interface,order,topic)

                if current_key == "":
                    current_key = key

                # if query_issued
                if ('QUERY_ISSUED' in vals):
                    #print "query", key
                    if current_key == key:
                        queries += 1
                        #print "curent==key"
                    else:
                        #print out key, num queries and click counts.

                        click_str = " ".join(str(x) for x in clicks )

                        print("{0} {1} {2}".format(current_key, queries, click_str))

                        queries = 1
                        clicks = [0]*31
                        current_key = key
                        # update click array

                # if doc viewed
                if 'DOC_MARKED_VIEWED' in vals:
                    m = int(vals[13])
                    if m > 31:
                        m = 31;
                    if m > 0:
                        clicks[m-1] += 1


    else:
            print 'Filename: %s  does not exist.' % (filename)





def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        process(filename)

    else:
        print "{0} <logfile>".format(sys.argv[0])

if __name__ == "__main__":
    sys.exit(main())
