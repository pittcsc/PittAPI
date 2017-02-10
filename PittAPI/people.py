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
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def get_person(query, max_people=10):

    query = query.replace(' ', '+')
    url_list = []

    for i in range(int(math.ceil(max_people/10.0))):

        url = "https://136.142.34.69/people/search?search=Search&filter={}&_region=kgoui_Rcontent_I0_Rcontent_I0_Ritems"
        url += '&_region_index_offset=' + str(i*10) + '&feed=directory&start=' + str(i*10)
        cmd = 'curl -k -s ' + '"' + url + '"'

        cmd = cmd.format(query)
        response = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        if not response:
            break

        while ("formatted" in response):
            response = response[response.index('"formatted"'):]
            response = response[response.index(":") + 2:]
            response_str = response[:response.index('}') - 1]
            response_str = response_str.replace('\\u0026', '&')
            response_str = response_str.replace('\\', '')
            if '&start=' not in response_str:
                url_list.append("https://136.142.34.69" + response_str)

            response = response[response.index('}'):]
    results = [grequests.get(u, verify=False) for u in url_list]
    people_info = grequests.imap(results)   # make requests
    persons_list = []
    for person in people_info:
        person_dict = {}
        soup = BeautifulSoup(person.text, 'html.parser')
        name = soup.find('h1', attrs={'class': 'kgoui_detail_title'})
        person_dict['name'] = str(name.get_text())
        for item in soup.find_all('div', attrs={'class': 'kgoui_list_item_textblock'}):
            if item is not None:
                person_dict[str(item.div.get_text())] = str(item.span.get_text())
        persons_list.append(person_dict)
        if len(persons_list) >= max_people:
            return persons_list   # only return up to amount specified
    return persons_list
