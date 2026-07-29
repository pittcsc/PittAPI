import pytest
import responses

from pittapi.shuttle import (
    ARRIVAL_TIMES_URL,
    CONFIGURATION_URL,
    ROUTES_URL,
    STOP_ESTIMATES_URL,
    VEHICLE_POINTS_URL,
    Route,
    ShuttleClient,
    ShuttleConfiguration,
    StopArrival,
    VehiclePoint,
    VehicleStopEstimates,
)

CONFIGURATION = ShuttleConfiguration(
    api_key="discovered-key",
    title="Pitt Shuttles",
    map_latitude=40.44,
    map_longitude=-79.95,
    map_zoom=14,
    time_format="h:mm tt",
)
CONFIGURATION_DATA = {
    "ApiKey": "discovered-key",
    "SiteTitle": "Pitt Shuttles",
    "StartLatitude": 40.44,
    "StartLongitude": -79.95,
    "StartZoom": 14,
    "TimeDisplayFormat": "h:mm tt",
    "Unknown": "ignored",
}
SHUTTLE_URLS = (
    CONFIGURATION_URL,
    VEHICLE_POINTS_URL,
    ARRIVAL_TIMES_URL,
    STOP_ESTIMATES_URL,
    ROUTES_URL,
)
VEHICLE = {
    "GroundSpeed": 3.0,
    "Heading": 317,
    "IsDelayed": False,
    "IsOnRoute": True,
    "Latitude": 40.44,
    "Longitude": -79.95,
    "Name": "51265",
    "RouteID": 21,
    "Seconds": 46,
    "TimeStamp": "time",
    "VehicleID": 25,
}
ARRIVAL = {
    "RouteID": 21,
    "RouteStopID": 473,
    "ScheduledTimes": [{"ArrivalTimeUTC": "arrival", "AssignedVehicleId": 25, "DepartureTimeUTC": "departure"}],
    "VehicleEstimates": [{"OnRoute": True, "SecondsToStop": 332, "VehicleID": 25}],
}
ESTIMATES = {
    "VehicleID": 25,
    "Estimates": [
        {
            "Description": "Cathedral",
            "EstimateTime": "time",
            "IsArriving": True,
            "OnRoute": True,
            "RouteStopID": 473,
            "Seconds": 7,
            "Text": "Arriving",
            "VehicleId": 25,
        }
    ],
}
ROUTE = {
    "Description": "10A Upper Campus",
    "MapLatitude": 40.44,
    "MapLineColor": "#04BB84",
    "MapLongitude": -79.95,
    "MapZoom": 14,
    "RouteID": 21,
    "Stops": [
        {
            "City": "Pittsburgh",
            "Latitude": 40.44,
            "Longitude": -79.95,
            "State": "PA",
            "Zip": "15260",
            "Description": "Cathedral",
            "MapPoints": [{"Heading": 0, "Latitude": 40.44, "Longitude": -79.95}],
            "RouteID": 21,
            "RouteStopID": 473,
        }
    ],
}


def test_shuttle_urls_use_the_working_https_host():
    assert all(url.startswith("https://pittshuttle.com/") for url in SHUTTLE_URLS)


@responses.activate
def test_shuttle_endpoints_return_domain_models():
    responses.add(responses.GET, CONFIGURATION_URL, json=CONFIGURATION_DATA)
    responses.add(responses.GET, VEHICLE_POINTS_URL, json=[VEHICLE])
    responses.add(responses.GET, ARRIVAL_TIMES_URL, json=[ARRIVAL])
    responses.add(responses.GET, STOP_ESTIMATES_URL, json=[ESTIMATES])
    responses.add(responses.GET, ROUTES_URL, json=[ROUTE])
    client = ShuttleClient()

    configuration = client.get_configuration()
    assert configuration == CONFIGURATION
    assert isinstance(client.get_map_vehicle_points(configuration)[0], VehiclePoint)
    assert isinstance(client.get_route_stop_arrivals(configuration, times_per_stop=3)[0], StopArrival)
    assert isinstance(client.get_vehicle_route_stop_estimates("25", 4)[0], VehicleStopEstimates)
    route = client.get_routes(configuration)[0]
    assert isinstance(route, Route)
    assert route.stops[0].map_points[0].latitude == 40.44


@responses.activate
def test_shuttle_requires_list_response():
    responses.add(responses.GET, ROUTES_URL, json={})
    with pytest.raises(ValueError, match="contain a list"):
        ShuttleClient().get_routes(CONFIGURATION)


@responses.activate
def test_shuttle_wraps_missing_required_fields():
    responses.add(responses.GET, ROUTES_URL, json=[{}])
    with pytest.raises(ValueError, match="missing required data"):
        ShuttleClient().get_routes(CONFIGURATION)


@responses.activate
def test_shuttle_rejects_malformed_configuration():
    responses.add(responses.GET, CONFIGURATION_URL, json={})
    with pytest.raises(ValueError, match="configuration"):
        ShuttleClient().get_configuration()
