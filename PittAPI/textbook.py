"""
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
"""
import json
import warnings

import grequests
import requests
from bs4 import BeautifulSoup

session = requests.session()

CODES = [
    'ADMJ','ADMPS','AFRCNA','AFROTC','ANTH','ARABIC','ARTSC','ASL','ASTRON','ATHLTR','BACC','BCHS','BECN','BFIN','BHRM','BIND',
    'BIOENG','BIOETH','BIOINF','BIOSC','BIOST','BMIS','BMKT','BOAH','BORG','BQOM','BSEO','BSPP','BUS','BUSACC','BUSADM','BUSBIS',
    'BUSECN','BUSENV','BUSERV','BUSFIN','BUSHRM','BUSMKT','BUSORG','BUSQOM','BUSSCM','BUSSPP','CDACCT','CDENT','CEE','CGS','CHE',
    'CHEM','CHIN','CLASS','CLRES','CLST','CMMUSIC','CMPBIO','COE','COEA','COEE','COMMRC','CS','CSD','DENHYG','DENT','DIASCI','DSANE',
    'EAS','ECE','ECON','EDUC','ELI','EM','ENDOD','ENGCMP','ENGFLM','ENGLIT','ENGR','ENGSCI','ENGWRT','ENRES','EOH','EPIDEM','FACDEV',
    'FILMG','FILMST','FP','FR','FTADMA','FTDA','FTDB','FTDC','FTDR','GEOL','GER','GERON','GREEK','GREEKM','GSWS','HAA','HIM','HINDI',
    'HIST','HONORS','HPA','HPM','HPS','HRS','HUGEN','IDM','IE','IL','IMB','INFSCI','INTBP','IRISH','ISB','ISSP','ITAL','JPNSE','JS',
    'KOREAN','LATIN','LAW','LCTL','LDRSHP','LEGLST','LING','LIS','LSAP','MATH','ME','MED','MEDEDU','MEMS','MILS','MOLBPH','MSCBIO',
    'MSCBMP','MSCMP','MSE','MSIMM','MSMBPH','MSMGDB','MSMPHL','MSMVM','MSNBIO','MUSIC','NEURO','NPHS','NROSCI','NUR','NURCNS','NURNM',
    'NURNP','NURSAN','NURSP','NUTR','ODO','OLLI','ORBIOL','ORSUR','OT','PAS','PEDC','PEDENT','PERIO','PERS','PETE','PHARM','PHIL','PHYS',
    'PIA','POLISH','PORT','PROSTH','PS','PSY','PSYC','PSYED','PT','PUBHLT','PUBSRV','REHSCI','REL','RELGST','RESTD','RUSS','SA','SERCRO',
    'SLAV','SLOVAK','SOC','SOCWRK','SPAN','STAT','SWAHIL','SWBEH','SWCOSA','SWE','SWGEN','SWINT','SWRES','SWWEL','TELCOM','THEA','TURKSH',
    'UKRAIN','URBNST','VIET']


# TODO(Alex Z.): Look into instructor names and whether they are useful
# TODO: Possibly make conversion between textbook term numbers and course term numbers
BASE_URL = 'http://pitt.verbacompare.com/'


def _fetch_term_codes():
    """Fetches current valid term codes"""
    try:
        page = requests.get(BASE_URL)
    except ConnectionError:
        return []
    script = BeautifulSoup(page.text, 'lxml').findAll('script')[-2].text
    data = json.loads(script[script.find('['):script.find(']') + 1])
    terms = [item['id'] for item in data]
    return terms


TERMS = _fetch_term_codes()


def _validate_term(term):
    """Validates term is a string and check if it is valid."""
    if len(TERMS) == 0:
        warnings.warn('Wasn\'t able to validate term. Assuming term code is valid.')
        return term
    if term in TERMS:
        return term
    raise ValueError("Invalid term")


def get_books_data(courses_info):
    """Returns list of dictionaries of book information."""
    request_objs = []
    course_names = []  # need to save these
    instructors = []  # need to save these

    # TODO(Alex Z.): Validation that argument is a list, add warning and correction is not or raise exception

    print(courses_info)
    for course in courses_info:
        book_info = course
        # TODO(Alex Z.): Check what information is actually needed
        course_names.append(book_info['course_name'])
        instructors.append(book_info['instructor'])
        request_objs.append(
            grequests.get(_get_department_url(book_info['department_code'], book_info['term']), timeout=10)
        )
    responses = grequests.map(request_objs)  # parallel requests

    course_ids = _extract_course_ids(responses, course_names, instructors)
    book_data = session.get(_construct_url(course_ids)).text

    return _extract_books(book_data)  # return list of dicts of books


def _construct_url(ids):
    return BASE_URL + 'comparison?id=' + '%2C'.join(ids)


def _extract_course_ids(responses, course_names, instructors):
    ids = []

    # counter to get course_names and instructors
    for j, r in enumerate(responses):
        sections = []
        course_id = ''

        for course_dict in r.json():
            if course_dict['id'] == course_names[j]:
                sections = course_dict['sections']
                break

        for section in sections:
            if section['instructor'] == instructors[j]:
                course_id = section['id']
                break

        ids.append(course_id)
    return ids


def _extract_books(data):
    books, keys = [], ['isbn', 'citation', 'title', 'edition', 'author']

    # TODO(Alex Z.): Added check for invalid response that return an empty json list
    start = data.find('Verba.Compare.Collections.Sections') + len('Verba.Compare.Collections.Sections') + 1
    end = data.find('}]}]);') + 4
    info = [json.loads(data[start:end])]

    for i in range(len(info[0])):
        for j in range(len(info[0][i]['books'])):
            data = info[0][i]['books'][j]
            books.append(
                _filter_dictionary(data, keys)
            )

    return books


def _filter_dictionary(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def _get_department_url(department_code, term):
    """Returns url for given department code."""
    # TODO(Alex Z.): Fix statements below to something more concrete then using static list of codes
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    if department_number > 22580:
        department_number += 1  # between codes PUBSRV and REHSCI 1 id number is skipped.
    query = 'compare/courses/?id={}&term_id={}'.format(department_number, _validate_term(term))
    return BASE_URL + query
