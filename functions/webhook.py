import json
from flask_lambda import FlaskLambda
from flask import request, jsonify

app = FlaskLambda(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook payload:", data)
    return jsonify({"message": "Webhook received"}), 200

# Netlify Functions handler
def handler(event, context):
    from flask_lambda import handler as lambda_handler
    return lambda_handler(app, event, context)

'''test'''