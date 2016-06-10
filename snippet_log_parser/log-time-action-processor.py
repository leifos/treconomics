__author__ = 'leif'
import os
import sys
from datetime import datetime, timedelta

class ActionCounter(object):

    def __init__(self, label, event):
        self.event = event
        self.label = label
        self.count = 0

    def __str__(self):
        return "%d" % (self.count)

    def action(self):
        return self.label

    def process(self, vals):
        if self.event in vals:
            self.count += 1

class ActionDependenceCounter(object):

    def __init__(self, label, curr_event, prev_event, acc_events=None):
        self.ce = curr_event
        self.pe = prev_event
        self.ac = acc_events
        self.label = label
        self.count = 0
        self.last_event = None
        self.last_event_time = None

    def __str__(self):
        return "%d" % (self.total.seconds)

    def totaltime(self):
        return self.total.seconds

    def action(self):
        return self.label

    def process(self, vals):
        # Looks to see if the current event to track (ce) is in vals (i.e. is the i+1 event)
        # If so, then it checks to see if the last_event tracked was event pe:
        # in which case count that we have seen pe (i) and ce (i+1)
        if self.ce in vals:
            if self.last_event == self.pe:
                self.count += 1
            self.last_event = self.ce
        else:
            # if the event was pe record this as the last event tracked, and continue. If it is not, then set the last event to None.
            if self.ac:
                for e in self.ac:
                    if e in vals:
                        self.last_event = e
            else:
                if self.pe in vals:
                    self.last_event = self.pe
                else:
                    self.last_event = None


class ActionDependenceTimer(object):

    def __init__(self, label, curr_event, prev_event, acc_events=None):
        self.ce = curr_event
        self.pe = prev_event
        self.ac = acc_events
        self.label = label
        self.count = 0
        self.last_event = None
        self.FMT = "%H:%M:%S,%f"
        self.total = timedelta(0,0,0,0)

    def __str__(self):
        return "%d" % (self.total.seconds)

    def totaltime(self):
        return self.total.seconds

    def process(self, vals):
        # Looks to see if the current event to track (ce) is in vals (i.e. is the i+1 event)
        # If so, then it checks to see if the last_event tracked was event pe:
        # in which case count that we have seen pe (i) and ce (i+1)
        if self.ce in vals:
            if self.last_event == self.pe:
                self.count += 1
                diff = ((datetime.strptime(vals[1],self.FMT)-datetime.strptime(self.last_event_time,self.FMT)) )
                self.total += ((datetime.strptime(vals[1],self.FMT)-datetime.strptime(self.last_event_time,self.FMT)) )
                print vals[1], self.last_event_time
                print self.ce, self.pe, diff.seconds
            self.last_event = self.ce
            self.last_event_time = vals[1]
        else:
            # if the event was pe record this as the last event tracked, and continue. If it is not, then set the last event to None.
            if self.ac:
                for e in self.ac:
                    if e in vals:
                        self.last_event = e
                        self.last_event_time = vals[1]
            else:
                if self.pe in vals:
                    self.last_event = self.pe
                    self.last_event_time = vals[1]
                else:
                    self.last_event = None
                    self.last_event_time = None



class ActionTimer(object):

    def __init__(self, label, curr_event_list, prev_event_list):
        self.cel = curr_event_list
        self.pel = prev_event_list
        self.label = label
        self.total = timedelta(0,0,0,0)
        self.count = 0
        self.last_event = None
        self.last_event_time = None
        self.FMT = "%H:%M:%S,%f"

    def __str__(self):
        return "%d" % (self.total.seconds)

    def totaltime(self):
        return self.total.seconds

    def action(self):
        return self.label

    def process(self, vals):
        for e in self.cel:
            if e in vals:
                if self.last_event in self.pel:
                    self.count += 1
                    self.total += ((datetime.strptime(vals[1],self.FMT)-datetime.strptime(self.last_event_time,self.FMT)) )
                    self.last_event = e
                    self.last_event_time = vals[1]
        for e in self.pel:
            if e in vals:
                self.last_event = e
                self.last_event_time = vals[1]

