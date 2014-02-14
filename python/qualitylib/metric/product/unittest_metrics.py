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

from qualitylib.domain import HigherIsBetterMetric, LowerIsBetterMetric
from qualitylib.metric.metric_source_mixin import SonarDashboardMetricMixin
from qualitylib.metric.quality_attributes import TEST_COVERAGE, TEST_QUALITY
    
    
class FailingUnittests(SonarDashboardMetricMixin, LowerIsBetterMetric):
    # pylint: disable=too-many-public-methods
    ''' Metric for measuring the number of unit tests that fail. '''
    
    norm_template = 'Alle unittests slagen.'
    perfect_template = '%(passed_tests)d van de %(tests)d unittests slagen. '
    template = '%(value)d van de %(tests)d unittests falen.'
    target_value = 0
    low_target_value = 0
    quality_attribute = TEST_QUALITY

    def value(self):
        return self._sonar.failing_unittests(self._sonar_id())
    
    def _get_template(self):
        # pylint: disable=protected-access
        return self.perfect_template if self._is_perfect() else \
            super(FailingUnittests, self)._get_template()

    def _parameters(self):
        # pylint: disable=protected-access
        parameters = super(FailingUnittests, self)._parameters()
        nr_unittests = self._sonar.unittests(self._sonar_id())
        parameters['tests'] = nr_unittests
        parameters['passed_tests'] = nr_unittests - self.value()
        return parameters
    
    def _sonar_id(self):
        return self._subject.unittests()

    
class UnittestCoverage(SonarDashboardMetricMixin, HigherIsBetterMetric):
    # pylint: disable=too-many-public-methods
    ''' Metric for measuring the coverage of unittests for a product. '''

    norm_template = 'Minimaal %(target)d%% van de regels code wordt gedekt ' \
        'door unittests. Lager dan %(low_target)d%% is rood.'
    template = '%(name)s unittest coverage is %(value)d%% (%(tests)d ' \
        'unittests).'
    perfect_value = 100
    target_value = 98
    low_target_value = 90
    quality_attribute = TEST_COVERAGE

    def value(self):
        return round(self._sonar.line_coverage(self._sonar_id()))

    def _sonar_id(self):
        return self._subject.unittests()

    def _parameters(self):
        # pylint: disable=protected-access
        parameters = super(UnittestCoverage, self)._parameters()
        parameters['tests'] = self._sonar.unittests(self._sonar_id())
        return parameters
