import time

from selenium import webdriver
from random import *

for i in range(200):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('-incognito')
    driver = webdriver.Chrome(executable_path='/home/mael/Téléchargements/chromedriver', options=chrome_options)
    driver.get('https://fr.surveymonkey.com/r/6TPJLTW')
    time.sleep(randrange(5))
    vote_master = driver.find_element_by_class_name('radio-button-label')
    vote_master.click()
    time.sleep(randrange(5))
    validate = driver.find_element_by_class_name('done-button')
    validate.click()
    time.sleep(randrange(5))
    driver.quit()
