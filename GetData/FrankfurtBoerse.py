# -*- coding: utf-8 -*-
"""
This scripts takes historical data from Frankfurt Boerse using Selenium
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

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
        print("Xetra")
        select_element = driver.find_element(By.CLASS_NAME, "custom-select")
        select = Select(select_element)
        select.select_by_visible_text("Xetra")
        
    if split == True: 
        print("Split taken into account")
        checkbox = driver.find_element(By.ID, 'input-clean-splits')
        checkbox.click()
        
    if dividends == True:
        print("Dividends taken into account")
        checkbox = driver.find_element(By.ID, 'input-clean-dividends')
        checkbox.click()
        
    if Bezugsrechte == True: 
        print("Bezugsrechte taken into account")
        checkbox = driver.find_element(By.ID, 'input-clean-subscription-rights')
        checkbox.click()
        
    if Date_von != "":
        print("Date von taken into account")
        wait = WebDriverWait(driver, 1)
        von_date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control.text-center')))
        von_date_input.click()
        von_date_input.clear()
        von_date_input.send_keys(Date_von)#'01/08/2024'
        von_date_input.send_keys(Keys.RETURN) # press enter
        
    if Date_bis != "":
        print("Date bis taken into account")
        wait = WebDriverWait(driver, 1)
        bis_date_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input.form-control.text-center')))
        bis_date_input = bis_date_inputs[1]
        bis_date_input.click()
        bis_date_input.clear()
        bis_date_input.send_keys(Date_bis)#'01/08/2024'
        bis_date_input.send_keys(Keys.RETURN) # press enter
        
        
    button = driver.find_element(By.CLASS_NAME, "form-button") #Play button auf der Website
    button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "widget-table"))
        )
    
    content = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', {'class': 'widget-table'}) 
    
    thead = table.find('thead')
    columns = [header.text.strip() for header in thead.find_all('th')] if thead else []
    tbody = table.find('tbody')
    data = [[col.text.strip() for col in row.find_all('td')] for row in tbody.find_all('tr')] if tbody else []
    df = pd.DataFrame(data, columns=columns)
    
    return df
