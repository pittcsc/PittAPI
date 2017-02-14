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
import requests
from bs4 import BeautifulSoup, SoupStrainer
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sess = requests.session()
#strainer = SoupStrainer('div', attrs={'class': 'kgoui_list_item_textblock'})


def get_news(feed="main_news"):
    # feed indicates the desired news feed
    # "main_news"      - main news
    # "cssd"           - student announcements, on my pitt
    # "news_chronicle" - the Pitt Chronicle news
    # "news_alerts"    - crime alerts

    # sample_url = 'https://m.pitt.edu/news/index.json?feed=main_news&id=&_object=kgoui_Rcontent_I0_Rcontent_I0&_object_include_html=1&start=0'
    news = [] 
    payload = {
        "feed": feed,
        "id": "",
        "_object": "kgoui_Rcontent_I0_Rcontent_I0",
        "_object_include_html": "1",
        "start": 0
    }
    
    while not False:
        data = sess.get('https://m.pitt.edu/news/index.json', params=payload).json()  # Should be UTF-8 by JSON standard
        soup = BeautifulSoup(data['response']['html'], 'lxml') #, parse_only=strainer)
        news_names = map((lambda i: i.getText()), soup.find_all('span', class_='kgoui_list_item_title'))
        news_links = map(_href_to_url, soup.find_all('a', class_="kgoui_list_item_action"))

        news.extend(list(map((lambda t, u: {'title': t, 'url': u}), news_names, news_links)))

        if any('Load more...' in s for s in news_names):
            news.pop()
            payload["start"] += 10
        else:
            return news

def _href_to_url(item):
    item = item['href']
    item = re.sub(r"\+at\+.+edu", "", item)
    item = item.replace("/news", "https://m.pitt.edu/news")
    return item

