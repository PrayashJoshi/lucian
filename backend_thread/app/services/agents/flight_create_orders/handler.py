import requests
import os

def flight_create_orders(offer_id, passenger_details):
    """
    Creates a flight order based on a flight offer ID and passenger details.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    url = "https://test.api.amadeus.com/v1/booking/flight-orders"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Construct the request payload with flight offer ID and passenger details
    payload = {
        "data": {
            "type": "flight-order",
            "flightOffers": [{"id": offer_id}],
            "travelers": passenger_details
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:  # Success - Order created
        return response.json()
    else:
        return {"error": f"Failed to create order: {response.text}"}
