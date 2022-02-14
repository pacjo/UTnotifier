import os
import time
import json
import signal
import inspect
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from colorama import init, Fore
from plyer import notification

# Catch ctrl + c
def ctrlc_handler(signum, frame):
    print(Fore.RED + "Killing webdriver")
    driver.quit()
    print(Fore.RED + "Exiting")
    exit()

signal.signal(signal.SIGINT, ctrlc_handler)

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='UserTesting.com notifier build with Selenium')
parser.add_argument('-nh', '--no_headless', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-ds', '--disable_saving', action='store_true',
                    help='Stops script from saving login details')

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
if (args.no_headless == True):
    options.add_argument("window-size=900,900")
else:
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

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
last_title = "Available tests - UserTesting"
last_count = 0
counter = 0

while (True):
    time.sleep(20)
    if ((last_title != driver.title) and (driver.title[0:1] == '(')):
        last_count = int(driver.title[1:2])
        # if (int(driver.title[1:2]) > last_count):
        print(Fore.BLUE + datetime.now().strftime("%H:%M:%S") + ": NEW TEST AVAILABLE: " + Fore.RED + driver.title[1:2])
        notification.notify(
            title="UTnotifier",
            message="Number of available tests: " + driver.title[1:2]
        )

    last_title = driver.title
    # print(last_title + "            " + driver.title)
    time.sleep(10)
    counter += 1
    if (counter >= 6): driver.refresh()
