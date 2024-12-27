from flask import Flask, request, jsonify, abort
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)

@app.route('/')
def homepage():
    return "Welcome to the Homepage!"

@app.route('/webhook', methods = ["POST"])
def webhook():
    if request.method == "POST":
        print ("Getting result...")
        print ("Getting results...",request.json) 
        return "success", 200
    else:
        abort(400)

if __name__ == "__main__":
    app.run()

'''test'''
