#
# Given a database, finds all the users, gets all documents, uses the QREL handler to get the judgement.
#

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treconomics_project.settings")

from treconomics.experiment_functions import qrels
from treconomics.models import DocumentsExamined
from treconomics.experiment_functions import get_performance_diversity

from django.contrib.auth.models import User

import django
django.setup()

doc_list = DocumentsExamined.objects.all()
lst = []

for doc in doc_list:
    topic_num = str(doc.topic_num)
    doc_num = doc.doc_num
    trec_assessment = qrels.get_value_if_exists(topic_num, doc_num)
    username = doc.user.username
    
    if username=='A2LT6KC1X51FVW' and topic_num == '341':
        print doc_num, topic_num, trec_assessment, username
        lst.append(doc_num)

scores = get_performance_diversity(lst, '341')

print scores