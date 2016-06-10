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
    from treconomics.models_anita_experiments import AnitaDemographicsSurvey
    exclude = ['id', 'user']  # Exclude the following fields from output
    fields = get_key(AnitaDemographicsSurvey, exclude)
    output = '{0},{1}{2}'.format(get_user_key(), fields, os.linesep)

    fields = fields.split(',')

    for treconomics_user in users:
        try:
            survey = AnitaDemographicsSurvey.objects.get(user=treconomics_user['userid'])

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

    print sys.argv
    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print 'Usage: {0} <db> <path_to_treconomics_project>'.format(sys.argv[0])
        exit(2)



    setup_django_env(sys.argv[2])



    users = get_user_accounts()
    demographics = get_demographics(users)


    from treconomics.models_anita_experiments import AnitaPreTaskSurvey, AnitaPostTask0Survey
    from treconomics.models_anita_experiments import AnitaPostTask1Survey, AnitaPostTask2Survey,AnitaPostTask3Survey
    from treconomics.models_anita_experiments import AnitaExit1Survey,AnitaExit2Survey,AnitaExit3Survey

    pretasksurvey = get_task_survey(users, AnitaPreTaskSurvey)
    posttasksurvey0 = get_task_survey(users, AnitaPostTask0Survey)
    posttasksurvey1 = get_task_survey(users, AnitaPostTask1Survey)
    posttasksurvey2 = get_task_survey(users, AnitaPostTask2Survey)
    posttasksurvey3 = get_task_survey(users, AnitaPostTask3Survey)

    exitsurvey1 = get_task_survey(users, AnitaExit1Survey)
    exitsurvey2 = get_task_survey(users, AnitaExit2Survey)
    exitsurvey3 = get_task_survey(users, AnitaExit3Survey)


    #examined = get_task_survey(users, DocumentsExamined, exclude=['id', 'user', 'url', 'title'])

    write('demographics.csv', demographics)
    write('pretasksurvey.csv', pretasksurvey)
    write('posttasksurvey0.csv', posttasksurvey0)
    write('posttasksurvey1.csv', posttasksurvey1)
    write('posttasksurvey2.csv', posttasksurvey2)
    write('posttasksurvey3.csv', posttasksurvey3)
    write('exitsurvey1.csv', exitsurvey1)
    write('exitsurvey2.csv', exitsurvey2)
    write('exitsurvey3.csv', exitsurvey3)


	