class ExpLogEntry(object):

    def __init__(self, username, actions={}, actiontimes={}, actiondeps={}, actiondeptimes={}):
        self.username = username
        self.counters = []
        self.depcounters = []
        self.timers = []
        self.deptimers= []
        self.title = ''
        self.state = ''

        for a in actions.keys():
            self.counters.append( ActionCounter( a, actions[a] ) )
            self.title += a + ' '

        for at in actiontimes.keys():
            self.timers.append( ActionTimer( at, actiontimes[at][0], actiontimes[at][1] ) )
            self.title += at + ' '

        for ads in actiondeps.keys():
            self.depcounters.append( ActionDependenceCounter( ads, actiondeps[ads][0], actiondeps[ads][1], actiondeps[ads][2] ) )
            self.title += ads + ' '

        for ads in actiondeptimes.keys():
            self.deptimers.append( ActionDependenceTimer( ads, actiondeptimes[ads][0], actiondeptimes[ads][1], actiondeptimes[ads][2] ) )
            self.title += ads + ' '


    def __str__(self):
        s = "%s " % (self.username)
        if len(self.counters)>0:
            for i in range(0,len(self.counters)):
                s= s + str(self.counters[i]) + " "

        if len(self.timers)> 0:
            for i in range(0,len(self.timers)):
                s = s + str(self.timers[i]) + " "

        if len(self.depcounters)> 0:
            for i in range(0,len(self.depcounters)):
                s = s + str(self.depcounters[i]) + " "

        if len(self.deptimers)> 0:
            for i in range(0,len(self.deptimers)):
                s = s + str(self.deptimers[i]) + " "

        return s

    def getTitle(self):
        return self.title

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def process(self, vals):
        for a in self.counters:
            a.process(vals)
        for ac in self.timers:
            ac.process(vals)
        for ads in self.depcounters:
            ads.process(vals)
        for adts in self.deptimers:
            adts.process(vals)


