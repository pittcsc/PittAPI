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
"""

import unittest
import responses
import pytest

from pittapi import lab
import tests.mocks.lab_mocks as lab_mocks


def create_test_url(lab_name: str) -> str:
    return lab.PITT_BASE_URL + lab.AVAIL_LAB_ID_MAP[lab_name] + "/status.json?noredir=1"


class LabTest(unittest.TestCase):
    @responses.activate
    def test_get_status_bellefield(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json=lab_mocks.mocked_bellefield_data,
        )

        result = lab.get_one_lab_data("BELLEFIELD")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="Bellefield 314",
                status=False,
                available_computers=29,
                off_computers=1,
                in_use_computers=0,
                out_of_service_computers=0,
                total_computers=30,
            ),
        )

    @responses.activate
    def test_get_status_lawrence(self):
        responses.add(
            responses.GET,
            create_test_url("LAWRENCE"),
            json=lab_mocks.mocked_lawrence_data,
        )

        result = lab.get_one_lab_data("LAWRENCE")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="David Lawrence 230",
                status=False,
                available_computers=25,
                off_computers=10,
                in_use_computers=5,
                out_of_service_computers=0,
                total_computers=40,
            ),
        )

    @responses.activate
    def test_get_status_sutherland(self):
        responses.add(
            responses.GET,
            create_test_url("SUTH"),
            json=lab_mocks.mocked_sutherland_data,
        )

        result = lab.get_one_lab_data("SUTH")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="Sutherland 120",
                status=False,
                available_computers=11,
                off_computers=1,
                in_use_computers=0,
                out_of_service_computers=0,
                total_computers=12,
            ),
        )

    @responses.activate
    def test_get_status_cathg27(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            json=lab_mocks.mocked_cathy_g27_data,
        )

        result = lab.get_one_lab_data("CATH_G27")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="Cathedral G27",
                status=False,
                available_computers=16,
                off_computers=3,
                in_use_computers=11,
                out_of_service_computers=0,
                total_computers=30,
            ),
        )

    @responses.activate
    def test_get_status_cathg62(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G62"),
            json=lab_mocks.mocked_cathy_g62_data,
        )

        result = lab.get_one_lab_data("CATH_G62")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="Cathedral G62",
                status=False,
                available_computers=26,
                off_computers=5,
                in_use_computers=0,
                out_of_service_computers=0,
                total_computers=31,
            ),
        )

    @responses.activate
    def test_get_status_benedum(self):
        responses.add(
            responses.GET,
            create_test_url("BENEDUM"),
            json=lab_mocks.mocked_benedum_data,
        )

        result = lab.get_one_lab_data("BENEDUM")

        self.assertIsInstance(result, lab.Lab)
        self.assertEqual(
            result,
            lab.Lab(
                name="Benedum B06",
                status=False,
                available_computers=28,
                off_computers=7,
                in_use_computers=4,
                out_of_service_computers=0,
                total_computers=39,
            ),
        )

    @responses.activate
    def test_get_all_lab_data(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json=lab_mocks.mocked_bellefield_data,
        )
        responses.add(
            responses.GET,
            create_test_url("LAWRENCE"),
            json=lab_mocks.mocked_lawrence_data,
        )
        responses.add(
            responses.GET,
            create_test_url("SUTH"),
            json=lab_mocks.mocked_sutherland_data,
        )
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            json=lab_mocks.mocked_cathy_g27_data,
        )
        responses.add(
            responses.GET,
            create_test_url("CATH_G62"),
            json=lab_mocks.mocked_cathy_g62_data,
        )
        responses.add(
            responses.GET,
            create_test_url("BENEDUM"),
            json=lab_mocks.mocked_benedum_data,
        )

        results = lab.get_all_labs_data()

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 6)

        for item in results:
            self.assertIsInstance(item, lab.Lab)

    def test_invalid_lab_name(self):
        with pytest.raises(
            ValueError,
            match="Invalid lab name: INVALID. Valid options: BELLEFIELD, LAWRENCE, SUTH, CATH_G27, CATH_G62, BENEDUM",
        ):
            lab.get_one_lab_data("INVALID")

    @responses.activate
    def test_handle_invalid_lab_id(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            body="Resource not found",
            status=404,
        )

        with pytest.raises(
            lab.LabAPIError,
            match="The Lab ID was invalid. Please open a GitHub issue so we can resolve this.",
        ):
            lab.get_one_lab_data("CATH_G27")

    @responses.activate
    def test_handle_unexpected_fetch_err(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            body="Unauthorized",
            status=401,
        )

        with pytest.raises(
            lab.LabAPIError,
            match="An unexpected error occurred while fetching lab data: Unauthorized",
        ):
            lab.get_one_lab_data("CATH_G27")

    @responses.activate
    def test_out_of_service_computer(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json={
                "hours": {"Test Lab": {"closed": False}},
                "state": {"computer": {"up": 3, "addr": "computer.example.edu"}},
            },
        )

        result = lab.get_one_lab_data("BELLEFIELD")

        self.assertEqual(result.out_of_service_computers, 1)

    @responses.activate
    def test_unknown_computer_state(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json={
                "hours": {"Test Lab": {"closed": False}},
                "state": {"computer": {"up": 99, "addr": "computer.example.edu"}},
            },
        )

        with pytest.raises(lab.LabAPIError, match="Unknown 'up' value for computer.example.edu"):
            lab.get_one_lab_data("BELLEFIELD")
