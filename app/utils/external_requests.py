import requests
import math

URL_API_FLIGHTS = "https://api.aviationstack.com/v1/flights"

def get_all_flights(params:dict) -> list[dict]:
    
    api_result = requests.get(URL_API_FLIGHTS, params)       
    api_response = api_result.json()

    obj_pagination = api_response["pagination"]

    if obj_pagination["total"] > 0:
        total_extra_requests = math.ceil(obj_pagination["total"]/100)
        all_flights = api_response["data"]

        if total_extra_requests > 1:
            for i in range(1, total_extra_requests):
                params["offset"] = 100 * i
                extra_api_result = requests.get(URL_API_FLIGHTS, params)
                extra_api_response = extra_api_result.json()
                all_flights += extra_api_response["data"]
    
    return all_flights