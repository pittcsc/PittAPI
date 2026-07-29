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

Articles published by Pittwire.
"""

from dataclasses import dataclass
import math
from typing import Literal

from bs4 import BeautifulSoup, Tag

from pittapi.base_client import BaseClient

__all__ = ["Article", "NewsClient"]

ARTICLES_PER_PAGE = 20
NEWS_BY_CATEGORY_URL = (
    "https://www.pitt.edu/pittwire/news/{category}?field_topics_target_id={topic_id}&field_article_date_value={year}"
    "&title={query}&field_category_target_id=All&page={page}"
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
TOPIC_IDS: dict[Topic, int] = {
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


@dataclass(frozen=True, slots=True)
class Article:
    title: str
    description: str
    url: str
    tags: tuple[str, ...]


class NewsClient(BaseClient):
    """Search Pittwire articles."""

    def get_articles_by_topic(
        self,
        topic: Topic,
        category: Category = "features-articles",
        query: str = "",
        year: int | None = None,
        max_num_results: int = ARTICLES_PER_PAGE,
    ) -> tuple[Article, ...]:
        if max_num_results < 0:
            raise ValueError("max_num_results cannot be negative")
        if topic not in TOPIC_IDS:
            raise ValueError(f"unknown news topic: {topic}")

        page_count = math.ceil(max_num_results / ARTICLES_PER_PAGE)
        articles = []
        for page in range(page_count):
            page_articles = self.get_page_articles(topic, category, query, year, page)
            remaining = max_num_results - len(articles)
            articles.extend(page_articles[:remaining])
        return tuple(articles)

    def get_page_articles(
        self,
        topic: Topic,
        category: Category,
        query: str,
        year: int | None,
        page: int,
    ) -> tuple[Article, ...]:
        url = NEWS_BY_CATEGORY_URL.format(
            category=category,
            topic_id=TOPIC_IDS[topic],
            year=year or "",
            query=query,
            page=page,
        )
        soup = BeautifulSoup(self.request("GET", url).text, "html.parser")
        main_content = soup.select_one("html > body > div > main > div > section")
        if not isinstance(main_content, Tag):
            raise ValueError("news page is missing its main content")
        return tuple(parse_article(card) for card in main_content.select("div.news-card"))


def parse_article(article_html: Tag) -> Article:
    heading = article_html.select_one("h2.news-card-title a")
    description = article_html.find("p")
    if not isinstance(heading, Tag) or not isinstance(description, Tag):
        raise ValueError("news card is missing its heading or description")
    href = heading.get("href")
    if not isinstance(href, str):
        raise ValueError("news card heading is missing its URL")
    tags = tuple(tag.get_text(strip=True) for tag in article_html.select("ul.news-card-tags li"))
    return Article(
        title=heading.get_text(strip=True),
        description=description.get_text(strip=True),
        url=PITT_BASE_URL + href,
        tags=tags,
    )
