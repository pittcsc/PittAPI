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

from datetime import datetime
import requests
from typing import Dict, Union, List
from bs4 import BeautifulSoup, Tag

SUBJECTS = ['ADMJ', 'ADMPS', 'AFRCNA', 'AFROTC', 'ANTH', 'ARABIC', 'ARTSC', 'ASL', 'ASTRON', 'ATHLTR', 'BACC', 'BCHS',
            'BECN', 'BFAE', 'BFIN', 'BHRM', 'BIND', 'BIOENG', 'BIOETH', 'BIOINF', 'BIOSC', 'BIOST', 'BMIS', 'BMKT',
            'BOAH', 'BORG', 'BQOM', 'BSEO', 'BSPP', 'BUS', 'BUSACC', 'BUSADM', 'BUSBIS', 'BUSECN', 'BUSENV', 'BUSERV',
            'BUSFIN', 'BUSHRM', 'BUSMKT', 'BUSORG', 'BUSQOM', 'BUSSCM', 'BUSSPP', 'CDACCT', 'CDENT', 'CEE', 'CGS',
            'CHE', 'CHEM', 'CHIN', 'CLASS', 'CLRES', 'CLST', 'CMME', 'CMMUSIC', 'CMPBIO', 'CMPINF', 'COE', 'COEA',
            'COEE', 'COMMRC', 'CS', 'CSD', 'DENHYG', 'DENT', 'DIASCI', 'DMED', 'DSANE', 'DUPOSC', 'EAS', 'ECE', 'ECON',
            'EDUC', 'EM', 'ENDOD', 'ENGCMP', 'ENGFLM', 'ENGLIT', 'ENGR', 'ENGSCI', 'ENGWRT', 'ENRES', 'EOH', 'EPIDEM',
            'FACDEV', 'FILMG', 'FILMST', 'FP', 'FR', 'FTADMA', 'FTDA', 'FTDB', 'FTDC', 'FTDJ', 'FTDR', 'GEOL', 'GER',
            'GERON', 'GREEK', 'GREEKM', 'GSWS', 'HAA', 'HEBREW', 'HIM', 'HINDI', 'HIST', 'HONORS', 'HPA', 'HPM', 'HPS',
            'HRS', 'HUGEN', 'IDM', 'IE', 'IL', 'IMB', 'INFSCI', 'INTBP', 'IRISH', 'ISB', 'ISSP', 'ITAL', 'JPNSE', 'JS',
            'KOREAN', 'LATIN', 'LAW', 'LCTL', 'LDRSHP', 'LEGLST', 'LING', 'LIS', 'LSAP', 'MATH', 'ME', 'MED', 'MEDEDU',
            'MEMS', 'MILS', 'MOLBPH', 'MSBMS', 'MSCBIO', 'MSCBMP', 'MSCMP', 'MSE', 'MSMBPH', 'MSMGDB', 'MSMI', 'MSMPHL',
            'MSMVM', 'MSNBIO', 'MUSIC', 'NEURO', 'NPHS', 'NROSCI', 'NUR', 'NURCNS', 'NURNM', 'NURNP', 'NURSAN', 'NURSP',
            'NUTR', 'ODO', 'ORBIOL', 'ORSUR', 'OT', 'PAS', 'PEDC', 'PEDENT', 'PEDS', 'PERIO', 'PERS', 'PETE', 'PHARM',
            'PHIL', 'PHYS', 'PIA', 'POLISH', 'PORT', 'PROSTH', 'PS', 'PSY', 'PSYC', 'PSYED', 'PT', 'PUBHLT', 'PUBSRV',
            'PWEA', 'QUECH', 'REHSCI', 'REL', 'RELGST', 'RESTD', 'RUSS', 'SA', 'SERCRO', 'SLAV', 'SLOVAK', 'SOC',
            'SOCWRK', 'SPAN', 'STAT', 'SWAHIL', 'SWBEH', 'SWCED', 'SWCOSA', 'SWE', 'SWGEN', 'SWINT', 'SWRES', 'SWWEL',
            'TELCOM', 'THEA', 'TURKSH', 'UKRAIN', 'URBNST', 'VIET']

