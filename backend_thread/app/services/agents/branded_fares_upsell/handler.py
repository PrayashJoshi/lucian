import requests
import os

BASE_URL = "https://test.api.amadeus.com/v1/shopping/flight-offers/upselling"
API_KEY = os.getenv("AMADEUS_API_KEY")

def get_upsell_offers(offer_id):
    payload = {"offerId": offer_id}
    response = requests.post(BASE_URL, headers={"Authorization": f"Bearer {API_KEY}"}, json=payload)
    return response.json()