class ExpLogReader(object):

    def __init__(self, actions={}, actiontimes={}, actiondeps={}, actiondeptimes={}, userpos=1):
        self.users = dict()
        self.actions = actions
        self.actiontimes = actiontimes
        self.actiondeps = actiondeps
        self.actiondeptimes = actiondeptimes
        self.userpos = userpos

    def process(self, filename):

        if os.path.exists( filename ):
            infile = open( filename, 'r' )

            while infile:
                line = infile.readline()
                vals = line.split()
                if len(vals) == 0:
                    break  #end of file??? clean up???
                else:
                    username = vals[self.userpos]
                    user_entry =  None
                    if username in self.users:
                        user_entry = self.users[username]
                    else:
                        user_entry = ExpLogEntry(username, self.actions, self.actiontimes, self.actiondeps, self.actiondeptimes)

                    user_entry.process(vals)
                    self.users[username] = user_entry
        else:
            print 'Filename: %s  does not exist.' % (filename)

    def report(self,showtitles=False):
        if showtitles:
           for u in self.users.keys():
                print self.users[u].getTitle()
                break
        for u in self.users.keys():
            print self.users[u]

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        actions = { 'task_count': 'SEARCH_TASK_COMPLETED', 'query_count':'QUERY_ISSUED',
                    'doc_view_count':'DOC_MARKED_VIEWED',
                    'doc_save_count':'DOC_MARKED_RELEVANT',
                    'query_suggest_count' : 'QUERY_SUGGESTIONS_ISSUED' }
        #actions = { 'query_count':'QUERY_ISSUED' }
        actiontimes = { 'judge_time':(('DOC_MARKED_RELEVANT',''),('DOC_MARKED_VIEWED','')),
                        'snippet_time': (('DOC_MARKED_VIEWED','' ),('VIEW_SEARCH_RESULTS_PAGE','')),
                        'query_time': (('QUERY_ISSUED',''),('VIEW_SEARCH_RESULTS_PAGE','DOC_MARKED_VIEWED','DOC_MARKED_RELEVANT' ,'SEARCH_TASK_COMMENCED')),
                        'doc_time':(('VIEW_SEARCH_RESULTS_PAGE','DOC_MARKED_VIEWED','DOC_MARKED_RELEVANT','DOC_MARKED_NONRELEVANT', 'QUERY_ISSUED','SEARCH_TASK_COMPLETED'),('DOC_MARKED_VIEWED','' ) ),
                        'task_time':(('SEARCH_TASK_COMPLETED','' ),('SEARCH_TASK_COMMENCED','' )) }
        #actiontimes = { 'task_time':(('SEARCH_TASK_COMPLETED','' ),('SEARCH_TASK_COMMENCED','' ))}

        ae = ('VIEW_SEARCH_RESULTS_PAGE','QUERY_ISSUED','DOC_MARKED_RELEVANT','DOC_MARKED_VIEWED','SEARCH_TASK_COMMENCED','SEARCH_TASK_COMPLETED')

        actiondeps = { 'rp_qu':  ('VIEW_SEARCH_RESULTS_PAGE', 'QUERY_ISSUED', ae),
                       'qu_tc':  ('QUERY_ISSUED', 'SEARCH_TASK_COMMENCED', ae),
                       'qu_rp':  ('QUERY_ISSUED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'dv_rp':  ('DOC_MARKED_VIEWED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'rp_rp':  ('VIEW_SEARCH_RESULTS_PAGE', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'dr_rp':  ('DOC_MARKED_RELEVANT', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'tc_rp':  ('SEARCH_TASK_COMPLETED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'qu_dv':  ('QUERY_ISSUED', 'DOC_MARKED_VIEWED', ae),
                       'dv_dv':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_VIEWED', ae),
                       'dr_dv':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_VIEWED', ae),
                       'rp_dv':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_VIEWED', ae),
                       'tc_dv':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_VIEWED', ae),
                       'dv_dr':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_RELEVANT', ae),
                       'rp_dr':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_RELEVANT', ae),
                       'dr_dr':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_RELEVANT', ae),
                       'qu_dr':  ('QUERY_ISSUED', 'DOC_MARKED_RELEVANT', ae),
                       'tc_dr':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_RELEVANT', ae)
                       }
        actiondeps = {}

        actiondeptimes = { 'rp_qu_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'QUERY_ISSUED', ae),
                       'qu_tc_t':  ('QUERY_ISSUED', 'SEARCH_TASK_COMMENCED', ae),
                       'qu_rp_t':  ('QUERY_ISSUED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'dv_rp_t':  ('DOC_MARKED_VIEWED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'rp_rp_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'dr_rp_t':  ('DOC_MARKED_RELEVANT', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'tc_rp_t':  ('SEARCH_TASK_COMPLETED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
                       'qu_dv_t':  ('QUERY_ISSUED', 'DOC_MARKED_VIEWED', ae),
                       'dv_dv_t':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_VIEWED', ae),
                       'dr_dv_t':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_VIEWED', ae),
                       'rp_dv_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_VIEWED', ae),
                       'tc_dv_t':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_VIEWED', ae),
                       'dv_dr_t':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_RELEVANT', ae),
                       'rp_dr_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_RELEVANT', ae),
                       'dr_dr_t':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_RELEVANT', ae),
                       'qu_dr_t':  ('QUERY_ISSUED', 'DOC_MARKED_RELEVANT', ae),
                       'tc_dr_t':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_RELEVANT', ae)
        }

        actiondeptimes = {
            'rp_qu_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'QUERY_ISSUED', ae),
            'dv_qu_t':  ('DOC_MARKED_VIEWED', 'QUERY_ISSUED', ae),
            'dr_qu_t':  ('DOC_MARKED_RELEVANT', 'QUERY_ISSUED', ae),
            'qu_qu_t':  ('QUERY_ISSUED', 'QUERY_ISSUED', ae),
            'qu_tc_t':  ('QUERY_ISSUED', 'SEARCH_TASK_COMMENCED', ae),
            'qu_rp_t':  ('QUERY_ISSUED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
            'dv_rp_t':  ('DOC_MARKED_VIEWED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
            'rp_rp_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'VIEW_SEARCH_RESULTS_PAGE', ae),
            'dr_rp_t':  ('DOC_MARKED_RELEVANT', 'VIEW_SEARCH_RESULTS_PAGE', ae),
            'tc_rp_t':  ('SEARCH_TASK_COMPLETED', 'VIEW_SEARCH_RESULTS_PAGE', ae),
            'qu_dv_t':  ('QUERY_ISSUED', 'DOC_MARKED_VIEWED', ae),
            'dv_dv_t':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_VIEWED', ae),
            'dr_dv_t':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_VIEWED', ae),
            'rp_dv_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_VIEWED', ae),
            'tc_dv_t':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_VIEWED', ae),
            'dv_dr_t':  ('DOC_MARKED_VIEWED', 'DOC_MARKED_RELEVANT', ae),
            'rp_dr_t':  ('VIEW_SEARCH_RESULTS_PAGE', 'DOC_MARKED_RELEVANT', ae),
            'dr_dr_t':  ('DOC_MARKED_RELEVANT', 'DOC_MARKED_RELEVANT', ae),
            'qu_dr_t':  ('QUERY_ISSUED', 'DOC_MARKED_RELEVANT', ae),
            'tc_dr_t':  ('SEARCH_TASK_COMPLETED', 'DOC_MARKED_RELEVANT', ae)
        }

        actiondeptimes = {}


        elr = ExpLogReader(actions, actiontimes, actiondeps, actiondeptimes, 3)
        elr.process(filename)
        elr.report(True)

if __name__ == "__main__":
    sys.exit(main())

# Q VSRP DV DR VSRP DV VSRP Q DV
# Q-> RP, RP->Q, RP->DV, DV->RP, DV->Q, DV->DR, DR->Q, DR->DV, DR->RP