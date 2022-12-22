import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium
[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)
This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.
Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# @st.experimental_singleton
# def Driver():
#     @st.experimental_singleton
#     def get_driver():
#         return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     options = Options()
#     options.add_argument('--disable-gpu')
#     options.add_argument('--headless')
#     driver = get_driver()
#     return driver
@st.experimental_singleton
def Driver():
    chrome_options = webdriver.ChromeOptions()
#     output_path = os.path.join(os.getcwd(),'output')
#     download_excel_prefs = {"download.default_directory" : output_path}
#     chrome_options.add_experimental_option("prefs",download_excel_prefs)   
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--enable-popup-blocking")
    chrome_options.add_argument('--disable-notifications')
#     chrome_path = ChromeDriverManager().install()
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
#     time.sleep(3)
    return driver

driver = Driver()
driver.get("https://www.lybrate.com/")
st.code(driver.page_source)
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.firefox import GeckoDriverManager

# URL = "https://www.lybrate.com/"
# TIMEOUT = 20

# st.title("Test Selenium")

# firefoxOptions = Options()
# firefoxOptions.add_argument("--headless")
# service = Service(GeckoDriverManager().install())
# driver = webdriver.Firefox(
#     options=firefoxOptions,
#     service=service,
# )
# driver.get(URL)
# st.code(driver.page_source)




        
        
        


