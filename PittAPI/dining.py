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

import requests
from bs4 import BeautifulSoup, SoupStrainer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.session()
strainer = SoupStrainer('div', attrs={'class': 'kgoui_list_item_textblock'})


def get_dining_locations():
    return get_dining_locations_by_status()


def get_dining_locations_by_status(status=None):
    # status can be nil, open, or closed
    # None     - returns all dining locations
    # 'all'    - same as None (or anything else)
    # 'open'   - returns open dining locations
    # 'closed' - returns closed dining locations

    # sample_url = 'https://m.pitt.edu/dining/index.json?_region=kgoui_Rcontent_I1_Ritems&_object_include_html=1&_object_js_config=1&_kgoui_page_state=eb95bc72eca310cbbe76a39964fc7143&_region_index_offset=15&feed=dining_locations&start=15'
    # the _region_index_offset is optional
    # -- seems like it's only for the id of the li for the html
    dining_locations = {}

    end_loop = False
    load_more = False
    counter = 0
    while not end_loop:
        load_more = False
        url = 'https://m.pitt.edu/dining/index.json?_region=kgoui_Rcontent_I1_Ritems&_object_include_html=1&_object_js_config=1&_kgoui_page_state=eb95bc72eca310cbbe76a39964fc7143&feed=dining_locations&start=' + str(
            counter)
        data = session.get(url).json()
        soup = BeautifulSoup(data['response']['html'], 'lxml', parse_only=strainer)
        res = soup.find_all('div', class_='kgoui_list_item_textblock')

        for i in res:
            if i.find('span').getText() != 'Load more...':
                if i.find('div') is not None:
                    if (('Next:' in i.find('div').getText()) and status != 'open') or (
                        ('Next:' not in i.find('div').getText()) and status != 'closed'):
                        dining_locations[_encode_dining_location(i.find('span').getText())] = {
                            'name': i.find('span').getText(),
                            'hours': i.find('div').getText().replace('\\u2013', '-').replace('\n', '').replace('Next: ',
                                                                                                               ''),
                            'status': 'closed' if 'Next:' in i.find('div').getText() else 'open'
                        }
                        end_loop = True
                elif status != 'open':
                    dining_locations[_encode_dining_location(i.find('span').getText())] = {
                        'name': i.find('span').getText(),
                        'hours': '',
                        'status': 'closed'
                    }
                    end_loop = True
            else:
                counter += 15
                end_loop = False
                load_more = True
        if not load_more:
            end_loop = True

    return dining_locations


def get_dining_location_by_name(location):
    try:
        return get_dining_locations()[_encode_dining_location(location)]
    except:
        raise ValueError('The dining location is invalid')


def get_dining_location_menu(location=None, date=None):
    # location can only be market, market's subordinates, and cathedral cafe
    # if location is none, return all menus, and date will be ignored
    # date has to be a day of the week, or if empty will return menus for all days of the week
    #
    # https://www.pc.pitt.edu/dining/menus/flyingStar.php
    # https://www.pc.pitt.edu/dining/menus/bellaTrattoria.php
    # https://www.pc.pitt.edu/dining/menus/basicKneads.php
    # https://www.pc.pitt.edu/dining/menus/basicKneads.php
    # https://www.pc.pitt.edu/dining/menus/magellans.php
    # https://www.pc.pitt.edu/dining/locations/cathedralCafe.php
    return


def _encode_dining_location(string):
    # changes full name into dict key name
    string = string.lower()
    string = string.replace(' ', '_')
    string = string.replace('_-_', '-')
    string = string.replace('hilman', 'hillman')
    string = string.replace('_library', '')
    string = string.replace('_hall', '')
    string = string.replace('litchfield_', '')
    string = string.replace(u'\xe9', 'e')
    string = string.replace('_science_center', '')
    string = string.replace('_events_center_food_court', '')
    string = string.replace('wesley_w._posvar,_second_floor', 'posvar')
    string = string.replace('_law_building', '')
    return string


def _decode_dining_location(string):
    string = string.replace('_', ' ')
    string = string.replace('-', ' - ')
    string = string.title()
    string = string.replace('\'S', '\'s')
    string = string.replace('Cafe', 'Caf\xe9')
    string = string.replace('Schenley Caf\xe9', 'Schenley Cafe')
    string = string.replace('Hillman', 'Hilman Library')
    string = string.replace('Towers', 'Litchfield Towers')
    string = string.replace('Chevron', 'Chevron Science Center')
    string = string.replace('Barco', 'Barco Law Building')
    string = string.replace('Panther', 'Panther Hall')
    string = string.replace('Sutherland', 'Sutherland Hall')
    string = string.replace('Petersen', 'Petersen Events Center Food Court')
    string = string.replace('Posvar', 'Wesley W. Posvar, Second Floor')
    string = string.replace('Benedum', 'Benedum Hall')
    string = string.replace('Langley', 'Langley Hall')
    string = string.replace('Amos', 'Amos Hall')
    string = string.replace(' At The', ' at the')
    string = string.replace(' And', ' and')
    string = string.replace(' Go', ' GO')
    return string
