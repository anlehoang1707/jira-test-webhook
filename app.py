from flask import Flask, request, jsonify
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook payload:", data)
    return jsonify({"message": "Webhook received"}), 200

if __name__ == "__main__":
    app.run(debug=True)

'''test'''