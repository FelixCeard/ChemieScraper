import json
import os
import time

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

from document import ChemieDocumentCreator9000
from name_scraper import CASsearcher


@st.cache(allow_output_mutation=True)
def get_data():
    return []


# setting
os.environ['WDM_LOG_LEVEL'] = '0'
with open('settings.json', 'r') as f:
    settings = json.load(f)

delays = settings['delays']
selenium = delays['Selenium']
search = delays['Search']
loop = delays['Loop']

Stoff = st.text_input('Stoffname', '')

if st.button("Add row"):
    get_data().append({"Stoffe": Stoff})

st.write(pd.DataFrame(get_data()))

progress_bar = st.progress(0)


with st.spinner('Fetching information from GHS'):
    if st.button('Suchen'):
        progress_bar.progress(0)

        try:
            s = Service(settings['geckodriver path'])
            driver = webdriver.Firefox(service=s)
        except Exception as e:
            print('Invalid Geckodriver path.\nPlease add the geckodriver path in the settings (settings.json)')
            exit()

        creator9000 = ChemieDocumentCreator9000(driver=driver, delays=delays)

        percentage = 1.0 / len(get_data())
        p = 0

        for stoff in get_data():

            time.sleep(loop['LoopDelay'])
            searcher = CASsearcher(driver=driver, delays=delays)

            time.sleep(search['AfterSearch'])
            found = searcher.search(stoff['Stoffe'])

            if found:
                time.sleep(loop['DelayExtraction'])
                creator9000.extract_table()
            else:
                creator9000.not_found_stoffe.append(stoff['Stoffe'])

            p += percentage
            progress_bar.progress(p)

        creator9000.save()
        driver.close()

        with open('Sicherheitstabelle.docx', 'rb') as file:
            btn = st.download_button(
                label="Download docx",
                data=file,
                file_name="Sicherheitstabelle.docx"
            )
