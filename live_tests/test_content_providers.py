import pytest

from pittapi.library import LibraryClient
from pittapi.news import NewsClient
from pittapi.people import PeopleClient

pytestmark = pytest.mark.live


def test_library_catalog_and_hillman_reservations():
    with LibraryClient() as library:
        documents = library.get_documents("computer science")
        reservation_total = library.hillman_total_reserved()

    assert documents.num_results > 0
    assert documents.documents
    assert reservation_total >= 0


def test_pittwire_topics_and_articles():
    with NewsClient() as news:
        topics = news.get_topics()
        articles = news.get_articles_by_topic(topics[0], max_num_results=1)

    assert topics
    assert articles
    assert articles[0].url.startswith("https://www.pittwire.pitt.edu/")


def test_people_directory_service_account():
    with PeopleClient() as people:
        matches = people.get_person("Technology Help Desk")

    assert matches
    assert matches[0].name == "Help Desk, Technology"
    assert any(field.name == "Email" for field in matches[0].fields)
