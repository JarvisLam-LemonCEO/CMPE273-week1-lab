from flask import Flask, jsonify, request
import logging
import time
import os

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [ServiceA] %(message)s"
)

@app.get("/health")
def health():
    return jsonify(status="ok", service="A")

@app.get("/data")
def data():
    logging.info("Request received: %s %s", request.method, request.path)
    return jsonify(message="Hello from Service A", pid=os.getpid())

@app.get("/slow")
def slow():
    logging.info("Request received: %s %s (slow)", request.method, request.path)
    time.sleep(3)
    return jsonify(message="Slow response from A")

if __name__ == "__main__":
    # Port 5001 for Service A
    app.run(host="127.0.0.1", port=5001)
