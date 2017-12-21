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

import grequests
from typing import List, Dict, Iterator, Any

PEOPLE_URL = "https://m.pitt.edu/people/search.json"
DETAIL_URL = "https://m.pitt.edu/people/detail.json"

def get_person(query: str, max_people: int=10) -> List[Dict[str,Any]]:
    """ Returns a list of people """
    id_list = [item for l_list in _get_person_id(query, max_people) for item in l_list]
    results = [_get_person_details(id) for id in id_list]
    people_info = [resp.json() for resp in grequests.map(results)]
    persons = [_extract_person(person) for person in people_info]

    return persons[:max_people]

def _extract_person(item: Dict[str,Any]) -> Dict[str,Any]:
    """ Returns person attributes """
    kgoui_person = item['response']['regions'][0]['contents'][0]['fields'] \
                       ['item']['value']['kgoDeflatedData']['attributes']

    person = {
        'name': ''
    }
    return kgoui_person



def _get_person_details(id_number: str):
    """ Returns unsent request """
    payload = {
        "search": "Search",
        "id": id_number,
        "_kgoui_object": "kgoui_Rcontent_I0_Rcontent_I1",
    }
    payload_str = "&".join("{}={}".format(k, v) for k, v in payload.items())
    return grequests.get(DETAIL_URL, params=payload_str)


def _get_person_id(query: str, max_people: int) -> List[Iterator[str]]:
    """ Returns list of people IDs """
    request_objs = []

    for i in range(int(max_people / 10) + 1):
        payload = {
            "search": "Search",
            "filter": query,
            "_kgoui_region": "kgoui_Rcontent_I0_Rcontent_I0_Ritems",
            "_object_include_html": 1,
            "_object_js_config": 1,
            "_kgoui_page_state": "439a1a9b6fb81b480ade61813e20e049",
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
        local_url_list = (dict(param.split("=") for param in x.split("&"))
                          for x in local_url_list)
        local_url_list = (x['id'] for x in local_url_list if 'id' in x)
        url_list.append(local_url_list)
    return url_list
