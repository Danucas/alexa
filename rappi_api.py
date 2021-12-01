from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pickle
import os
import requests
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium import webdriver


class Rappi:
    def __init__(self, user_device_id):
        self.driver = None
        self.device_id = user_device_id
        self.save_status('')

    def get_account_status(self):
        return self.get_status()['sign']

    def login_status(self):
        self.reload_driver()
        search_url = "https://www.rappi.com.co/login"
        self.driver.get(search_url)
        time.sleep(1)
        try:

            cel_input = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div[2]/form/div[1]/div/input')
            return False
        except Exception as e:
            print(e)
            return True

    def reload_driver(self):
        op = webdriver.chrome.options.Options()
        # session_path = f'{os.getcwd()}/sessions/{self.device_id}.session'
        user_path = f'{os.getcwd()}/sessions/{self.device_id}.user'
        op.headless = True
        op.add_argument(f'user-data-dir={user_path}')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(720, 768)

    def login(self, action, phone):
        self.reload_driver()
        if action == 'init':
            search_url = "https://www.rappi.com.co/login"
            self.driver.get(search_url)
            try:
                cel_input = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div[2]/form/div[1]/div/input')
            except Exception as e:
                return 'already signed'

            self.save_status('init', "UNSIGNED")

            cel_input.send_keys(phone)

            sms_btn = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div[2]/form/div[2]/button[2]')
            sms_btn.click()
            self.save_status('sms')

            verified_code = False
            while not verified_code:
                # Fetch the status file to check if the code is setted
                while self.get_status()['code'] is None:
                    time.sleep(1)
                    try:
                        timeout = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div/div/div[2]/span/span')
                        timeo = timeout.text.split(': ')[1]
                        if timeo == '00:00':
                            self.save_status('timeout')
                            return
                    except:
                        pass
                stat = self.get_status()
                code = stat.get('code')
                self.code4(code)
                # Check if the code works and there's no problem with the login
                try:
                    time.sleep(2)
                    email_val = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div/div/div[1]/span[2]')
                    if '@' in email_val.text:
                        self.save_status('email')
                        verified_code = True
                    elif phone in email_val.text:
                        self.save_status('resend_sms')
                        time.sleep(3)
                        continue
                except Exception as e:
                    self.save_status('finish', "SIGNED")
                    return
            while self.get_status()['code'] is None:
                time.sleep(1)
            stat = self.get_status()
            code = stat.get('code')
            self.code6(code)
            self.save_status('finish', "SIGNED")
            return 'finish'

    def code4(self, code):
        code_input1 = self.get_by_xpath('//*[@id="validation-input-0"]')
        code_input1.send_keys(code[0])
        code_input2 = self.get_by_xpath('//*[@id="validation-input-1"]')
        code_input2.send_keys(code[1])
        code_input3 = self.get_by_xpath('//*[@id="validation-input-2"]')
        code_input3.send_keys(code[2])
        code_input4 = self.get_by_xpath('//*[@id="validation-input-3"]')
        code_input4.send_keys(code[3])
        verify_btn = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div/div/div[1]/div/button')
        verify_btn.click()

    def code6(self, code):
        code_input1 = self.get_by_xpath('//*[@id="validation-input-0"]')
        code_input1.send_keys(code[0])
        code_input2 = self.get_by_xpath('//*[@id="validation-input-1"]')
        code_input2.send_keys(code[1])
        code_input3 = self.get_by_xpath('//*[@id="validation-input-2"]')
        code_input3.send_keys(code[2])
        code_input4 = self.get_by_xpath('//*[@id="validation-input-3"]')
        code_input4.send_keys(code[3])
        code_input5 = self.get_by_xpath('//*[@id="validation-input-4"]')
        code_input5.send_keys(code[4])
        code_input6 = self.get_by_xpath('//*[@id="validation-input-5"]')
        code_input6.send_keys(code[5])
        val_btn = self.get_by_xpath('//*[@id="__next"]/div/div[2]/div/div/div[1]/div/button')
        val_btn.click()

    def list_food_categories(self):
        self.reload_driver()
        self.driver.get('https://www.rappi.com.co/restaurantes')
        time.sleep(6)
        slider = self.get_by_xpath('//*[@id="__next"]/div[2]/div/div[2]/div/div/div/div/div/div')
        food_categories = []
        for child in slider.find_elements_by_xpath('.//h3'):
            if child.text and child.text != '':
                food_categories.append((child.find_element_by_xpath('..//..//..//..//'), child.text))
        return food_categories

    def list_restaurants(self, category=None):
        food_categories = self.list_food_categories()
        cat = None
        for f_cat in food_categories:
            if f_cat[1].lower() == category.lower():
                cat = f_cat[0]
        self.driver.execute_script("arguments[0].click();", cat)
        time.sleep(10)
        restaurants_container = self.get_by_xpath('//*[@id="__next"]/div[2]/div/div[4]/section/ul')
        restaurants = []
        for child in restaurants_container.find_elements_by_xpath('.//h3'):
            if child.text != '':
                restaurants.append({
                    'name': child.text,
                    'url': child.find_element_by_xpath('..//..//..').get_attribute('href')
                })
        return restaurants

    def list_menu_categories(self, restaurant):
        self.reload_driver()
        self.driver.get(restaurant)
        categories_container = self.get_by_xpath('//*[@id="restaurantLayoutContainer"]/div[2]/div[2]')
        menu_categories = []
        for child in categories_container.find_elements_by_xpath('.//span'):
            menu_categories.append(child.text)
        return menu_categories

    def get_by_xpath(self, xpath, driver=None):
        el = WebDriverWait(driver if driver else self.driver, 4).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    xpath
                )
            )
        )
        return el
    
    def save_status(self, st, sign=None):
        try:
            stats = self.get_status()
        except FileNotFoundError:
            stats = {
                "action": st,
                "code": None,
                "sign": "UNSIGNED"
            }
        if sign:
            stats['sign'] = sign
        stats['action'] = st
        stats['code'] = None
        status_path = f'{os.getcwd()}/sessions/{self.device_id}.status'
        with open(status_path, 'w') as status_file:
            status_file.write(json.dumps(stats))

    def get_status(self):
        status_path = f'{os.getcwd()}/sessions/{self.device_id}.status'
        with open(status_path, 'r') as status_file:
            return json.loads(status_file.read())
