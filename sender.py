import json
import argparse
import paho.mqtt.client as mqtt
from colorama import init, Fore

# ArgParser configuration
parser = argparse.ArgumentParser(description='Very simple MQTT publisher for UTnotifier')
parser.add_argument('payload',
                    help='The payload to publish')

args = parser.parse_args()

# Initialise Colorama
init(autoreset=True)

# JSON
file = open('credentials.json', 'r')
load = json.load(file)
json_mqtt = load.get('mqtt')
host = json_mqtt['host']
port = json_mqtt['port']
tls = json_mqtt['tls']               # currently not used
username = json_mqtt['username']
password = json_mqtt['password']
topic = json_mqtt['topic']

# MQTT connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(host, port)

    # Publish message
    client.publish(topic, args.payload)
    print(Fore.GREEN + "MQTT message published")

    client.disconnect()

except TimeoutError:
    print(Fore.RED + "MQTT server didn't respond, message not sent")
