import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChemieScrapper():

    def init_browser(self):
        self.s = Service("C:\Program Files\Google\Chrome\Application\geckodriver.exe")
        self.driver = webdriver.Firefox(service=self.s)

    def __init__(self, driver=None):
        self.url_base = "https://gestis.dguv.de/data?name="

        if driver is not None:
            self.driver = driver
        else:
            self.init_browser()

    def scrape(self, zvg: str = None):

        if zvg is not None:
            url = self.url_base + zvg
            self.driver.get(url)

            # wartet bis seite geladen ist und data sheet gefunden hat
            delay = 3  # seconds
            try:
                geladen = WebDriverWait(self.driver, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "data-sheet-section-subchapter")))
            except TimeoutException:
                print("Loading took too much time!")

        content = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div[2]/div/div/div[2]')

        children = content.find_elements(By.XPATH, "*")

        vorschriften = None

        for child in children:
            try:
                span = child.find_element(By.XPATH, 'div/span')
                if span.text == "VORSCHRIFTEN":
                    vorschriften = child
            except Exception as e:
                pass

        blocks = vorschriften.find_elements(By.CLASS_NAME, "block")

        h, p, sw = None, None, None

        for block in blocks:
            if h is not None and p is not None and sw is not None:
                try:
                    title = block.find_element(By.XPATH, 'tbody/tr[1]/td/b').text
                    print('title', title)
                    if title == "Gefahrenhinweise - H-Sätze:":
                        h = block.find_element(By.XPATH, 'tbody/tr[2]/td/b').text
                    elif title == "Sicherheitshinweise - P-Sätze:":
                        p = block.find_element(By.XPATH, 'tbody/tr[2]/td/b').text
                    else:
                        title = block.find_element(By.XPATH, 'tbody/tr/td/table/tbody/tr/td[1]').text
                        print('title', title)
                        if title == "Signalwort:":
                            sw = block.find_element(By.XPATH, 'tbody/tr/td/table/tbody/tr/td[2]').text
                except Exception as e:
                    pass

        print('h:', h , 'p:', p , 'sw:', sw )

        # h = vorschriften.find_element(By.XPATH, "div[4]/div/table[8]/tbody/tr[2]/td").text
        # p = vorschriften.find_element(By.XPATH, "div[4]/div/table[10]/tbody/tr[2]/td").text
        # sw = vorschriften.find_element(By.XPATH, "div[4]/div/table[6]/tbody/tr/td/table/tbody/tr/td[2]").text

        div_element = vorschriften.find_element(By.XPATH, "div[4]/div/table[4]/tbody/tr")

        name = self.driver.find_element(By.CLASS_NAME, 'bevorzugtername')

        imgs = div_element.find_elements(By.CSS_SELECTOR, "img")
        src = [img.get_attribute("alt") for img in imgs]

        hs = re.findall(r'([HP\d+]+):', h)
        ps = re.findall(r'([HP\d+]+):', p)

        return hs, ps, sw, src, name.text
