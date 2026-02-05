from flask import Flask, jsonify, request
import logging
import os
import requests

# Create the Flask application for Service B
app = Flask(__name__)

# Basic Logging Configuration
# Enables console logging with timestamp, log level, and service name
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [ServiceB] %(message)s"
)

# Service A Configuration
# Base URL for Service A (Provider
SERVICE_A_URL = "http://127.0.0.1:5001"

# Health Check Endpoint
# Used to verify whether Service B is running
@app.get("/health")
def health():
    return jsonify(status="ok", service="B")

# Combine Endpoint (Consumer Logic)
# Calls Service A over the network and combines responses
# Demonstrates failure propagation and graceful degradation
@app.get("/combine")
def combine():
     # Log every incoming request
    logging.info("Request received: %s %s", request.method, request.path)

    try:
        # Downstream Service Call
        
        # Handles failures gracefully when service A is unavailable
        # 503
        # Uncomment the line below to demonstrate normal operation (HTTP 200)
        # r = requests.get(f"{SERVICE_A_URL}/data", timeout=1.0) 
        
        # 504 time 
        # Uncomment the line below to demonstrate request timeout (HTTP 504)
        r = requests.get(f"{SERVICE_A_URL}/slow", timeout=1.0)
        # Raise exception for HTTP error responses
        r.raise_for_status()
        # Successful response from Service A
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="reachable",
            from_a=r.json()
        ), 200
    # Failure Case: Provider Down / Connection Refused
    except requests.exceptions.ConnectionError:
        # Triggered when Service A is stopped or unreachable
        logging.warning("Service A unavailable (connection error)")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="unavailable",
            from_a=None
        ), 503

    # Failure Case: Request Timeout
    except requests.exceptions.Timeout:
        # Triggered when Service A responds too slowly
        logging.warning("Service A timed out")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="timeout",
            from_a=None
        ), 504

    # Catch-All for Unexpected Errors
    except Exception as e:
        # Ensures Service B never crashes due to unexpected errors
        logging.exception("Unexpected error in /combine")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="error",
            error=str(e),
            from_a=None
        ), 502

# Application Entry Point
# Runs Service B as an independent process on port 5002
if __name__ == "__main__":
    # Port 5002 for Service B
    # Disable debug mode for stable behavior (debug=Flase)
    # Prevent multiple processes on Windows (use_reloader=False)
    # you can change to 8081
    app.run(host="127.0.0.1", port=5002, debug=False, use_reloader=False)
