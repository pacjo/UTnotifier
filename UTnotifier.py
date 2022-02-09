import os
import time
from selenium import webdriver
from colorama import init, Fore

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
driver = webdriver.Chrome(options=options)

# Access UT account
driver.get('https://app.usertesting.com/my_dashboard/available_tests_v3');
print(Fore.GREEN + "Log in to continue...")

while(driver.current_url != 'https://app.usertesting.com/my_dashboard/available_tests_v3'):
    time.sleep(1)
print(Fore.GREEN + "Logged in successfully")

# Look for available tests
last_title = "Available tests - UserTesting"

print(Fore.GREEN + "Ready, waiting for tests...")
while (True):
    if ((last_title != driver.title) and (driver.title[0:1] == '(')):
        print(Fore.RED + "NEW TEST AVAILABLE: " + driver.title[1:2])

    last_title = driver.title
    time.sleep(1)
