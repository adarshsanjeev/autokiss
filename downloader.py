from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

FIREFOX = '/usr/bin/firefox'
CHORME = '/usr/bin/chromium'
URL = 'http://kisscartoon.me/Cartoon/Gravity-Falls-Season-02/'

def init():
    global browser
    browser = webdriver.Firefox(executable_path = FIREFOX)

def get_list(URL):
    browser.set_script_timeout(10)
    browser.get(URL)
    sleep(10)
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    episode_table = browser.find_element_by_class_name('listing').find_element_by_css_selector("*")
    episode_list = episode_table.find_elements_by_tag_name('tr')[:2:-1]
    episode_list = [i.find_element_by_tag_name('a') for i in episode_list]
    
    return episode_list

def parse_input(episodes):
    episode_list = episodes.split(',')
    for index, entry in enumerate(episode_list):
        try:
            if type(entry) == int:
                continue
            entry = entry.strip()
            if '-' in entry:
                range_start, range_end = entry.split('-')
                range_start, range_end = int(range_start), int(range_end)
                del episode_list[index]
                for _ in range(range_start, range_end+1)[::-1]:
                    episode_list.insert(index, _)
            else:
                episode_list[index] = int(entry)
        except ValueError:
            print "%s found, must be a valid integer" % (entry)
            browser.Quit()
            raise
    return episode_list

def download_vid(element):
    link = element.get_attribute('href')
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    browser.set_script_timeout(15)
    browser.get(link)
    sleep(20)

    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    print browser.find_element_by_css_selector('.clsTempMSg > div:nth-child(3) > a:nth-child(1)').text
    browser.find_element_by_css_selector('.clsTempMSg > div:nth-child(3) > a:nth-child(1)').click()

if __name__ == "__main__":
    init()
    episode_list = get_list(URL)
    for index, entry in enumerate(episode_list):
      print "%d. %s"  %(index, entry.text)
      
    print """
    Enter the list of episodes to download.
    Format: 1, 2, 4-6
    """
    
    # download_list = parse_input(raw_input())
    download_vid(episode_list[0])

"""    for _ in download_list:
        try:
            download_vid(episode_list[_])
        except IndexError:
            raise IndexError("%s is not in the list" %(_) )
"""

"""
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    browser.set_script_timeout(15)
"""
