from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook data received:", data)  # Logs the data
    return jsonify({"message": "Webhook received"}), 200

# Netlify handler
from flask import jsonify
from flask import Response as res
from flask import Response
