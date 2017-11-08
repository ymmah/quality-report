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


from ... import metric_source
from ...domain import LowerIsBetterMetric


class OpenBugs(LowerIsBetterMetric):
    """ Metric for measuring the number of open bug reports. """

    name = 'Hoeveelheid open bugreports'
    unit = 'open bugreports'
    norm_template = 'Het aantal {unit} is minder dan {target}. Meer dan {low_target} {unit} is rood.'
    template = 'Het aantal {unit} is {value}.'
    target_value = 50
    low_target_value = 100
    metric_source_class = metric_source.BugTracker

    def value(self):
        return self._metric_source.nr_issues(*self._get_metric_source_ids()) if self._metric_source else -1


class OpenSecurityBugs(OpenBugs):
    """ Metric for measuring the number of open security bugs. """

    name = 'Hoeveelheid open beveiligingsbugreports'
    unit = 'open beveiligingsbugreports'
    target_value = 0
    low_target_value = 3
    metric_source_class = metric_source.SecurityBugTracker


class OpenStaticSecurityAnalysisBugs(OpenSecurityBugs):
    """ Metric for measuring the number of open static security analysis bugs. """

    name = 'Hoeveelheid open beveiligingsbugreports uit statische security analyse'
    unit = 'open beveiligingsbugreports uit statische security analyse'
    metric_source_class = metric_source.StaticSecurityBugTracker


class OpenFindings(OpenBugs):
    """ Metric for open findings in different test environments. """

    name = 'Hoeveelheid open bevindingen'
    unit = 'open blokkerende bevindingen'
    target_value = 0
    low_target_value = 0
    metric_source_class = metric_source.FindingTracker


class TechnicalDebtIssues(OpenBugs):
    """ Metric for measuring the number of technical debt issues. """

    name = 'Hoeveelheid technische schuld issues'
    unit = 'technische schuld issues'
    target_value = 10
    low_target_value = 50
    metric_source_class = metric_source.TechnicalDebtTracker
