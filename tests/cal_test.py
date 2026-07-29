import pytest
import responses

from pittapi.cal import (
    ACADEMIC_CALENDAR_URL,
    COURSE_CALENDAR_URL,
    ENROLLMENT_CALENDAR_URL,
    GRADES_CALENDAR_URL,
    GRADUATION_CALENDAR_URL,
    CalendarClient,
    Event,
    parse_event,
)

EVENT_DATA = {
    "title": "Fall term begins",
    "startDateTime": "2026-08-24T00:00:00",
    "customFields": [{"label": "Event Title", "value": "First day of classes"}],
    "categoryCalendar": "Academic|Fall",
}


@responses.activate
def test_calendar_endpoints():
    client = CalendarClient()
    endpoints = (
        (ACADEMIC_CALENDAR_URL, client.get_academic_calendar),
        (GRADES_CALENDAR_URL, client.get_grades_calendar),
        (ENROLLMENT_CALENDAR_URL, client.get_enrollment_calendar),
        (COURSE_CALENDAR_URL, client.get_course_calendar),
        (GRADUATION_CALENDAR_URL, client.get_graduation_calendar),
    )
    expected = (
        Event(
            date="2026-08-24",
            title="Fall term begins",
            content="First day of classes",
            categories=("Academic", "Fall"),
        ),
    )

    for url, method in endpoints:
        responses.add(responses.GET, url, json=[EVENT_DATA])
        assert method() == expected


@responses.activate
def test_calendar_requires_a_list():
    responses.add(responses.GET, ACADEMIC_CALENDAR_URL, json={})
    with pytest.raises(ValueError, match="list of events"):
        CalendarClient().get_academic_calendar()


def test_calendar_rejects_unexpected_custom_field():
    event = EVENT_DATA | {"customFields": [{"label": "Other", "value": "value"}]}
    with pytest.raises(ValueError, match="unexpected custom field"):
        parse_event(event)


def test_calendar_rejects_missing_data():
    with pytest.raises(ValueError, match="missing required data"):
        parse_event({})
