from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sys import argv
from time import sleep
from downloader import download_file

INDEX_SELECTOR = '.listing'
TIME_LIMIT = 60
browser = None

def init():
    global browser
    browser = webdriver.Firefox()

def get_episode_list(URL):
    browser.get(URL)
    WebDriverWait(browser, TIME_LIMIT).until(\
                    EC.presence_of_element_located((By.CSS_SELECTOR, INDEX_SELECTOR)))
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    episode_table = browser.find_element_by_css_selector(INDEX_SELECTOR).find_element_by_css_selector("*")
    episode_list = episode_table.find_elements_by_tag_name('tr')[:2:-1]
    episode_list = [i.find_element_by_tag_name('a') for i in episode_list]

    return episode_list

def parse_input(episodes):
    episode_list = episodes.split(',')
    for index, entry in enumerate(episode_list):
        try:
            if isinstance(entry, int):
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
            browser.driver.quit()
            raise
    return episode_list

def download_vid(link):
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    browser.get(link)
    WebDriverWait(browser, TIME_LIMIT).until(EC.presence_of_element_located((By.LINK_TEXT, "HERE")))
    assert "If the player does not work, CLICK" in browser.page_source
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    save_link = browser.find_element_by_link_text('HERE').get_attribute('href')
    browser.close()
    filename = link.split('/')[-1].split('?')[0] + '.mp4'
    print filename, save_link
    download_file(save_link, filename)

if __name__ == "__main__":
    try:
        URL = argv[1]
    except IndexError:
        raise SyntaxError("Wrong usage: autokiss.py <url>")

    init()

    episode_list = get_episode_list(URL)
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
                print "Sleeping for 1 min to avoid detection"
                sleep(60)
                break
            except KeyboardInterrupt: 
                break
            except:
                print "Download failed, attempting again infinitely, Use control C to exit"
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                raise

