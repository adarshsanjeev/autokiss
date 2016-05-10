from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import urlretrieve
import downloader
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import argv

URL = argv[1]

def init():
    global browser
    browser = webdriver.Firefox()

def get_list(URL):
    browser.set_script_timeout(20)
    browser.get(URL)
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bigBarContainer:nth-child(4) > div:nth-child(2)")))
    # browser.implicitly_wait(20)
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

def download_vid(link):
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    browser.set_script_timeout(15)
    browser.get(link)
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".clsTempMSg > div:nth-child(3) > a:nth-child(1)")))

    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    save_link = browser.find_element_by_css_selector('.clsTempMSg > div:nth-child(3) > a:nth-child(1)').get_attribute('href')
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    filename = link.split('/')[-1].split('?')[0] + '.mp4'
    print filename, save_link
    downloader.download_file(save_link, filename)

if __name__ == "__main__":
    init()
    episode_list = get_list(URL)
    for index, entry in enumerate(episode_list):
      print "%d. %s"  %(index, entry.text)
      
    print """
    Enter the list of episodes to download.
    Format: 1, 2, 4-6
    """
    
    download_list = parse_input(raw_input())

    print "DOWNLOADING:", download_list
    for _ in download_list:
        while True:
            try:
                download_vid(episode_list[_].get_attribute('href'))
                break
            except KeyboardInterrupt:
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                break
            except:
                print "Download failed, attempting again, Use control C to exit"
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                continue
