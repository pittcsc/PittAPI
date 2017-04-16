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
import requests
import json
import time

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


# TODO: Create function to automatically retrieve valid terms
# TODO: Possibly make conversion between textbook term numbers and course term numbers
TERMS = ['2600', '2671']

URL = 'http://pitt.verbacompare.com/'


def get_books_data(*courses_info):
    """Returns list of dictionaries of book information."""
    request_objs = []
    course_names = []  # need to save these
    instructors = []  # need to save these

    for i in range(len(courses_info)):
        book_info = courses_info[i]
        course_names.append(book_info['course_name'])
        instructors.append(book_info['instructor'])
        request_objs.append(grequests.get(_get_department_url(book_info['department_code'], book_info['term']), timeout=10))
    responses = grequests.map(request_objs)  # parallel requests

    course_ids = _extract_course_ids(responses, course_names, instructors)
    book_data = session.get(_construct_url(course_ids)).text

    keys = ['isbn', 'citation', 'title', 'edition', 'author']
    return _extract_books(book_data, keys)  # return list of dicts of books


def _construct_url(ids):
    url = URL + 'comparison?id='
    if len(ids) > 1:
        for course_id in ids:
            url += course_id + '%2C'  # format url for multiple classes
    else:
        url += ids[0]  # just one course
    return url


def _extract_course_ids(responses, course_names, instructors):
    ids = []

    # counter to get course_names and instructors
    for r, j in zip(responses, range(len(responses))):
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

def _extract_books(data, keys):
    books = []
    try:
        start = data.find('Verba.Compare.Collections.Sections') + len('Verba.Compare.Collections.Sections') + 1
        end = data.find('}]}]);') + 4
        info = [json.loads(data[start:end])]

        for i in range(len(info[0])):
            for j in range(len(info[0][i]['books'])):
                data = info[0][i]['books'][j]
                books.append(_filter_dictionary(data, keys))

    except ValueError as e:
        raise e
    return books


def _filter_dictionary(d, keys):
    return dict((k, d[k]) for k in keys if k in d)


def _get_department_url(department_code,term='2600'):  # 2600 --> spring 2017
    """Returns url for given department code."""
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    if department_number > 22580:
        department_number += 1  # between codes PUBSRV and REHSCI 1 id number is skipped.
    url = 'http://pitt.verbacompare.com/compare/courses/' + '?id=' + str(department_number) + '&term_id=' + term
    return url
