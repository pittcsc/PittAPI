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
import urllib.parse
import pprint
import json

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

    course_ids = []
    for book_info in courses_info:
        course_ids.append(get_course_id(book_info['department_code'], book_info['course_name'], book_info['instructor']))  # create list of course ids

    book_url = 'http://pitt.verbacompare.com/comparison?id='
    if (len(course_ids) > 1):
        for course_id in course_ids:
             book_url += course_id + '%2C'  # format url for multiple classes
    else:
        book_url += course_ids[0]  # just one course
    
    book_data = session.get(book_url).text
    start = book_data.find('Verba.Compare.Collections.Sections') + len('Verba.Compare.Collections.Sections') + 1
    end = book_data.find('}]}]);') + 4
    info = [json.loads(book_data[start:end])]
    books_list = []
    for i in range(len(info[0])):
        book_dict = {}
        big_dict = info[0][i]['books'][0]
        book_dict['isbn'] = big_dict['isbn']
        book_dict['citation'] = big_dict['citation']
        book_dict['title'] = big_dict['title']
        book_dict['edition'] = big_dict['edition']
        book_dict['author'] = big_dict['author']
        books_list.append(book_dict)
    return books_list  # return list of dicts of books

def get_course_id(department_code, course_name, instructor, term='2600'):  # 2600 --> spring 2017
    department_number = CODES.index(department_code) + 22399
    if department_number > 22462:
        department_number += 2  # between codes DSANE and EAS 2 id numbers are skipped.
    url = 'http://pitt.verbacompare.com/compare/courses/' + '?id=' + str(department_number) + '&term_id=' + term
    #print(url)
    r = session.get(url)
    json_data = r.json()
    sections = []
    course_id = ''
    #print(json_data)
    for course_dict in (json_data):
        if course_dict['id'] == course_name:
            sections = course_dict['sections']
            break
    for section in sections:
        if section['instructor'] == instructor:
            course_id = section['id']
            break
    return course_id

print(get_books_data([{'department_code': 'CS', 'course_name': 'CS0401', 'instructor': 'HOFFMAN'}, {'department_code': 'CS', 'course_name': 'CS0445', 'instructor': 'GARRISON III'}]))  # testing
