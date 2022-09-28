import os
import json
import inspect
import argparse
from gotify import Gotify
import paho.mqtt.client as mqtt
from colorama import init, Fore
from plyer import notification

# Script path
filename = inspect.getframeinfo(inspect.currentframe()).filename
file_path = os.path.dirname(os.path.abspath(filename))

# ArgParser configuration
parser = argparse.ArgumentParser(description='Very simple MQTT publisher for UTnotifier')
parser.add_argument('payload', help='The payload to publish')
parser.add_argument('filepath', nargs='?', default=file_path, help='Filepath of UTnotifier.py')
parser.add_argument('--mqtt', action='store_true', help='Send MQTT notification')
parser.add_argument('--gotify', action='store_true', help='Send Gotify notification')
parser.add_argument('--local', action='store_true', help='Send local (PC) notification')
args = parser.parse_args()

# Initialise Colorama
init(autoreset=True)

def send_local(title, message, icon):
    notification.notify(
        title=title,
        message=message,
        app_icon=icon
    )

def send_mqtt(title, payload, host, port, tls, username, password, topic):
    # MQTT connection
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    client = mqtt.Client()
    client.on_connect = on_connect

    client.username_pw_set(username, password=password)

    try:
        client.connect(host, port)

        # Publish message
        client.publish(topic, payload=payload)
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

# Get data from JSON file
file = open(f'{args.filepath}\credentials.json', 'r')
load = json.load(file)

if(args.mqtt): 
    json_mqtt = load.get('mqtt')
    mqtt_host = json_mqtt['host']
    mqtt_port = json_mqtt['port']
    mqtt_tls = json_mqtt['tls']               # currently not used
    mqtt_username = json_mqtt['username']
    mqtt_password = json_mqtt['password']
    mqtt_topic = json_mqtt['topic']
    send_mqtt("UTnotifier", args.payload, mqtt_host, mqtt_port, mqtt_tls, mqtt_username, mqtt_password, mqtt_topic)
if(args.gotify): 
    json_gotify = load.get('gotify')
    gotify_url = json_gotify['url']
    gotify_token = json_gotify['token']
    send_gotify("UTnotifier", args.payload, gotify_url, gotify_token)
if(args.local): send_local("UTnotifier", args.payload, f'{file_path}\\assets\\ut_icon.ico')
