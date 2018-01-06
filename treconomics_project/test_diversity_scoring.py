#
# Tests the diversity scoring function
# Author: David
# Date: 2018-01-06
#

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treconomics_project.settings")
import unittest
from treconomics.experiment_functions import get_performance_diversity

TOPIC_NUM = '367'

class TestScoring(unittest.TestCase):
    
    def test_dud(self):
        doc_lst = ['DUD', 'DUD1', 'DUD2']
        results = get_performance_diversity(doc_lst, TOPIC_NUM)
        self.assertAlmostEquals(results['trec_acc'], 0.0)
    
    def test_all_rel(self):
        # judgements = [2,2,2,2]
        doc_lst = ['XIE20000424.0068', 'XIE20000424.0074', 'XIE20000506.0150', 'XIE20000803.0091']
        results = get_performance_diversity(doc_lst, TOPIC_NUM)
        self.assertAlmostEquals(results['trec_acc'], 1.0)
    
    def test_some_trec_nonrel(self):
        # judgements = [2, 2, 0, 0]
        doc_lst = ['XIE20000424.0068', 'XIE20000424.0074', 'XIE20000416.0148', 'XIE20000410.0142']
        results = get_performance_diversity(doc_lst, TOPIC_NUM)
        self.assertAlmostEquals(results['trec_acc'], 0.5)
    
    def test_none_trec_nonrel(self):
        # judgements = [2, 2, None, None]
        doc_lst = ['XIE20000424.0068', 'XIE20000424.0074', 'DUD', 'DUD2']
        results = get_performance_diversity(doc_lst, TOPIC_NUM)
        self.assertAlmostEquals(results['trec_acc'], 1.0)
    
    def test_assortment(self):
        # judgements = [2, 2, None, None, 0]
        doc_lst = ['XIE20000424.0068', 'XIE20000424.0074', 'DUD', 'DUD2', 'XIE20000410.0142']
        results = get_performance_diversity(doc_lst, TOPIC_NUM)
        self.assertAlmostEquals(results['trec_acc'], 0.666666)

if __name__ == '__main__':
    unittest.main()