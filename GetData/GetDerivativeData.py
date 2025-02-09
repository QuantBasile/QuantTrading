# -*- coding: utf-8 -*-
"""
This scripts takes ISIN from derivative and outputs the underlying
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

def get_Data_derivate(ISIN="DE000DY2XH19"):
    base_url = f"https://www.boerse-frankfurt.de/zertifikat/{ISIN}"
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin GUI)
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(base_url)
    
    try:
        stammdaten_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Stammdaten')]"))
        )
        stammdaten_button.click()
        time.sleep(3)  # Give time for the page to load Stammdaten content
    except Exception as e:
        print("Error clicking Stammdaten button:", e)
        driver.quit()
        return None

    # Extract page source after clicking
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    stammdaten_data = {}
    stammdaten_heading = soup.find("h2", class_="widget-table-headline", string="Stammdaten")
    table = stammdaten_heading.find_next("table", class_="widget-table")
    for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 2:  # Ensure there are key-value pairs
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                stammdaten_data[key] = value
        
    basiswert_data = {}
    basiswert_heading = soup.find("h2", class_="widget-table-headline", string="Basiswert")
    table = basiswert_heading.find_next("table", class_="widget-table")
    for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) == 2:  # Ensure there are key-value pairs
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                basiswert_data[key] = value
    
    return stammdaten_data,basiswert_data


def GetQuotesZertifikate(ISIN="DE000DY2XH19",date = "05/02/2025"):
    base_url = f"https://www.boerse-frankfurt.de/zertifikat/{ISIN}"
    
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin GUI)
    options.add_argument("--start-maximized")
    service = webdriver.chrome.service.Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(base_url)
    
    try:
        kurshistorie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Kurshistorie')]"))
        )
        kurshistorie_button.click()
        time.sleep(3)  # Give time for the page to load Stammdaten content
    except Exception as e:
        print("Error clicking kurshistorie button:", e)
        driver.quit()
        return None
    
    df_list = []
    for spec_date in date:
        wait = WebDriverWait(driver, 1)
        date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control.text-center")))
        date_input.clear()
        date_input.send_keys(spec_date)
        time.sleep(1)  # Give time for website to detect change
        date_input.send_keys(Keys.RETURN)  # Press Enter to register change
        time.sleep(1) 
    
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Suche starten')]")))
        search_button.click()
        time.sleep(1) 
    
        wait = WebDriverWait(driver, 3)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "widget-table")))

        first_row = driver.find_element(By.XPATH, "//tr[td[text()='First']]")
        first_geld = first_row.find_element(By.XPATH, "./td[2]").text  # Geld column
        first_brief = first_row.find_element(By.XPATH, "./td[3]").text  # Brief column

    
        last_row = driver.find_element(By.XPATH, "//tr[td[text()='Last']]")
        last_geld = last_row.find_element(By.XPATH, "./td[2]").text  # Geld column
        last_brief = last_row.find_element(By.XPATH, "./td[3]").text  # Brief column
        df_list.append([spec_date,first_geld,first_brief,last_geld,last_brief])
    driver.quit()
    
    return df_list

df=GetQuotesZertifikate(date=["05/02/2025", "06/02/2025","07/02/2025"])

