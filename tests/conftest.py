import socket

import pytest


@pytest.fixture(autouse=True)
def block_live_network(monkeypatch):
    def fail_on_network(*args, **kwargs):
        raise AssertionError("Tests must mock all network access")

    monkeypatch.setattr(socket, "create_connection", fail_on_network)
    monkeypatch.setattr(socket.socket, "connect", fail_on_network)
