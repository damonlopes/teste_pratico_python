from app.utils import external_requests
from app.db import postgres

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
        pass

    def conn_close(self):
        pass

def mock_function(*args, **kwargs):
    if "dep_iata" in args[0]:
        return [{
            "flight_date":"2019-02-01",
            "flight":{
                "iata":"AAA00",
            },
            "flight_status":"scheduled",
            "airline":{
                "name":"GOL",
            },
            "departure":{
                "iata": "XCZ",
                "delay": None,
            },
            "arrival":{
                "iata": "ZXC",
                "delay": None,
            },
        }]
    elif "arr_iata" in args[0]:
        return [{
            "flight_date":"2019-02-01",
            "flight":{
                "iata":"AAA10",
            },
            "flight_status":"cancelled",
            "airline":{
                "name":"Azul",
            },
            "departure":{
                "iata": "ZPL",
                "delay": None,
            },
            "arrival":{
                "iata": "XCZ",
                "delay": None,
            },
        }]

def test_get_flights_no_iata_code(app, client):
    res = client.get('/get_flights')
    expected = "Missing IATA code"
    assert res.status_code == 400
    assert expected == res.get_data(as_text=True)

def test_get_flights_with_wrong_status(app, client):
    res = client.get('/get_flights?iata_code=CWB&status=alerted')
    expected = "The possible status for flights are: scheduled, active, landed, cancelled, incident and diverted."
    assert res.status_code == 400
    assert expected == res.get_data(as_text=True)

def test_get_flights_correct(app, client, monkeypatch):
    
    monkeypatch.setattr(external_requests, 'get_all_flights', mock_function)
    monkeypatch.setattr(postgres, 'PostgresDB', MockDB)

    res = client.get('/get_flights?iata_code=XCZ')
    expected = "Teve 2 vôos registrados referentes ao aeroporto de XCZ"
    assert res.status_code == 200
    assert expected == res.get_data(as_text=True)