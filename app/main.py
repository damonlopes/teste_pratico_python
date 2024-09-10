from flask import Flask, request, Response
from dotenv import load_dotenv
import requests
import math
import os

from app.utils import external_requests
from app.db import postgres

load_dotenv()

app = Flask(__name__)

postgres.PostgresDB().conn_close()

list_status = ["scheduled", "active", "landed", "cancelled", "incident", "diverted"]

@app.route("/")
def home():
    return "Hello, world!"

@app.route("/get_flights")
def get_info_flights():

    params = {
        "access_key":os.environ["CHAVE_API"],
    }

    if not request.args.get("iata_code"):
        print(request.args.get("iata_code"))
        response = Response(
            status = 400,
            response = "Missing IATA code"
        )
        return response

    if request.args.get("status") is not None:
        if request.args.get("status") in list_status:        
            params["flight_status"] = request.args.get("status")
        else:
            response = Response(
                status = 400,
                response = "The possible status for flights are: scheduled, active, landed, cancelled, incident and diverted." 
            )
            return response

    dep_params = params.copy()
    arr_params = params.copy()
    dep_params["dep_iata"] = request.args.get("iata_code")
    arr_params["arr_iata"] = request.args.get("iata_code")
    # voos partindo
    all_flights = external_requests.get_all_flights(dep_params)

    # voos chegando
    all_flights += external_requests.get_all_flights(arr_params)

    # salvar os vôos registrados no PSQL
    pgclient = postgres.PostgresDB()
    if all_flights:
        for data in all_flights:
            flight = [
                data["flight_date"],
                data["flight"]["iata"],
                data["flight_status"],
                data["airline"]["name"],
                data["departure"]["iata"],
                data["departure"]["delay"],
                data["arrival"]["iata"],
                data["arrival"]["delay"],
            ]
            pgclient.insert_flight(flight)

    pgclient.conn_close()

    return f"Teve {len(all_flights)} vôos registrados"