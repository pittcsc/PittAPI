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

def get_books_data(courses_info):
    """Returns list of dictionaries of book information."""
    request_objs = []
    course_names = []  # need to save these
    instructors = []  # need to save these
    for i in range(len(courses_info)):
        book_info = courses_info[i]
        print(book_info)
        course_names.append(book_info['course_name'])
        instructors.append(book_info['instructor'])
        request_objs.append(grequests.get(get_department_url(book_info['department_code'], book_info['term']), timeout=10))
    responses = grequests.map(request_objs)  # parallel requests
    course_ids = []

    j = 0  # counter to get course_names and instructors
    for r in responses:
        json_data = r.json()
        sections = []
        course_id = ''
        for course_dict in (json_data):
            if course_dict['id'] == course_names[j]:
                sections = course_dict['sections']
                break
        for section in sections:
            if section['instructor'] == instructors[j]:
                course_id = section['id']
                break
        course_ids.append(course_id)
        j += 1
    book_url = 'http://pitt.verbacompare.com/comparison?id='

    if (len(course_ids) > 1):
        for course_id in course_ids:
             book_url += course_id + '%2C'  # format url for multiple classes
    else:
        book_url += course_ids[0]  # just one course

    book_data = session.get(book_url).text

    try:
        start = book_data.find('Verba.Compare.Collections.Sections') + len('Verba.Compare.Collections.Sections') + 1
        end = book_data.find('}]}]);') + 4
        info = [json.loads(book_data[start:end])]
        books_list = []
        for i in range(len(info[0])):
            for j in range(len(info[0][i]['books'])):
                book_dict = {}
                big_dict = info[0][i]['books'][j]
                book_dict['isbn'] = big_dict['isbn']
                book_dict['citation'] = big_dict['citation']
                book_dict['title'] = big_dict['title']
                book_dict['edition'] = big_dict['edition']
                book_dict['author'] = big_dict['author']
                books_list.append(book_dict)
    except ValueError:
        print('Error while decoding response, try again!')

    return books_list  # return list of dicts of books

def get_department_url(department_code,term='2600'):  # 2600 --> spring 2017
    """Returns url for given department code."""
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    if department_number > 22580:
        department_number += 1  # between codes PUBSRV and REHSCI 1 id number is skipped.
    url = 'http://pitt.verbacompare.com/compare/courses/' + '?id=' + str(department_number) + '&term_id=' + term
    return url
