import pytest

from pittapi.cal import CalendarClient, Event
from pittapi.course import CourseClient
from pittapi.textbook import TextbookClient

pytestmark = pytest.mark.live


@pytest.mark.parametrize(
    "method_name",
    [
        "get_academic_calendar",
        "get_grades_calendar",
        "get_enrollment_calendar",
        "get_course_calendar",
        "get_graduation_calendar",
    ],
)
def test_calendar_feed(method_name):
    with CalendarClient() as calendar:
        events = getattr(calendar, method_name)()

    assert isinstance(events, tuple)
    assert all(isinstance(event, Event) for event in events)


def test_course_catalog():
    with CourseClient() as courses:
        subject = courses.get_subject_courses("CS")

    assert subject.subject_code == "CS"
    assert subject.courses
    assert all(course.course_id for course in subject.courses)


def test_textbook_terms_and_subjects():
    with TextbookClient() as textbooks:
        terms = textbooks.get_terms()
        term = next(term for term in terms if term.inquiry_enabled)
        textbooks.select_term(term)
        textbooks.initialize_subjects()

    assert textbooks.subject_ids
