from flask import Flask, request, jsonify
import threading
import time
import queue
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# In-memory queue for demo (bounded to simulate backpressure)
JOB_QUEUE = queue.Queue(maxsize=100)

# Metrics
queue_length = Gauge('sensor_queue_length', 'Number of jobs currently queued')
processed = Counter('sensor_processed_total', 'Number of sensor jobs processed', ['status'])
processing_time = Histogram('sensor_processing_seconds', 'Processing time for sensor job')
failures = Counter('sensor_processing_failures_total', 'Number of job processing failures')

def worker_loop():
    while True:
        job = None
        try:
            job = JOB_QUEUE.get()
            queue_length.set(JOB_QUEUE.qsize())
            # simulate variable work: compute / aggregate + occasional failure
            start = time.time()
            # simulate processing time depending on value
            val = job.get('value', 0)
            # if value high, longer processing
            simulated = 0.2 + min(abs(float(val)) % 3, 2.0)
            time.sleep(simulated)
            # simulate random failure on specific values
            if job.get('value') == "fail":
                raise RuntimeError("simulated failure")
            processing_time.observe(time.time() - start)
            processed.labels(status='ok').inc()
        except Exception as e:
            failures.inc()
            processed.labels(status='error').inc()
        finally:
            if job is not None:
                JOB_QUEUE.task_done()
            queue_length.set(JOB_QUEUE.qsize())

@app.route("/enqueue", methods=["POST"])
def enqueue():
    try:
        payload = request.get_json(force=True)
        # non-blocking put with quick rejection if queue is full
        JOB_QUEUE.put_nowait(payload)
        queue_length.set(JOB_QUEUE.qsize())
        return jsonify({"accepted": True}), 200
    except queue.Full:
        queue_length.set(JOB_QUEUE.qsize())
        return jsonify({"accepted": False, "reason": "queue full"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # start background worker threads
    for _ in range(2):  # two worker threads per container keeps demo interesting
        t = threading.Thread(target=worker_loop, daemon=True)
        t.start()
    app.run(host="0.0.0.0", port=8001)
