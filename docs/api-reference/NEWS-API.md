> [Home](README.md) > News API

---

# News API

`NewsClient` searches Pittwire and discovers its available filters from the
current Pittwire page. Topic IDs, category paths, and publication years are
not maintained as hardcoded lists in PittAPI.

## Discovering filters

```python
from pittapi import NewsClient

with NewsClient() as news:
    topics = news.get_topics()
    categories = news.get_categories()
    years = news.get_years()
```

`get_topics()` returns `NewsTopic` models containing Pittwire's topic ID and
display name. `get_categories()` returns `NewsCategory` models containing the
category path and display name. `get_years()` returns integers.

## Fetching articles

```python
from pittapi import NewsClient

with NewsClient() as news:
    topics = news.get_topics()
    technology = next(
        topic for topic in topics if topic.name == "Technology & Science"
    )
    articles = news.get_articles_by_topic(
        technology,
        query="robotics",
        year=2026,
        max_num_results=5,
    )
```

`get_articles_by_topic()` returns an immutable tuple of `Article` models in
Pittwire's page order. Pass a discovered `NewsCategory` with `category=` to
search a category other than Features & Articles.
