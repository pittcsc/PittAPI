# Pitt API

![Build Status](https://img.shields.io/github/actions/workflow/status/pittcsc/PittAPI/autotest.yml?branch=dev)
![License](https://img.shields.io/badge/license-GPLv2-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.13-green.svg)
[![PyPI Version](https://img.shields.io/pypi/v/pittapi.svg)](https://pypi.org/project/PittAPI/)

PittAPI is an unofficial Python library for public data from the University of Pittsburgh and related services.
Version 2.0 provides synchronous service clients and immutable, typed result models.

## Installation

PittAPI requires Python 3.13. Add it to a uv-managed project with:

```sh
uv add pittapi
```

## Client basics

Each data source has its own client. A client accepts an optional `requests.Session` and a timeout in seconds. When
PittAPI creates the session, using the client as a context manager closes it automatically:

```python
from pittapi import CourseClient

with CourseClient(timeout=15) as courses:
    cs = courses.get_subject_courses("CS")
    for course in cs.courses:
        print(course.course_number, course.course_title)
```

An injected session remains owned by the caller and is not closed by PittAPI.

All structured results are frozen, slotted dataclasses. Nested collections are tuples, so callers cannot accidentally
change a response after it is returned.

## Examples

```python
from datetime import datetime

from pittapi import DiningClient, LibraryClient, NewsClient

with DiningClient() as dining:
    locations = dining.get_locations()
    hours = dining.get_location_hours("The Eatery", datetime(2024, 4, 12))

with LibraryClient() as library:
    books = library.get_documents("computer science")

with NewsClient() as news:
    topics = news.get_topics()
    technology = next(topic for topic in topics if topic.name == "Technology & Science")
    articles = news.get_articles_by_topic(technology, max_num_results=5)
```

Services whose available resources change over time provide discovery methods:

```python
from pittapi import LabClient, LaundryClient, ShuttleClient, TextbookClient
from pittapi.textbook import CourseInfo

with LabClient() as labs:
    locations = labs.get_locations()
    status = labs.get_status(locations[0])

with LaundryClient() as laundry:
    rooms = laundry.get_locations()
    machines = laundry.get_machine_statuses(rooms[0])

with ShuttleClient() as shuttle:
    configuration = shuttle.get_configuration()
    routes = shuttle.get_routes(configuration)

with TextbookClient() as textbooks:
    term = next(term for term in textbooks.get_terms() if term.inquiry_enabled)
    textbooks.select_term(term)
    books = textbooks.get_textbooks_for_course(CourseInfo("CS", "0441"))
```

Network and HTTP failures remain standard `requests` exceptions. Invalid arguments or malformed provider responses
raise `ValueError`; a valid lookup with no matching entity raises `LookupError`.

Users upgrading from PittAPI 1.x should read the [2.0 migration guide](docs/MIGRATING-2.0.md).

## Development

Install the locked Python 3.13 development environment and run the full validation suite:

```sh
uv sync --locked
uv run pytest --cov=pittapi --cov-branch --cov-fail-under=100 tests/
uv run pre-commit run --all-files
```

See the [contributing guidelines](CONTRIBUTING.md) for the project’s readability and testing expectations.

## License

PittAPI is licensed under the [GPLv2](LICENSE).