CLASS_SEARCH_URL = 'https://psmobile.pitt.edu/app/catalog/classSearch'
CLASS_SEARCH_API_URL = 'https://psmobile.pitt.edu/app/catalog/getClassSearch'
COURSE_CATALOG_URL = 'https://psmobile.pitt.edu/app/catalog/listCatalog'
CLASS_LIST_URL = 'https://psmobile.pitt.edu/app/catalog/listclasses/{term}/{subject}'
SECTION_LIST_URL = 'https://psmobile.pitt.edu/app/catalog/listsections/UPITT/{term}/{class_number}/{campus_id}'

extract = lambda s: s.split(': ')[1]


class PittSubject:
    def __init__(self, subject: str):
        self.subject = subject
        self.courses = {}

    # def __getitem__(self, item):
    #     if isinstance(item, int) or isinstance(item, slice):
    #         return self.courses[item]

    def parse_webpage(self, resp: str):
        soup = BeautifulSoup(resp.text, 'lxml')
        classes = soup.find('div', {'class': 'primary-head'}).parent.contents
        class_description = ""
        course = None
        for child in classes:
            if any(child != i for i in ['\n', ' ']):
                if isinstance(child, Tag) and 'class' not in child.attrs:
                    class_sections_url = child.attrs['href']
                    self._add_class(
                        class_section_url=class_sections_url,
                        course=course,
                        class_data=child.text.strip().split('\n')
                    )
                elif isinstance(child, Tag):

                    class_description = child.text
                    number, *_ = class_description.split(' - ')
                    number = number.split(' ')[1]
                    if number not in self.courses:
                        self.courses[number] = PittCourse(parent=self, course_number=number, term=2191)

                    course = self.courses[number]

    def _add_class(self, class_section_url, course, class_data):
        self.courses.append(PittSection(self, course, class_section_url, class_data))

    def __repr__(self):
        return '< Pitt Subject | {subject} | {num} classes >'.format(subject=self.subject, num=len(self.classes))


class PittSection:
    def __init__(self, parent: PittSubject, course, class_section_url: str, class_data: List[str]):
        self.parent_subject = parent
        self.parent_course = course

        self.section = extract(class_data[0])
        self.room = extract(class_data[3])
        self.instructor = extract(class_data[4])

        date = extract(class_data[5]).split(' - ')
        self.start_date = datetime.strftime(date[0], '%m/%d/%Y')
        self.end_date = datetime.strftime(date[1], '%m/%d/%Y')

        self.url = class_section_url

    def to_dict(self):
        pass

    def retrieve_sections(self):
        pass

    def __repr__(self):
        return '<Pitt Class | {subject} {course_number} | {class_number}>'.format(subject=self.parent_subject.subject,
                                                                                  course_number=self.parent_course.course_number,
                                                                                  class_number=self.class_number)


class PittCourse:
    def __init__(self, parent: PittSubject, course_number: str, term: Union[int, str]):
        self.parent_subject: PittSubject = parent
        self.number: str = course_number
        self.term: Union[int, str] = term
        self.sections: List[PittSection] = []

    def append(self, section: PittSection):
        self.sections.append(section)

    def __getitem__(self, item):
        return self.sections[item]

    def __repr__(self):
        return ''


def _validate_subject(subject: str) -> str:
    subject = subject.upper()
    if subject in SUBJECTS:
        return subject
    return ''


def _validate_term(term: str) -> bool:
    pass


def get_classes(term: int, subject: str) -> PittSubject:
    """Returns a list of classes available in term."""
    subject = _validate_subject(subject)

    # Generate new CSRFToken
    s = requests.Session()
    s.get(CLASS_SEARCH_URL)

    payload = {
        'CSRFToken': s.cookies['CSRFCookie'],
        'term': term,
        'campus': 'PIT',
        'subject': subject,
        'acad_career': '',
        'catalog_nbr': '',
        'class_nbr': ''
    }

    response = s.post(CLASS_SEARCH_API_URL, data=payload)
    container = PittSubject(subject=subject)
    container.parse_webpage(response)
    return container


def get_sections():
    """Return details on all sections taught in a certain class"""
    pass


def get_class_detail():
    """Returns information pertaining to a certain class."""
    pass


def get_courses(subject: str) -> Dict:
    """Returns a list of all courses offered under a subject."""
    pass
