import os, os.path
import inspect
import json
from colorama import init, Fore

from login import login
from monitor import monitor_title
from notify import apprise_notify

if __name__ == '__main__':

    # Initialise Colorama
    init(autoreset=True)

    print(Fore.BLUE + "  _   _ _____            _   _  __ _            ")
    print(Fore.BLUE + " | | | |_   _| __   ___ | |_(_)/ _(_) ___ _ __  ")
    print(Fore.BLUE + " | | | | | || '_ \ / _ \| __| | |_| |/ _ \ '__| ")
    print(Fore.BLUE + " | |_| | | || | | | (_) | |_| |  _| |  __/ |    ")
    print(Fore.BLUE + "  \___/  |_||_| |_|\___/ \__|_|_| |_|\___|_|    ")
    print(Fore.MAGENTA + "\n https://github.com/pacjo/UTnotifier \n")

    with open('config.json', 'r') as file:
        load = json.load(file)
        username = load.get('user')
        password = load.get('password')

    # Log in and get the driver.
    driver = login(username, password)

    # Watch for page title changes.
    monitor_title(driver, apprise_notify)
