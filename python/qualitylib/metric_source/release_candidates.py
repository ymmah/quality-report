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

from qualitylib.metric_source import url_opener
from qualitylib import utils


class ReleaseCandidates(url_opener.UrlOpener):
    # pylint: disable=incomplete-protocol
    ''' Class representing the file with release candidate version numbers. '''
    
    def __init__(self, url):
        super(ReleaseCandidates, self).__init__()
        self.__url = url
        
    def url(self):
        ''' Return the url of the release candidates file. '''
        return self.__url
        
    def __getitem__(self, product):
        buildnr_prefix = 'buildnr_'
        for line in self.__rc_file_contents():
            if not line.startswith(buildnr_prefix):
                continue
            line = line[len(buildnr_prefix):].lower().strip()
            if line.startswith(product):
                return line.split('=')[1]
        return ''

    @utils.memoized
    def __rc_file_contents(self):
        ''' Return the lines in the release candidates file. '''
        return self.url_open(self.__url).readlines() if self.__url else []
