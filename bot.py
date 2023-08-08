from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import json
import configparser

def get_auth_token():
    config = configparser.ConfigParser()
    config.read('config.ini')

    LOGIN_URL = config.get('Credentials', 'login_url')
    USERNAME = config.get('Credentials', 'username')
    PASSWORD = config.get('Credentials', 'password')

    USERNAME_XPATH = '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div/div/div/div/form/div[1]/div/div/div/span/input'
    PASSWORD_XPATH = '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div/div/div/div/form/div[2]/div/div/div/span/div/div/div/span/input'
    LOGIN_XPATH = '/html/body/div[1]/div[2]/div[2]/div/div/div[4]/div/div/div/div/div/form/div[3]/div/div/span/button'

    driver = webdriver.Firefox()
    print('BOT:-')
    print('\tLoggin in...')
    driver.get(LOGIN_URL)
    time.sleep(2)

    username = driver.find_element(By.XPATH, USERNAME_XPATH)
    username.clear()
    username.send_keys(USERNAME)
    time.sleep(2)

    password = driver.find_element(By.XPATH, PASSWORD_XPATH)
    password.clear()
    password.send_keys(PASSWORD)
    time.sleep(2)

    login = driver.find_element(By.XPATH, LOGIN_XPATH)
    login.click()
    time.sleep(5)

    # for request in driver.requests:
    #     print(request.headers)

    # print(driver.requests[-1].headers)
    print('\tCollection Authentication token...')
    with open('access_token.txt', 'w') as file:
        headers = driver.requests[-1].headers
        file.write(str(headers))

    driver.quit()


