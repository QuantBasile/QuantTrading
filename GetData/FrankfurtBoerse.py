# -*- coding: utf-8 -*-
"""
This scripts takes historical data from Frankfurt Boerse using Selenium
"""

from imports import *

def AbrufData(Boerse="Frankfurt"):

    url = "https://www.boerse-frankfurt.de/aktie/deutsche-bank-ag/kurshistorie/historische-kurse-und-umsaetze"
    
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
        
    button = driver.find_element(By.CLASS_NAME, "form-button")
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