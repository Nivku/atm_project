# server.py
from flask import Flask, request, jsonify
from routes.accounts_route import accounts_router

app = Flask(__name__)


app.register_blueprint(accounts_router, url_prefix="/accounts"  )


@app.route("/")
def home():
    return "ATM server is running!"



def run_server():
    app.run(port=5000, debug=False, use_reloader=False)
    print("ATM server started on port 5000")


