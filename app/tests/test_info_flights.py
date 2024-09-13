from app.db import postgres
import datetime
import json

class MockDB():
    def __init__(self):
        pass

    def new_connection(self):
        pass

    def create_table(self):
        pass

    def insert_flight(self, flight):
        pass

    def select_flights_date(self):
        return [
            (
                0, datetime.datetime(2019, 2, 1, 0, 0), 'AAA00', 'scheduled', 'GOL', 'XCZ', None, 'ZXC', None
            ),
            (
                1, datetime.datetime(2019, 2, 1, 0, 0), 'AAA10', 'cancelled', 'Azul', 'ZPL', None, 'XCZ', None
            )
        ]

    def conn_close(self):
        pass

def test_info_flights(app, client, monkeypatch):
    monkeypatch.setattr(postgres, 'PostgresDB', MockDB)

    res = client.get('/info_flights')
    expected = [
        {
            "airline": "GOL",
            "arr_delay": None,
            "arr_iata": "ZXC",
            "dep_delay": None,
            "dep_iata": "XCZ",
            "flight_date": "Fri, 01 Feb 2019 00:00:00 GMT",
            "flight_iata": "AAA00",
            "flight_status": "scheduled"
        },
        {
            "airline": "Azul",
            "arr_delay": None,
            "arr_iata": "XCZ",
            "dep_delay": None,
            "dep_iata": "ZPL",
            "flight_date": "Fri, 01 Feb 2019 00:00:00 GMT",
            "flight_iata": "AAA10",
            "flight_status": "cancelled"
        }
    ]
    assert res.status_code == 200
    assert expected == json.loads(res.get_data(as_text = True))