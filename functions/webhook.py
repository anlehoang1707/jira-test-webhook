import json
from flask_lambda import FlaskLambda
from flask import request, jsonify

app = FlaskLambda(__name__)

# Temporary storage for payloads (for demonstration purposes)
payloads = []

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Parse incoming JSON payload
    payloads.append(data)  # Store payload in memory
    print("Received webhook payload:", data)  # Log payload to the console
    return jsonify({"message": "Webhook received"}), 200

@app.route('/view-payloads', methods=['GET'])
def view_payloads():
    # Return the stored payloads as JSON
    return jsonify(payloads), 200

# Netlify Functions handler
def handler(event, context):
    from flask_lambda import handler as lambda_handler
    return lambda_handler(app, event, context)


'''test'''