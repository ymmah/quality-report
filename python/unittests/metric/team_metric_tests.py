'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from qualitylib import metric, domain
import datetime
import unittest

    
class FakeSubject(object):  # pylint:disable=too-few-public-methods
    ''' Fake subject (team). ''' 
    def __str__(self):
        return 'FakeSubject'


class FakeBirt(object):
    ''' Fake Birt so we can return fake velocity information. '''
    # pylint: disable=unused-argument
      
    @staticmethod
    def planned_velocity(birt_id):
        ''' Return the planned velocity of the team. '''
        return 1
    
    @staticmethod
    def actual_velocity(birt_id):
        ''' Return the actual velocity of the team so far. '''
        return 0.5
    
    @staticmethod
    def required_velocity(birt_id):
        ''' Return the required velocity of the team. '''
        return 2
    
    @staticmethod
    def nr_points_planned(birt_id):
        ''' Return the number of points planned for the sprint. '''
        return 20
    
    @staticmethod
    def nr_points_realized(birt_id):
        ''' Return the number of points realized so far. '''
        return 10
    
    @staticmethod
    def days_in_sprint(birt_id):
        ''' Return the number of working days in the sprint. '''
        return 20
    
    @staticmethod
    def day_in_sprint(birt_id):
        ''' Return the current day in the sprint. '''
        return 10
    
    @staticmethod
    def sprint_progress_url(birt_id):
        ''' Return the url of the sprint progress report. '''
        return 'http://birt/report/'
    
    
class TeamProgressTest(unittest.TestCase):
     # pylint: disable=too-many-public-methods
    ''' Unit tests for the team progress metric. '''
    
    def setUp(self):  # pylint: disable=invalid-name
        self.__subject = domain.Team('ABC')
        self.__metric = metric.TeamProgress(subject=self.__subject, 
                                            birt=FakeBirt(), 
                                            wiki=None, history=None)
        
    def test_value(self):
        ''' Test that the value of the metric equals the required velocity. '''
        self.assertEqual(2, self.__metric.value())

    def test_report(self):
        ''' Test that the report is correct. '''
        self.assertEqual('Team ABC heeft een velocity van 2.0 punt per dag '\
                         'nodig om het sprintdoel van de huidige sprint ' \
                         '(20.0 punten) te halen. De geplande velocity is ' \
                         '1.0 punt per dag. De tot nu toe (dag 10 van 20) ' \
                         'gerealiseerde velocity is 0.5 punt per dag ' \
                         '(10.0 punten).', self.__metric.report())

    def test_url(self):
        ''' Test that the url of the metric is the url of the Birt report. '''
        self.assertEqual(dict(Birt='http://birt/report/'), self.__metric.url())


class FakeWiki(object):
    ''' Fake a wiki metric source. '''
    @staticmethod  # pylint: disable=unused-argument
    def team_spirit(*args):
        ''' Return a fake team spirit. '''
        return ':-)'
    
    @staticmethod  # pylint: disable=unused-argument
    def date_of_last_team_spirit_measurement(*args):  
        # pylint: disable=invalid-name
        ''' Return a fake date. '''
        return datetime.datetime.now()
    
    @staticmethod
    def url():
        ''' Return a fake url. '''
        return 'http://wiki'
    

class TeamSpiritTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the ARTstability metric. '''
    
    def setUp(self):  # pylint: disable=invalid-name
        self.__wiki = FakeWiki()
        self.__metric = metric.TeamSpirit(subject=FakeSubject(), 
                                          wiki=self.__wiki, history=None)
        
    def test_value(self):
        ''' Test that the value of the metric equals the team spirit reported
            by the wiki. '''
        self.assertEqual(self.__wiki.team_spirit(FakeSubject()),
                         self.__metric.value())

    def test_numerical_value(self):
        ''' Test that the smiley is translated into an integer. '''
        self.assertEqual(2, self.__metric.numerical_value())
    
    def test_y_axis_range(self):
        ''' Test that the y axis range is 0-2. '''
        self.assertEqual((0, 2), self.__metric.y_axis_range())
        
    def test_status(self):
        ''' Test that the status is perfect. '''
        self.assertEqual('perfect', self.__metric.status())
        
    def test_url(self):
        ''' Test that the metric url uses the wiki url. '''
        self.assertEqual(dict(Wiki=FakeWiki().url()), self.__metric.url())
