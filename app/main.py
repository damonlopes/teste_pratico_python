from flask import Flask, request, Response
from dotenv import load_dotenv
import requests
import math
import os

from app.utils import external_requests

load_dotenv()

app = Flask(__name__)

list_status = ["scheduled", "active", "landed", "cancelled", "incident", "diverted"]

@app.route('/')
def home():
    return 'Hello, world!'

@app.route('/get_flights')
def get_info_flights():

    params = {
        'access_key':os.environ["CHAVE_API"],
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

    return f"Teve {len(all_flights)} vôos registrados"

    api_result = requests.get('https://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()

    obj_pagination = api_response["pagination"]

    return f"São necessários {math.ceil(obj_pagination["total"]/100)} chamadas de API para buscar todos os vôos com esses parâmetros"


    # teste = request.args.get("teste")
    # if teste is not None:
    #     return teste
    # else:
    #     return os.environ["CHAVE_API"]

# if __name__ == "__main__":
#     app.run(host = "0.0.0.0", port = 5000, debug = True)