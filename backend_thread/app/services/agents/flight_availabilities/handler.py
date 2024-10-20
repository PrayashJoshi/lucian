import requests
import os

BASE_URL = "https://test.api.amadeus.com/v1/shopping/availability/flight-availabilities"
API_KEY = os.getenv("AMADEUS_API_KEY")

def check_availability(origin, destination, date):
    payload = {
        "origin": origin,
        "destination": destination,
        "departureDate": date
    }
    response = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload)
    return response.json()
