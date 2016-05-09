from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from sys import argv

FIREFOX = '/usr/bin/firefox'
URL = 'http://kisscartoon.me/Cartoon/Gravity-Falls-Season-02/Short-Lefty' #argv[1]

browser = webdriver.Firefox(executable_path = FIREFOX)
browser.set_script_timeout(10)
browser.get(URL)
sleep(10)

a = browser.find_element_by_css_selector('.clsTempMSg > div:nth-child(3) > a:nth-child(1)')
print a.text
a.click()
