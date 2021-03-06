"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import unittest

from hqlib import metric, domain, metric_source


class FakeBirt(object):
    """ Provide for a fake Birt object. """
    # pylint: disable=unused-argument
    metric_source_name = metric_source.Birt.metric_source_name
    needs_metric_source_id = metric_source.Birt.needs_metric_source_id
    date_of_last_manual_tests = datetime.datetime.now() - datetime.timedelta(days=5)
    nr_manual_tests = 10

    def __init__(self, test_design=True):
        self.__test_design = test_design
        self.down = False

    @staticmethod
    def approved_ltcs():
        """ Return the number of approved logical test cases. """
        return 100

    def nr_ltcs(self):
        """ Return the number of logical test cases. """
        return -1 if self.down else 120

    @staticmethod
    def reviewed_ltcs():
        """ Return the number of reviewed logical test cases. """
        return 110

    @staticmethod
    def whats_missing_url():
        """ Return the url for the what's missing report. """
        return 'http://whats_missing'

    def date_of_last_manual_test(self, *args):
        """ Return the date that the manual test cases were last executed. """
        return self.date_of_last_manual_tests

    def nr_manual_ltcs(self, version='trunk'):
        """ Return the number of manual logical test cases. """
        return self.nr_manual_tests

    @staticmethod
    def nr_manual_ltcs_too_old(version, target):
        """ Return the number of manual logical test cases that haven't been executed recently enough. """
        return 5

    @staticmethod
    def nr_automated_ltcs():
        """ Return the number of automated logical test cases. """
        return 20

    def nr_ltcs_to_be_automated(self):
        """ Return the number of logical test cases that should be automated. """
        return -1 if self.down else 25

    @staticmethod
    def manual_test_execution_url(*args):
        """ Return the url for the manual test execution report. """
        return 'http://manual_tests'


class FakeSubject(object):
    """ Provide for a fake subject. """
    version = ''
    version_type = 'trunk'

    def __init__(self, birt_id=True, team=True, scrum_team=True):
        self.__birt_id = birt_id
        self.__team = team
        self.__scrum_team = scrum_team

    @staticmethod
    def name():
        """ Return the name of the subject. """
        return 'FakeSubject'

    def metric_source_id(self, metric_src):  # pylint: disable=unused-argument
        """ Return the Birt id of the subject. """
        return 'birt id' if self.__birt_id else ''


