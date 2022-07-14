from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd

import time

from datetime import datetime


options = Options()
options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

PATH = "C:\webdrivers\chromedriver.exe"

driver = webdriver.Chrome(options = options, service = Service(PATH))

#### testing ground for the loop

base_url = "https://www.yellowpages.com/search?search_terms="

term = ["cleaning"]

base_url_w_term = []

city = ['Bradenton','Ellenton','Sarasota','Longboat Key','Palmetto','Venice','Parrish','Osprey','Nokomis','North Port','Port Charlotte','Fort Ogden','Arcadia']

#'Bradenton','Ellenton','Sarasota','Longboat Key','Palmetto','Venice','Parrish'
#'Osprey','Nokomis','North Port','Port Charlotte','Fort Ogden','Arcadia'

base_url_term_city = []

pages_scraped = ["1","2","3"]

full_urls = []

for i in term:
    x = base_url + i +"&geo_location_terms="
    base_url_w_term.append(x)


for i in range(len(base_url_w_term)):
    x = base_url_w_term[i] 
    for i in range(len(city)):
        y = x+city[i]
        for i in range(len(pages_scraped)):
            z = y+"%2C+FL&page="+ pages_scraped[i]
            full_urls.append(z)

#### testing ground for the loop
biz_loc = []
biz_name = []
biz_phone = []
biz_site = []
biz_email = []
biz_fb = []

for i in full_urls:

    driver.get(i)

    print(i)

    biz_link = []

    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results') and contains(@class, 'organic')]"))
        )
        organic_div = driver.find_element(By.XPATH, "//div[contains(@class, 'search-results') and contains(@class, 'organic')]")
        biz_name_links = organic_div.find_elements(By.XPATH, "//a[@class='business-name']")

        for href in biz_name_links:
            biz_link.append(href.get_attribute('href'))

        print(biz_link)

        for url in biz_link:
            driver.get(url)
            time.sleep(2)
            try:
                element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//h1"))
                )
                biz_loc.append(i)
                biz_name.append(driver.find_element(By.XPATH, "//h1").text)
                try:
                    biz_phone.append(driver.find_element(By.XPATH, "//a[contains(@class, 'phone') and contains(@class, 'dockable')]").text)
                except:
                    biz_phone.append("N/A")   
                try:
                    biz_site.append(driver.find_element(By.XPATH, "//a[contains(@class, 'website-link') and contains(@class, 'dockable')]").get_attribute('href'))
                except:
                    biz_site.append("N/A")
                try:
                    biz_email.append(driver.find_element(By.XPATH, "//a[@class='email-business']").get_attribute('href'))
                except:
                    biz_email.append("N/A")
                try:
                    biz_fb.append(driver.find_element(By.XPATH, "//a[@class='fb-link']").get_attribute('href'))
                except:
                    biz_fb.append("N/A")  
            except:
                continue
    except:
        print("issue finding search results - skipped")
    

print("Compiling Complete")

data = pd.DataFrame({'Location/Page': biz_loc,
                    'Business Name': biz_name, 
                    'Phone No.': biz_phone, 
                    'Website': biz_site, 
                    'Email': biz_email,
                    'Facebook': biz_fb})

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y-%m-%d %H.%M.%S")
filename = "PC "+timestampStr+".csv"
data.to_csv(filename, index=False)

print("CSV Created")