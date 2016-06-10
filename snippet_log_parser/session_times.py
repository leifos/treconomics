import sys
from datetime import datetime, timedelta

from utils import get_time_diff
from exp_time_log_reader import ExpTimeLogReader


class ExpLogEntry(object):

    def __init__(self, key, vals, qrel_handler=None, engine=None):
        self.qrel_handler = qrel_handler
        self.key = key
        self.title = ''
        self.state = ''
        self.event_count = 0

        self.session_start_time = None
        self.doc_clicked_time = None
        self.doc_lag_time = 0.0
        self.session_time = 0.0
        self.engine = engine

    def __str__(self):
        s = "{0} {1} {2} {3}".format(self.key, self.event_count,self.session_time, self.doc_lag_time)
        return s

    def getTitle(self):
        return self.title

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state


    def process(self, vals):
        self.event_count = self.event_count + 1

        event = vals[8]
        curr_time = vals[1]
        
        if event in ['PRACTICE_SEARCH_TASK_COMMENCED','SEARCH_TASK_COMMENCED']:
            self.session_start_time = curr_time

        if self.session_start_time is not None and event in ['PRACTICE_SEARCH_TASK_COMPLETED','SESSION_COMPLETED','EXPERIMENT_TIMEOUT','SNIPPET_POSTTASK_SURVEY_STARTED','SEARCH_TASK_COMPLETED']:
            self.session_time = get_time_diff(self.session_start_time, curr_time)
            self.session_start_time = None

        if event in ['DOC_CLICKED']:
            self.doc_clicked_time = curr_time

        if event in ['DOC_MARKED_VIEWED', 'DOC_MARKED_RELEVANT']:
            self.doc_lag_time +=  get_time_diff(self.doc_clicked_time, curr_time)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        elr = ExpTimeLogReader(ExpLogEntry)
        elr.process(filename)
        elr.report(True)

if __name__ == "__main__":
    sys.exit(main())
