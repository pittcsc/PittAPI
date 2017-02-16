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

import re
import math
import requests
import grequests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sess = requests.session()


def _href_to_url(item):
    url = item['href']
    url = re.sub(r'\+at\+.+edu', '', url)
    url = url.replace('/news', 'https://m.pitt.edu/news')
    return url


def _load_n_items(feed, max_news_items):
    payload = {
        'feed': feed,
        'id': '',
        '_object': 'kgoui_Rcontent_I0_Rcontent_I0',
        'start': 0
    }

    request_objs = []
    for i in range(int(math.ceil(max_news_items / 10))):
        payload['start'] = i * 10
        request_objs.append(grequests.get('https://m.pitt.edu/news/index.json', params=payload))

    responses = grequests.imap(request_objs)

    return responses


def get_news(feed='main_news', max_news_items=10):
    # feed indicates the desired news feed
    # 'main_news'      - main news
    # 'cssd'           - student announcements, on my pitt
    # 'news_chronicle' - the Pitt Chronicle news
    # 'news_alerts'    - crime alerts

    news = []

    resps = _load_n_items(feed, max_news_items)
    resps = [r.json()["response"]["regions"][0]["contents"] for r in resps]

    for resp in resps:
        for data in resp:
            fields = data["fields"]
            if fields["type"] == "loadMore":
                continue

            title = fields["title"]
            url = fields["url"]["formatted"]
            news.extend({'title': title, 'url': url})

    return news[:max_news_items]

