#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

    def __init__(self, driver=None, delays=None):
        self.url_base = "https://gestis.dguv.de/data?name="

        if driver is not None:
            self.driver = driver
        else:
            self.init_browser()

        self.delays = None
        if delays is not None:
            self.delays = delays

    def scrape(self, zvg: str = None):

        if zvg is not None:
            url = self.url_base + zvg
            self.driver.get(url)

            # wartet bis seite geladen ist und data sheet gefunden hat
            delay = self.delays['Selenium']['OpeningDelay']  # seconds
            try:
                geladen = WebDriverWait(self.driver, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "data-sheet-section-subchapter")))
            except TimeoutException:
                ...

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

        h, p, euh, sw = None, None, None, None

        for block in blocks:
            if h is None or p is None or euh is None:
                try:
                    title = block.find_element(By.XPATH, 'tbody/tr[1]/td/b').text
                    if title == "Gefahrenhinweise - H-Sätze:":
                        h = block.find_element(By.XPATH, 'tbody').text
                    elif title == "Sicherheitshinweise - P-Sätze:":
                        p = block.find_element(By.XPATH, 'tbody').text
                    elif title == "Ergänzende Gefahrenhinweise - EUH-Sätze:":
                        euh = block.find_element(By.XPATH, 'tbody').text
                except Exception as e:
                    pass

        # signal wort
        html_text = self.driver.find_element(By.CSS_SELECTOR, 'html').text
        sw = ""
        if re.findall(r'"Achtung"', html_text):
            sw = '"Achtung"'
        elif re.findall(r'"Gefahr"', html_text):
            sw = '"Gefahr"'

        div_element = vorschriften.find_element(By.XPATH, "div[4]/div/table[4]/tbody/tr")

        name = self.driver.find_element(By.CLASS_NAME, 'bevorzugtername')

        imgs = div_element.find_elements(By.CSS_SELECTOR, "img")
        src = [img.get_attribute("alt") for img in imgs]

        hs, ps = [], []

        if h is not None:
            hs = re.findall(r'([HP\d+iI]+):', h)
            if euh is not None:
                euh = re.findall(r'([HP\d+iIEU]+):', euh)
                hs = hs + euh

        if p is not None:
            ps = re.findall(r'([HP\d+iI]+):', p)


        ist_gefahr = re.findall(r'Kein gefährlicher Stoff nach GHS', html_text)
        if len(ist_gefahr) == 1:
            ist_gefahr = 'Kein gefährlicher Stoff nach GHS'
        else:
            ist_gefahr = ''

        return hs, ps, sw, src, name.text, ist_gefahr
