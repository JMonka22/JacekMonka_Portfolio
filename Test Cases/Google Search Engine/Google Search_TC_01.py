from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By                             #
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC        #
from selenium.webdriver.chrome.service import Service
import unittest
import time


s = Service('C:\Webdrivers\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get("https://www.google.com/")
driver.implicitly_wait(10)
accept = driver.find_element(By.ID, "L2AGLb")
accept.click()
search = driver.find_element(By.NAME, "q")
search.clear()
search_phrase = "Automated Testing"
search.send_keys(search_phrase)
search.send_keys(Keys.RETURN)

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    results = driver.find_elements(By.XPATH,'//div[@class="yuRUbf"]/a')   
    for result in results:
        print(result.get_attribute("href"))
    
    assert len(results), "Search Engine works correctly"
      

finally:
    driver.quit()



