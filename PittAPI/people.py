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

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.session()


def get_person(query, max_people=10):
    '''
    Doesn't work completely for now. IT WORKS
    Returns a dict with URLs of user profiles. No scraping yet.
    '''

    query = query.replace(' ', '+')
    persons_list = []
    tens = 0
    while tens < max_people:
        url = "https://136.142.34.69/people/search?search=Search&filter={}&_region=kgoui_Rcontent_I0_Rcontent_I0_Ritems"
        url += '&_region_index_offset=' + str(tens) + '&feed=directory&start=' + str(tens)
        cmd = 'curl -k -s ' + '"' + url + '"'

        cmd = cmd.format(query)
        response = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        if not response:  # no more responses, so break
            break

        results = []
        while ("formatted" in response):
            response = response[response.index('"formatted"'):]
            response = response[response.index(":") + 2:]
            response_str = response[:response.index('}') - 1]
            response_str = response_str.replace('\\u0026', '&')
            response_str = response_str.replace('\\', '')
            if '&start=' not in response_str:
                results.append("https://136.142.34.69" + response_str)

            response = response[response.index('}'):]

        for url in results:
            # results is url
            personurl = str(''.join(url))

            if personurl.lower().startswith("https://"):
                f = session.get(personurl, verify=False)
            else:
                f = session.get(personurl)

            person_dict = {}
            soup = BeautifulSoup(f.text, 'html.parser')
            name = soup.find('h1', attrs={'class': 'kgoui_detail_title'})
            person_dict['name'] = str(name.get_text())
            for item in soup.find_all('div', attrs={'class': 'kgoui_list_item_textblock'}):
                if item is not None:
                    person_dict[str(item.div.get_text())] = str(item.span.get_text())
            persons_list.append(person_dict)
        tens += 10
    return persons_list
