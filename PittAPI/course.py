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
COURSE_CATALOG_URL = 'https://psmobile.pitt.edu/app/catalog/listCatalog'
CLASS_LIST_URL = 'https://psmobile.pitt.edu/app/catalog/listclasses/{term}/{subject}'


def get_classes(term: int, subject: str) -> Dict:
    """Returns a list of classes available in term."""
    pass


def get_class_detail():
    """Returns information pertaining to a certain class."""
    pass


def get_courses(subject: str) -> Dict:
    """Returns a list of all courses offered under a subject."""
    pass
