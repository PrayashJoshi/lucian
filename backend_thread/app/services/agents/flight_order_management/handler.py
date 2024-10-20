import requests
import os

def flight_order_management(order_id, action):
    """
    Manages flight orders, allowing actions like cancellation or retrieval.
    """
    api_key = os.getenv("AMADEUS_API_KEY")
    base_url = "https://test.api.amadeus.com/v1/booking/flight-orders"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    if action.lower() == "retrieve":
        url = f"{base_url}/{order_id}"
        response = requests.get(url, headers=headers)
    elif action.lower() == "cancel":
        url = f"{base_url}/{order_id}"
        response = requests.delete(url, headers=headers)
    else:
        return {"error": "Invalid action. Use 'retrieve' or 'cancel'."}

    if response.status_code in [200, 204]:  # Successful retrieval or deletion
        return {"message": f"Order {action} successful", "data": response.json()}
    else:
        return {"error": f"Failed to {action} order: {response.text}"}
