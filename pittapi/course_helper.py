from typing import List
import re
import requests

SUBJECT_CODES_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogSubjects?institution=UPITT"
SUBJECT_COURSES_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_SubjectCourses?institution=UPITT&subject={subject}"
COURSE_DETAIL_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_COURSE_CATALOG.FieldFormula.IScript_CatalogCourseDetails?institution=UPITT&course_id={id}&effdt=2018-06-30&x_acad_career={career}&crse_offer_nbr=1&use_catalog_print=Y"
COURSE_SECTIONS_API = "https://prd.ps.pitt.edu/psc/pitcsprd/EMPLOYEE/SA/s/WEBLIB_HCX_CM.H_BROWSE_CLASSES.FieldFormula.IScript_BrowseSections?institution=UPITT&campus=&location=&course_id={id}&institution=UPITT&x_acad_career={career}&term={term}&crse_offer_nbr=1"
    # id -> unique course ID, not to be confused with course code (for instance, CS 0007 has code 105611)
    # career -> for example, UGRD (undergraduate)


def _validate_term(term: str) -> str:
    """Validates that the term entered follows the pattern that Pitt does for term codes."""
    valid_terms = re.compile("2\d\d[147]")
    if valid_terms.match(str(term)):
        return str(term)
    raise ValueError("Term entered isn't a valid Pitt term.")

def _validate_subject(subject: str) -> str:
    """Validates that the subject code entered is present in the API request."""
    if subject in _get_subject_codes():
        return subject
    raise ValueError("Subject code entered isn't a valid Pitt subject code.")

def _validate_course(course: str) -> str:
    """Validates that the course name entered is 4 characters long and in string form."""
    if course == "":
        raise ValueError("Invalid course number.")
    if (type(course) is str) and (not course.isdigit()):
        raise ValueError("Invalid course number.")
    if (type(course) is int) and (course <= 0):
        raise ValueError("Invalid course number.")
    course_length = len(str(course))
    if course_length < 4:
        return ("0" * (4 - course_length)) + str(course)
    elif course_length > 4:
        raise ValueError("Invalid course number.")
    return str(course)

def _get_subject_codes() -> List[str]:
    response = requests.get(SUBJECT_CODES_API).json()
    codes = []
    for subject in response["subjects"]:
        codes.append(subject["subject"])
    return codes

def _get_internal_id_dict(subject: str) -> dict:
    response = requests.get(SUBJECT_COURSES_API.format(subject=subject)).json()
    internal_id_dict = {}
    for course in response["courses"]:
        if course["catalog_nbr"] not in internal_id_dict:
            internal_id_dict[course["catalog_nbr"]] = course["crse_id"]
    return internal_id_dict