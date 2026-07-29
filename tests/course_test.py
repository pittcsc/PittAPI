from copy import deepcopy
import json

import pytest
import responses

from pittapi.course import (
    COURSE_DETAIL_API,
    COURSE_SECTIONS_API,
    SECTION_DETAILS_API,
    SUBJECT_COURSES_API,
    SUBJECTS_API,
    Course,
    CourseClient,
    CourseDetails,
    Section,
    Subject,
    parse_catalog_section,
    parse_course_details,
    parse_detailed_meeting,
    parse_instructors,
    parse_section_details,
    validate_course_number,
    validate_term,
)
from tests.mocks.course_mocks import (
    mocked_course_info_data,
    mocked_course_sections_data,
    mocked_courses_data,
    mocked_section_details_data,
    mocked_subject_data,
)

TERM = "2231"
SUBJECT = "CS"
COURSE_NUMBER = "0007"
COURSE_ID = "105611"


def add_subject_response(data=mocked_subject_data):
    responses.add(responses.GET, SUBJECTS_API, json=data)


@responses.activate
def test_get_subject_courses_returns_models():
    add_subject_response()
    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json=mocked_courses_data)

    result = CourseClient().get_subject_courses("cs")

    assert isinstance(result, Subject)
    assert isinstance(result.courses[0], Course)
    assert result.courses[0].course_number == COURSE_NUMBER


@responses.activate
def test_people_soft_redirect_preserves_session_cookie():
    url = SUBJECT_COURSES_API.format(subject=SUBJECT)
    responses.add(
        responses.GET,
        url,
        status=302,
        headers={"Location": f"{url}&", "Set-Cookie": "pscheck=accepted; Path=/"},
    )

    def return_courses(request):
        assert "pscheck=accepted" in request.headers["Cookie"]
        return 200, {"Content-Type": "application/json"}, json.dumps(mocked_courses_data)

    responses.add_callback(responses.GET, f"{url}&", callback=return_courses)

    assert CourseClient().get_subject_course_data(SUBJECT) == mocked_courses_data
    assert responses.calls[0].request.url == url
    assert responses.calls[1].request.url == f"{url}&"


@responses.activate
def test_get_course_details_returns_nested_models():
    add_subject_response()
    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json=mocked_courses_data)
    responses.add(responses.GET, COURSE_DETAIL_API.format(id=COURSE_ID), json=mocked_course_info_data)
    responses.add(
        responses.GET,
        COURSE_SECTIONS_API.format(id=COURSE_ID, term=TERM),
        json=mocked_course_sections_data,
    )

    result = CourseClient().get_course_details(TERM, SUBJECT, 7)

    assert "effdt" not in responses.calls[2].request.url
    assert isinstance(result, CourseDetails)
    assert result.course.course_id == COURSE_ID
    assert result.components[0].required
    assert result.attributes[0].value == "ALG"
    assert result.sections[0].instructors[0].email == "rmf105@pitt.edu"
    assert result.sections[0].meetings[0].instructors[0].name == "Robert Fishel"


@responses.activate
def test_get_section_details_returns_nested_models():
    responses.add(
        responses.GET,
        SECTION_DETAILS_API.format(term=TERM, id=27815),
        json=mocked_section_details_data,
    )
    result = CourseClient().get_section_details(TERM, 27815)
    assert isinstance(result, Section)
    assert result.details.enrollment_available == "4"
    assert result.meetings[0].instructors[0].name == "Robert Fishel"


@pytest.mark.parametrize("term", [2191, "2194", "2197"])
def test_validate_term(term):
    assert validate_term(term) == str(term)


@pytest.mark.parametrize("term", ["214", "1111", "12345"])
def test_reject_invalid_term(term):
    with pytest.raises(ValueError, match="four-digit Pitt term"):
        validate_term(term)


@pytest.mark.parametrize(("value", "expected"), [(7, "0007"), ("449", "0449"), (1501, "1501")])
def test_validate_course_number(value, expected):
    assert validate_course_number(value) == expected


@pytest.mark.parametrize("value", ["", "abc", 0, -1])
def test_reject_nonpositive_or_nonnumeric_course(value):
    with pytest.raises(ValueError, match="positive number"):
        validate_course_number(value)


def test_reject_long_course_number():
    with pytest.raises(ValueError, match="four digits"):
        validate_course_number("12345")


@responses.activate
def test_subject_validation_errors():
    add_subject_response()
    with pytest.raises(ValueError, match="invalid subject code"):
        CourseClient().validate_subject("MISSING")

    add_subject_response({})
    with pytest.raises(ValueError, match="subject response"):
        CourseClient().validate_subject("CS")


