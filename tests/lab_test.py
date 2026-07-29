import pytest
import responses

from pittapi.lab import AVAILABLE_LAB_IDS, PITT_BASE_URL, Lab, LabClient, parse_lab

LAB_NAMES = {
    "THAW": "Thaw Hall M06",
    "LAWRENCE": "David Lawrence 230",
    "CATH_LMC": "Catheral - LMC",
    "SUTH": "Sutherland 120",
    "CATH_G27": "Cathedral G27",
    "HILLMAN": "Hillman",
    "CATH_G62": "Cathedral G62",
}


def lab_url(name):
    return f"{PITT_BASE_URL}{AVAILABLE_LAB_IDS[name]}/status.json?noredir=1"


def lab_response(name):
    return {"hours": {name: {"closed": False}}, "state": {}}


def test_lab_ids_match_the_published_keyserve_maps():
    assert AVAILABLE_LAB_IDS == {
        "THAW": "bba4a8796295ff6a8df116524b40e178",
        "LAWRENCE": "98a4759fc02ca3655d56cd58abed4e90",
        "CATH_LMC": "8b2a1c62ea8a23745101b998439310d2",
        "SUTH": "8adaaeb974aa38b2283c73532c095ca7",
        "CATH_G27": "6fd5a4e0dd0a32e3ccb441e25a1a2d78",
        "HILLMAN": "6638c1e72b9a56e5119ff9848b2bdc98",
        "CATH_G62": "04853e8d1453c90a910a0b803529a3a0",
    }


@responses.activate
def test_get_one_lab():
    responses.add(responses.GET, lab_url("THAW"), json=lab_response("Thaw Hall M06"))

    result = LabClient().get_one_lab_data("THAW")

    assert result == Lab(
        name="Thaw Hall M06",
        is_closed=False,
        available_computers=0,
        off_computers=0,
        in_use_computers=0,
        out_of_service_computers=0,
        total_computers=0,
    )


@responses.activate
def test_get_all_labs():
    for key, name in LAB_NAMES.items():
        responses.add(responses.GET, lab_url(key), json=lab_response(name))

    labs = LabClient().get_all_labs_data()
    assert tuple(lab.name for lab in labs) == tuple(LAB_NAMES.values())


def test_invalid_lab_name():
    with pytest.raises(ValueError, match="invalid lab name"):
        LabClient().get_one_lab_data("INVALID")


def test_parse_all_machine_states():
    data = {
        "hours": {"Test Lab": {"closed": True}},
        "state": {
            "off": {"up": 0},
            "available": {"up": 1},
            "used": {"up": 2},
            "service": {"up": 3},
        },
    }
    result = parse_lab(data)
    assert result.is_closed
    assert result.off_computers == 1
    assert result.available_computers == 1
    assert result.in_use_computers == 1
    assert result.out_of_service_computers == 1


def test_parse_rejects_unknown_state():
    data = {"hours": {"Test": {"closed": False}}, "state": {"machine": {"up": 99}}}
    with pytest.raises(ValueError, match="unknown computer state for unknown computer"):
        parse_lab(data)


def test_parse_rejects_missing_data():
    with pytest.raises(ValueError, match="missing required data"):
        parse_lab({})
