__author__ = 'leif'
import os


def populate():
    print 'Adding Task Descriptions'
    add_task(topic_num='341',
             title='Airport Security',
             description='<p>For this task, '
                         'your job is to find articles '
                         'that discuss procedures taken by international '
                         'airports, to better screen passengers '
                         'and their carry-on luggage.</p>'
                         '<p>A relevant document would discuss how effective government orders to '
                         'better scrutinize passengers and luggage on international flights and to step '
                         'up screening of all carry-on baggage has been.</p>')
    add_task(topic_num='347',
             title='Wildlife Extinction',
             description='<p>For this task, your job is '
                         'to find articles that discuss efforts '
                         'made by countries other than the United States '
                         'to prevent the extinction of wildlife species '
                         'native to their countries. </p>'
                         '<p>A relevant document will specify the country, the involved species, and steps taken to save the species.</p>')
    add_task(topic_num='354',
             title='Journalist Risks',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances where journalists '
                         'have been put at risk '
                         '(e.g., killed, arrested or taken hostage) '
                         'in the performance of their work.</p>'
                         '<p>Any document identifying an instance where a journalist or correspondent has been killed, arrested or taken hostage in the performance of his work is relevant.</p>')
    add_task(topic_num='435',
             title='Curbing Population Growth',
             description='<p>For this task, your job '
                         'is to find articles that discuss countries '
                         'that have been successful in curbing population '
                         'growth and the measures they have taken to do so.</p>'
                         '<p>A relevant document must describe an actual case in which population measures have been taken and their results are known. The reduction measures must have been actively pursued; that is, passive events such as disease or famine involuntarily reducing the population are not relevant.</p>')
    add_task(topic_num='367',
             title='Piracy',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances of piracy, '
                         'or the illegal boarding or taking control of a boat.</p>'
                         '<p>Documents discussing piracy on any body of water are relevant.  Documents discussing the legal taking of ships or their contents by a national authority are non-relevant.  Clashes between fishing vessels over fishing are not relevant, unless one vessel is boarded.</p>')

    add_task(topic_num='408',
             title='Tropical Storms',
             description='<p>For this task, your job is to find '
                        'about tropical storms (hurricanes and typhoons) that have caused significant property damage and loss of life? '
                         'The date of the storm, the area affected, and the extent of damage/casualties are all of interest</p>'
                         '<p>Documents that describe the damage caused by a tropical storm as  '
                         ' "slight", "limited", or "small" are not relevant.</p>')


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