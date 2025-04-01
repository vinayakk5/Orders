from flask import Flask, jsonify
import threading
import time
import order_service

app = Flask(__name__)

@app.route("/start", methods=["GET"])
def start_order_processing():
    """Starts continuous order fetching in a background thread."""
    def run():
        while True:
            order_service.get_order_list()
            time.sleep(5)  # Avoid excessive requests

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return jsonify({"message": "Order processing started"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
