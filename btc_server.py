import websocket
import threading
import time
import json
from flask import Flask, jsonify

# Flask app
app = Flask(__name__)

# Global price store
latest_price = {"price": None}

# --- WebSocket event handlers ---
def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get("type") == "ticker" and data.get("product_id") == "BTC-USD":
            price = float(data["price"])
            latest_price["price"] = price
            print(f"Live BTC price: ${price:,.2f}")
    except Exception as e:
        print("Error parsing message:", e)

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed:", close_status_code, close_msg)

def on_open(ws):
    print("WebSocket connection opened. Subscribing to BTC-USD ticker.")
    subscribe_msg = {
        "type": "subscribe",
        "channels": [{
            "name": "ticker",
            "product_ids": ["BTC-USD"]
        }]
    }
    ws.send(json.dumps(subscribe_msg))

# --- Flask endpoint ---
@app.route("/price")
def get_price():
    if latest_price["price"] is not None:
        return jsonify({"price": latest_price["price"]})
    else:
        return jsonify({"error": "No price available yet"}), 503

# --- WebSocket Thread Starter ---
def start_ws():
    WS_URL = "wss://ws-feed.exchange.coinbase.com"
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    # Start WebSocket in background
    ws_thread = threading.Thread(target=start_ws)
    ws_thread.daemon = True
    ws_thread.start()

    # Start Flask server
    app.run(host="0.0.0.0", port=8080)