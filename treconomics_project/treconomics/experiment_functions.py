import logging

__author__ = 'leif and david'

import math
import datetime

from django.contrib.auth.models import User
from pytz import timezone
from django.conf import settings

from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from models import DocumentsExamined
from experiment_configuration import event_logger, qrels_file, qrels_diversity_file, experiment_setups

from ifind.seeker.trec_diversity_qrel_handler import EntityQrelHandler

settings_timezone = timezone(settings.TIME_ZONE)
qrels = TrecQrelHandler(qrels_file)
qrels_diversity = EntityQrelHandler(qrels_diversity_file)


def get_experiment_context(request):
    """
    This is a helper function that returns the correct experimental context
    based on the request provided.
    :param request:
    :return: experimental context dictionary
    """
    ec = {"username": request.user.username}
    u = User.objects.get(username=ec["username"])
    profile = u.profile
    ec["rotation"] = profile.rotation
    ec["condition"] = profile.condition
    ec["completed_steps"] = profile.steps_completed
    ec["workflow"] = experiment_setups[ec['condition']].workflow

    if "current_step" in request.session:
        ec["current_step"] = int(request.session['current_step'])
    else:
        # in the profile steps_completed is zero.
        # if the user logs in again, then if the session variable is not set, we take the one from the datbase
        steps_completed = ec["completed_steps"]
        ec["current_step"] = steps_completed
        request.session['current_step'] = steps_completed

    if "taskid" in request.session:
        ec["taskid"] = int(request.session['taskid'])
    else:
        ec["taskid"] = 0

    es = experiment_setups[ec['condition']]
    esd = es.get_exp_dict(ec["taskid"],ec["rotation"])
    ec["topicnum"] = esd["topic"]
    ec["interface"] = esd["interface"]
    ec["diversity"] = esd["diversity"]
    ec["rpp"] = esd["rpp"]
    ec["autocomplete"] = esd["autocomplete"]
    ec["target"] = esd["target"]

    return ec

    # if "taskid" in request.session:
    #     ec["taskid"] = int(request.session['taskid'])
    #     t = ec["taskid"] - 1
    #     r = ec["rotation"] - 1
    #     if t >= 0:
    #         ec["topicnum"] = experiment_setups[ec['condition']].get_rotation_topic(r, t)
    #     else:
    #         ec["topicnum"] = experiment_setups[ec['condition']].practice_topic
    # else:
    #     ec["taskid"] = 0
    #     request.session["taskid"] = 0
    #     ec["topicnum"] = experiment_setups[ec['condition']].practice_topic


def print_experiment_context(ec):
    for key, value in ec.iteritems():
        if key is not 'workflow':
            logging.debug('%s: %s', key, str(value))


def time_search_experiment_out(request):
    start_time = request.session['start_time']
    ec = get_experiment_context(request)
    task_id = ec["taskid"]
    timeout = experiment_setups[ec['condition']].get_timeout(task_id)
    print "Timeout: ", timeout
    logging.debug('%s %d' % ('timeout:', timeout))

    if timeout == 0:
        log_event(event="SEARCH_TASK_COMPLETED", request=request)
        log_event(event="SEARCH_TASK_COMPLETED_TIMEOUT", request=request)
        return False
    else:
        current_time = datetime.datetime.now()
        start_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        datetime.timedelta(0, 2700)

        diff = (current_time - start_time_obj)
        d = diff.total_seconds()
        if d > timeout:
            return True
        else:
            return False


def log_performance(request, perf):
    ec = get_experiment_context(request)

    msg = ec["username"] + " " + str(ec["condition"]) + " 0 0 " + perf["num"] + " VIEW_PERFORMANCE "
    msg = msg + " " + str(perf["total"]) + " " + str(perf["score"]) + " " + str(perf["rels"]) + " " + str(perf["nons"])
    event_logger.info(msg)


