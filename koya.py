
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_address(latitude, longitude):
    api_key = os.getenv("API_KEY")
    print("Loaded API key:", api_key)

    if not api_key:
        raise ValueError("POSITIONSTACK_API_KEY was not loaded from .env")

    url = "https://api.apilayer.net/positionstack/v1/reverse"

    params = {
        "access_key": api_key.strip(),
        "query": f"{latitude},{longitude}"
    }

    print("API key loaded:", bool(api_key))
    print("Request parameters:", {
        "access_key": "***hidden***",
        "query": params["query"]
    })

    response = requests.get(url, params=params, timeout=30)

    print("Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    if data.get("data"):
        return data["data"][0].get("label")

    return "No address found"


address = get_address(6.4410, 3.5357)
print("Full address:", address)
