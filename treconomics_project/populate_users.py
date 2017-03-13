__author__ = 'leif'
import os


def populate():
    print 'Adding Users'

    for i in range(0,20):
        uname = 'fin'+str(i)
        add_user(uname,uname,0,0,i)

def add_user(username, password, condition, experiment, rotation, data=None):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    up = \
        UserProfile.objects.get_or_create(user=u,
                                          condition=condition,
                                          experiment=experiment,
                                          rotation=rotation,
                                          data=data)[0]
    print '%s, %s, %d, %d  ' % (username, password, condition, rotation)


def add_task(topic_num, title, description):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num,
                                              title=title,
                                              description=description)[0]
    print "\t %s" % t
    return t


if __name__ == '__main__':
    import django

    print "Starting Treconomics population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')

    django.setup()
    from treconomics.models import TaskDescription
    from treconomics.models import UserProfile
    from django.contrib.auth.models import User


    populate()