from flask import Flask, request, jsonify, Response
import os
import requests
import time
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
worker_url = os.environ.get("WORKER_URL", "http://worker:8001/enqueue")

# prometheus metrics
ingest_requests = Counter('sensor_ingest_requests_total', 'Total ingest requests', ['status'])
forward_failures = Counter('sensor_forward_failures_total', 'Total failures forwarding to worker')
ingest_latency = Histogram('sensor_ingest_latency_seconds', 'Latency of ingest requests')

# metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# ingest endpoint
@app.route('/ingest', methods=['POST'])
def ingest():
    start = time.time()
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        ingest_requests.labels(status='bad_request').inc()
        return jsonify({"error": "Invalid payload", "details": str(e)}), 400

    # forward to worker
    try:
        r = requests.post(worker_url, json=payload, timeout=5)
        if r.status_code != 200:
            forward_failures.inc()
            ingest_requests.labels(status='forward_failure').inc()
            return jsonify({"error": "Worker rejected"}), 500
    except Exception as e:
        forward_failures.inc()
        ingest_requests.labels(status='forward_failure').inc()
        return jsonify({"error": "Failed to reach worker", "details": str(e)}), 500

    ingest_latency.observe(time.time() - start)
    return jsonify({"status": "accepted"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)