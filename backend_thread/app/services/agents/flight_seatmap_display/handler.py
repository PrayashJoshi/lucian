import requests
import os

BASE_URL = "https://test.api.amadeus.com/v1/shopping/seatmaps"
API_KEY = os.getenv("AMADEUS_API_KEY")

def get_seatmap(flight_offer_id):
    response = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json={"flightOfferId": flight_offer_id})
    return response.json()
