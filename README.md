# PVL_ObservabilityStack

Technologies:
- App (api + worker)
- Prometheus
- Grafana
- UI


Documentation:
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