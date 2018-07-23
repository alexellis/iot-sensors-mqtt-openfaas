## Deploy OpenFaaS on Swarm

Follow the guide: https://docs.openfaas.com/deployment/docker-swarm/

## Deploy InfluxDB and Grafana

```
docker stack deploy monitor -c docker-compose.yml
```

## Create initial database

```
curl -XPOST "http://127.0.0.1:8086/query" --data-urlencode "q=CREATE DATABASE iot_environment"
```

## Create a Python3 function

Replace `alexellis2` with your name on the Docker Hub.

```bash
faas-cli new --lang python3 accept-sample --prefix=alexellis2
```

Now edit accept-sample/requirements.txt:

```
influxdb
```

Edit accept-sample.yml and add the environmental variables:


```
    environment:
       influx_host: influxdb
       influx_port: 8086
       influx_db: iot_environment
```

Now create secure secrets for your username/password for InfluxDB:

```
echo -n root | docker secret create influx-user -
echo -n root | docker secret create influx-pass -
```

Add a section under the function for the secrets:

```
    secrets:
       - influx-user
       - influx-pass
```

Create the handler:

Copy the example handler.py from the GitHub repo.

## Build/push/deploy the function

You'll need a Docker Hub account for this step.

```
faas-cli build -f accept-sample.yml && \
faas-cli push -f accept-sample.yml && \
faas-cli deploy -f accept-sample.yml --network=func_functions && \
docker service update accept-sample  --network-add=monitor_monitoring

# Update the function to access the monitoring services

```

## Send a fake sensor reading


```
echo -n '
{ "sensor": "s1",
  "temp": "30.4",
  "humidity": "54.2"
}
' | curl -i -XPOST -H "Content-Type: application/json" \
  http://127.0.0.1:8080/function/accept-sample --data-binary @- 
```

## Create the dashboard

Now you can set up the data-source for InfluxDB in Grafana.

Navigate to the Grafana interface at: http://127.0.0.1:3000, use admin/admin to log in and create your new password.

Import the data-source for InfluxDB:

```
curl -H "Content-Type: application/json" \
-X POST http://admin:admin@127.0.0.1:3000/api/datasources --data-binary '
{
  "id": 1,
  "orgId": 1,
  "name": "influx",
  "type": "influxdb",
  "typeLogoUrl": "public/app/plugins/datasource/influxdb/img/influxdb_logo.svg",
  "access": "proxy",
  "url": "http://influx:8086",
  "password": "root",
  "user": "root",
  "database": "iot_environment",
  "basicAuth": false,
  "isDefault": false,
  "jsonData": {
    "keepCookies": []
  },
  "readOnly": false
}'
```

Now create the dashboard:

```
curl -H "Content-Type: application/json" \
-X POST http://admin:admin@127.0.0.1:3000/api/dashboards/db --data-binary @./dashboard.json
```
