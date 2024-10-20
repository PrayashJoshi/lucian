# flight_inspiration_search/handler.py
import requests
import os

def flight_inspiration_search(origin):
    """
    Retrieves inspiration flights based on the origin airport.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    url = f"https://test.api.amadeus.com/v1/shopping/flight-destinations?origin={origin}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status {response.status_code}"}
