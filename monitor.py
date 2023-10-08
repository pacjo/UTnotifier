import time

def number_of_tests(driver):
    title = driver.title
    if (title[0:1] == '('):
        return int(title[1:title.find(")")])
    else:
        return 0

def monitor_title(driver, action_callback):
    last_count = number_of_tests(driver)

    while True:
        current_count = number_of_tests(driver)
        if current_count > last_count:
            print("New tests available, calling callback")
            action_callback('apprise.yaml', current_count)

        last_count = current_count

        print(f"Number of available tests: {current_count}")
        time.sleep(10)
