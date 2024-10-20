# flight_offers_price/handler.py
def flight_offers_price(offer_id):
    """
    Retrieves the pricing information for a specific flight offer.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    url = f"https://test.api.amadeus.com/v1/shopping/flight-offers/pricing"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"offerId": offer_id}

    response = requests.post(url, headers=headers, json=data)
    return response.json() if response.status_code == 200 else {"error": response.text}
