from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(executable_path = chrome)
driver.implicitly_wait(60)



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
reg_url = "https:XXXXOOOO"

bursa = "https://www.investing.com/markets/malaysia"
driver.get(bursa)
table = driver.find_element_by_id('cross_rate_markets_stocks_1')
df = pd.read_html(table.get_attribute('outerHTML'), header=0)[0]
links = [link.get_attribute('href') for link in table.find_elements_by_tag_name('a')]
df['links'] = links
df['historical'] = df['links']+"-historical-data"
failed = []

for i in range(1,len(df)):
    driver.get(df.iloc[i]['historical'])
    print(i)
    wait = WebDriverWait(driver, 10)
    time.sleep(10)
    try:
        e1 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.float_lang_base_2.historicDate')))
        e1.click()

    except:
        e1 = driver.find_element_by_css_selector('.float_lang_base_2.historicDate')
        e1.click()


    driver.find_element_by_xpath("//*[@id='startDate']").clear()
    driver.find_element_by_xpath("//*[@id='startDate']").send_keys("01/01/2000")
    time.sleep(1)
    driver.find_element_by_css_selector('.newBtn.Arrow.LightGray.float_lang_base_2').click()
    time.sleep(10)
    #download
    try:
        e2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.newBtn.LightGray.downloadBlueIcon.js-download-data')))
        e2.click()

    except:
        e2 = driver.find_element_by_css_selector('.newBtn.LightGray.downloadBlueIcon.js-download-data')
        e2.click()
