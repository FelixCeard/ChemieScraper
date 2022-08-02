import time

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from streamlit.state import SessionState

from document import ChemieDocumentCreator9000
from name_scraper import CASsearcher


@st.cache(allow_output_mutation=True)
def get_data():
    return []

Stoff = st.text_input('Stoffname', '')

if st.button("Add row"):
    get_data().append({"Stoffe": Stoff})

st.write(pd.DataFrame(get_data()))

if st.button('Suchen'):
    s = Service("C:\Program Files\Google\Chrome\Application\geckodriver.exe")
    driver = webdriver.Firefox(service=s)

    creator9000 = ChemieDocumentCreator9000(driver=driver)

    for stoff in get_data():
        time.sleep(1)
        searcher = CASsearcher(driver=driver)
        time.sleep(1)
        searcher.search(stoff['Stoffe'])
        time.sleep(1)
        creator9000.extract_table()

    creator9000.save()
    print('added table to document')

