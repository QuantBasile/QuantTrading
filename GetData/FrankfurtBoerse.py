# -*- coding: utf-8 -*-
"""
This scripts takes historical data from Frankfurt Boerse using Selenium
"""

import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)
    
def click_checkbox(driver, checkbox_id, label):
    try:
        checkbox = driver.find_element(By.ID, checkbox_id)
        js_click(driver, checkbox)
        logging.info(f"{label} option enabled.")
    except Exception as e:
        logging.warning(f"Could not enable {label}: {e}")
        
def input_date(driver, date_value, index=0):
    try:
        date_inputs = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input.form-control.text-center'))
        )
        date_input = date_inputs[index]  # Use index 0 for "From Date", 1 for "To Date"
        js_click(driver, date_input)
        date_input.clear()
        date_input.send_keys(date_value)
        date_input.send_keys(Keys.RETURN)
        logging.info(f"Date set: {date_value}")
    except Exception as e:
        logging.warning(f"Could not set date {date_value}: {e}")

def AbrufData(Boerse="Frankfurt",aktie_or_ISIN="deutsche-bank-ag",split=False,
              dividends=False,Bezugsrechte=False,Date_von="",Date_bis=""):
    
    url = f"https://www.boerse-frankfurt.de/aktie/{aktie_or_ISIN}/kurshistorie/historische-kurse-und-umsaetze"
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin GUI)
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    WebDriverWait(driver, 3)
    
    if Boerse == "Xetra": 
        try:
            select_element = driver.find_element(By.CLASS_NAME, "custom-select")
            js_click(driver, select_element)
            select = Select(select_element)
            select.select_by_visible_text("Xetra")
            logging.info("Xetra selected.")
        except Exception as e:
            logging.warning(f"Could not select Xetra: {e}")
        
    if split:
        click_checkbox(driver, 'input-clean-splits', "Split")
    if dividends:
        click_checkbox(driver, 'input-clean-dividends', "Dividends")
    if Bezugsrechte:
        click_checkbox(driver, 'input-clean-subscription-rights', "Subscription Rights")
        
    if Date_von:
        input_date(driver, Date_von, index=0)  # From Date
    if Date_bis:
        input_date(driver, Date_bis, index=1)  # To Date
        
    try:
        button = driver.find_element(By.CLASS_NAME, "form-button")
        js_click(driver, button)
        logging.info("Data fetch initiated.")
    except Exception as e:
        logging.warning(f"Could not click fetch button: {e}")

    # Wait for data table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "widget-table"))
    )    
    
    df_list = []
    wait = WebDriverWait(driver, 1)
    while True:
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        table = soup.find('table', {'class': 'widget-table'}) 
        df = extract_table_data(table)
        df_list.append(df)
        try:
            # Attempt to find and click the "next page" button
            next_page_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.page-bar-type-button.btn.btn-lg[title^="Zeige Seite"] i span.icon-arrow-step-right-grey-big')))
            next_page_button.click()
            time.sleep(2)  # Wait for the next page to load
            
            content_after_click = driver.page_source
            if content == content_after_click:
                print("Page content did not change. No more pages to navigate.")
                break
        except:
            # Break the loop if the next page button is not found or not clickable
            print("No more pages to navigate.")
            break
    

    driver.quit()
    
    final_df = pd.concat(df_list, ignore_index=True)
    
    return final_df

def extract_table_data(table):
    thead = table.find('thead')
    columns = [header.text.strip() for header in thead.find_all('th')] if thead else []
    tbody = table.find('tbody')
    data = [[col.text.strip() for col in row.find_all('td')] for row in tbody.find_all('tr')] if tbody else []
    df = pd.DataFrame(data, columns=columns)
    return df