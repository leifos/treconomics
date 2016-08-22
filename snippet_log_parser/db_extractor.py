import os
import sys
from utils import setup_django_env



def get_user_accounts():
    from django.contrib.auth.models import User
    from treconomics.models import UserProfile

    accounts = []

    count = 0
    users = User.objects.all()
    print "number of users", len(users)
    for user in users:
        try:
            treconomics_user = UserProfile.objects.get(user=user)
        
        
        
            if treconomics_user.steps_completed > 0:
                count = count + 1
                accounts.append({'userid': treconomics_user.user.id,
                     'username': treconomics_user.user.username,
                     'condition': treconomics_user.condition,
                     'rotation': treconomics_user.rotation})
        except:
            pass
    
    print "number of users with step:", count
    return accounts

def get_user_key():
    return 'userid,username,condition,rotation'

def get_user_details(treconomics_user):
    keys = get_user_key().split(',')
    return_str = ""

    for key in keys:
        return_str = '{0}{1},'.format(return_str, treconomics_user[key])

    return return_str[:-1]

def get_key(model, exclude_fields):
    return_str = ''
    fields = model._meta.get_all_field_names()

    for field in fields:
        if field not in exclude_fields:
            return_str = '{0}{1},'.format(return_str, field)

    return return_str[:-1]





def get_demographics(users):
    from snippets.models import SnippetDemographicsSurvey
    exclude = ['id', 'user']  # Exclude the following fields from output
    fields = get_key(SnippetDemographicsSurvey, exclude)
    output = '{0},{1}{2}'.format(get_user_key(), fields, os.linesep)

    fields = fields.split(',')

    for treconomics_user in users:
        try:
            survey = SnippetDemographicsSurvey.objects.get(user=treconomics_user['userid'])

            output_line = get_user_details(treconomics_user) + ','

            for field in fields:
                output_line = '{0}{1},'.format(output_line, survey.__dict__[field])

            output = output + output_line[:-1]
            output = output + os.linesep
        except:
            # user does not have a record
            print "user didnt complete demographics", treconomics_user
            pass


    output = output[:-1]
    return output


def get_task_survey(users, model, exclude=['id', 'user']):
    fields = get_key(model, exclude)
    output = '{0},{1}{2}'.format(get_user_key(), fields, os.linesep)

    fields = fields.split(',')

    for treconomics_user in users:
        surveys = model.objects.filter(user=treconomics_user['userid'])

        for survey in surveys:
            output_line = get_user_details(treconomics_user) + ','

            for field in fields:
                output_line = '{0}{1},'.format(output_line, survey.__dict__[field])

            output = output + output_line[:-1]
            output = output + os.linesep

    output = output[:-1]
    return output

def write(filename, contents):
    f = open(filename, 'w')
    f.write(contents)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print 'Usage: {0} <db> <path_to_treconomics_project>'.format(sys.argv[0])
        exit(2)
    
    setup_django_env(sys.argv[2])
    
    users = get_user_accounts()
    demographics = get_demographics(users)
    
    from snippets.models import SnippetExitSurvey
    from snippets.models import SnippetPostTaskSurvey
    from snippets.models import SnippetPreTaskTopicKnowledgeSurvey
    from snippets.models import SystemSnippetPostTaskSurvey
    
    exit_survey = get_task_survey(users, SnippetExitSurvey)
    post_task = get_task_survey(users, SnippetPostTaskSurvey)
    pre_task_knowledge = get_task_survey(users, SnippetPreTaskTopicKnowledgeSurvey)
    system_post_task = get_task_survey(users, SystemSnippetPostTaskSurvey)
    
    write('demographics.csv', demographics)
    write('pre_task_knowledge.csv', pre_task_knowledge)
    write('post_task.csv', post_task)
    write('system_post_task.csv', system_post_task)