import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Grab 3Commas API key/secret from .env
API_KEY = os.getenv("THREECOMMAS_API_KEY")
API_SECRET = os.getenv("THREECOMMAS_API_SECRET")
API_BASE = "https://api.3commas.io/public/api/ver1"

def check_account():
    url = f"{API_BASE}/accounts"
    headers = {
        "APIKEY": API_KEY,
        "Signature": API_SECRET
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS: Connected to 3Commas! Account info:")
            print(response.json())
        else:
            print("❌ ERROR: Could not fetch account info.")
            print(response.text)
    except Exception as e:
        print("❌ Exception occurred:", str(e))

if __name__ == "__main__":
    check_account()