def log_event(event, request, query="", whooshid=-2, judgement=-2, trecid="", rank=-2, page=-2, doc_length=0,
              metrics=None):
    ec = get_experiment_context(request)

    msg = "{0} {1} {2} {3} {4} {5} {6}".format(ec["username"], ec["condition"], ec["interface"], ec["diversity"], ec["taskid"], ec["topicnum"], event)

    if whooshid > -1:
        event_logger.info(
            msg + " " + str(whooshid) + " " + trecid + " " + str(doc_length) + " " + str(judgement) + " " + str(rank))
    else:
        if page > 0:
            event_logger.info(msg + " " + str(page))
        elif metrics:
            metrics_string = ""

            # The order in which metrics appear is determined by how they are returned in
            # experiment_functions.get_query_performance_metrics().
            for metric in metrics:
                if type(metric) == int:
                    metrics_string = metrics_string + " " + str(metric)
                else:
                    metrics_string = metrics_string + " " + ("%.4f" % metric)

            event_logger.info(msg + " '" + query + "'" + str(metrics_string))
        else:
            if query and rank > 0:
                event_logger.info(msg + " '" + query + "' " + str(rank))
            elif query:
                event_logger.info(msg + " '" + query + "'")
            else:
                event_logger.info(msg)


def mark_document(request, whooshid, judgement, title="", trecid="", rank=0, doc_length=-1):
    ec = get_experiment_context(request)
    username = ec["username"]
    task = ec["taskid"]
    topicnum = ec["topicnum"]

    if judgement == 1:
        # write_to_log("DOC_MARKED_RELEVANT", whooshid )
        log_event(event="DOC_MARKED_RELEVANT", request=request, whooshid=whooshid, judgement=1, trecid=trecid,
                  rank=rank, doc_length=doc_length)
        print "DOC_MARKED_RELEVANT " + str(whooshid) + " " + trecid + " " + str(rank)

    if judgement == 0:
        # write_to_log("DOC_MARKED_NONRELEVANT", whooshid )
        print "DOC_MARKED_NONRELEVANT " + str(whooshid) + " " + trecid + " " + str(rank)
        log_event(event="DOC_MARKED_NONRELEVANT", request=request, whooshid=whooshid, judgement=0, trecid=trecid,
                  rank=rank, doc_length=doc_length)

    if judgement < 0:
        # write_to_log("DOC_VIEWED"), whooshid )
        log_event(event="DOC_MARKED_VIEWED", whooshid=whooshid, request=request, trecid=trecid, rank=rank,
                  doc_length=doc_length)
        print "DOC_VIEWED " + str(whooshid) + " " + trecid + " " + str(rank)

    # check if user has marked the document or not
    u = User.objects.get(username=username)
    try:
        doc = DocumentsExamined.objects.filter(user=u).filter(task=task).get(docid=whooshid)
        if doc:
            # update judgement that is already there
            if judgement > -1:
                print "doc judge changed to: " + str(judgement) + " from: " + str(doc.judgement)
                doc.judgement = judgement
                doc.save()
            else:
                judgement = doc.judgement

    except DocumentsExamined.DoesNotExist:
        # create an entry to show the document has been judged
        # print "no doc found in db"
        if judgement > -1:
            doc = DocumentsExamined(user=u, title=title, docid=whooshid, url='/treconomics/' + whooshid + '/',
                                    task=task, topic_num=topicnum, doc_num=trecid, judgement=judgement,
                                    judgement_date=datetime.datetime.now(tz=settings_timezone))
            doc.save()

    return judgement


def get_trec_assessed_doc_list(lst, topic_num, is_assessed=True):
    """
    Filters the given list to the documents that have been assessed for the given document.
    """
    ret_lst = []
    
    for doc in lst:
        val = qrels.get_value_if_exists(topic_num, doc)
        """
        if val is None:
            if not is_assessed:
                ret_lst.append(doc)

        else:
            ret_lst.append(doc)
        """
        if is_assessed:
            if val>=0:
                ret_lst.append(doc)
        else:
            if not val:
                ret_lst.append(doc)

    return ret_lst



def get_trec_scores(lst, topic_num):
    """

    :param lst: list of doc nums
    :param topic_num: integer
    :return:  returns (total, trec_rels, trec_nonrels, unassessed)
    """
    total = len(lst)
    trec_rels = 0
    trec_nonrels = 0
    unassessed = 0
    for doc in lst:
        val = qrels.get_value_if_exists(topic_num, doc)
        if val is None:
            unassessed += 1
        else:
            if int(val) > 0:
                trec_rels += 1
            else:
                trec_nonrels += 1
    return (total, trec_rels, trec_nonrels, unassessed)



