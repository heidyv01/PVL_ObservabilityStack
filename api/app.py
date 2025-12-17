from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import requests
import time
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

worker_url = os.environ.get("WORKER_URL", "http://worker:8001/enqueue")

# define prometheus metrics
ingest_requests = Counter('sensor_ingest_requests_total', 'Total ingest requests', ['status'])
forward_failures = Counter('sensor_forward_failures_total', 'Total failures forwarding to worker')
ingest_latency = Histogram('sensor_ingest_latency_seconds', 'Latency of ingest requests')

sensor_value = Gauge('sensor_value', 'Current sensor value', ['sensor_id'])
sensor_status = Gauge('sensor_status', 'Current sensor status (0=OK,1=WARN,2=FAIL)', ['sensor_id'])

status_map = {'OK': 0, 'WARN': 1, 'FAIL': 2}

# metrics endpoint for prometheus
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# sensor endpoint
@app.route('/ingest', methods=['POST'])
def ingest():
    start = time.time()
    try:
        payload = request.get_json(force=True)
        sensor_id = payload['sensor_id']
        value = float(payload['value'])
        status = payload.get('status', 'OK').upper()
    except Exception as e:
        ingest_requests.labels(status='bad_request').inc()
        return jsonify({"error": "Invalid payload", "details": str(e)}), 400

    # set to prometheus metrics
    sensor_value.labels(sensor_id=sensor_id).set(value)
    sensor_status.labels(sensor_id=sensor_id).set(status_map[status])

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

    ingest_requests.labels(status='ok').inc()
    ingest_latency.observe(time.time() - start)
    return jsonify({"status": "accepted"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)