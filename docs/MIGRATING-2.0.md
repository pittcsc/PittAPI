# Migrating from PittAPI 1.x to 2.0

PittAPI 2.0 replaces module-level functions, named tuples, and structured dictionaries with service clients and
immutable dataclasses.

Create the client for the service you need and call the corresponding method:

```python
from pittapi import CourseClient

with CourseClient() as courses:
    result = courses.get_subject_courses("CS")
```

Clients accept an optional `requests.Session` and timeout. A client closes sessions it creates when used as a context
manager; an injected session remains owned by the caller.

Labs, laundry rooms, shuttle configuration, textbook terms, dining locations, and Pittwire topics are discovered at
runtime. Pass the returned model to later calls instead of using an embedded string or numeric identifier.

Structured results are frozen, slotted dataclasses, and nested collections are tuples. Invalid arguments or malformed
provider responses raise `ValueError`, missing requested entities raise `LookupError`, and network failures remain
standard `requests` exceptions.
