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

from qualitylib import domain
from unittests.domain.measurement.fake import FakeWiki, FakeHistory, \
    FakeSubject
import unittest   


class DummyMetric(domain.Metric):
    # pylint: disable=too-many-public-methods,W0223
    ''' Override to implement abstract methods that are needed for running 
        the unit tests. '''
    def value(self):
        return 0


class MetaMetricUnderTest(domain.MetaMetricMixin, 
                          domain.HigherPercentageIsBetterMetric):
    # pylint: disable=too-many-public-methods
    ''' Use MetaMetricMixin to create a concrete meta metric that can be 
        tested. '''
    pass


class MetaMetricMixinTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Test case for meta metric mixin class. '''
        
    def setUp(self):  # pylint: disable=invalid-name
        subject = [DummyMetric(FakeSubject(), wiki=FakeWiki(), 
                               history=FakeHistory())]
        self._metric = MetaMetricUnderTest(subject, wiki=FakeWiki(), 
                                           history=FakeHistory())
        
    def test_value(self):
        ''' Test  the value of the metric. '''
        self.assertEqual(0, self._metric.value())
