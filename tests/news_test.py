from pathlib import Path

import pytest
import requests
import responses

from pittapi.news import (
    ARTICLES_PER_PAGE,
    DEFAULT_NEWS_CATEGORY,
    NEWS_BY_CATEGORY_URL,
    Article,
    NewsCategory,
    NewsClient,
    NewsTopic,
)

SAMPLES = Path("tests/samples")
PAGE_ZERO = (SAMPLES / "news_university_news_features_articles_page_0.html").read_text()
PAGE_ONE = (SAMPLES / "news_university_news_features_articles_page_1.html").read_text()
UNIVERSITY_NEWS = NewsTopic(id=432, name="University News")


def news_url(page=0, year="", query="", category=DEFAULT_NEWS_CATEGORY):
    request = requests.Request(
        "GET",
        NEWS_BY_CATEGORY_URL.format(category=category),
        params={
            "field_topics_target_id": UNIVERSITY_NEWS.id,
            "field_article_date_value": year,
            "title": query,
            "field_category_target_id": "All",
            "page": page,
        },
    )
    return request.prepare().url


def filter_url():
    return NEWS_BY_CATEGORY_URL.format(category=DEFAULT_NEWS_CATEGORY)


@responses.activate
def test_articles_are_models_and_preserve_page_order():
    responses.add(responses.GET, news_url(0), body=PAGE_ZERO)
    responses.add(responses.GET, news_url(1), body=PAGE_ONE)

    articles = NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, max_num_results=ARTICLES_PER_PAGE + 5)

    assert len(articles) == 25
    assert isinstance(articles[0], Article)
    assert isinstance(articles[0].tags, tuple)
    assert articles[0].title == "Questions for the ‘Connecting King’"
    assert articles[-1].title == "Pitt has 2 new Goldwater Scholars"


@responses.activate
def test_article_filters_and_empty_limit():
    filtered = (SAMPLES / "news_university_news_features_articles_fulbright.html").read_text()
    responses.add(responses.GET, news_url(query="fulbright"), body=filtered)
    assert len(NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, query="fulbright")) == 3
    assert NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, max_num_results=0) == ()


@responses.activate
def test_year_filter():
    page = (SAMPLES / "news_university_news_features_articles_2020.html").read_text()
    responses.add(responses.GET, news_url(year=2020), body=page)
    assert len(NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, year=2020)) == 5


def test_negative_limit():
    with pytest.raises(ValueError, match="cannot be negative"):
        NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, max_num_results=-1)


@responses.activate
def test_discovers_filters_from_pittwire():
    responses.add(responses.GET, filter_url(), body=PAGE_ZERO)
    topics = NewsClient().get_topics()
    assert topics[0] == UNIVERSITY_NEWS
    assert NewsTopic(id=470, name="Sustainability") in topics

    responses.add(responses.GET, filter_url(), body=PAGE_ZERO)
    categories = NewsClient().get_categories()
    assert categories == (
        NewsCategory(slug="features-articles", name="Features & Articles"),
        NewsCategory(slug="accolades-honors", name="Accolades & Honors"),
        NewsCategory(slug="ones-to-watch", name="Ones to Watch"),
        NewsCategory(slug="announcements-and-updates", name="Announcements and Updates"),
    )

    responses.add(responses.GET, filter_url(), body=PAGE_ZERO)
    years = NewsClient().get_years()
    assert years[0] == 2012
    assert years[-1] == 2024


@responses.activate
def test_uses_discovered_category():
    category = NewsCategory(slug="accolades-honors", name="Accolades & Honors")
    responses.add(responses.GET, news_url(category=category.slug), body=PAGE_ZERO)
    articles = NewsClient().get_articles_by_topic(UNIVERSITY_NEWS, category=category, max_num_results=1)
    assert len(articles) == 1


@pytest.mark.parametrize(
    ("method", "html", "message"),
    [
        ("get_topics", "<html></html>", "missing its topic filter"),
        (
            "get_topics",
            "<select name='field_topics_target_id'><option>Broken</option></select>",
            "invalid topic ID",
        ),
        (
            "get_topics",
            "<select name='field_topics_target_id'><option value='new'>New</option></select>",
            "invalid topic ID",
        ),
        ("get_categories", "<html></html>", "missing its category links"),
        (
            "get_categories",
            "<div class='view-category-menu'><div class='view-content'><a>Broken</a></div></div>",
            "invalid category link",
        ),
        (
            "get_categories",
            "<div class='view-category-menu'><div class='view-content'><a href='/other'>Broken</a></div></div>",
            "invalid category link",
        ),
        ("get_years", "<html></html>", "missing its year filter"),
        (
            "get_years",
            "<select name='field_article_date_value'><option value='recent'>Recent</option></select>",
            "invalid publication year",
        ),
    ],
)
@responses.activate
def test_malformed_news_filters(method, html, message):
    responses.add(responses.GET, filter_url(), body=html)
    with pytest.raises(ValueError, match=message):
        getattr(NewsClient(), method)()


@pytest.mark.parametrize(
    ("html", "message"),
    [
        ("<html><body></body></html>", "missing its main content"),
        (
            "<html><body><div><main><div><section><div class='news-card'></div></section></div></main></div></body></html>",
            "missing its heading or description",
        ),
        (
            "<html><body><div><main><div><section><div class='news-card'>"
            "<h2 class='news-card-title'><a>Title</a></h2><p>Description</p>"
            "</div></section></div></main></div></body></html>",
            "missing its URL",
        ),
    ],
)
@responses.activate
def test_malformed_news_pages(html, message):
    responses.add(responses.GET, news_url(), body=html)
    with pytest.raises(ValueError, match=message):
        NewsClient().get_articles_by_topic(UNIVERSITY_NEWS)