class LogicalTestCasesNotAutomatedTest(unittest.TestCase):
    """ Unit tests for the logical test cases to be automated metric. """
    def setUp(self):
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(metric_sources={metric_source.Birt: self.__birt})
        self.__metric = metric.LogicalTestCasesNotAutomated(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the percentage of user stories that has enough logical test cases
            as reported by Birt. """
        self.assertEqual(5, self.__metric.value())

    def test_value_on_error(self):
        """ Test that the value is -1 when the metric source is not available. """
        self.__birt.down = True
        self.assertEqual(-1, self.__metric.value())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({self.__birt.metric_source_name: self.__birt.whats_missing_url()}, self.__metric.url())


class LogicalTestCasesNotReviewedTest(unittest.TestCase):
    """ Unit tests for the unreviewed logical test cases metric. """
    def setUp(self):
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(metric_sources={metric_source.Birt: self.__birt})
        self.__metric = metric.LogicalTestCasesNotReviewed(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the number of not reviewed logical test cases as reported by Birt. """
        self.assertEqual(10, self.__metric.value())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({self.__birt.metric_source_name: self.__birt.whats_missing_url()}, self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertEqual('FakeSubject heeft 10 niet gereviewde logische testgevallen van in totaal 120 '
                         'logische testgevallen.', self.__metric.report())


class LogicalTestCasesNotApprovedTest(unittest.TestCase):
    """ Unit tests for the unapproved logical test case metric. """
    def setUp(self):
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(metric_sources={metric_source.Birt: self.__birt})
        self.__metric = metric.LogicalTestCasesNotApproved(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the number of not approved logical test cases as reported by Birt. """
        self.assertEqual(10, self.__metric.value())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({self.__birt.metric_source_name: self.__birt.whats_missing_url()}, self.__metric.url())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertEqual('FakeSubject heeft 10 niet goedgekeurde logische testgevallen van in totaal 110 gereviewde '
                         'logische testgevallen.', self.__metric.report())


class NumberOfManualLogicalTestCasesTest(unittest.TestCase):
    """ Unit tests for the NumberOfManualLogicalTestCases metric. """
    def setUp(self):
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(metric_sources={metric_source.Birt: self.__birt})
        self.__metric = metric.NumberOfManualLogicalTestCases(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the number of manual logical test cases. """
        self.assertEqual(10, self.__metric.value())

    def test_value_when_birt_missing(self):
        """ Test that the value is -1 when Birt is missing. """
        manual_ltcs = metric.NumberOfManualLogicalTestCases(subject=self.__subject, project=domain.Project())
        self.assertEqual(-1, manual_ltcs.value())

    def test_report(self):
        """ Test the metric report. """
        self.assertEqual('10 van de 120 logische testgevallen zijn handmatig.', self.__metric.report())

    def test_norm(self):
        """ Test the norm text. """
        self.assertEqual('Maximaal 10 van de logische testgevallen is handmatig. Meer dan 50 is rood.',
                         self.__metric.norm())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({self.__birt.metric_source_name: self.__birt.manual_test_execution_url()}, self.__metric.url())


class ManualLogicalTestCasesTest(unittest.TestCase):
    """ Unit tests for the ManualLogicalTestCases metric. """
    def setUp(self):
        self.__birt = FakeBirt()
        self.__subject = FakeSubject()
        self.__project = domain.Project(metric_sources={metric_source.Birt: self.__birt})
        self.__metric = metric.ManualLogicalTestCases(subject=self.__subject, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the number of days ago that the manual logical test cases have been
            last executed as reported by Birt. """
        self.assertEqual(5, self.__metric.value())

    def test_value_when_untested(self):
        """ Test that the value is the age of the version when the release has not been tested. """
        self.__birt.date_of_last_manual_tests = datetime.datetime(2000, 1, 1)
        expected_value = (datetime.datetime.now() - datetime.datetime(2000, 1, 1)).days
        self.assertEqual(expected_value, self.__metric.value())

    def test_report(self):
        """ Test that the report is correct. """
        self.assertTrue('5 van de 10 handmatige logische testgevallen van FakeSubject zijn te lang geleden '
                        '(meest recente 5 dag(en))' in self.__metric.report())

    def test_report_with_untested(self):
        """ Test that the report mentions the number of test cases that have never been tested. """
        self.__birt.date_of_last_manual_tests = datetime.datetime.now() - datetime.timedelta(days=60)
        self.assertTrue(
            self.__metric.report().startswith('5 van de 10 handmatige logische testgevallen van FakeSubject zijn '
                                              'te lang geleden (meest recente 60 dag(en))'))

    def test_report_when_untested(self):
        """ Test that the report uses the correct template when the manual tests have not been executed at all. """
        self.__birt.date_of_last_manual_tests = datetime.datetime.min
        self.assertEqual('De 10 handmatige logische testgevallen van FakeSubject zijn nog niet allemaal uitgevoerd.',
                         self.__metric.report())

    def test_report_without_manual_testcases(self):
        """ Test the report when there are no manual test cases. """
        self.__birt.nr_manual_tests = 0
        self.assertEqual(self.__metric.no_manual_tests_template.format(name='FakeSubject', unit=self.__metric.unit),
                         self.__metric.report())

    def test_status_without_manual_testcases(self):
        """ Test that the status is green when there are no manual test cases. """
        self.__birt.nr_manual_tests = 0
        self.assertEqual('perfect', self.__metric.status())

    def test_url(self):
        """ Test that the url is correct. """
        self.assertEqual({'Birt reports': self.__birt.manual_test_execution_url()}, self.__metric.url())


class FakeJira(object):
    """ A fake Jira for testing purposes. """
    metric_source_name = metric_source.Jira.metric_source_name
    needs_metric_source_id = metric_source.Jira.needs_metric_source_id

    @staticmethod
    def manual_test_cases_time():
        """ Return a fake duration of manual tests. """
        return 110

    @staticmethod
    def manual_test_cases_url():
        """ Return the url for the manual test case query. """
        return 'http://jira'

    @staticmethod
    def nr_manual_test_cases():
        """ Return the number of manual test cases. """
        return 5

    @staticmethod
    def nr_manual_test_cases_not_measured():
        """ Return the number of manual test cases whose duration hasn't been measured. """
        return 2


class DurationOfManualLogicalTestCasesTest(unittest.TestCase):
    """ Unit tests for the DurationOfManualLogicalTestCases metric. """
    def setUp(self):
        self.__jira = FakeJira()
        self.__project = domain.Project(metric_sources={metric_source.Jira: self.__jira})
        self.__metric = metric.DurationOfManualLogicalTestCases(subject=self.__project, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the duration of the manual logical test cases. """
        self.assertEqual(110, self.__metric.value())

    def test_report(self):
        """ Test the metric report. """
        self.assertEqual('De uitvoering van 3 van de 5 handmatige logische testgevallen kost 110 minuten.',
                         self.__metric.report())

    def test_report_without_jira(self):
        """ Test the metric report when no Jira has been configured. """
        self.assertEqual('De uitvoeringstijd van handmatige logische testgevallen van <no name> kon niet gemeten '
                         'worden omdat de bron Jira niet is geconfigureerd.',
                         metric.DurationOfManualLogicalTestCases(domain.Project(), domain.Project()).report())

    def test_norm(self):
        """ Test the norm text. """
        self.assertEqual('De uitvoering van de handmatige logische testgevallen kost maximaal 120 minuten. '
                         'Meer dan 240 is rood.', self.__metric.norm())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({FakeJira.metric_source_name: FakeJira.manual_test_cases_url()}, self.__metric.url())


class ManualLogicalTestCasesWithoutDurationTest(unittest.TestCase):
    """ Unit tests for the ManualLogicalTestCasesMeasured metric. """
    def setUp(self):
        self.__jira = FakeJira()
        self.__project = domain.Project(metric_sources={metric_source.Jira: self.__jira})
        self.__metric = metric.ManualLogicalTestCasesWithoutDuration(subject=self.__project, project=self.__project)

    def test_value(self):
        """ Test that the value of the metric is the number of logical test cases not measured for duration. """
        self.assertEqual(2, self.__metric.value())

    def test_report(self):
        """ Test the metric report. """
        self.assertEqual('Van 2 van de 5 handmatige logische testgevallen is de uitvoeringstijd niet ingevuld.',
                         self.__metric.report())

    def test_report_without_jira(self):
        """ Test the metric report when no Jira has been configured. """
        self.assertEqual('De hoeveelheid logische testgevallen zonder ingevulde uitvoeringstijd van <no name> kon niet '
                         'gemeten worden omdat de bron Jira niet is geconfigureerd.',
                         metric.ManualLogicalTestCasesWithoutDuration(domain.Project(), domain.Project()).report())

    def test_norm(self):
        """ Test the norm text. """
        self.assertEqual('Van alle handmatige logische testgevallen is de uitvoeringstijd ingevuld. '
                         'Meer dan 5 handmatige logische testgevallen niet ingevuld is rood.',
                         self.__metric.norm())

    def test_url(self):
        """ Test the url is correct. """
        self.assertEqual({FakeJira.metric_source_name: FakeJira.manual_test_cases_url()}, self.__metric.url())
