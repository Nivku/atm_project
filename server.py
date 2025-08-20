from flask import Flask
from routes.accounts_route import accounts_router
import os

app = Flask(__name__)


app.register_blueprint(accounts_router, url_prefix="/accounts"  )

@app.route("/")
def home():
    return "ATM server is running!"


# def run_server():
#     app.run(port=5000, debug=False, use_reloader=False)
#     print("ATM server started on port 8080")
#



if __name__ == "__main__":
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port, debug=False)