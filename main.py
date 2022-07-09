import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.keys import Keys

TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

PROMISED_DOWN = 150
PROMISED_UP = 10

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome(
            options=chrome_options,
            service=Service(ChromeDriverManager().install())
        )
        self.driver.maximize_window()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        time.sleep(2)
        self.driver.find_element("css selector", ".js-start-test").click()
        time.sleep(60*2)
        self.down = self.driver.find_element("xpath", '//*[@id="container"]/div/div[3]/div/'
                                                      'div/div/div[2]/div[3]/div[3]/div/div[3]'
                                                      '/div/div/div[2]/div[1]/div[1]/div/div[2]/span'
                                             ).text
        self.up = self.driver.find_element("xpath", '//*[@id="container"]/div/div[3]/div/div/div/'
                                                    'div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]'
                                                    '/div[1]/div[2]/div/div[2]/span'
                                           ).text

    def tweet_at_provider(self):
        time.sleep(1)
        self.driver.get("https://twitter.com/")
        time.sleep(5)
        try:
            self.driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/main/div/div/'
                                              'div[1]/div[1]/div/div[3]/div[5]/a/div'
                                     ).click()
        except NoSuchFrameException:
            time.sleep(3)
            self.driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/main/div/div/'
                                              'div[1]/div[1]/div/div[3]/div[5]/a/div'
                                     ).click()
        time.sleep(2)

        email = self.driver.find_element("name", "text")
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)

        time.sleep(2)

        password = self.driver.find_element("name", "password")
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)

        time.sleep(5)

        start_tweet = self.driver.find_element("xpath", '//*[@id="react-root"]/div/div/div[2]/header'
                                                        '/div/div/div/div[1]/div[3]/a/div'
                                               )
        start_tweet.click()

        time.sleep(2)

        message = self.driver.find_element("xpath", '//*[@id="layers"]/div[2]/div/div/div/div/div'
                                                    '/div[2]/div[2]/div/div/div/div[3]/div/div[1]'
                                                    '/div/div/div/div/div[2]/div[1]/div/div/div/div'
                                                    '/div/div/div/div/div/label/div[1]/div/div/div'
                                                    '/div/div[2]/div/div/div/div/span/br'
                                           )
        message.send_keys(f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up "
                          f"when i pay for {PROMISED_DOWN}down/{PROMISED_UP}up?")
        send_tweet = self.driver.find_element("xpath", '//*[@id="layers"]/div[2]/div/div/div/div/div'
                                                       '/div[2]/div[2]/div/div/div/div[3]/div/div[1]'
                                                       '/div/div/div/div/div[2]/div[3]/div/div/div[2]'
                                                       '/div[4]/div'
                                              )
        send_tweet.click()


internet_speed_twitter_bot = InternetSpeedTwitterBot()

internet_speed_twitter_bot.get_internet_speed()

if float(internet_speed_twitter_bot.up) < PROMISED_UP or \
        float(internet_speed_twitter_bot.down) < PROMISED_DOWN:
    internet_speed_twitter_bot.tweet_at_provider()

time.sleep(5)

internet_speed_twitter_bot.driver.quit()

