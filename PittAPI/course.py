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
import warnings

import requests
import re
from typing import Dict
from bs4 import BeautifulSoup, SoupStrainer, Tag, ResultSet

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


class PittSubject:
    DEFAULT_CAMPUS = 'PIT/PGH'

    def __init__(self, subject: str):
        self.subject = subject
        self.classes = []

    def parse_webpage(self, resp: str):
        soup = BeautifulSoup(resp.text, 'lxml')
        classes = soup.find('div', {'class': 'primary-head'}).parent.contents[1:]
        class_description = ""
        for child in classes:
            if any(child != i for i in ['\n', ' ']):
                if isinstance(child, Tag) and 'class' not in child.attrs:
                    print(child)
                    class_sections_url = child.attrs['href']
                    self._add_class(
                        class_section_url=class_sections_url,
                        class_description=class_description
                    )
                elif isinstance(child, Tag):
                        class_description = child.text

    def _add_class(self, class_section_url, class_description):
        self.classes.append(PittClass(self, self.subject, class_section_url, class_description))


class PittClass:
    def __init__(self, parent: PittSubject, subject_id: str, class_section_url: str, class_description: str):
        self.parent_subject = parent
        self.subject_id = subject_id
        self.class_number, self.description, *_ = class_description.split(' - ')
        url_split = class_section_url.split('/')
        if 'campuses' in class_section_url:
            self.campus_id = self.parent_subject.DEFAULT_CAMPUS
            self.internal_class_number = url_split[-1]
            self.term = url_split[-2]
            self.section_url = SECTION_LIST_URL.format(
                term=self.term,
                class_number=self.class_number,
                campus_id=self.campus_id
            )
        else:
            self.campus_id = '/'.join(url_split[-2:])
            self.internal_class_number = url_split[-3]
            self.term = url_split[-4]
            self.section_url = class_section_url

    def to_dict(self):
        pass

    def retrieve_sections(self):
        pass

    def __repr__(self):
        return '<Pitt Class | {subject} {class_number}>'.format(subject=self.subject_id, class_number=self.class_number)


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
