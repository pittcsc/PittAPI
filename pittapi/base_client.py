"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Shared HTTP lifecycle for PittAPI service clients.
"""

from __future__ import annotations

from types import TracebackType
from typing import Any, Self

import requests

__all__ = ["BaseClient"]


class BaseClient:
    """Own a requests session and apply one timeout policy consistently."""

    def __init__(self, session: requests.Session | None = None, timeout: float = 10.0) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.session = session or requests.Session()
        self.timeout = timeout
        self.owns_session = session is None

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Send a request, enforce the configured timeout, and check its status."""
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def close(self) -> None:
        """Close a session created by this client."""
        if self.owns_session:
            self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()
