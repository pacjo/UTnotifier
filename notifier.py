import os
import inspect
import json
import apprise
import argparse
from colorama import init, Fore

# Script path
filename = inspect.getframeinfo(inspect.currentframe()).filename
file_path = os.path.dirname(os.path.abspath(filename))

# ArgParser configuration
parser = argparse.ArgumentParser(description='Very simple Apprise helper for UTnotifier')
parser.add_argument('payload', help='The payload to publish')
parser.add_argument('filepath', nargs='?', default=file_path, help='Filepath of UTnotifier.py')
args = parser.parse_args()

# Initialise Colorama
init(autoreset=True)

# Get data from json
file = open(f'{args.filepath}\credentials.json', 'r')
load = json.load(file)

number_of_urls = len(load.get('apprise_urls'))

# Apprise config, taken from https://pypi.org/project/apprise/#developer-api-usage
# Create new instance 
ar = apprise.Apprise()

# Add URLs to Apprise instance (ar)
for i in range(number_of_urls):
    ar.add(load.get('apprise_urls')[i])

ar.notify(
    body=args.payload,
    title='UTnotifier'
)
