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
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from pittapi.base_client import BaseClient

__all__ = ["Article", "NewsCategory", "NewsClient", "NewsTopic"]

ARTICLES_PER_PAGE = 20
PITTWIRE_BASE_URL = "https://www.pittwire.pitt.edu"
DEFAULT_NEWS_CATEGORY = "features-articles"
NEWS_BY_CATEGORY_URL = PITTWIRE_BASE_URL + "/pittwire/news/{category}"


@dataclass(frozen=True, slots=True)
class NewsTopic:
    id: int
    name: str


@dataclass(frozen=True, slots=True)
class NewsCategory:
    slug: str
    name: str


@dataclass(frozen=True, slots=True)
class Article:
    title: str
    description: str
    url: str
    tags: tuple[str, ...]


class NewsClient(BaseClient):
    """Search Pittwire articles."""

    def get_topics(self) -> tuple[NewsTopic, ...]:
        """Return the topics currently offered by Pittwire's search form."""
        soup = self.get_filter_page()
        topic_select = soup.select_one("select[name=field_topics_target_id]")
        if not isinstance(topic_select, Tag):
            raise ValueError("news page is missing its topic filter")

        topics = []
        for option in topic_select.find_all("option"):
            topic_id = option.get("value")
            if topic_id == "All":
                continue
            if not isinstance(topic_id, str) or not topic_id.isdigit():
                raise ValueError("news page contains an invalid topic ID")
            topics.append(NewsTopic(id=int(topic_id), name=option.get_text(strip=True)))
        return tuple(topics)

    def get_categories(self) -> tuple[NewsCategory, ...]:
        """Return the article categories currently linked by Pittwire."""
        soup = self.get_filter_page()
        category_links = soup.select(".view-category-menu .view-content a")
        if not category_links:
            raise ValueError("news page is missing its category links")

        categories = []
        path_prefix = "/pittwire/news/"
        for link in category_links:
            href = link.get("href")
            if not isinstance(href, str) or not href.startswith(path_prefix):
                raise ValueError("news page contains an invalid category link")
            categories.append(
                NewsCategory(
                    slug=href.removeprefix(path_prefix),
                    name=link.get_text(strip=True),
                )
            )
        return tuple(categories)

    def get_years(self) -> tuple[int, ...]:
        """Return the publication years currently offered by Pittwire."""
        soup = self.get_filter_page()
        year_select = soup.select_one("select[name=field_article_date_value]")
        if not isinstance(year_select, Tag):
            raise ValueError("news page is missing its year filter")

        years = []
        for option in year_select.find_all("option"):
            year = option.get("value")
            if year == "":
                continue
            if not isinstance(year, str) or not year.isdigit():
                raise ValueError("news page contains an invalid publication year")
            years.append(int(year))
        return tuple(years)

    def get_filter_page(self) -> BeautifulSoup:
        """Fetch the default news page used to discover available filters."""
        url = NEWS_BY_CATEGORY_URL.format(category=DEFAULT_NEWS_CATEGORY)
        return BeautifulSoup(self.request("GET", url).text, "html.parser")

    def get_articles_by_topic(
        self,
        topic: NewsTopic,
        category: NewsCategory | None = None,
        query: str = "",
        year: int | None = None,
        max_num_results: int = ARTICLES_PER_PAGE,
    ) -> tuple[Article, ...]:
        if max_num_results < 0:
            raise ValueError("max_num_results cannot be negative")

        page_count = math.ceil(max_num_results / ARTICLES_PER_PAGE)
        articles = []
        for page in range(page_count):
            page_articles = self.get_page_articles(topic, category, query, year, page)
            remaining = max_num_results - len(articles)
            articles.extend(page_articles[:remaining])
        return tuple(articles)

    def get_page_articles(
        self,
        topic: NewsTopic,
        category: NewsCategory | None,
        query: str,
        year: int | None,
        page: int,
    ) -> tuple[Article, ...]:
        category_slug = category.slug if category else DEFAULT_NEWS_CATEGORY
        url = NEWS_BY_CATEGORY_URL.format(category=category_slug)
        parameters = {
            "field_topics_target_id": topic.id,
            "field_article_date_value": year or "",
            "title": query,
            "field_category_target_id": "All",
            "page": page,
        }
        soup = BeautifulSoup(self.request("GET", url, params=parameters).text, "html.parser")
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
        url=urljoin(PITTWIRE_BASE_URL, href),
        tags=tags,
    )
