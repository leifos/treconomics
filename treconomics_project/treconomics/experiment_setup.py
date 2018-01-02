__author__ = 'leif'
from ifind.common.rotation_ordering import PermutatedRotationOrdering


class ExperimentSetup(object):
    """
    The 0th task is the practice task, then 1st task is next, etc, in each list i.e. interface, engine, timeout, etc.
    if it is not a list, then it assigns the value to all setups.
    """

    def __init__(self,
                 workflow,
                 engine,
                 timeout=0,
                 topics=['347', '344'],
                 practice_topic='367',
                 practice_interface=1,
                 practice_diversity=0,
                 rpp=10,
                 interface=[1, 2, 3],
                 diversity=[0,1,1],
                 description='',
                 delay_results=0,
                 delay_docview=0,
                 rotation_type=0,
                 autocomplete=False,
                 tasks=2,
                 trie=None):
        self.timeout = timeout
        self.topics = topics
        self.rpp = rpp
        self.interface = interface
        self.diversity = diversity
        self.engine = engine
        self.description = description
        self.workflow = workflow
        self.pro = PermutatedRotationOrdering()

        # Instance variable to allow you to delay results from appearing, and for delaying documents from appearing.
        # Specify an integer or float value. The value specifies the number of seconds the delay should last for.
        # If 0, there is no delay.
        self.delay_results = delay_results
        self.delay_docview = delay_docview
        self.practice_topic = practice_topic
        self.practice_interface = practice_interface
        self.practice_diversity = practice_diversity
        self.rotation_type = rotation_type
        # Do you want to use AJAX suggestions if the AJAX search interface is used?
        # To ensure that suggestions do not show with the structured interface, wrap the following assignments
        # in an if - if interface == 1:
        self.autocomplete = autocomplete
        self.trie = trie
        self.tasks = tasks

        if self.autocomplete and not self.trie:
            raise ValueError("If you want to use autocomplete, you must also specify the 'trie' parameter.")

    def _get_check_i(self, items, i):
        return i % self.pro.number_of_orderings(items)

    def _get_value(self, var, t):
        if type(var) is list:
            return var[t]
        else:
            return var

    def get_rotations(self, items, i):
        """ get the ith rotation from the items
        :param i:
        :return: returns the list of item numbers
        """
        ith = self._get_check_i(items, i)
        return self.pro.get_ordering(items, ith)

    def get_rotation_topic(self, i, t):
        """ get the ith rotation and the tth topic
        :param i: integer
        :param t: integer
        :return: returns the topic number
        """
        if self.rotation_type == 0:
            ith = self._get_check_i(self.topics, i)
            rotations = self.pro.get_ordering(self.topics, ith)
            t -= 1
            return rotations[t]
        else:
            return self.get_topic(t)

    def get_rotation_interface(self, i, t):
        """ get the ith rotation and the tth interface
        :param i: integer
        :param t: integer
        :return: returns the interface number
        """

        if self.rotation_type == 1:
            ith = self._get_check_i(self.interface, i)
            rotations = self.pro.get_ordering(self.interface, ith)
            t -= 1
            return rotations[t]
        else:
            return self.get_interface(t)

    def get_rotation_diversity(self, i, t):
        """ get the ith rotation and the tth diversity
        :param i: integer
        :param t: integer
        :return: returns the diversity number
        """

        if self.rotation_type == 2:
            ith = self._get_check_i(self.diversity, i)
            rotations = self.pro.get_ordering(self.diversity, ith)
            t -= 1
            return rotations[t]
        else:
            return self.get_diversity(t)

    def get_topic(self, t=0):

        if t == 0:
            return self.practice_topic
        else:
            t -= 1
            return self._get_value(self.topics, t)

    def get_interface(self, t=0):

        if t == 0:
            return self.practice_interface
        else:
            t -= 1
            return self._get_value(self.interface, t)

    def get_diversity(self, t=0):
        if t == 0:
            return self.practice_diversity
        else:
            t -= 1
            return self._get_value(self.diversity, t)

    def get_engine(self, t=0):
        return self._get_value(self.engine, t)

    def get_timeout(self, t=0):
        return self._get_value(self.timeout, t)

    def get_trie(self):
        return self.trie

    def get_result_delay(self, t=0):
        return self._get_value(self.delay_results, t)

    def get_docview_delay(self, t=0):
        return self._get_value(self.delay_docview, t)

    def get_rpp(self, t=0):
        return self._get_value(self.rpp, t)

    def get_exp_dict(self, t=0, i=0):

        exp = {'engine': self.get_engine(t),
               'interface': self.get_interface(t),
               'diversity': self.get_diversity(t),
               'result_delay': self.get_result_delay(t),
               'docview_delay': self.get_docview_delay(t),
               'rpp': self.get_rpp(t),
               'timeout': self.get_timeout(t),
               'workflow': self.workflow,
               'autocomplete': self.autocomplete,
               'trie': self.trie,

        }
        if t == 0:
            exp['topic'] = self.practice_topic
            exp['interface'] = self.practice_interface
            exp['diversity'] = self.practice_diversity
            exp['desc'] = 'practice'
        else:
            if self.rotation_type == 0:
                exp['topic'] = self.get_rotation_topic(i, t)
                exp['interface'] = self.get_interface(t)
                exp['diversity'] = self.get_diversity(t)
            else:
                if self.rotation_type == 2:

                    exp['topic'] = self.get_topic(t)
                    exp['interface'] = self.get_interface(t)
                    exp['diversity'] = self.get_rotation_diversity(i, t)
                else:
                    exp['interface'] = self.get_rotation_interface(i, t)
                    exp['topic'] = self.get_topic(t)
                    exp['diversity'] = self.get_diversity(t)

            exp['desc'] = 'real'

        return exp

    def __str__(self):
        return self.description


if __name__ == '__main__':

    es = ExperimentSetup(workflow=None, engine=None, practice_topic='341',
                           topics=['347', '367', '354','999'],
                           rpp=10,
                           practice_interface=1,
                           practice_diversity=0,
                           interface= [1, 2, 3, 4],
                           diversity =[1, 1, 0, 0],
                           rotation_type=2,
                         tasks=4)


    for r in range(0, 13):
        print "User on rotation", r
        for t in range(0, 5):
            des = es.get_exp_dict(t, r)

            print "Taskno: {0} Rotation: {1} Topic: {2} Interface: {3} Diversity: {4}".format(t,  r, des['topic'], des['interface'], des['diversity'])
