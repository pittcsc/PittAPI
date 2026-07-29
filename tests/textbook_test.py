import json
from pathlib import Path

import pytest
import requests
import responses

from pittapi.textbook import (
    BASE_URL,
    BOOKS_URL,
    COURSES_URL,
    MAX_REQUEST_ATTEMPTS,
    SUBJECTS_URL,
    CourseInfo,
    Textbook,
    TextbookClient,
    TextbookTerm,
    find_section,
    find_section_id,
    parse_textbook,
)

SAMPLES = Path("tests/samples")
BASE_HTML = (SAMPLES / "textbook_base_page.html").read_text()
SUBJECTS = json.loads((SAMPLES / "textbook_subjects.json").read_text())
CS_COURSES = json.loads((SAMPLES / "textbook_courses_CS.json").read_text())
MATH_COURSES = json.loads((SAMPLES / "textbook_courses_MATH.json").read_text())
CS_BOOKS = json.loads((SAMPLES / "textbook_textbooks_CS_0441_garrison.json").read_text())
MATH_BOOKS = json.loads((SAMPLES / "textbook_textbooks_MATH_0430_pan.json").read_text())
CS_ID = "22457"
MATH_ID = "22528"
CS_SECTION = "4558031"
MATH_SECTION = "4631097"
HEADERS = {"X-CSRF-Token": "token"}
TERM = TextbookTerm("78104", "Fall 24", True, True)


def subjects_url(term=TERM):
    return SUBJECTS_URL.format(term_id=term.id)


def courses_url(subject_id, term=TERM):
    return COURSES_URL.format(department_id=subject_id, term_id=term.id)


@pytest.mark.parametrize(
    ("course", "expected"),
    [
        (CourseInfo("cs", "441", "garrison iii", "1245"), CourseInfo("CS", "0441", "GARRISON III", "1245")),
        (CourseInfo("MATH", "0430"), CourseInfo("MATH", "0430")),
    ],
)
def test_course_info_normalization(course, expected):
    assert course == expected


@pytest.mark.parametrize("number", ["abc", "12345", ""])
def test_invalid_course_number(number):
    with pytest.raises(ValueError, match="invalid course number"):
        CourseInfo("CS", number)


@pytest.mark.parametrize("section", ["123", "abcd"])
def test_invalid_section_number(section):
    with pytest.raises(ValueError, match="invalid section number"):
        CourseInfo("CS", "0441", section_num=section)


@responses.activate
def test_initialize_headers():
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    client = TextbookClient()
    client.initialize_headers()
    assert client.headers
    assert client.terms == (TERM,)


@responses.activate
def test_get_terms_caches_discovery_and_selecting_a_new_term_resets_subjects():
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    client = TextbookClient()
    assert client.get_terms() == (TERM,)
    assert client.get_terms() == (TERM,)
    assert len(responses.calls) == 1

    client.subject_ids = {"CS": CS_ID}
    client.select_term(TERM)
    assert client.subject_ids is None
    client.subject_ids = {"CS": CS_ID}
    client.select_term(TERM)
    assert client.subject_ids == {"CS": CS_ID}


@responses.activate
def test_get_terms_allows_empty_discovery():
    html = BASE_HTML.replace(
        '[{"id":"78104","name":"Fall 24","inquiry":true,"ordering":true}]',
        "[]",
    )
    responses.add(responses.GET, BASE_URL, body=html)
    assert TextbookClient().get_terms() == ()


@pytest.mark.parametrize(
    "html",
    [
        "<html></html>",
        "<html><head><meta name='csrf-token'></head></html>",
    ],
)
@responses.activate
def test_initialize_headers_requires_token(html):
    responses.add(responses.GET, BASE_URL, body=html)
    with pytest.raises(requests.ConnectionError, match="credentials"):
        TextbookClient().initialize_headers()


@pytest.mark.parametrize(
    "html",
    [
        "<meta name='csrf-token' content='token'>",
        "<meta name='csrf-token' content='token'><script>new Verba.Compare.Collections.Terms(not-json)</script>",
        ("<meta name='csrf-token' content='token'><script>" "new Verba.Compare.Collections.Terms([{}])</script>"),
    ],
)
@responses.activate
def test_initialize_headers_requires_valid_terms(html):
    responses.add(responses.GET, BASE_URL, body=html)
    with pytest.raises(ValueError, match="term"):
        TextbookClient().initialize_headers()


@responses.activate
def test_initialize_headers_retries_then_fails():
    responses.add(responses.GET, BASE_URL, status=400)
    with pytest.raises(requests.ConnectionError, match=str(MAX_REQUEST_ATTEMPTS)):
        TextbookClient().initialize_headers()
    assert len(responses.calls) == MAX_REQUEST_ATTEMPTS


@responses.activate
def test_initialize_subjects_with_existing_and_missing_headers():
    responses.add(responses.GET, subjects_url(), json=SUBJECTS)
    client = TextbookClient(TERM)
    client.headers = HEADERS
    client.initialize_subjects()
    assert client.subject_ids["CS"] == CS_ID

    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    responses.add(responses.GET, subjects_url(), json=SUBJECTS)
    fresh_client = TextbookClient(TERM)
    fresh_client.initialize_subjects()
    assert fresh_client.headers


@responses.activate
def test_initialize_subjects_rejects_malformed_data():
    responses.add(responses.GET, subjects_url(), json=[{}])
    client = TextbookClient(TERM)
    client.headers = HEADERS
    with pytest.raises(ValueError, match="subject response"):
        client.initialize_subjects()


@responses.activate
def test_initialize_subjects_refreshes_and_eventually_fails():
    responses.add(responses.GET, subjects_url(), status=400)
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    client = TextbookClient(TERM)
    client.headers = HEADERS
    with pytest.raises(requests.ConnectionError, match="retrieve subjects"):
        client.initialize_subjects()


