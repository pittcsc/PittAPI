import json
from pathlib import Path

import pytest
import responses

from pittapi.status import STATUS_URL, StatusClient, StatusSummary

SAMPLE_PATH = Path("tests/samples/status.json")


@responses.activate
def test_get_status_models_nested_data():
    responses.add(responses.GET, STATUS_URL, json=json.loads(SAMPLE_PATH.read_text()))

    result = StatusClient().get_status()

    assert isinstance(result, StatusSummary)
    assert result.components
    assert result.incidents
    assert result.incidents[0].incident_updates
    assert result.incidents[0].incident_updates[0].affected_components


@responses.activate
def test_get_status_rejects_missing_data():
    responses.add(responses.GET, STATUS_URL, json={})
    with pytest.raises(ValueError, match="missing required data"):
        StatusClient().get_status()
