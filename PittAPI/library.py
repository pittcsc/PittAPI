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

import requests
from html.parser import HTMLParser

LIBRARY_URL = "http://pitt.summon.serialssolutions.com/api/search"

class HTMLStrip(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.data = []
    def handle_data(self, d):
        self.data.append(d)
    def get_data(self):
        return ''.join(self.data)

sess = requests.session()

def get_documents(query, page=1):
    """Return ten resource results from the specified page"""
    if page > 50:
        # Max supported page number is 50
        page = 50

    payload = {'q': query, 'pn': page}
    resp = sess.get(LIBRARY_URL, params=payload)
    resp = resp.json()

    results = _extract_results(resp)
    return results


def get_document_by_bookmark(bookmark):
    """Return resource referenced by bookmark"""
    payload = {'bookMark': bookmark}
    resp = sess.get(LIBRARY_URL, params=payload)
    resp = resp.json()

    for error in resp.get("errors"):
        if error['code'] == 'invalid.bookmark.format':
            raise ValueError("Invalid bookmark")

    results = _extract_results(resp)
    return results

def _strip_html(html):
    strip = HTMLStrip()
    strip.feed(html)
    return strip.get_data()

def _extract_results(json):
    results = {
        'page_count': json['page_count'],
        'record_count': json['record_count'],
        'page_number': json['query']['page_number'],
        'facet_fields': _extract_facets(json['facet_fields'])
        }

    results['documents'] = _extract_documents(json['documents'])

    return results

def _extract_documents(documents):
    new_docs = []

    keep_keys = ['bookmarks', 'content_types', 'subject_terms', 'languages', \
        'isbns', 'full_title', 'publishers', 'publication_years', 'discipline', \
        'authors', 'abstracts', 'link', 'lc_call_numbers']

    for doc in documents:
        new_doc = {}
        for key in doc.keys() & keep_keys:
            new_doc[key] = doc[key]
        new_doc['full_title'] = _strip_html(new_doc['full_title'])
        new_docs.append(new_doc)

    return new_docs

def _extract_facets(facet_fields):
    facets = {}
    for facet in facet_fields:
        facets[facet['display_name']] = []
        for count in facet['counts']:
            facets[facet['display_name']].append({'value': count['value'], \
                'count': count['count']})

    return facets
