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

import unittest

from hqlib.formatting import MetricSourcesFormatter, MetricClassesFormatter, SectionsFormatter, \
    SectionNavigationMenuFormatter
from . import fake_report


class SectionsFormatterTest(unittest.TestCase):
    """ Unit tests for the sections HTML formatter. """
    def setUp(self):
        self.__report = fake_report.Report()

    def test_sections(self):
        """ Test the sections. """
        self.assertEqual('''<div id="section_dashboard">
  <br />
  <table class="table table-condensed table-bordered">
    <thead>
      <tr style="color: white; font-weight: bold; background-color: #2F95CF;">
        <th colspan="1" style="text-align: center;">ME</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="1" rowspan="1" align="center" bgcolor="lightsteelblue">
          <div class="link_section_ID" title="Section title"></div>
          <div id="section_summary_chart_ID"></div>
        </td>
      </tr>
    </tbody>
  </table>
</div>
<section id="section_all" style="display:none">
  <div id="table_all"></div>
</section>
<section id="section_id">
  <br />
  <div class="page-header">
    <h1>Section title <small>Section subtitle</small></h1>
  </div>
  <div id="table_id"></div>
</section>''', SectionsFormatter.process(self.__report))


class SectionNaviationMenuFormatterTest(unittest.TestCase):
    """ Unit tests for the section navigation menu HTML formatter. """
    def setUp(self):
        self.__report = fake_report.Report()

    def test_menu(self):
        """ Test the menu items. """
        self.assertEqual('<li><a class="link_section_id" href="#section_id">Section title</a></li>',
                         SectionNavigationMenuFormatter.process(self.__report))


class MetaDataFormatterTest(unittest.TestCase):
    """ Unit tests for the meta data HTML formatters. """
    def setUp(self):
        self.__report = fake_report.Report()

    def test_metric_classes(self):
        """ Test the metric classes table. """
        self.assertEqual('''<table class="table table-striped first-col-centered">
  <tr>
    <th>In dit rapport?</th>
    <th>Metriek (<code><small>Identifier</small></code>)</th>
    <th>Norm</th>
  </tr>
  <tr>
    <td></td>
    <td>Automatic regression test statement coverage (<code><small>ARTStatementCoverage</small></code>)</td>
    <td>Minimaal 80% van de statements wordt gedekt door geautomatiseerde functionele tests. Minder dan 70% is rood.</td>
  </tr>
</table>''', MetricClassesFormatter.process(self.__report))

    def test_metric_sources(self):
        """ Test the metric sources table. """
        self.assertEqual('''<table class="table table-striped first-col-centered">
  <tr>
    <th>In dit rapport?</th>
    <th>Metriekbron (<code><small>Identifier</small></code>)</th>
    <th>Instanties</th>
  </tr>
  <tr>
    <td>
      <span aria-hidden="true" class="glyphicon glyphicon-ok"></span>
    </td>
    <td>Git (<code><small>Git</small></code>)</td>
    <td>
      <a href="http://git/" target="_blank">http://git/</a>
    </td>
  </tr>
</table>''', MetricSourcesFormatter.process(self.__report))
