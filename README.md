# PVL_ObservabilityStack
### Project Overview

he project is part of a Modern Software course and demonstrates microservice principles, containerization, and built-in monitoring using Prometheus and Grafana. The goal of the application is to collect sensor data from three different machines, ingest the data through an API, and process it using containerized services.

Currently, sensor data is sent manually using curl commands. 

### Architecture Overview

The system consists of the following main components:

- Sensor (Machine 1–3) – Simulated sensors that generate data

- UI (Client)

    - A lightweight frontend (build with HTML and CSS)

- API Service (Python / Flask)

    - External entry point for sensor data ingestion
    - Exposes a REST endpoint /ingest
    - Validates incoming JSON payloads
    - Exposes application metrics at /metrics

- Worker Service (Python)

    - Processes incoming sensor data asynchronously
    - Simulates background processing logic
    -Exposes its own metrics endpoint for monitoring

- Prometheus

    - Periodically scrapes metrics from the API and Worker services
    - Stores time-series metrics data

- Grafana

    - Visualizes Prometheus metrics
    - Uses pre-provisioned dashboards and datasource configuration

![](/images/PVL_Diagram_flow.jpeg)

## Technologies:
- **App (api + worker)** - Python-based: Application Logic for sensor data ingestion
- **Docker & Docker Compose** – Containerization and orchestration
- **UI** – Possible for the user to interact with the application
- **CURL** – Manual testing and data submission
- **Prometheus** – Metrics collection and monitoring
- **Grafana** – Visualization and dashboards


## Services & key ports:
- api – host:8000 → container:8000 – REST ingestion endpoint

- ui – host:8080 → container:80 – frontend UI

- prometheus – host:9090 → container:9090 – metrics server

- grafana – host:3000 → container:3000 – metrics dashboards

- worker – internal only – background processing service

## Running the Application
### Prerequisites (if the user dont use Codespace)

Make sure you have the following installed:

- Docker
- Docker Compose
- requirement.txt packages

### Start the Application

To build and start all services, run:
``` 
# Start Docker Build
docker-compose up --build 
```
- This command will:
    - Build the Docker images
    - Start the API and worker services

Sensor data is sent using a curl command.

``` 
# Curl commands
curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d "{\"sensor_id\":\"sensor-1\",\"value\":42,\"status\":\"OK\"}"

```
Expose the API on localhost
### Access the application

- API: http://localhost:8000

- UI: http://localhost:8080

- Prometheus: http://localhost:9090

- Grafana: http://localhost:3000

    - Default credentials: admin / admin

## Project structure

PVL_OBSERVABILITYSTACK/

│── api/

│   │── app.py

│   │── Dockerfile

│   │── requirements.txt

│

│── worker/

│   │── worker.py

│   │── Dockerfile

│   │── requirements.txt

│

│── ui/

│   │── index.html

│   │── Dockerfile

│

│── prometheus/

│   │── prometheus.yml

│

│── grafana/

│   │── dashboards/

│   │   └── sensor_dashboard.json

│   │── provisioning/

│   │   ├── dashboards/dashboard.yml

│   │   └── datasources/data_source.yml

│

│── images/PVL_Diagram_flow.jpeg

│── docker-compose.yml

│── README.md

## Conclusion

This project demonstrates a modern, containerized microservice architecture with built-in monitoring and visualization. It highlights key concepts such as:

- Microservices and separation of concerns

- Container orchestration with Docker Compose

- RESTful API design

- Observability using Prometheus and Grafana

The system provides a solid foundation for further extensions such as persistent storage, message queues, authentication, or automated sensor simulation.