def assess_performance(topic_num, doc_list):
    rels_found = 0
    non_rels_found = 0

    total = len(doc_list)
    for doc in doc_list:
        val = qrels.get_value(topic_num, doc)
        if val:
            if int(val) >= 1:
                rels_found += 1
            else:
                non_rels_found += 1
        else:
            non_rels_found += 1
    
    accuracy = 0.0
    
    if total > 0:
        accuracy = float(rels_found) / total
    
    performance = {'topicnum': topic_num, 'total_marked': total, 'rels': rels_found, 'nons': non_rels_found, 'accuracy': accuracy}
    return performance


# def assess_performance_diversity(topic_num, doc_list, diversity_flag):
#     performance = assess_performance(topic_num, doc_list)
#
#     observed_entities = []
#     new_doc_count = 0
#
#     for docid in doc_list:
#         doc_entities = qrels_diversity.get_mentioned_entities_for_doc(topic_num, docid)
#         new_in_doc = list(set(doc_entities) - set(observed_entities))
#         observed_entities = observed_entities + list(set(doc_entities) - set(observed_entities))
#
#         if len(new_in_doc) > 0:
#             new_doc_count = new_doc_count + 1
#
#     performance['diversity_new_docs'] = new_doc_count
#     performance['diversity_new_entities'] = len(observed_entities)
#
#     performance['diversity_accuracy'] = 0.0
#
#     if performance['total_marked'] > 0:
#         performance['diversity_accuracy'] = float(new_doc_count) / performance['total_marked']
#
#     return performance


def get_performance(username, topic_num):
    u = User.objects.get(username=username)
    docs = DocumentsExamined.objects.filter(user=u).filter(topic_num=topic_num)
    print "Documents to Judge for topic %s " % topic_num
    doc_list = []
    for d in docs:
        if d.judgement > 0:
            doc_list.append(d.doc_num)
            print str(d.topic_num) + " " + d.doc_num

    return assess_performance(str(topic_num), doc_list)


def get_user_performance_diversity(username, topic_num):
    """
    Given a username and a topic number, calls get_performance_diversity(), and return its output.
    """
    u = User.objects.get(username=username)
    docs = DocumentsExamined.objects.filter(user=u).filter(topic_num=topic_num)
    doc_list = []

    # Select all documents that were marked/saved by the searcher.
    for d in docs:
        if d.judgement > 0:
            doc_list.append(d.doc_num)
    
    return get_performance_diversity(doc_list, topic_num)
    

def get_performance_diversity(doc_list, topic_num):
    """
    A revised get_performance_diversity function.
    For debugging, use debug_doc_list as a list of documents that an imaginary user has saved (list of strings, TREC docnums).
    """
    return_dict = {}  # Return dictionary for all values.
    (total, trec_rels, trec_nonrels, unassessed) = get_trec_scores(doc_list, topic_num)
    
    # Calculate TREC accuracy -- i.e. accuracy considering only documents that were assessed.
    return_dict['trec_acc'] = 0.0
    
    if (trec_rels + trec_nonrels) > 0:
        return_dict['trec_acc'] = float(trec_rels) / (trec_rels + trec_nonrels)
    
    # Calculate accuracy -- i.e. considering all saved documents.
    return_dict['acc'] = 0.0
    
    if total > 0:
        return_dict['acc'] = float(trec_rels) / total
    
    # Assign raw values to the dictionary.
    return_dict['trec_rels'] = trec_rels
    return_dict['trec_nonrels'] = trec_nonrels
    return_dict['trec_unassessed'] = unassessed
    return_dict['total'] = total
    
    # Estimated accuracy and relevant documents
    return_dict['estimated_acc'] = (return_dict['trec_acc'] + return_dict['acc']) / 2.0
    return_dict['estimated_rels'] = math.floor(trec_rels + return_dict['estimated_acc'] * unassessed)
    
    # Entity calculations
    observed_entities = []
    new_doc_count = 0
    
    for docid in doc_list:
        doc_entities = qrels_diversity.get_mentioned_entities_for_doc(topic_num, docid)
        new_in_doc = list(set(doc_entities) - set(observed_entities))
        observed_entities = observed_entities + list(set(doc_entities) - set(observed_entities))
        
        if len(new_in_doc) > 0:
            new_doc_count = new_doc_count + 1
    
    return_dict['diversity_new_docs'] = new_doc_count
    return_dict['diversity_new_entities'] = len(observed_entities)
    
    return return_dict


