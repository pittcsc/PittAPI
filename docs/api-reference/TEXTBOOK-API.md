> [Home](README.md) > Textbook API

# Textbook API

Textbook terms are discovered from the bookstore instead of being embedded in PittAPI. Select a term before looking
up a course:

```python
from pittapi import TextbookClient
from pittapi.textbook import CourseInfo

with TextbookClient() as textbooks:
    terms = textbooks.get_terms()
    fall = next(term for term in terms if term.name == "Fall 26")
    textbooks.select_term(fall)
    books = textbooks.get_textbooks_for_course(
        CourseInfo("CS", "0441", instructor="GARRISON III")
    )
```

A term can also be supplied to `TextbookClient(term=...)`. Changing it with `select_term()` clears cached
term-specific subjects. `get_textbooks_for_courses()` accepts a list or tuple and preserves course order.

`CourseInfo` normalizes the subject and instructor to uppercase and pads course numbers to four digits. Specify an
instructor or four-digit section number when a course has multiple distinguishable sections.
