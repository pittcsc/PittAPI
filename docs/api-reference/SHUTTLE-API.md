> [Home](README.md) > Shuttle API

# Shuttle API

Pitt publishes the shuttle API key as part of its map configuration. Discover it once and pass the resulting
`ShuttleConfiguration` to methods that require it:

```python
from pittapi import ShuttleClient

with ShuttleClient() as shuttle:
    configuration = shuttle.get_configuration()
    routes = shuttle.get_routes(configuration)
    vehicles = shuttle.get_map_vehicle_points(configuration)
    arrivals = shuttle.get_route_stop_arrivals(configuration, times_per_stop=3)
```

`get_vehicle_route_stop_estimates(vehicle_id, quantity=2)` does not require the configuration. All methods return
immutable models for routes, stops, vehicles, arrivals, and estimates.
