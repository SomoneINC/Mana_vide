from selenium import webdriver
import selenium
import requests
import threading
import re
from bs4 import BeautifulSoup
from subprocess import call
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import webbrowser
import time
import pandas as pd
import os

#Parimiters
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--disable-gpu")

#Varubles
Username =  "40103362321"
Password =  "rnplietotajs123"
UsernameXPath = '/html/body/div[1]/div/div[1]/div[3]/div/div[6]/form/div[1]/div/input'
PasswordXPath = '/html/body/div[1]/div/div[1]/div[3]/div/div[6]/form/div[2]/div/input'
LoginXPath = '/html/body/div[1]/div/div[1]/div[3]/div/div[6]/form/div[4]/button'
NavigationRight = '/html/body/div[1]/div/div[2]/div[3]/main/div[4]/div/main/div/div[3]/div/div[2]/div/div/nav/a[2]'
GraphicLinks = []
StreetName = '/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div[1]/div/p'
Date = '/html/body/div[1]/div/div[2]/div[3]/main/div[4]/div/main/div/div/div[1]/div/div/div[2]/div[1]/h2'
Calander = '/html/body/div[1]/div/div[2]/div[3]/main/div[4]/div/main/div/div/div[1]/div/div/div[4]/div/section/div/div[2]/table/tbody'
CollectedData = []

#Create driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.get('https://manai.videi.lv/login')

#Login
wait.until(EC.presence_of_element_located((By.XPATH, UsernameXPath)))
UserBox = driver.find_element(By.XPATH, UsernameXPath)
PassBox = driver.find_element(By.XPATH, PasswordXPath)
UserBox.send_keys(Username)
PassBox.send_keys(Password)
driver.find_element(By.XPATH, LoginXPath).click()


#Scrape
x = 0
for x in range(0, 1):
    wait.until(EC.presence_of_element_located((By.XPATH, NavigationRight)))
    Stain = wait.until(EC.presence_of_element_located((By.XPATH, NavigationRight)))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    FoundLinks = driver.find_elements(By.CSS_SELECTOR, "a.view-schedule")
    for links in FoundLinks:
        href = links.get_attribute('href')
        if href != " " :
            if "schedule" in href:
                GraphicLinks.append(href)
    NextPage =driver.find_element(By.XPATH, NavigationRight)
    if "opacity-50" in NextPage.get_attribute('class'):
        break
    else :
        NextPage.click()
    wait.until(EC.staleness_of(Stain))

for links in GraphicLinks:
    driver.get(links)
    GatheredData =[]
    wait.until(EC.presence_of_element_located((By.XPATH, Date)))
    DateText = driver.find_element(By.XPATH, Date).text
    StreetText = driver.find_element(By.XPATH, StreetName).text
    CalanderLocation = driver.find_element(By.XPATH, Calander)
    CalanderAllTd = driver.find_elements(By.CSS_SELECTOR, "td")
    CSAList = []
    MIXList = []
    for td in CalanderAllTd:
        CalanderDate = td.find_element(By.TAG_NAME, "span").text
        ClanderDiv = td.find_elements(By.TAG_NAME, "div")
        for div in ClanderDiv:
            if "bg-CSA" in div.get_attribute('class') and CalanderDate not in CSAList:
                CSAList.append(CalanderDate)
            if "bg-MIX" in div.get_attribute('class') and CalanderDate not in MIXList:
                MIXList.append(CalanderDate)

    GatheredData = [StreetText.split(",")[0], DateText, len(CSAList), len(MIXList)]
    print(GatheredData)
    CollectedData.append(GatheredData)



df = pd.DataFrame(CollectedData, columns=['Iela', 'Mēnesis', 'CSA', 'MIX'])	

excel_file_path = 'output5.xlsx'

df.to_excel(excel_file_path, index=False)

os.system(f'start excel {excel_file_path}')

driver.close()
