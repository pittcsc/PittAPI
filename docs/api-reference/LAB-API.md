> [Home](README.md) > Lab API

# Lab API

`LabClient.get_locations()` returns the computing labs currently published by Pitt as `LabLocation` models. Pass one
of those models to `get_status()`:

```python
from pittapi import LabClient

with LabClient() as labs:
    locations = labs.get_locations()
    thaw = next(location for location in locations if location.name == "Thaw Hall M06")
    status = labs.get_status(thaw)
```

`get_all_statuses()` discovers the locations and returns a `Lab` for each one in the same order. A `Lab` contains
open/closed state and counts for available, off, in-use, out-of-service, and total computers.
