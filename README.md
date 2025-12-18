# PVL_ObservabilityStack
### Project Overview

This project is part of a Modern Software course. The goal of the application is to collect sensor data from three different machines, ingest the data through an API, and process it using containerized services.

Currently, sensor data is sent manually using curl commands. 

### Architecture Overview

The system consists of the following main components:

- Sensor (Machine 1–3) – Simulated sensors that generate data
- API Service – Receives sensor data via HTTP requests
- Worker Service – Processes incoming data asynchronously
- Docker Compose – Orchestrates all services
![](/images/PVL_Diagramm.JPG)

## Technologies:
- App (api + worker)
- Prometheus
- Grafana
- UI
- **App (api + worker)** - Python: Application Logic
- **Docker & Docker Compose** – Containerization and orchestration
- **UI** – Possible for the user to interact with the application
- **CURL** – Manual testing and data submission
- **Prometheus** – Metrics collection and monitoring
- **Grafana** – Visualization and dashboards


## Documentation:
- Architecture Picture
- (Build Image beforehand)
- Add compose/build commands
- Add curl/app commands necessary for usage

## Running the Application
### Prerequisites

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
curl -X POST http://localhost:8000/ingest \
-H "Content-Type: application/json" \
-d '{"sensor_id": "sensor-1", "value": 42}'

```
Expose the API on localhost
## Documentation:
``` 
# Start Docker Build
docker-compose up --build 
```

``` 
# Curl commands
curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d "{\"sensor_id\":\"sensor-1\",\"value\":42,\"status\":\"OK\"}"

```