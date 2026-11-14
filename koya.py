
import requests

def get_address(latitude, longitude, api_key):
    url = "http://api.positionstack.com/v1/reverse"

    params = {
        "access_key": api_key,
        "query": f"{latitude},{longitude}"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if data["data"]:
        return data["data"][0]["label"]

    return "No address found"


address = get_address(6.4410, 3.5357, "YOUR_API_KEY")
print(address)
