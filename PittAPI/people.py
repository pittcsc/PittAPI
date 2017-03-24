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

import urllib.parse

import grequests

PEOPLE_URL = "https://m.pitt.edu/people/search.json"
DETAIL_URL = "https://m.pitt.edu/people/detail.json"


def get_person(query, max_people=10):
    """ """
    url_list = [item for l_list in _get_person_url(query, max_people) for item in l_list]
    results = [_get_person_details(url) for url in url_list]
    people_info = [resp.json()["response"] for resp in grequests.map(results)]
    persons = [_extract_person(person) for person in people_info]

    return persons[:max_people]


def _extract_person(item):
    """ """
    person = {
        'name': item["fields"]["title"],
        'fields': {}
    }

    for tree in item["regions"][1]["contents"]:
        tree = tree["regions"][0]["contents"][0]["fields"]
        person["fields"].update({tree["label"]: tree['title']})

    return person


def _get_person_details(url):
    """ """
    payload = {
        "id": url,
        "_object": "kgoui_Rcontent_I0_Rcontent_I1",
        "_object_include_html": 1
    }
    payload_str = "&".join("{}={}".format(k, v) for k, v in payload.items())
    return grequests.get(DETAIL_URL, params=payload_str)


def _get_person_url(query, max_people):
    """ """
    query = query.replace(' ', '+')
    request_objs = []

    for i in range(int(max_people / 10)):
        payload = {
            "search": "Search",
            "filter": query,
            "_region": "kgoui_Rcontent_I0_Rcontent_I0_Ritems",
            "_object_include_html": 1,
            "_object_js_config": 1,
            "_kgoui_page_state": "8c6ef035807a2a969576d6d78d211c78",
            "_region_index_offset": i * 10,
            "feed": "directory",
            "start": i * 10
        }
        request_objs.append(grequests.get(PEOPLE_URL, params=payload))

    responses = grequests.imap(request_objs)

    url_list = []
    for response_obj in responses:
        response = response_obj.json()['response']['contents']
        local_url_list = (x['fields']['url']['formatted'] for x in response)
        local_url_list = (x.replace('\\', '').split('&')[-1].replace('id=', '')
                          for x in local_url_list if '&start' not in x)
        local_url_list = (urllib.parse.unquote(x) for x in local_url_list)
        url_list.append(local_url_list)

    return url_list
