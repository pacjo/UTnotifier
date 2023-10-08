from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(username, password):
    driver = webdriver.Chrome()  # TODO: add other browsers, maybe?
    driver.get('https://app.usertesting.com/my_dashboard/available_tests_v3')

    try:
        # Wait for the "form-input" element to be available before proceeding.
        form_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-input"))
        )

        # Once the element is available, proceed with login.
        username_field = driver.find_elements(By.CLASS_NAME, "form-input")[0]
        password_field = driver.find_elements(By.CLASS_NAME, "form-input")[1]
        login_button = driver.find_elements(By.CLASS_NAME, "btn")[1]

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
    except Exception as e:
        print(f"An error occurred while waiting for the 'form-input' element: {str(e)}")

    return driver
