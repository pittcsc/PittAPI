import pytest

from pittapi.dining import DiningClient
from pittapi.gym import GymClient
from pittapi.lab import LabClient
from pittapi.laundry import LaundryClient
from pittapi.shuttle import ShuttleClient

pytestmark = pytest.mark.live


def test_dining_locations():
    with DiningClient() as dining:
        locations = dining.get_locations()

    assert locations
    assert all(location.id and location.name for location in locations)


def test_gym_occupancy():
    with GymClient() as gyms:
        occupancy = gyms.get_all_gyms_info()

    assert occupancy
    assert all(gym.location_id and gym.facility_id for gym in occupancy)
    assert all(gym.current_count >= 0 and gym.total_capacity >= 0 for gym in occupancy)


def test_lab_discovery_and_status():
    with LabClient() as labs:
        locations = labs.get_locations()
        status = labs.get_status(locations[0])

    counted_computers = (
        status.available_computers + status.off_computers + status.in_use_computers + status.out_of_service_computers
    )
    assert locations
    assert status.total_computers == counted_computers


def test_laundry_discovery_and_machines():
    with LaundryClient() as laundry:
        locations = laundry.get_locations()
        machines = laundry.get_machine_statuses(locations[0])

    assert locations
    assert isinstance(machines, tuple)


def test_shuttle_configuration_and_routes():
    with ShuttleClient() as shuttle:
        configuration = shuttle.get_configuration()
        routes = shuttle.get_routes(configuration)

    assert configuration.api_key
    assert routes
    assert all(route.route_id for route in routes)
