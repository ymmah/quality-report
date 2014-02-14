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

from argparse import ArgumentParser


def parse():
    ''' Parse the command line arguments. '''
    parser = ArgumentParser(description='Generate a quality report.')
    parser.add_argument('--project',
                        help='definition file of the project to report on')
    parser.add_argument('--html',
                        help='write HTML report to the given HTML file')
    parser.add_argument('--json',
                        help='append metrics data to the given JSON file')
    parser.add_argument('--dot',
                        help='write product dependency graph to the given '
                             'dot file')
    parser.add_argument('--log', default="WARNING",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL'],
                        help="log level (WARNING by default)")
    args = parser.parse_args()
    if not args.project:
        parser.error('Need a project definition file.')
    if not args.html and not args.json and not args.dot:
        parser.error('Need at least one of --html, --json, and --dot')
    return args
