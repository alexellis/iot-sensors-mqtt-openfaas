import datetime
import json
import os

import paho.mqtt.client as mqtt
import requests

topic_name = os.getenv("topic", "sensor-readings")
gateway_url = os.getenv("gateway_url", "http://127.0.0.1:8080")

print("Using gateway {} and topic {}".format(gateway_url, topic_name))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_name)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    with open("./samples.txt", "a") as f:
        r = json.loads(str(msg.payload))
        r["created_at"] = str(datetime.datetime.now())
        f.write(json.dumps(r) + "\n")
        f.close()

    print(msg.topic+" "+json.dumps(r))

    res = requests.post(gateway_url + "/function/accept-sample", json=r)
    print("Log reading with function: ", res.status_code)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
