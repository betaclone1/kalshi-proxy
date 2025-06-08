from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = 'f513bc50-8660-44f5-9458-ac6b4c3773d6'
BASE_URL = 'https://trading-api.kalshi.com/trade-api/v2'
MARKET_TICKER = 'BTC-YES-T05:00'  # Update this hourly if needed

@app.route("/btc-price", methods=["GET"])
def get_btc_price():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    url = f"{BASE_URL}/markets/{MARKET_TICKER}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)