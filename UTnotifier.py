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
    driver.stop_client()
    # driver.close()
    driver.quit()
    print(Fore.RED + "Exiting")
    exit()

def rHandler():
    if (driver.current_url == 'https://app.usertesting.com/my_dashboard/available_tests_v3'):
        driver.refresh()
        print(Fore.CYAN + "R key detected, title: " + Fore.GREEN + driver.title + Fore.CYAN + ", number of tests: " + Fore.GREEN + str(numberOfTests()))
    else: print(Fore.RED + "Page has not loaded yet")

signal.signal(signal.SIGINT, ctrlcHandler)
keyboard.on_press_key("r", lambda _: rHandler())

# General purpose functions
def numberOfTests():
    if (driver.title[0:1] == '('):
        return int(driver.title[1:driver.title.find(")")])
    else:
        return 0

def sendMQTTMessage(payload, filepath):
    os.system(f"python {filepath}\sender.py " + payload)

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='UserTesting.com notifier build with Selenium')
parser.add_argument('browser', nargs='?', default="chrome",
                    help='Browser that should be used for this session (default: chrome)')
parser.add_argument('-dh', '--disable_headless', action='store_true',
                    help='Disables headless mode')
parser.add_argument('-ds', '--disable_saving', action='store_true',
                    help='Stops script from saving login details')
parser.add_argument('-dm', '--disable_mqtt', action='store_true',
                    help='Stops script from publishing data to mqtt server')
parser.add_argument('-dn', '--disable_notifications', action='store_true',
                    help='Stops script showing system notifications')
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

if (args.debug == True):
    print(Fore.BLUE + "Debugging is enabled, remove \"--debug\" or \"-d\" to disable it")
else:
    os.environ['WDM_LOG_LEVEL'] = '0'


# WebDriver initialization
match args.browser:
    case "chrome":      # Chrome
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--mute-audio")
        if (args.disable_headless == True):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(Fore.GREEN + "WebDriver started")

    case "firefox":      # Firefox
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager

        options = webdriver.FirefoxOptions()
        options.add_argument("--mute-audio")
        if (args.disable_headless == True):
            options.add_argument("window-size=900,900")
        else:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        print(Fore.GREEN + "WebDriver started")

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
    print(Fore.GREEN + "Input the credentails than press enter " + Fore.RED + "in script window" + Fore.GREEN + " to continue")
    input()
    if (args.disable_saving != True):
        file = open(f'{file_path}/STOCKcredentials.json', 'r')
        load = json.load(file)
        file.close()
        file = open(f'{file_path}/credentials.json', 'w')
        load["user"] = driver.find_elements(By.CLASS_NAME, "form-input")[0].get_attribute("value")
        load["password"] = driver.find_elements(By.CLASS_NAME, "form-input")[1].get_attribute("value")
        # print("Email: " + driver.find_elements(By.CLASS_NAME, "form-input")[0].get_attribute("value"))
        # print("Password: " + driver.find_elements(By.CLASS_NAME, "form-input")[1].get_attribute("value"))
        file.write(json.dumps(load))
        file.close()
        print(Fore.BLUE + "Credentails saved")

    driver.find_elements(By.CLASS_NAME, "btn")[1].click()

while (driver.current_url != 'https://app.usertesting.com/my_dashboard/available_tests_v3'):
    time.sleep(1)
print(Fore.GREEN + "Logged in successfully, waiting for tests...")

# Setup successful message
notification.notify(
    title="UTnotifier",
    message="Setup completed successfully, UTnotifier is now running",
    app_icon=f'{file_path}\\assets\\ut_icon.ico'
)

# Look for available tests
last_count = 0
counter = 0

while (True):
    time.sleep(10)
    if (numberOfTests() > last_count):
        last_count = numberOfTests()
        print(Fore.BLUE + datetime.now().strftime("%H:%M:%S") + ": NEW TEST AVAILABLE: " + Fore.RED + str(last_count))
        if(args.disable_notifications == False):
            notification.notify(
                title="UTnotifier",
                message="Number of available tests: " + str(last_count),
                app_icon=f'{file_path}\\assets\\ut_icon.ico'
            )
        if (args.disable_mqtt == False): sendMQTTMessage(str(last_count), file_path)

    last_count = numberOfTests()
    time.sleep(20)
    counter += 1
    if (counter >= 6):
        driver.refresh()
        counter = 0
        if (args.debug == True): print(Fore.BLUE + datetime.now().strftime("%H:%M:%S") + ": Page refreshed")
