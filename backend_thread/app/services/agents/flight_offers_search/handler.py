# flight_offers_search/handler.py
def flight_offers_search(origin, destination, departure_date):
    """
    Searches for available flight offers based on origin, destination, and date.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {"originLocationCode": origin, "destinationLocationCode": destination, "departureDate": departure_date}
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else {"error": response.text}
