## MQTT Broker

### Install the MQTT Python client:

```
sudo pip install paho.mqtt.client
```

### Run the broker

Open `tmux` so that we can keep the process running.

Now run the code replacing the IP address with your OpenFaaS gateway:

```
topic=sensor-readings gateway_url=http://127.0.0.1:8080 python app.py
```

Hit Control + A + D to disconnect the terminal and use `tmux attach` later on to re-attach.

