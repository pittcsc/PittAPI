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

from __future__ import annotations

import math
import requests
from bs4 import BeautifulSoup, Tag
from typing import Literal, NamedTuple

NUM_ARTICLES_PER_PAGE = 20

NEWS_BY_CATEGORY_URL = (
    "https://www.pitt.edu/pittwire/news/{category}?field_topics_target_id={topic_id}&field_article_date_value={year}"
    "&title={query}&field_category_target_id=All&page={page_num}"
)
PITT_BASE_URL = "https://www.pitt.edu"

Category = Literal["features-articles", "accolades-honors", "ones-to-watch", "announcements-and-updates"]
Topic = Literal[
    "university-news",
    "health-and-wellness",
    "technology-and-science",
    "arts-and-humanities",
    "community-impact",
    "innovation-and-research",
    "global",
    "diversity-equity-and-inclusion",
    "our-city-our-campus",
    "teaching-and-learning",
    "space",
    "ukraine",
    "sustainability",
]

TOPIC_ID_MAP: dict[Topic, int] = {
    "university-news": 432,
    "health-and-wellness": 2,
    "technology-and-science": 391,
    "arts-and-humanities": 4,
    "community-impact": 6,
    "innovation-and-research": 1,
    "global": 9,
    "diversity-equity-and-inclusion": 8,
    "our-city-our-campus": 12,
    "teaching-and-learning": 7,
    "space": 440,
    "ukraine": 441,
    "sustainability": 470,
}

sess = requests.Session()


class Article(NamedTuple):
    title: str
    description: str
    url: str
    tags: list[str]

    @classmethod
    def from_html(cls, article_html: Tag) -> Article:
        article_heading = article_html.select_one("h2.news-card-title a")
        article_subheading = article_html.find("p")
        if not isinstance(article_heading, Tag) or not isinstance(article_subheading, Tag):
            raise ValueError("News card is missing its heading or description")

        article_title = article_heading.get_text(strip=True)
        article_href = article_heading.get("href")
        if not isinstance(article_href, str):
            raise ValueError("News card heading is missing its URL")
        article_url = PITT_BASE_URL + article_href
        article_description = article_subheading.get_text(strip=True)
        article_tags = [tag.get_text(strip=True) for tag in article_html.select("ul.news-card-tags li")]

        return cls(title=article_title, description=article_description, url=article_url, tags=article_tags)


def _get_page_articles(
    topic: Topic,
    category: Category,
    query: str,
    year: int | None,
    page_num: int,
) -> list[Article]:
    year_str = str(year) if year else ""
    page_num_str = str(page_num) if page_num else ""
    response = sess.get(
        NEWS_BY_CATEGORY_URL.format(
            category=category, topic_id=TOPIC_ID_MAP[topic], year=year_str, query=query, page_num=page_num_str
        )
    )
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.select_one("html > body > div > main > div > section")
    if not isinstance(main_content, Tag):
        raise ValueError("News page is missing its main content")
    news_cards = main_content.select("div.news-card")
    page_articles = [Article.from_html(news_card) for news_card in news_cards]
    return page_articles


def get_articles_by_topic(
    topic: Topic,
    category: Category = "features-articles",
    query: str = "",
    year: int | None = None,
    max_num_results: int = NUM_ARTICLES_PER_PAGE,
) -> list[Article]:
    num_pages = math.ceil(max_num_results / NUM_ARTICLES_PER_PAGE)

    # Fetch pages sequentially so articles remain in page order.
    results: list[Article] = []
    for page_num in range(num_pages):  # Page numbers in url are 0-indexed
        page_articles = _get_page_articles(topic, category, query, year, page_num)
        num_articles_to_add = min(len(page_articles), max_num_results - len(results))
        results.extend(page_articles[:num_articles_to_add])
    return results
