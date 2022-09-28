import os
import json
import inspect
import argparse
from gotify import Gotify
import paho.mqtt.client as mqtt
from colorama import init, Fore

# Script path
filename = inspect.getframeinfo(inspect.currentframe()).filename
file_path = os.path.dirname(os.path.abspath(filename))

# ArgParser configuration
parser = argparse.ArgumentParser(description='Very simple MQTT publisher for UTnotifier')
parser.add_argument('payload', help='The payload to publish')
parser.add_argument('filepath', nargs='?', default=file_path, help='Filepath of UTnotifier.py')
args = parser.parse_args()

# Initialise Colorama
init(autoreset=True)

def send_mqtt():
    # JSON
    file = open(f'{args.filepath}\credentials.json', 'r')
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

    client.username_pw_set(username, password=password)

    try:
        client.connect(host, port)

        # Publish message
        client.publish(topic, payload=args.payload)
        print(Fore.GREEN + "MQTT message published")

        client.disconnect()

    except TimeoutError:
        print(Fore.RED + "MQTT server didn't respond, message not sent")

def send_gotify(title, message, base_url, app_token, priority=0):
    # Gotify setup
    gotify = Gotify(
        base_url=base_url,
        app_token=app_token,
    )

    # Gotify send notification
    gotify.create_message(
        message,
        title=title,
        priority=0,
    )

# JSON
file = open(f'{args.filepath}\credentials.json', 'r')
load = json.load(file)
json_gotify = load.get('gotify')
gotify_url = json_gotify['url']
gotify_token = json_gotify['token']

send_gotify("UTnotifier", args.payload, gotify_url, gotify_token)