#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import time

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

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



# content
Stoff = st.text_input('Stoffname', '')


if st.button("Add row"):
    get_data().append({"Stoffe": Stoff})

st.write(pd.DataFrame(get_data()))

progress_bar = st.progress(0)

allow_scrapping = True

with st.spinner('Fetching information from GHS'):
    placeholder = st.empty()
    btn = placeholder.button('GESTIS Durchsuchen', disabled=False, key='1')
    if btn:
        placeholder.empty()
        placeholder.button('GESTIS Durchsuchen', disabled=True, key='2')
        progress_bar.progress(0)
        allow_scrapping = False

        try:

            # background window
            CHROME_PATH = '/usr/bin/google-chrome'
            CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
            WINDOW_SIZE = "1920,1080"

            ff_option = Options()
            ff_option.add_argument('--headless')
            ff_option.add_argument("--disable-gpu")
            ff_option.add_argument("--window-size=%s" % WINDOW_SIZE)

            s = Service(executable_path=settings['geckodriver path'])

            driver = webdriver.Firefox(service=s, options=ff_option)
        except Exception as e:
            print(e)
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
        allow_scrapping = True
        placeholder.button('GESTIS Durchsuchen', disabled=False, key='3')
        # placeholder.empty()
