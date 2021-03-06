#
# Diversification Algorithm with access to the diversity QRELs
# Mark II -- More complex algorithm, not as rewarding as the first attempt.
# Updated to work with the ifind search objects.
#
# Slightly updated to make it easier to drop into the treconomis environment.
# 
# Author: David Maxwell and Leif Azzopardi
# Date: 2018-01-06
#

import copy
from treconomics.experiment_functions import qrels_diversity 


# TODO: @leifos
# - What values do we use above?
# - To diversity, you need:
#   * a list of results
#   * a topic number
#   * a lambda value
#   * a DIVERSIFY_TO_RANK value
#
# - call diversify(results, topic_num, to_rank, lam)
#   This returns a new list, with the diversified set of results according to our algorithm.
#   The results object you pass in should be an iterable -- it can be a whoosh.results object or a list.
#   The object that is returned is just a Python list -- so there could be an issue down the line if it relies on something whoosh.results provides. Hope not -- I can't create an artifical whoosh.results object (easily, at least).


def convert_results_to_list(results, deep_copy=True):
    """
    Given a Whoosh results object, converts it to a list and returns that list.
    Useful, as the Whoosh results object does not permit reassignment of Hit objects.
    Note that if deep_copy is True, a deep copy of the list is returned.
    """
    results_list = []
    
    for hit in results:
        if deep_copy:
            results_list.append(copy.copy(hit))
            continue
        
        results_list.append(hit)
    
    return results_list


def get_highest_score_index(results_list):
    """
    Given a list of results, returns the index of the hit with the highest score.
    Simple find the maximum algorithm stuff going on here.
    """
    highest_score = 0.0
    highest_index = 0
    index = 0
    
    for hit in results_list:
        if hit.score > highest_score:
            highest_score = hit.score
            highest_index = index
        
        index = index + 1
    
    return highest_index


def get_new_entities(observed_entities, document_entities):
    """
    Given a list of previously seen entities, and a list of document entities, returns
    a list of entities in the document which have not yet been previously seen.
    """
    return list(set(document_entities) - set(observed_entities))


# def get_existing_entities(observed_entities, document_entities):
#     """
#     Given a list of previously seen entities, and a list of document entities, returns
#     the intersection of the two lists -- i.e. the entities that have already been seen.
#     """
#     return list(set(observed_entities) & set(document_entities))


def get_observed_entities_for_list(topic, rankings_list):
    """
    Given a list of Whoosh Hit objects, returns a list of the different entities that are mentioned in them.
    """
    observed_entities = []
    
    for hit in rankings_list:
        docid = hit.docid
        
        entities = qrels_diversity.get_mentioned_entities_for_doc(topic, docid)
        new_entities = get_new_entities(observed_entities, entities)
        
        observed_entities = observed_entities + new_entities
    
    return observed_entities


def diversify_results(results, topic, to_rank=30, lam=1.0):
    """
    The diversification algorithm.
    Given a ifind results object, returns a re-ranked list, with more diverse content at the top.
    By diverse, we mean a selection of documents discussing a wider range of identified entities.
    """

    results_len = len(results.results)
    #results_len = results.scored_length()  # Doing len(results) returns the number of hits, not the top k.
    #print(results)
    # Simple sanity check -- no results? Can't diversify anything!
    if results_len == 0:
        return results
    
    # Before diversifying, check -- are there enough results to go to to_rank?
    # If not, change to_rank to the length of the results we have.
    if to_rank is None:
        to_rank = results_len
    
    # Not enough results to get to to_rank? Change the to_rank cap to the results length.
    if results_len < to_rank:
        to_rank = results_len
    
    # Check that lambda is a float in case of floating point calculations...
    if type(lam) != float:
        lam = float(lam)
    
    ############################
    ### Main algorithm below ###
    ############################
    observed_entities = []  # What entities have been previously seen? This list holds them.
    
    # As the list of results is probably larger than the depth we re-rank to, take a slice.
    # This is our original list of results that we'll be modifiying and popping from.
    old_rankings = results.results[:to_rank]
    
    # For our new rankings, start with the first document -- this won't change.
    # This list will be populated as we iterate through the other rankings list.
    new_rankings = [old_rankings.pop(0)]
    
    for i in range(1, to_rank):
        observed_entities = get_observed_entities_for_list(topic, new_rankings)
        
        for j in range(0, len(old_rankings)):
            docid = old_rankings[j].docid
            entities = qrels_diversity.get_mentioned_entities_for_doc(topic, docid)
            new_entities = get_new_entities(observed_entities, entities)
            #seen_entities = get_existing_entities(qrels_diversity, observed_entities, entities)
            
            old_rankings[j].score = old_rankings[j].score + (lam * len(new_entities))
            
        # Sort the list in reverse order, so the highest score is first. Then pop from old, push to new.
        old_rankings.sort(key=lambda x: x.score, reverse=True)
        new_rankings.append(old_rankings.pop(0))
    
    results.results = new_rankings + results.results[to_rank:]
    return results
    
    # The main algorithm -- only work on the top to_rank documents.
    
    # Leif notes (algorithm): two loops still...
    # for first doc, get the mentioned entities. this is outside the loop (set to x).
    # for each doc in the rest of the list, what entities are in those docs, and how different are they?
    # compute score, sort it, take the first element from that, that becomes the second document
    #   the key is to sort the sublist scores, and pick the top element from that list.
    # take entities from the first two now - replace x with this.
    # repeat this until all documents have been observed.
    #
    # how does lambda influence the performance?
    #   alpha ndcg -- run the queries from the sigir study from before to see what happens when you change lambda.
    
    # More:
    # take all documents that have been judged
    #   take the non-rel documents in the QRELs for the 
    # so you update the list of entities with those previously seen (i.e. x) after each document has been observed.
