> [Home](README.md) > Laundry API

# Laundry API

`LaundryClient.get_locations()` returns Pitt's currently published rooms as `LaundryLocation` models. Pass a
discovered location to either status method:

```python
from pittapi import LaundryClient

with LaundryClient() as laundry:
    locations = laundry.get_locations()
    holland = next(location for location in locations if location.name == "Holland Hall")
    machines = laundry.get_machine_statuses(holland)
    summary = laundry.get_building_status(holland)
```

`get_machine_statuses()` returns immutable `LaundryMachine` models with the provider's status, message, remaining
time, progress, model number, and stacked/combo flags. `get_building_status()` summarizes free and total washers and
dryers.
