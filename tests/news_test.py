from pathlib import Path

import pytest
import responses

from pittapi.news import ARTICLES_PER_PAGE, NEWS_BY_CATEGORY_URL, Article, NewsClient

SAMPLES = Path("tests/samples")
PAGE_ZERO = (SAMPLES / "news_university_news_features_articles_page_0.html").read_text()
PAGE_ONE = (SAMPLES / "news_university_news_features_articles_page_1.html").read_text()


def news_url(page=0, year="", query=""):
    return NEWS_BY_CATEGORY_URL.format(
        category="features-articles",
        topic_id=432,
        year=year,
        query=query,
        page=page,
    )


@responses.activate
def test_articles_are_models_and_preserve_page_order():
    responses.add(responses.GET, news_url(0), body=PAGE_ZERO)
    responses.add(responses.GET, news_url(1), body=PAGE_ONE)

    articles = NewsClient().get_articles_by_topic("university-news", max_num_results=ARTICLES_PER_PAGE + 5)

    assert len(articles) == 25
    assert isinstance(articles[0], Article)
    assert isinstance(articles[0].tags, tuple)
    assert articles[0].title == "Questions for the ‘Connecting King’"
    assert articles[-1].title == "Pitt has 2 new Goldwater Scholars"


@responses.activate
def test_article_filters_and_empty_limit():
    filtered = (SAMPLES / "news_university_news_features_articles_fulbright.html").read_text()
    responses.add(responses.GET, news_url(query="fulbright"), body=filtered)
    assert len(NewsClient().get_articles_by_topic("university-news", query="fulbright")) == 3
    assert NewsClient().get_articles_by_topic("university-news", max_num_results=0) == ()


@responses.activate
def test_year_filter():
    page = (SAMPLES / "news_university_news_features_articles_2020.html").read_text()
    responses.add(responses.GET, news_url(year=2020), body=page)
    assert len(NewsClient().get_articles_by_topic("university-news", year=2020)) == 5


def test_invalid_topic_and_limit():
    with pytest.raises(ValueError, match="cannot be negative"):
        NewsClient().get_articles_by_topic("university-news", max_num_results=-1)
    with pytest.raises(ValueError, match="unknown news topic"):
        NewsClient().get_articles_by_topic("invalid")


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
        NewsClient().get_articles_by_topic("university-news")
