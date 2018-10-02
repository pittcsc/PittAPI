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

