import re
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CASsearcher:

    def __init__(self, driver):
        # self.s = Service("C:\Program Files\Google\Chrome\Application\geckodriver.exe")
        self.url_base = "https://gestis.dguv.de/data?name="
        # self.url = "https://gestis.dguv.de/data?name="+cas
        # self.driver = webdriver.Firefox(service=self.s)

        self.driver = driver
        self.driver.get("https://gestis.dguv.de/search")

    def search(self, query:str):
        delay = 3  # seconds
        try:
            # geladen = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "data-sheet-section-subchapter")))
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, "input-133")))
        except TimeoutException:
            print("Loading took too much time!")

        search_field = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/input')

        for c in query:
            search_field.send_keys(c)



        time.sleep(1)
        elements = self.driver.find_elements(By.CLASS_NAME, 'index-item-even')

        # click element
        elements[0].find_element(By.CLASS_NAME, 'v-responsive__content').click()