@responses.activate
def test_get_courses_success_and_validation():
    responses.add(responses.GET, courses_url(CS_ID), json=CS_COURSES)
    client = TextbookClient(TERM)
    client.headers = HEADERS
    client.subject_ids = {"CS": CS_ID}
    assert client.get_courses("CS") == CS_COURSES

    client.subject_ids = None
    with pytest.raises(LookupError, match="invalid textbook subject"):
        client.get_courses("CS")


@responses.activate
def test_get_courses_initializes_headers_and_rejects_nonlist():
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    responses.add(responses.GET, courses_url(CS_ID), json={})
    client = TextbookClient(TERM)
    client.subject_ids = {"CS": CS_ID}
    with pytest.raises(ValueError, match="must contain a list"):
        client.get_courses("CS")


@responses.activate
def test_get_courses_refreshes_and_fails():
    responses.add(responses.GET, courses_url(CS_ID), status=400)
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    client = TextbookClient(TERM)
    client.headers = HEADERS
    client.subject_ids = {"CS": CS_ID}
    with pytest.raises(requests.ConnectionError, match="retrieve CS courses"):
        client.get_courses("CS")


@responses.activate
def test_get_textbooks_for_one_course():
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    responses.add(responses.GET, subjects_url(), json=SUBJECTS)
    responses.add(responses.GET, courses_url(CS_ID), json=CS_COURSES)
    responses.add(responses.GET, BOOKS_URL.format(section_id=CS_SECTION), json=CS_BOOKS)

    books = TextbookClient(TERM).get_textbooks_for_course(CourseInfo("CS", "0441", instructor="GARRISON III"))

    assert len(books) == 1
    assert books[0].title == "Ia Canvas Content"


@responses.activate
def test_get_textbooks_for_multiple_courses_and_cache_subject():
    client = TextbookClient(TERM)
    client.headers = HEADERS
    client.subject_ids = {"CS": CS_ID, "MATH": MATH_ID}
    responses.add(responses.GET, courses_url(CS_ID), json=CS_COURSES)
    responses.add(responses.GET, courses_url(MATH_ID), json=MATH_COURSES)
    responses.add(responses.GET, BOOKS_URL.format(section_id=CS_SECTION), json=CS_BOOKS)
    responses.add(responses.GET, BOOKS_URL.format(section_id=CS_SECTION), json=CS_BOOKS)
    responses.add(responses.GET, BOOKS_URL.format(section_id=MATH_SECTION), json=MATH_BOOKS)
    courses = [
        CourseInfo("CS", "0441", instructor="GARRISON III"),
        CourseInfo("CS", "0441", section_num="1245"),
        CourseInfo("MATH", "0430", instructor="PAN"),
    ]

    books = client.get_textbooks_for_courses(courses)

    assert len(books) == 3
    assert sum(call.request.url == courses_url(CS_ID) for call in responses.calls) == 1


def test_get_textbooks_rejects_unknown_subject():
    client = TextbookClient(TERM)
    client.subject_ids = {}
    with pytest.raises(LookupError, match="invalid textbook subject"):
        client.get_textbooks_for_courses([CourseInfo("FAKE", "0001")])


@responses.activate
def test_section_textbooks_initializes_headers_and_filters_empty_records():
    responses.add(responses.GET, BASE_URL, body=BASE_HTML)
    responses.add(responses.GET, BOOKS_URL.format(section_id=CS_SECTION), json=[{}, *CS_BOOKS])
    books = TextbookClient(TERM).get_textbooks_for_section(CS_SECTION)
    assert len(books) == 1


@responses.activate
def test_section_textbooks_requires_list():
    responses.add(responses.GET, BOOKS_URL.format(section_id=CS_SECTION), json={})
    client = TextbookClient(TERM)
    client.headers = HEADERS
    with pytest.raises(ValueError, match="must contain a list"):
        client.get_textbooks_for_section(CS_SECTION)


def test_textbook_requests_require_selected_term():
    client = TextbookClient()
    course = CourseInfo("CS", "0441")
    with pytest.raises(ValueError, match="select a textbook term"):
        client.initialize_subjects()
    with pytest.raises(ValueError, match="select a textbook term"):
        client.get_courses("CS")
    with pytest.raises(ValueError, match="select a textbook term"):
        client.get_textbooks_for_course(course)
    with pytest.raises(ValueError, match="select a textbook term"):
        client.get_textbooks_for_section("1")


def test_find_section_variants():
    sections = [
        {"name": "0001", "instructor": "SAME", "id": "1"},
        {"name": "0002", "instructor": "SAME", "id": "2"},
    ]
    assert find_section(sections, None, "0002") == "2"
    assert find_section(sections, "SAME", None) == "1"
    assert find_section(sections, None, None) == "1"
    assert find_section([sections[0]], None, None) == "1"

    with pytest.raises(LookupError, match="section not found"):
        find_section(sections, None, "9999")
    with pytest.raises(LookupError, match="instructor not found"):
        find_section(sections, "OTHER", None)

    ambiguous = [sections[0], sections[1] | {"instructor": "OTHER"}]
    with pytest.raises(LookupError, match="provide an instructor"):
        find_section(ambiguous, None, None)


def test_find_section_id_and_invalid_course():
    course = CourseInfo("CS", "0441", section_num="1245")
    assert find_section_id(CS_COURSES, course) == CS_SECTION
    with pytest.raises(LookupError, match="invalid textbook course"):
        find_section_id(CS_COURSES, CourseInfo("CS", "0001"))


def test_parse_textbook():
    assert isinstance(parse_textbook(CS_BOOKS[0]), Textbook)
    assert parse_textbook({}) is None
