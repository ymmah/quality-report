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


from ..metric_source_mixin import BirtTestDesignMetric
from ...domain import LowerIsBetterMetric
from hqlib.typing import MetricParameters


class UserStoryMetric(BirtTestDesignMetric, LowerIsBetterMetric):
    """ Base class for metrics measuring the quality of user stories. """
    unit = 'user stories'

    def value(self):
        nr_user_stories, nr_user_stories_ok = self._nr_user_stories(), self._nr_user_stories_ok()
        if -1 in [nr_user_stories, nr_user_stories_ok] or None in [nr_user_stories, nr_user_stories_ok]:
            return -1
        else:
            return nr_user_stories - nr_user_stories_ok

    def _nr_user_stories_ok(self) -> int:
        """ Return the number of user stories whose quality is good. """
        raise NotImplementedError

    def _nr_user_stories(self) -> int:
        """ Return the total number of user stories. """
        return self._metric_source.nr_user_stories()

    def _parameters(self) -> MetricParameters:
        # pylint: disable=protected-access
        parameters = super()._parameters()
        parameters['total'] = self._nr_user_stories()
        return parameters


class UserStoriesNotReviewed(UserStoryMetric):
    """ Metric for measuring the percentage of user stories that not have been reviewed. """

    name = 'Reviewstatus van user stories'
    norm_template = 'Maximaal {target} van de {unit} is niet gereviewd. Meer dan {low_target} is rood.'
    template = '{name} heeft {value} niet gereviewde {unit} van in totaal {total} {unit}.'
    target_value = 0
    low_target_value = 5

    def _nr_user_stories_ok(self) -> int:
        return self._metric_source.reviewed_user_stories()


class UserStoriesNotApproved(UserStoryMetric):
    """ Metric for measuring the number of user stories that not have been approved. """

    name = 'Goedgekeuring van user stories'
    norm_template = 'Maximaal {target} van de gereviewde {unit} is niet goedgekeurd. Meer dan {low_target} is rood.'
    template = '{name} heeft {value} niet goedgekeurde {unit} van in totaal {total} gereviewde {unit}.'
    target_value = 0
    low_target_value = 3

    def _nr_user_stories_ok(self) -> int:
        return self._metric_source.approved_user_stories()

    def _nr_user_stories(self) -> int:
        """ Override the total number of user stories. """
        return self._metric_source.reviewed_user_stories()


class UserStoriesWithTooFewLogicalTestCases(UserStoryMetric):
    """ Metric for measuring the number of user stories that has too few logical test cases. """

    name = 'Hoeveelheid logische testgevallen per user story'
    norm_template = 'Maximaal {target} van de {unit} heeft onvoldoende logische testgevallen. ' \
        'Meer dan {low_target} is rood.'
    template = '{name} heeft {value} {unit} met een onvoldoende aantal logische testgevallen van ' \
        'in totaal {total} {unit}.'
    target_value = 3
    low_target_value = 5

    def _nr_user_stories_ok(self) -> int:
        return self._metric_source.nr_user_stories_with_sufficient_ltcs()