@responses.activate
def test_subject_course_response_validation():
    add_subject_response()
    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json={})
    with pytest.raises(ValueError, match="subject course response"):
        CourseClient().get_subject_courses(SUBJECT)


@responses.activate
def test_find_course_id_errors_and_duplicate_selection():
    client = CourseClient()
    duplicate = {
        "courses": [
            {"catalog_nbr": "0001", "crse_id": "other"},
            {"catalog_nbr": COURSE_NUMBER, "crse_id": "first"},
            {"catalog_nbr": COURSE_NUMBER, "crse_id": "second"},
        ]
    }
    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json=duplicate)
    assert client.find_course_id(SUBJECT, COURSE_NUMBER) == "first"

    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json={"courses": []})
    with pytest.raises(LookupError, match="course not found"):
        client.find_course_id(SUBJECT, "9999")

    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json={})
    with pytest.raises(ValueError, match="subject course response"):
        client.find_course_id(SUBJECT, COURSE_NUMBER)


@responses.activate
def test_low_level_lookup_errors():
    client = CourseClient()
    responses.add(responses.GET, COURSE_DETAIL_API.format(id="bad"), json={"course_details": {}})
    with pytest.raises(LookupError, match="course ID not found"):
        client.get_course_data("bad")

    responses.add(responses.GET, COURSE_SECTIONS_API.format(id="bad", term=TERM), json={"sections": []})
    with pytest.raises(LookupError, match="no sections"):
        client.get_course_section_data("bad", TERM)

    responses.add(responses.GET, SECTION_DETAILS_API.format(term=TERM, id="bad"), json={"error": "missing"})
    with pytest.raises(LookupError, match="section not found"):
        client.get_section_data(TERM, "bad")


@responses.activate
def test_public_parsing_errors_are_value_errors():
    add_subject_response()
    responses.add(responses.GET, SUBJECT_COURSES_API.format(subject=SUBJECT), json=mocked_courses_data)
    responses.add(responses.GET, COURSE_DETAIL_API.format(id=COURSE_ID), json={"course_details": {"bad": True}})
    responses.add(
        responses.GET,
        COURSE_SECTIONS_API.format(id=COURSE_ID, term=TERM),
        json={"sections": [{"bad": True}]},
    )
    with pytest.raises(ValueError, match="course response"):
        CourseClient().get_course_details(TERM, SUBJECT, COURSE_NUMBER)

    responses.add(
        responses.GET,
        SECTION_DETAILS_API.format(term=TERM, id="bad"),
        json={"section_info": {}},
    )
    with pytest.raises(ValueError, match="section response"):
        CourseClient().get_section_details(TERM, "bad")


def test_optional_course_data_and_unnamed_meetings():
    catalog = {
        "descrlong": None,
        "units_minimum": 1,
        "units_maximum": 2,
    }
    raw_section = deepcopy(mocked_course_sections_data["sections"][0])
    raw_section["instructors"] = ["To be Announced"]
    raw_section["meetings"][0]["instructor"] = ""

    result = parse_course_details(catalog, [raw_section], TERM, SUBJECT, COURSE_NUMBER, COURSE_ID)

    assert result.requisites is None
    assert result.components == ()
    assert result.attributes == ()
    assert result.sections[0].instructors == ()
    assert result.sections[0].meetings[0].instructors == ()


def test_catalog_section_without_meetings():
    raw_section = deepcopy(mocked_course_sections_data["sections"][0])
    raw_section.pop("meetings")
    assert parse_catalog_section(raw_section, TERM).meetings == ()


def test_combined_section_and_unnamed_detailed_instructors():
    section_info = deepcopy(mocked_section_details_data["section_info"])
    section_info["is_combined"] = True
    section_info["combined_sections"] = [{"class_nbr": 1}, {"class_nbr": "2"}]
    section_info["meetings"][0]["instructors"] = [
        {"name": "To be Announced", "email": None},
        {"name": "-", "email": None},
    ]

    result = parse_section_details(section_info, TERM, "27815")

    assert result.details.combined_section_numbers == ("1", "2")
    assert result.meetings[0].instructors == ()


def test_parse_instructors_empty_and_email_optional():
    assert parse_instructors(()) == ()
    assert parse_instructors([{"name": "Teacher"}])[0].email is None


def test_detailed_meeting_requires_date_range():
    meeting = deepcopy(mocked_section_details_data["section_info"]["meetings"][0])
    meeting["date_range"] = "invalid"
    with pytest.raises(ValueError):
        parse_detailed_meeting(meeting)