def query_result_performance(results, topic_num):
    i = 0
    rels_found = 0
    for r in results:
        i += 1
        if qrels.get_value(topic_num, r.docid) > 0:
            rels_found += 1

    # TODO rels_found = sum(qrels.get_value(topic_num, r.docid) > 0 for r in results)
    # return [rels_found, len(results)]

    return [rels_found, i]


def get_topic_relevant_count(topic_num):
    """
    Returns the number of documents considered relevant for topic topic_num.
    """
    count = 0

    for document in qrels.get_doc_list(topic_num):
        if qrels.get_value(topic_num, document) > 0:
            count += 1

    # TODO return sum(qrels.get_value(topic_num, doc) > 0 for doc in qrels.get_doc_list(topic_num))
    return count


def calculate_precision(results, topic_num, k):
    """
    Returns a float representing the precision @ k for a given topic, topic_num, and set of results, results.
    """
    results = results[0:k]
    no_relevant = query_result_performance(results, topic_num)[0]
    return no_relevant / float(k)


def get_query_performance_metrics(results, topic_num):
    """
    Returns performance metrics for a given list of results,
    results, and a TREC topic, topic_num.
    List returned is in the format [p@1, p@2, p@3, p@4, p@5,
     p@10, p@15, p@20, p@125, p@30, p@40, p@50, Rprec, total rel. docs]
    """

    total_relevant_docs = get_topic_relevant_count(topic_num)

    p_at_1 = calculate_precision(results, topic_num, 1)
    p_at_2 = calculate_precision(results, topic_num, 2)
    p_at_3 = calculate_precision(results, topic_num, 3)
    p_at_4 = calculate_precision(results, topic_num, 5)
    p_at_5 = calculate_precision(results, topic_num, 6)
    p_at_10 = calculate_precision(results, topic_num, 10)
    p_at_15 = calculate_precision(results, topic_num, 15)
    p_at_20 = calculate_precision(results, topic_num, 20)
    p_at_25 = calculate_precision(results, topic_num, 25)
    p_at_30 = calculate_precision(results, topic_num, 30)
    p_at_40 = calculate_precision(results, topic_num, 40)
    p_at_50 = calculate_precision(results, topic_num, 50)
    r_prec = int(calculate_precision(results, topic_num, total_relevant_docs))

    p_at_1_to_5 = [calculate_precision(results, topic_num, i) for i in xrange(1, 6)]
    p_at_10_to_25 = [calculate_precision(results, topic_num, i) for i in xrange(10, 26, 5)]
    p_at_30_to_50 = [calculate_precision(results, topic_num, i) for i in xrange(30, 51, 10)]

    return [p_at_1, p_at_2, p_at_3, p_at_4, p_at_5, p_at_10, p_at_15, p_at_20, p_at_25, p_at_30, p_at_40, p_at_50,
            r_prec, total_relevant_docs]


def populate_context_dict(experiment_context, page_context_dict):

    if "username" in experiment_context:
        page_context_dict["participant"] = experiment_context["username"]
    if "condition" in experiment_context:
        page_context_dict["condition"] = experiment_context["condition"]
    if "topicnum" in experiment_context:
        page_context_dict["topic"] = experiment_context["topicnum"]
    if "interface" in experiment_context:
        page_context_dict["interface"]  = experiment_context["interface"]
    if "rpp" in experiment_context:
        page_context_dict["rpp"] = experiment_context["rpp"]
    if "diversity" in experiment_context:
        page_context_dict["diversity"] = experiment_context["diversity"]
    if "target" in experiment_context:
        page_context_dict["target"] = experiment_context["target"]
    return page_context_dict