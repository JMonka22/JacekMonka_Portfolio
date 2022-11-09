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
email = "john.doe@example.com"
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

    for element in genders:                                                                             # It turned out that driver was only able to click on a label instead of input field             
        if element.find_element(By.NAME, 'gender').get_attribute('value') == gender:                    # and because I wanted this script to be easily modifable I choose to search for child
            element.find_element(By.TAG_NAME, 'label').click()                                          # elements matching gender value I specified earlier and then click matching label

    actions.move_to_element(birthdateForm)                                                              # Clearing by birthdateForm.clear() failed, so I decided to clear this input field by utilizing action chains
    actions.drag_and_drop_by_offset(birthdateForm, -100,0)
    actions.send_keys(date_of_birth)
    actions.perform()

    submitButton.click()
    
    main = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "closeLargeModal")))
    time.sleep(0.2)

    if driver.find_elements(By.ID, "closeLargeModal"):
        print(f"{bcolors.GREEN}Succesfully submitted following data:\n{bcolors.ENDC}")
        results = driver.find_elements(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/table/tbody/tr')
        for tr in results:
            for td in tr.find_elements(By.TAG_NAME, "td"):
                print(td.text)

    assert driver.find_elements(By.ID, "closeLargeModal"), f"{bcolors.FAIL}Form was not submitted succesfully{bcolors.ENDC}"

finally:
    driver.quit()





