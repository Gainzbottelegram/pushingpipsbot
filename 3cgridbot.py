import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("THREECOMMAS_API_KEY")
API_SECRET = os.getenv("THREECOMMAS_API_SECRET")
API_BASE = "https://api.3commas.io/public/api/ver1"  # <- Correct 3Commas endpoint

def test_connection():
    url = f"{API_BASE}/accounts"
    headers = {
        "APIKEY": API_KEY,
        "Signature": API_SECRET,
        "Content-Type": "application/json"
    }
    r = requests.get(url, headers=headers)
    print("Status Code:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    print("API KEY:", API_KEY[:6], "...")      # Shows first 6 chars for sanity check
    print("API SECRET:", API_SECRET[:6], "...")
    test_connection()

