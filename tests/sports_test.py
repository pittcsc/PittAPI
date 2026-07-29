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

from copy import deepcopy
import unittest
from unittest.mock import patch

import responses
from pittapi import sports


class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.mocked_basketball_data = {
            "team": {
                "id": "221",
                "record": {
                    "items": [
                        {
                            "description": "Overall Record",
                            "type": "total",
                            "summary": "11-21",
                        },
                        {
                            "description": "Home Record",
                            "type": "home",
                            "summary": "9-11",
                        },
                    ]
                },
                "nextEvent": [
                    {
                        "date": "2022-03-08T19:00Z",
                        "competitions": [
                            {
                                "venue": {
                                    "fullName": "Barclays Center",
                                    "address": {"city": "Brooklyn", "state": "NY"},
                                },
                                "competitors": [
                                    {
                                        "id": "221",
                                        "homeAway": "home",
                                        "team": {
                                            "id": "221",
                                            "location": "Pittsburgh",
                                            "nickname": "Pittsburgh",
                                            "abbreviation": "PITT",
                                            "displayName": "Pittsburgh Panthers",
                                        },
                                    },
                                    {
                                        "id": "103",
                                        "homeAway": "away",
                                        "team": {
                                            "id": "103",
                                            "location": "Boston College",
                                            "nickname": "Boston College",
                                            "abbreviation": "BC",
                                            "displayName": "Boston College Eagles",
                                        },
                                    },
                                ],
                                "status": {"type": {"name": "STATUS_FINAL"}},
                            }
                        ],
                    }
                ],
                "standingSummary": "12th in ACC",
            }
        }
        self.mocked_football_data = {
            "team": {
                "id": "221",
                "name": "Pittsburgh",
                "record": {
                    "items": [
                        {
                            "description": "Overall Record",
                            "type": "total",
                            "summary": "10-2",
                        },
                        {
                            "description": "Home Record",
                            "type": "home",
                            "summary": "5-2",
                        },
                    ]
                },
                "nextEvent": [
                    {
                        "id": "401405793",
                        "date": "2022-03-08T19:00Z",
                        "name": "Pittsburgh Panthers at Wake Forest Deamon Deacons",
                        "competitions": [
                            {
                                "venue": {
                                    "fullName": "Bank of America Stadium",
                                    "address": {"city": "Charlotte", "state": "NC"},
                                },
                                "competitors": [
                                    {
                                        "id": "221",
                                        "homeAway": "away",
                                        "team": {
                                            "id": "221",
                                            "location": "Pittsburgh",
                                            "nickname": "Pittsburgh",
                                            "abbreviation": "PITT",
                                            "displayName": "Pittsburgh Panthers",
                                        },
                                    },
                                    {
                                        "id": "104",
                                        "homeAway": "away",
                                        "team": {
                                            "id": "103",
                                            "location": "Wake Forest",
                                            "nickname": "Wake Forest",
                                            "abbreviation": "WAKE",
                                            "displayName": "Wake Forest Deamon Deacons",
                                        },
                                    },
                                ],
                                "status": {"type": {"name": "STATUS_IN_PROGRESS"}},
                            }
                        ],
                    }
                ],
                "standingSummary": "1st in ACC - Coastal",
            }
        }
        basketball_patcher = patch.object(
            sports,
            "_get_mens_basketball_data",
            return_value=self.mocked_basketball_data,
        )
        football_patcher = patch.object(
            sports,
            "_get_football_data",
            return_value=self.mocked_football_data,
        )
        self.mock_get_basketball_data = basketball_patcher.start()
        self.mock_get_football_data = football_patcher.start()
        self.addCleanup(basketball_patcher.stop)
        self.addCleanup(football_patcher.stop)

    def test_get_mens_basketball_record(self):
        self.assertEqual("11-21", sports.get_mens_basketball_record())

    def test_get_mens_basketball_record_offseason(self):
        offseason_data = {"team": {"id": "221", "record": {}}}
        self.mock_get_basketball_data.return_value = offseason_data

        self.assertEqual("There's no record right now.", sports.get_mens_basketball_record())

    def test_get_football_record(self):
        self.assertEqual("10-2", sports.get_football_record())

    def test_get_football_record_offseason(self):
        offseason_data = {"team": {"id": "221", "record": {}}}
        self.mock_get_football_data.return_value = offseason_data

        self.assertEqual("There's no record right now.", sports.get_football_record())

    def test_get_mens_basketball_standings(self):
        self.assertEqual("12th in ACC", sports.get_mens_basketball_standings())

    def test_get_football_standings(self):
        self.assertEqual("1st in ACC - Coastal", sports.get_football_standings())

    def test_get_next_mens_basketball_game(self):
        next_game_details = sports.get_next_mens_basketball_game()
        self.assertEqual("GAME_COMPLETE", next_game_details.status)
        self.assertEqual("103", next_game_details.opponent["id"])
        self.assertEqual("home", next_game_details.home_away)

    def test_get_next_football_game(self):
        next_game_details = sports.get_next_football_game()
        self.assertEqual("IN_PROGRESS", next_game_details.status)
        self.assertEqual("103", next_game_details.opponent["id"])
        self.assertEqual("away", next_game_details.home_away)

    def test_get_next_mens_basketball_game_offseason(self):
        offseason_data = {"team": {"nextEvent": []}}
        self.mock_get_basketball_data.return_value = offseason_data

        next_game_details = sports.get_next_mens_basketball_game()
        self.assertIsNone(next_game_details.timestamp)
        self.assertIsNone(next_game_details.opponent)
        self.assertIsNone(next_game_details.home_away)
        self.assertIsNone(next_game_details.location)
        self.assertEqual("NO_GAME_SCHEDULED", next_game_details.status)

    def test_get_next_football_game_offseason(self):
        offseason_data = {"team": {"nextEvent": []}}
        self.mock_get_football_data.return_value = offseason_data

        next_game_details = sports.get_next_football_game()
        self.assertIsNone(next_game_details.timestamp)
        self.assertIsNone(next_game_details.opponent)
        self.assertIsNone(next_game_details.home_away)
        self.assertIsNone(next_game_details.location)
        self.assertEqual("NO_GAME_SCHEDULED", next_game_details.status)

    def test_basketball_in_progress_with_pitt_second(self):
        basketball_data = deepcopy(self.mocked_basketball_data)
        competition = basketball_data["team"]["nextEvent"][0]["competitions"][0]
        competition["status"]["type"]["name"] = "STATUS_IN_PROGRESS"
        competition["competitors"].reverse()
        self.mock_get_basketball_data.return_value = basketball_data

        game = sports.get_next_mens_basketball_game()

        self.assertEqual(game.status, "IN_PROGRESS")
        self.assertEqual(game.opponent["id"], "103")
        self.assertEqual(game.home_away, "home")

    def test_basketball_scheduled_game(self):
        basketball_data = deepcopy(self.mocked_basketball_data)
        basketball_data["team"]["nextEvent"][0]["competitions"][0]["status"]["type"]["name"] = "STATUS_SCHEDULED"
        self.mock_get_basketball_data.return_value = basketball_data

        self.assertIsNone(sports.get_next_mens_basketball_game().status)

    def test_football_final_game(self):
        football_data = deepcopy(self.mocked_football_data)
        football_data["team"]["nextEvent"][0]["competitions"][0]["status"]["type"]["name"] = "STATUS_FINAL"
        self.mock_get_football_data.return_value = football_data

        self.assertEqual(sports.get_next_football_game().status, "GAME_COMPLETE")

    def test_football_scheduled_with_pitt_second(self):
        football_data = deepcopy(self.mocked_football_data)
        competition = football_data["team"]["nextEvent"][0]["competitions"][0]
        competition["status"]["type"]["name"] = "STATUS_SCHEDULED"
        competition["competitors"].reverse()
        self.mock_get_football_data.return_value = football_data

        game = sports.get_next_football_game()

        self.assertIsNone(game.status)
        self.assertEqual(game.opponent["id"], "103")
        self.assertEqual(game.home_away, "away")


class SportsHttpHelperTest(unittest.TestCase):
    @responses.activate
    def test_sports_http_helpers(self):
        basketball_data = {"team": {"id": "221"}}
        football_data = {"team": {"id": "221"}}
        responses.add(responses.GET, sports.MENS_BASKETBALL_URL, json=basketball_data, status=200)
        responses.add(responses.GET, sports.FOOTBALL_URL, json=football_data, status=200)

        self.assertEqual(sports._get_mens_basketball_data(), basketball_data)
        self.assertEqual(sports._get_football_data(), football_data)
