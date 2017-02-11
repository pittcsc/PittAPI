'''
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

import subprocess
import math
import requests
import grequests

from bs4 import BeautifulSoup, SoupStrainer


requests.packages.urllib3.disable_warnings()
s = requests.Session()


def _get_person_url(query, max_people):
    to_query = []
    for i in range(int(math.ceil(max_people / 10.0))):
        to_query.append('https://m.pitt.edu/people/search.json?search=Search&filter={0}&_region=kgoui_Rcontent_I0_Rcontent_I0_Ritems&_object_include_html=1&_object_js_config=1&_kgoui_page_state=8c6ef035807a2a969576d6d78d211c78&_region_index_offset={1}&feed=directory&start={2}'.format(query, str(i*10), str(i*10)))

    request_objs = [grequests.get(url, session=s) for url in to_query]
    responses = grequests.imap(request_objs)

    url_list = []
    for response_obj in responses:
        response = response_obj.json()['response']['contents']
        local_url_list = [x['fields']['url']['formatted'] for x in response]
        local_url_list = ['https://m.pitt.edu' + x.replace('\\', '') for x in local_url_list if '&start' not in x]
        url_list.append(local_url_list)

    return url_list


def get_person(query, max_people=10):
    query = query.replace(' ', '+')
    url_list = _get_person_url(query, max_people)
    url_list = [item for l_list in url_list for item in l_list]  # flatmap

    results = [grequests.get(url, session=s) for url in url_list]
    people_info = grequests.imap(results)   # make requests
    persons_list = []
    strainer = SoupStrainer('div',
            {'class': lambda x: 'kgoui_detail_header' in x.split() or 'kgoui_list_item_textblock' in x.split()})

    for person in people_info:
        person_dict = {}
        soup = BeautifulSoup(person.text, 'lxml', parse_only=strainer)
        name = soup.find('h1', attrs={'class': 'kgoui_detail_title'})
        person_dict['name'] = str(name.get_text())
        for item in soup.find_all('div', attrs={'class': 'kgoui_list_item_textblock'}):
            if item is not None:
                person_dict[str(item.div.get_text())] = str(item.span.get_text())
        persons_list.append(person_dict)
        if len(persons_list) >= max_people:
            break   # only return up to amount specified

    return persons_list
