"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose  # Testing framework
import logging
import arrow
from flask_brevets import retrieve_data, set_data
from acp_times import open_time, close_time

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.WARNING)
log = logging.getLogger(__name__)


def test_zero_distances():
    start_time1 = arrow.get("2023-06-24T08:15:00")
    end_time1 = arrow.get("2023-06-24T09:15:00")
    assert open_time(0, 200, start_time1) == start_time1
    assert close_time(0, 200, start_time1) == end_time1

def test_end_times():
    start_time1 = arrow.get("2023-06-24T08:15:00")

    final_time1 = arrow.get("2023-06-25T03:03:00")
    assert open_time(600, 600, start_time1) == final_time1
    
    final_time2 = arrow.get("2023-06-26T00:15:00")
    assert close_time(600, 600, start_time1) == final_time2


def test_opening_times_1():
    # from the example on the acp page
    # 600km ACP BREVET
    # Checkpoint       Date  Time
    # ==========       ====  ====
    #     0km   start: 06/24 08:15
    #           close: 06/24 09:15
    start_time1 = arrow.get("2023-06-24T08:15:00")
    final_time1 = arrow.get("2023-06-24T08:15:00")
    assert open_time(0, 600, start_time1) == final_time1
    #   100km    open: 06/24 11:11
    #           close: 06/24 14:55
    final_time2 = arrow.get("2023-06-24T11:11:00")
    assert open_time(100, 600, start_time1) == final_time2

    #   200km    open: 06/24 14:08
    #           close: 06/24 21:35
    final_time3 = arrow.get("2023-06-24T14:08:00")
    assert open_time(200, 600, start_time1) == final_time3

    #   350km    open: 06/24 18:49
    #           close: 06/25 07:35
    final_time4 = arrow.get("2023-06-24T18:49:00")
    assert open_time(350, 600, start_time1) == final_time4

    #   550km    open: 06/25 01:23
    #           close: 06/25 20:55
    final_time5 = arrow.get("2023-06-25T01:23:00")
    assert open_time(550, 600, start_time1) == final_time5


def test_closing_times_1():
    # from the example on the acp page
    # 600km ACP BREVET
    # Checkpoint       Date  Time
    # ==========       ====  ====
    #     0km   start: 06/24 08:15
    #           close: 06/24 09:15
    start_time1 = arrow.get("2023-06-24T08:15:00")
    final_time1 = arrow.get("2023-06-24T09:15:00")
    assert close_time(0, 600, start_time1) == final_time1
    #   100km    open: 06/24 11:11
    #           close: 06/24 14:55
    final_time2 = arrow.get("2023-06-24T14:55:00")
    assert close_time(100, 600, start_time1) == final_time2

    #   200km    open: 06/24 14:08
    #           close: 06/24 21:35
    final_time3 = arrow.get("2023-06-24T21:35:00")
    assert close_time(200, 600, start_time1) == final_time3

    #   350km    open: 06/24 18:49
    #           close: 06/25 07:35
    final_time4 = arrow.get("2023-06-25T07:35:00")
    assert close_time(350, 600, start_time1) == final_time4

    #   550km    open: 06/25 01:23
    #           close: 06/25 20:55
    final_time5 = arrow.get("2023-06-25T20:55:00")
    assert close_time(550, 600, start_time1) == final_time5


def test_example_1():
    # 300km ACP BREVET
    # Checkpoint       Date  Time
    # ==========       ====  ====
    #     0km   start: 06/24 08:15
    #           close: 06/24 09:15
    start_time1 = arrow.get("2023-06-24T08:15:00")

    test_open_time = arrow.get("2023-06-24T08:15:00")
    test_close_time = arrow.get("2023-06-24T09:15:00")
    assert open_time(0, 300, start_time1) == test_open_time
    assert close_time(0, 300, start_time1) == test_close_time

    #    40km    open: 06/24 09:26
    #           close: 06/24 11:15

    test_open_time = arrow.get("2023-06-24T09:26:00")
    test_close_time = arrow.get("2023-06-24T11:15:00")
    assert open_time(40, 300, start_time1) == test_open_time
    assert close_time(40, 300, start_time1) == test_close_time

    #   200km    open: 06/24 14:08
    #           close: 06/24 21:35
    test_open_time = arrow.get("2023-06-24T14:08:00")
    test_close_time = arrow.get("2023-06-24T21:35:00")
    assert open_time(200, 300, start_time1) == test_open_time
    assert close_time(200, 300, start_time1) == test_close_time

def test_retrieval_empty():
    # Test the retrival with an empty database
    assert retrieve_data() == None

def test_insertion():
    test_data = {
        "begin_date": "2023-06-24T14:08:00",
        "brevet_distance": 200,
        "items": [50, 100,200],
    }

    assert set_data(test_data)
    retrieved_data = retrieve_data()
    retrieved_data = {
        "begin_date": retrieved_data["begin_date"],
        "brevet_distance": retrieved_data["brevet_distance"],
        "items": retrieved_data["items"],
    }
    assert retrieved_data == test_data