# flight_cheapest_date_search/handler.py
def flight_cheapest_date_search(origin, destination):
    """
    Finds the cheapest flight dates between two airports.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    url = f"https://test.api.amadeus.com/v1/shopping/flight-dates?origin={origin}&destination={destination}"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed: {response.status_code}"}
