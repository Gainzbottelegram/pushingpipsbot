import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("THREECOMMAS_API_KEY")
API_SECRET = os.getenv("THREECOMMAS_API_SECRET")
API_BASE = "https://api.3commas.io/public/api/v2"

def generate_signature(path, nonce, secret):
    message = f"{nonce}{path}"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def get_account_info():
    path = "/accounts"
    url = f"{API_BASE}{path}"
    nonce = str(int(time.time() * 1000))
    signature = generate_signature(path, nonce, API_SECRET)

    headers = {
        "APIKEY": API_KEY,
        "Signature": signature,
        "Nonce": nonce
    }

    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Failed:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    info = get_account_info()
    if info:
        print("✅ Connected to your 3Commas account(s):")
        for acc in info:
            print(f"- {acc['name']} ({acc['id']})")

