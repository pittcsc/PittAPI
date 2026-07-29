import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest
import responses

from pittapi.dining import (
    HOURS_URL,
    LOCATIONS_URL,
    MENU_URL,
    PERIODS_URL,
    DiningClient,
    DiningLocation,
    LocationHours,
    Menu,
    parse_menu,
    select_period,
)

SAMPLES = Path("tests/samples")
LOCATIONS_DATA = json.loads((SAMPLES / "dining_locations.json").read_text())
SCHEDULE_DATA = json.loads((SAMPLES / "dining_schedule.json").read_text())
MENU_DATA = json.loads((SAMPLES / "dining_menu.json").read_text())
DATE = datetime(2024, 4, 12)
LOCATION_ID = "610b1f78e82971147c9f8ba5"
PERIOD_ID = "659daa4d351d53068df67835"


@responses.activate
def test_get_locations_returns_models():
    responses.add(responses.GET, LOCATIONS_URL, json=LOCATIONS_DATA)
    locations = DiningClient().get_locations()
    assert isinstance(locations[0], DiningLocation)
    assert locations[0].status.label == "closed"


@responses.activate
def test_get_locations_rejects_malformed_response():
    responses.add(responses.GET, LOCATIONS_URL, json={})
    with pytest.raises(ValueError, match="location response"):
        DiningClient().get_locations()


@responses.activate
def test_get_all_and_selected_location_hours():
    url = HOURS_URL.format(date="2024-04-12")
    responses.add(responses.GET, url, json=SCHEDULE_DATA)
    responses.add(responses.GET, url, json=SCHEDULE_DATA)

    all_hours = DiningClient().get_location_hours(date=DATE)
    selected = DiningClient().get_location_hours("The Eatery", DATE)

    assert all(isinstance(item, LocationHours) for item in all_hours)
    assert selected[0].name == "The Eatery"
    assert selected[0].hours[0].start_hour == 7


@responses.activate
def test_hours_default_date_and_missing_location():
    url = HOURS_URL.format(date="2024-04-12")
    responses.add(responses.GET, url, json={"the_locations": []})
    with patch("pittapi.dining.datetime") as clock:
        clock.now.return_value = DATE
        with pytest.raises(LookupError, match="not found"):
            DiningClient().get_location_hours("Missing")


@responses.activate
def test_hours_reject_malformed_response():
    responses.add(responses.GET, HOURS_URL.format(date="2024-04-12"), json={})
    with pytest.raises(ValueError, match="hours response"):
        DiningClient().get_location_hours(date=DATE)


@responses.activate
def test_get_menu_with_named_period():
    responses.add(responses.GET, LOCATIONS_URL, json=LOCATIONS_DATA)
    responses.add(
        responses.GET,
        PERIODS_URL.format(location_id=LOCATION_ID, date="24-04-12"),
        json=MENU_DATA,
    )
    responses.add(
        responses.GET,
        MENU_URL.format(location_id=LOCATION_ID, period_id=PERIOD_ID, date="24-04-12"),
        json=MENU_DATA,
    )

    menu = DiningClient().get_location_menu("the eatery", DATE, "breakfast")

    assert isinstance(menu, Menu)
    assert menu.period.name == "Breakfast"
    assert menu.period.categories[0].items[0].nutrients
    assert menu.period.categories[0].items[0].filters


@responses.activate
def test_get_menu_uses_default_date_and_period():
    responses.add(responses.GET, LOCATIONS_URL, json=LOCATIONS_DATA)
    responses.add(
        responses.GET,
        PERIODS_URL.format(location_id=LOCATION_ID, date="24-04-12"),
        json=MENU_DATA,
    )
    responses.add(
        responses.GET,
        MENU_URL.format(location_id=LOCATION_ID, period_id=PERIOD_ID, date="24-04-12"),
        json=MENU_DATA,
    )
    with patch("pittapi.dining.datetime") as clock:
        clock.today.return_value = DATE
        assert DiningClient().get_location_menu("The Eatery").period.id == PERIOD_ID


@responses.activate
def test_menu_rejects_missing_location_and_malformed_payloads():
    responses.add(responses.GET, LOCATIONS_URL, json={"locations": []})
    with pytest.raises(LookupError, match="location not found"):
        DiningClient().get_location_menu("Missing", DATE)

    responses.add(responses.GET, LOCATIONS_URL, json=LOCATIONS_DATA)
    responses.add(responses.GET, PERIODS_URL.format(location_id=LOCATION_ID, date="24-04-12"), json={})
    with pytest.raises(ValueError, match="periods response"):
        DiningClient().get_location_menu("The Eatery", DATE)

    responses.add(responses.GET, LOCATIONS_URL, json=LOCATIONS_DATA)
    responses.add(
        responses.GET,
        PERIODS_URL.format(location_id=LOCATION_ID, date="24-04-12"),
        json=MENU_DATA,
    )
    responses.add(
        responses.GET,
        MENU_URL.format(location_id=LOCATION_ID, period_id=PERIOD_ID, date="24-04-12"),
        json={},
    )
    with pytest.raises(ValueError, match="menu response"):
        DiningClient().get_location_menu("The Eatery", DATE)


def test_period_selection_errors_and_single_period():
    period = {"id": "1", "name": "Only"}
    assert select_period([period], "ignored") is period
    with pytest.raises(LookupError, match="no dining periods"):
        select_period([], None)
    with pytest.raises(LookupError, match="period not found"):
        select_period([period, {"id": "2", "name": "Other"}], "Dinner")


def test_parse_menu_ignores_unknown_fields():
    menu_data = MENU_DATA["menu"] | {"new_provider_field": True}
    assert parse_menu(menu_data).date == "2024-04-12"
