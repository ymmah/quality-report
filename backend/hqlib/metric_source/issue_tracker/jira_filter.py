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


from hqlib.metric_source import IssueTracker


class JiraFilter(IssueTracker):
    """ Metric source for Jira filters. The metric source id is the filter id. """
    def __init__(self, url: str, username: str, password: str, jira=None) -> None:
        from hqlib.metric_source import Jira  # Import here to prevent circular import
        self.__jira = jira or Jira(url, username, password)
        super().__init__()

    def nr_issues(self, *filter_ids: str) -> int:
        """ Return the number of issues in the filter. """
        results = [self.__jira.query_total(int(filter_id)) for filter_id in filter_ids]
        return -1 if -1 in results else sum(results)
