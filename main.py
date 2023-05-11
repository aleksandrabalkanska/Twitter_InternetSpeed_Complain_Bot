from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import auth

TWITTER_EMAIL = auth.EMAIL
TWITTER_USER = auth.USERNAME
TWITTER_PASS = auth.PASS
EXPECTED_DOWN = 100
EXPECTED_UP = 10
TWITTER_URL = "https://twitter.com/login"
SPEED_TEST_URL = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.chrome_driver_path = auth.CHROME_DRIVER_PATH
        self.service = Service(executable_path=self.chrome_driver_path)
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.implicitly_wait(3)
        self.dl_data = 0
        self.up_data = 0

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        time.sleep(3)
        cookie_close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
        cookie_close.click()
        speed_button = self.driver.find_element(By.CSS_SELECTOR, ".js-start-test.test-mode-multi")
        speed_button.click()
        time.sleep(80)
        self.dl_data = float(self.driver.find_element(By.XPATH,
                                                      '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text)
        self.up_data = float(self.driver.find_element(By.XPATH,
                                                      '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)

    def post_tweet(self):
        if self.dl_data < EXPECTED_DOWN or self.up_data < EXPECTED_UP:
            self.driver.get(TWITTER_URL)
            username_field = self.driver.find_element(By.NAME, 'text')
            username_field.send_keys(TWITTER_EMAIL)
            username_field.send_keys(Keys.ENTER)
            try:
                password_field = self.driver.find_element(By.NAME, 'password')
                password_field.send_keys(TWITTER_PASS)
            except NoSuchElementException:
                unusual_activity = self.driver.find_element(By.NAME, 'text')
                unusual_activity.send_keys(TWITTER_USER)
                unusual_activity.send_keys(Keys.ENTER)
                password_field = self.driver.find_element(By.NAME, 'password')
                password_field.send_keys(TWITTER_PASS)
                password_field.send_keys(Keys.ENTER)
            text_box = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Tweet text"]')
            text_box.send_keys(
                f"Hey, Internet Provider, why is my internet speed {self.dl_data}down/{self.up_data}up when I pay for {EXPECTED_DOWN}down/{EXPECTED_UP}up?")
            tweet_button = self.driver.find_element(By.XPATH,
                                                    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
            tweet_button.click()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
time.sleep(2)
bot.post_tweet()
