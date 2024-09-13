from flask import Flask, request, Response
from dotenv import load_dotenv
import os

from app.utils import external_requests
from app.db import postgres

load_dotenv()

app = Flask(__name__)

# Criação da tabela
postgres.PostgresDB().conn_close()

# Lista de status possíveis
list_status = ["scheduled", "active", "landed", "cancelled", "incident", "diverted"]

@app.route("/")
def home():
    return "Hello, world!"

@app.route("/get_flights")
def get_info_flights():

    # Gera o parâmetro com a chave da API
    params = {
        "access_key":os.environ["CHAVE_API"],
    }

    # Verifica se na requisição consta o código IATA
    if not request.args.get("iata_code"):
        print(request.args.get("iata_code"))
        response = Response(
            status = 400,
            response = "Missing IATA code"
        )
        return response

    # Se requisitado, verifica se o valor é válido e gera o parâmetro com o status de vôo
    if request.args.get("status") is not None:
        if request.args.get("status") in list_status:        
            params["flight_status"] = request.args.get("status")
        else:
            response = Response(
                status = 400,
                response = "The possible status for flights are: scheduled, active, landed, cancelled, incident and diverted." 
            )
            return response

    # Cria dois grupos de parâmetros, e insere o código IATA (um para Partidas e outro para Chegadas)
    dep_params = params.copy()
    arr_params = params.copy()
    dep_params["dep_iata"] = request.args.get("iata_code")
    arr_params["arr_iata"] = request.args.get("iata_code")

    # Requisições de vôos
    all_flights = external_requests.get_all_flights(dep_params)
    all_flights += external_requests.get_all_flights(arr_params)

    # Salva os vôos obtidos no PostgreSQL
    if all_flights:
        pgclient = postgres.PostgresDB()
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

    # Retorna uma contagem com todos os vôos registrados no PostgreSQL
    return f"Teve {len(all_flights)} vôos registrados referentes ao aeroporto de {request.args.get("iata_code")}"

@app.route("/info_flights")
def select_flights():
    # Coleta todos os vôos registrados no PostgreSQL
    pgclient = postgres.PostgresDB()
    raw_flights = pgclient.select_flights_date()
    all_flights = []

    # Formata cada entrada, de acordo com o dado obtido
    for flight in raw_flights:
        all_flights.append(
            {
                "flight_date":flight[1],
                "flight_iata":flight[2],
                "flight_status":flight[3],
                "airline":flight[4],
                "dep_iata":flight[5],
                "dep_delay":flight[6],
                "arr_iata":flight[7],
                "arr_delay":flight[8]
            }
        )

    # Retorna todos os vôos registrados
    return all_flights