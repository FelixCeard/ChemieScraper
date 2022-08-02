import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CASsearcher:

    def __init__(self, driver, delays=None):
        # self.s = Service("C:\Program Files\Google\Chrome\Application\geckodriver.exe")
        self.url_base = "https://gestis.dguv.de/data?name="
        # self.url = "https://gestis.dguv.de/data?name="+cas
        # self.driver = webdriver.Firefox(service=self.s)

        self.driver = driver
        self.driver.get("https://gestis.dguv.de/search")

        self.delays = None
        if delays is not None:
            self.delays = delays

    def search(self, query: str):
        delay = self.delays['Selenium']['OpeningDelay']  # seconds

        while True:
            # reload until the page is loaded
            try:

                try:

                    WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, "input-133")))
                    break
                except TimeoutException:
                    break
            except Exception as e:
                self.driver.refresh()

        search_field = self.driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div[1]/main/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/div/div/input')

        for c in query:
            search_field.send_keys(c)

        time.sleep(self.delays['Search']['AfterSearchInput'])
        elements = self.driver.find_elements(By.CLASS_NAME, 'index-item-even')

        if len(elements) > 0:
            # click element
            elements[0].find_element(By.CLASS_NAME, 'v-responsive__content').click()
            return True
        else:
            return False
