> [Home](README.md) > People API

# People API

`PeopleClient.get_person(query)` returns matching directory entries as immutable `Person` models:

```python
from pittapi import PeopleClient

with PeopleClient() as people:
    matches = people.get_person("Jane Doe")
```

Each person's `fields` tuple contains `PersonField` models. Field names are the non-empty labels published by Pitt;
repeated labels are grouped into one field whose `values` are a tuple. This preserves new directory fields without a
PittAPI release.
