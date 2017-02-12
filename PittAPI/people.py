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

import math
import requests
import grequests

from bs4 import BeautifulSoup, SoupStrainer


requests.packages.urllib3.disable_warnings()


def _get_person_url(query, max_people):
    request_objs = []
    for i in range(int(math.ceil(max_people / 10.0))):
        payload = {
            "search": "Search",
            "filter": query,
            "_region": "kgoui_Rcontent_I0_Rcontent_I0_Ritems",
            "_object_include_html": 1,
            "_object_js_config": 1,
            "_kgoui_page_state": "8c6ef035807a2a969576d6d78d211c78",
            "_region_index_offset": str(i*10),
            "feed": "directory",
            "start": str(i*10)
        }
        url = "https://m.pitt.edu/people/search.json"
        request_objs.append(grequests.get(url, params=payload))

    responses = grequests.imap(request_objs)

    url_list = []
    for response_obj in responses:
        response = response_obj.json()['response']['contents']
        local_url_list = [x['fields']['url']['formatted'] for x in response]
        local_url_list = [x.replace('\\', '').split('&')[-1].replace('id=', '')
                          for x in local_url_list if '&start' not in x]
        url_list.append(local_url_list)

    return url_list


def get_person(query, max_people=10):
    query = query.replace(' ', '+')
    url_list = _get_person_url(query, max_people)
    url_list = [item for l_list in url_list for item in l_list]  # flatmap

    results = set()
    detail_url = "https://m.pitt.edu/people/detail.json"
    for url in url_list:
        detail_url = "https://m.pitt.edu/people/detail.json?id=" + url + "&_object=kgoui_Rcontent_I0_Rcontent_I1&_object_include_html=1"
        results.add(grequests.get(detail_url))

    people_info = grequests.map(results)   # make requests
    people_info = [resp.json()["response"] for resp in people_info]

    persons_list = []

    for person in people_info:
        person_dict = {}
        name = person["fields"]["title"]
        person_dict["name"] = name
        person_dict["fields"] = []
        for tree in person["regions"][1]["contents"]:
            key = tree["regions"][0]["contents"][0]["fields"]["label"]
            value = tree["regions"][0]["contents"][0]["fields"]["title"]
            person_dict["fields"].append({key: value})

        persons_list.append(person_dict)
        if len(persons_list) >= max_people:
            break   # only return up to amount specified

    return persons_list
