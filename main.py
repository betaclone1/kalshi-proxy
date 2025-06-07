from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/proxy")
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(target_url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
