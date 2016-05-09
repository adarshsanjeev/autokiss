from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

FIREFOX = '/usr/bin/firefox'
URL = 'http://kisscartoon.me/Cartoon/Gravity-Falls-Season-02/'
browser = webdriver.Firefox(executable_path = FIREFOX)

browser.set_script_timeout(10)
browser.get(URL)
sleep(10)

episode_table = browser.find_element_by_class_name('listing').find_element_by_css_selector("*")
episode_list = episode_table.find_elements_by_tag_name('tr')[:2:-1]
browser.close()

for index, entry in enumerate(episode_list):
    print "%d. %s"  %(index, entry.text)

print """
Enter the list of episodes to download.
Format: 1, 2, 4-6
"""

download_range = range(2) #raw_input().split(',').strip()


"""
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    browser.set_script_timeout(15)
"""
