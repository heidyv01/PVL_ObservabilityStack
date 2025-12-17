# PVL_ObservabilityStack
### Project Overview

This project is part of a Modern Software course. The goal of the application is to collect sensor data from three different machines, ingest the data through an API, and process it using containerized services.

Currently, sensor data is sent manually using curl commands. The system is designed to be modular, scalable, and easy to deploy using Docker Compose.

## Technologies:
- App (api + worker)
- Prometheus
- Grafana
- UI


## Documentation:
- Architecture Picture
- (Build Image beforehand)
- Add compose/build commands
- Add curl/app commands necessary for usage


## Documentation:
``` 
# Start Docker Build
docker-compose up --build 
```

``` 
# Curl commands
curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d "{\"sensor_id\":\"sensor-1\",\"value\":42,\"status\":\"OK\"}"

```