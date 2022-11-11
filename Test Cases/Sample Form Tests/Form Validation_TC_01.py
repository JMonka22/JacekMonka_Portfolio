from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By                             
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC        
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import time
import logging
class bcolors:
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    

s = Service('C:\Webdrivers\chromedriver.exe')
driver = webdriver.Chrome(service=s)

#Example correct data to fill in the form
name = "John"
surname = "Doe"
email = "john.doeexample.com"
gender = "Male"
mobile_number = "1231231231"
date_of_birth = "1 Jan 2000"

driver.get("https://demoqa.com/automation-practice-form")
driver.implicitly_wait(10)

nameForm = driver.find_element(By.ID, "firstName")
surnameForm = driver.find_element(By.ID, "lastName")
emailForm = driver.find_element(By.ID, "userEmail")
mobileForm = driver.find_element(By.ID, "userNumber")
birthdateForm = driver.find_element(By.ID, "dateOfBirthInput")
genders = driver.find_elements(By.XPATH, '//*[@id="genterWrapper"]/div[2]/div')
submitButton = driver.find_element(By.XPATH, '//*[@id="submit"]')

actions = ActionChains(driver)

try:
    nameForm.send_keys(name) 
    surnameForm.send_keys(surname)
    emailForm.send_keys(email)
    mobileForm.send_keys(mobile_number)


    for element in genders:                                                                                          
        if element.find_element(By.NAME, 'gender').get_attribute('value') == gender:           
            element.find_element(By.TAG_NAME, 'label').click()                                          

    actions.move_to_element(birthdateForm)                                                                
    actions.drag_and_drop_by_offset(birthdateForm, -100,0)
    actions.send_keys(date_of_birth)
    actions.perform()                
    
    submitButton.click()
    time.sleep(0.1)
    if len(driver.find_elements(By.CSS_SELECTOR, ".form-control:invalid")):
        print(f"{bcolors.GREEN}Invalid input detected (CSS Selector){bcolors.ENDC}")

    assert not len(driver.find_elements(By.ID, "closeLargeModal")), f"{bcolors.FAIL}Invalid e-mail format was not detected (Close button from summary window found){bcolors.ENDC}"

finally:
    driver.quit()





