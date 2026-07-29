from unittest.mock import Mock

import pytest
import requests

from pittapi.base_client import BaseClient


def test_timeout_must_be_positive():
    with pytest.raises(ValueError, match="greater than zero"):
        BaseClient(timeout=0)


def test_request_applies_timeout_and_checks_status():
    session = Mock(spec=requests.Session)
    response = Mock(spec=requests.Response)
    session.request.return_value = response
    client = BaseClient(session=session, timeout=4)

    assert client.request("GET", "https://example.test") is response
    session.request.assert_called_once_with("GET", "https://example.test", timeout=4)
    response.raise_for_status.assert_called_once_with()


def test_request_preserves_explicit_timeout():
    session = Mock(spec=requests.Session)
    session.request.return_value = Mock(spec=requests.Response)

    BaseClient(session=session).request("GET", "https://example.test", timeout=2)

    session.request.assert_called_once_with("GET", "https://example.test", timeout=2)


def test_injected_session_is_not_closed():
    session = Mock(spec=requests.Session)
    with BaseClient(session=session) as client:
        assert client.session is session
    session.close.assert_not_called()


def test_owned_session_is_closed(monkeypatch):
    session = Mock(spec=requests.Session)
    monkeypatch.setattr(requests, "Session", Mock(return_value=session))

    client = BaseClient()
    client.close()

    session.close.assert_called_once_with()
