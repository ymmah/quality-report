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

from typing import Dict, List, Type, Tuple, TYPE_CHECKING

import functools
import logging

from .metric_source import MetricSource
from .measurable import MeasurableObject
from hqlib.typing import MetricParameters, MetricValue, DateTime, Number
if TYPE_CHECKING:  # pragma: no cover
    from ..software_development.project import Project


class Metric(object):
    """ Base class for metrics. """

    name: str = 'Subclass responsibility'
    template: str = 'Subclass responsibility'
    norm_template: str = 'Subclass responsibility'
    unit: str = 'Subclass responsibility'

    target_value: MetricValue = 'Subclass responsibility'
    low_target_value: MetricValue = 'Subclass responsibility'
    perfect_value: MetricValue = 'Subclass responsibility'

    missing_template: str = 'De {metric} van {name} kon niet gemeten worden omdat niet alle benodigde bronnen ' \
                            'beschikbaar zijn.'
    missing_source_template: str = 'De {metric} van {name} kon niet gemeten worden omdat de bron ' \
                                   '{metric_source_class} niet is geconfigureerd.'
    missing_source_id_template: str = 'De {metric} van {name} kon niet gemeten worden omdat niet alle benodigde ' \
                                      'bron-ids zijn geconfigureerd. Configureer ids voor de bron ' \
                                      '{metric_source_class}.'
    perfect_template: str = ''

    url_label_text: str = ''
    comment_url_label_text: str = ''

    metric_source_class: Type[MetricSource] = None

    @classmethod
    def is_applicable(cls, subject: MeasurableObject) -> bool:  # pylint: disable=unused-argument
        """ Return whether this metric applies to the specified subject. """
        return True

    @classmethod
    def norm_template_default_values(cls) -> MetricParameters:
        """ Return the default values for parameters in the norm template. """
        return dict(unit=cls.unit, target=cls.target_value, low_target=cls.low_target_value)

    def __init__(self, subject=None, project: 'Project'=None) -> None:
        self._subject = subject
        self._project = project
        self._metric_source = self._project.metric_source(self.metric_source_class) if self.metric_source_class \
            else None
        if isinstance(self._metric_source, list):
            for source in self._metric_source:
                try:
                    source_id = self._subject.metric_source_id(source)
                except AttributeError:
                    continue
                if source_id:
                    self._metric_source = source
                    self._metric_source_id = source_id
                    break
            else:
                logging.warning("Couldn't find metric source for %s", self.stable_id())
                self._metric_source = None
                self._metric_source_id = None
        else:
            try:
                self._metric_source_id = self._subject.metric_source_id(self._metric_source)
            except AttributeError:
                self._metric_source_id = None
            if self._metric_source and self._metric_source.needs_metric_source_id and not self._metric_source_id:
                self._metric_source = None
        self.__id_string = self.stable_id()
        from hqlib import metric_source
        self.__history = self._project.metric_source(metric_source.History)

    def stable_id(self) -> str:
        """ Return an id that doesn't depend on numbering/order of metrics. """
        stable_id = self.__class__.__name__
        if not isinstance(self._subject, list):
            # Add the product or team to the id:
            stable_id += self._subject.name() if self._subject else str(self._subject)
        return stable_id

    def set_id_string(self, id_string: str) -> None:
        """ Set the identification string. This can be set by a client since the identification of a metric may
            depend on the section the metric is reported in. E.g. A-1. """
        self.__id_string = id_string

    def id_string(self) -> str:
        """ Return the identification string of the metric. """
        return self.__id_string

    def target(self) -> MetricValue:
        """ Return the target value for the metric. If the actual value of the
            metric is below the target value, the metric is not green. """
        subject_target = self._subject.target(self.__class__) if hasattr(self._subject, 'target') else None
        return self.target_value if subject_target is None else subject_target

    def low_target(self) -> MetricValue:
        """ Return the low target value for the metric. If the actual value is below the low target value, the metric
            needs immediate action and its status/color is red. """
        subject_low_target = self._subject.low_target(self.__class__) if hasattr(self._subject, 'low_target') else None
        return self.low_target_value if subject_low_target is None else subject_low_target

    def __technical_debt_target(self):
        """ Return the reduced target due to technical debt for the subject. If the subject has technical debt and
            the actual value of the metric is below the technical debt target, the metric is red, else it is grey. """
        try:
            return self._subject.technical_debt_target(self.__class__)
        except AttributeError:
            return None

    @functools.lru_cache(maxsize=8*1024)
    def status(self) -> str:
        """ Return the status/color of the metric. """
        for status_string, has_status in [('missing_source', self.__missing_source_configuration),
                                          ('missing', self._missing),
                                          ('grey', self.__has_accepted_technical_debt),
                                          ('red', self._needs_immediate_action),
                                          ('yellow', self._is_below_target),
                                          ('perfect', self.__is_perfect)]:
            if has_status():
                return status_string
        return 'green'

    def status_start_date(self) -> DateTime:
        """ Return since when the metric has the current status. """
        return self.__history.status_start_date(self.stable_id(), self.status())

    def __has_accepted_technical_debt(self) -> bool:
        """ Return whether the metric is below target but above the accepted technical debt level. """
        technical_debt_target = self.__technical_debt_target()
        if technical_debt_target:
            return self._is_below_target() and self._is_value_better_than(technical_debt_target.target_value())
        else:
            return False

    def _missing(self) -> bool:
        """ Return whether the metric source is missing. """
        return self.value() == -1

    def __missing_source_configuration(self) -> bool:
        """ Return whether the metric sources have been completely configured. """
        return self.__missing_source_class() or self.__missing_source_ids()

    def __missing_source_class(self) -> bool:
        """ Return whether the metric source class that needs to be configured for the metric to be measurable is
            available from the project. """
        return not self._project.metric_source(self.metric_source_class) if self.metric_source_class else False

    def __missing_source_ids(self) -> bool:
        """ Return whether the metric source ids have been configured for the metric source class. """
        return bool(self.metric_source_class) and self.metric_source_class.needs_metric_source_id and \
            not self._subject.metric_source_id(self._project.metric_source(self.metric_source_class))

    def _needs_immediate_action(self) -> bool:
        """ Return whether the metric needs immediate action, i.e. its actual value is below its low target value. """
        return not self._is_value_better_than(self.low_target())

    def _is_below_target(self) -> bool:
        """ Return whether the actual value of the metric is below its target value. """
        return not self._is_value_better_than(self.target())

    def __is_perfect(self) -> bool:
        """ Return whether the actual value of the metric equals its perfect value,
            i.e. no further improvement is possible. """
        return self.value() == self.perfect_value

    def value(self) -> MetricValue:
        """ Return the actual value of the metric. """
        raise NotImplementedError

    def _is_value_better_than(self, target: MetricValue) -> bool:
        """ Return whether the actual value of the metric is better than the specified target value. """
        raise NotImplementedError

    def report(self, max_subject_length: int=200) -> str:
        """ Return the actual value of the metric in the form of a short, mostly one sentence, report. """
        name = self.__subject_name()
        if len(name) > max_subject_length:
            name = name[:max_subject_length] + '...'
        logging.info('Reporting %s on %s', self.__class__.__name__, name)
        return self._get_template().format(**self._parameters())

    def _get_template(self) -> str:
        """ Return the template for the metric report. """
        if self.__missing_source_class():
            return self.missing_source_template
        if self.__missing_source_ids():
            return self.missing_source_id_template
        elif self._missing():
            return self.missing_template
        elif self.__is_perfect() and self.perfect_template:
            return self.perfect_template
        else:
            return self.template

    def _parameters(self) -> MetricParameters:
        """ Return the parameters for the metric report template and for the metric norm template. """
        return dict(name=self.__subject_name(),
                    metric=self.name[0].lower()+self.name[1:],
                    unit=self.unit,
                    target=self.target(),
                    low_target=self.low_target(),
                    value=self.value(),
                    metric_source_class=self.metric_source_class.__name__ if self.metric_source_class
                    else '<metric has no metric source defined>')

    def norm(self) -> str:
        """ Return a description of the norm for the metric. """
        try:
            return self.norm_template.format(**self._parameters())
        except KeyError:
            logging.error('Key missing in parameters of %s: %s', self.__class__.__name__, self._parameters())
            raise

    def url(self) -> Dict[str, str]:
        """ Return a dictionary of urls for the metric. The key is the anchor, the value the url. """
        label = self._metric_source.metric_source_name if self._metric_source else 'Unknown metric source'
        urls = [url for url in self._metric_source_urls() if url]  # Weed out urls that are empty or None
        if len(urls) == 1:
            return {label: urls[0]}
        else:
            return {'{label} ({index}/{count})'.format(label=label, index=index, count=len(urls)): url
                    for index, url in enumerate(urls, start=1)}

    def _metric_source_urls(self) -> List[str]:
        """ Return a list of metric source urls to be used to create the url dict. """
        if self._metric_source:
            if self._metric_source.needs_metric_source_id:
                return self._metric_source.metric_source_urls(*self._get_metric_source_ids())
            else:
                return [self._metric_source.url()]
        else:
            return []

    def _get_metric_source_ids(self) -> List[str]:
        """ Allow for subclasses to override what the metric source id is. """
        ids = self._metric_source_id if isinstance(self._metric_source_id, list) else [self._metric_source_id]
        return [id_ for id_ in ids if id_]

    def comment(self) -> str:
        """ Return a comment on the metric. The comment is retrieved from either the technical debt or the subject. """
        comments = [comment for comment in (self.__technical_debt_comment(), self.__subject_comment()) if comment]
        return ' '.join(comments)

    def __subject_comment(self) -> str:
        """ Return the comment of the subject about this metric, if any. """
        try:
            return self._subject.metric_options(self.__class__)['comment']
        except (AttributeError, TypeError, KeyError):
            return ''

    def __technical_debt_comment(self) -> str:
        """ Return the comment of the accepted technical debt, if any. """
        td_target = self.__technical_debt_target()
        return td_target.explanation(self.unit) if td_target else ''

    def comment_urls(self) -> Dict[str, str]:  # pylint: disable=no-self-use
        """ Return the source for the comment on the metric. """
        return dict()

    def recent_history(self) -> List[int]:
        """ Return a list of recent values of the metric, to be used in e.g. a spark line graph. """
        history = self.__history.recent_history(self.stable_id()) or []
        return [int(round(float(value))) for value in history]

    def y_axis_range(self) -> Tuple[int, int]:
        """ Return a two-tuple (min, max) for use in graphs. """
        history = self.recent_history()
        if not history:
            return 0, 100
        minimum, maximum = min(history), max(history)
        return (minimum - 1, maximum + 1) if minimum == maximum else (minimum, maximum)

    def numerical_value(self) -> Number:
        """ Return a numerical version of the metric value for use in graphs. By default this simply returns the
            regular value, assuming it is already numerical. Metrics that don't have a numerical value by default
            can override this method to convert the non-numerical value into a numerical value. """
        value = self.value()
        if isinstance(value, (int, float)):
            return value
        else:
            raise NotImplementedError

    def __subject_name(self) -> str:
        """ Return the subject name, or a string representation if the subject has no name. """
        try:
            return self._subject.name()
        except AttributeError:
            return str(self._subject)
