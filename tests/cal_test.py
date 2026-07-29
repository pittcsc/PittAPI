import unittest

import responses

from pittapi import cal


class CalendarTest(unittest.TestCase):
    @responses.activate
    def test_calendar_endpoints(self):
        event_data = [
            {
                "title": "Fall term begins",
                "startDateTime": "2026-08-24T00:00:00",
                "customFields": [{"label": "Event Title", "value": "First day of classes"}],
                "categoryCalendar": "Academic|Fall",
            }
        ]
        calendar_functions = {
            cal.ACADEMIC_CALENDAR_URL: cal.get_academic_calendar,
            cal.GRADES_CALENDAR_URL: cal.get_grades_calendar,
            cal.ENROLLMENT_CALENDAR_URL: cal.get_enrollment_calendar,
            cal.COURSE_CALENDAR_URL: cal.get_course_calendar,
            cal.GRADUATION_CALENDAR_URL: cal.get_graduation_calendar,
        }

        for url, calendar_function in calendar_functions.items():
            with self.subTest(url=url):
                responses.add(responses.GET, url, json=event_data, status=200)
                self.assertEqual(
                    calendar_function(),
                    [
                        cal.Event(
                            date="2026-08-24",
                            title="Fall term begins",
                            content="First day of classes",
                            meta=["Academic", "Fall"],
                        )
                    ],
                )
