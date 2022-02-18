import os
import time
import json
import signal
import inspect
import keyboard
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from colorama import init, Fore
from plyer import notification

# Register keyboard events handlers
def ctrlcHandler(signum, frame):
    print(Fore.RED + "Killing webdriver")
    driver.close()
    driver.quit()
    print(Fore.RED + "Exiting")
    exit()

def rHandler():
    if (driver.current_url == 'https://app.usertesting.com/my_dashboard/available_tests_v3'):
        driver.refresh()
        print(Fore.CYAN + "R key detected, current number of tests: " + str(numberOfTests()))
    else: print(Fore.RED + "Page has not loaded yet")

signal.signal(signal.SIGINT, ctrlcHandler)
keyboard.on_press_key("r", lambda _: rHandler())

# General purpose functions
def numberOfTests():
    if (driver.title[0:1] == '('):
        return int(driver.title[1:2])
    else:
        return 0

def sendMQTTMessage(payload):
    os.system("python sender.py " + payload)

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='UserTesting.com notifier build with Selenium')
parser.add_argument('-dh', '--disable_headless', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-ds', '--disable_saving', action='store_true',
                    help='Stops script from saving login details')
parser.add_argument('-dm', '--disable_mqtt', action='store_true',
                    help='Stops script from publishing data to mqtt server')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Shows debug messages like refresh information')

args = parser.parse_args()

# Cosmetic
init(autoreset=True)        # initialise Colorama
os.system('cls||clear')     # clear terminal before executing

print(Fore.BLUE + "  _   _ _____            _   _  __ _            ")
print(Fore.BLUE + " | | | |_   _| __   ___ | |_(_)/ _(_) ___ _ __  ")
print(Fore.BLUE + " | | | | | || '_ \ / _ \| __| | |_| |/ _ \ '__| ")
print(Fore.BLUE + " | |_| | | || | | | (_) | |_| |  _| |  __/ |    ")
print(Fore.BLUE + "  \___/  |_||_| |_|\___/ \__|_|_| |_|\___|_|    ")
print(Fore.MAGENTA + "\n https://github.com/pacjo/UTnotifier \n")

# WebDriver initialization
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
if (args.disable_headless == True):
    options.add_argument("window-size=900,900")
else:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

if (args.debug == True): print(Fore.BLUE + "Debugging is enabled, remove \"--debug\" or \"-d\" to disable it")

try:
    driver = webdriver.Chrome(options=options)
    print(Fore.GREEN + "WebDriver started")
except:
    print(Fore.RED + "Chrome WebDriver doesn't appear to be available. Make sure it's in PATH or in the script directory")
    exit()

# Access UT account
driver.get('https://app.usertesting.com/my_dashboard/available_tests_v3')

filename = inspect.getframeinfo(inspect.currentframe()).filename
file_path = os.path.dirname(os.path.abspath(filename))

try:
    file = open(f'{file_path}/credentials.json', 'r')
    load = json.load(file)
    user = load.get('user')
    password = load.get('password')
    file.close()
    driver.find_elements(By.CLASS_NAME, "form-input")[0].send_keys(user)
    driver.find_elements(By.CLASS_NAME, "form-input")[1].send_keys(password)
    time.sleep(0.5)
    driver.find_elements(By.CLASS_NAME, "btn")[1].click()
except:
    print(Fore.GREEN + "Log in to continue...")

while (driver.current_url != 'https://app.usertesting.com/my_dashboard/available_tests_v3'):
    time.sleep(1)
print(Fore.GREEN + "Logged in successfully, waiting for tests...")

# Look for available tests
last_count = 0
counter = 0

while (True):
    time.sleep(10)
    if (numberOfTests() > last_count):
        last_count = numberOfTests()
        print(Fore.BLUE + datetime.now().strftime("%H:%M:%S") + ": NEW TEST AVAILABLE: " + Fore.RED + str(last_count))
        notification.notify(
            title="UTnotifier",
            message="Number of available tests: " + str(last_count)
        )
        if (args.disable_mqtt == False): sendMQTTMessage(str(last_count))

    last_count = numberOfTests()
    time.sleep(20)
    counter += 1
    if (counter >= 6):
        driver.refresh()
        counter = 0
        if (args.debug == True): print(Fore.BLUE + datetime.now().strftime("%H:%M:%S") + ": Page refreshed")
