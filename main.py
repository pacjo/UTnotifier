import os, os.path
import inspect
import json

from login import login
from monitor import monitor_title
from notify import apprise_notify

if __name__ == '__main__':
    with open('credentials.json', 'r') as file:
        load = json.load(file)
        username = load.get('user')
        password = load.get('password')

    # Log in and get the driver.
    driver = login(username, password)

    # Watch for page title changes.
    monitor_title(driver, apprise_notify)
