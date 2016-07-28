#!/usr/bin/env python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from sys import argv
from time import sleep
from downloader import download_file
import os

INDEX_SELECTOR = '.listing'
TIME_LIMIT = 60
TIME_INTERVAL = 30
browser = None

HTTP_PROXY = os.environ.get("http_proxy")
HTTPS_PROXY = os.environ.get("https_proxy")
FTP_PROXY = os.environ.get("ftp_proxy")

SELENIUM_PROXY = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': HTTP_PROXY,
    'httpsProxy': HTTPS_PROXY,
    'ftpProxy': FTP_PROXY,
})

URLLIB_PROXY = {
    'http':HTTP_PROXY,
    'https':HTTPS_PROXY,
    'ftp':FTP_PROXY,
}

def print_help():
    print '''
    Autokiss downloader
    Requires python 2.7

    Usage : python autokiss.py < URL of show page from kissanime/kisscartoon >
    '''

def init():
    global browser
    browser = webdriver.Firefox(proxy=SELENIUM_PROXY)

def get_episode_list(URL):
    browser.get(URL)
    WebDriverWait(browser, TIME_LIMIT).until(\
                    EC.presence_of_element_located((By.CSS_SELECTOR, INDEX_SELECTOR)))
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

    episode_table = browser.find_element_by_css_selector(INDEX_SELECTOR).find_element_by_css_selector("*")
    episode_list = episode_table.find_elements_by_tag_name('tr')[:1:-1]
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
    if "kisscartoon" in link:
        link_text = "HERE"
    elif "kissanime" in link:
        link_text = "CLICK HERE"
    else:
        raise SystemError("Unknown domain")
    WebDriverWait(browser, TIME_LIMIT).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
    assert "If the player does not work," in browser.page_source
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    save_link = browser.find_element_by_link_text(link_text).get_attribute('href')
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    filename = link.split('/')[-1].split('?')[0] + '.mp4'
    if download_file(save_link, filename, URLLIB_PROXY) is False:
        raise SystemError("Connection error")

if __name__ == "__main__":
    try:
        URL = argv[1]
    except IndexError:
        print_help()
        raise SystemExit
    init()

    episode_list = get_episode_list(URL)
    for index, entry in enumerate(episode_list):
        print "%d. %s"  %(index+1, entry.text)

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
                print "Sleeping for %d seconds to avoid spamming requests" %(TIME_INTERVAL)
                sleep(TIME_INTERVAL)
                break
            except KeyboardInterrupt: 
                confirm = raw_input("[t]ry again / [s]kip to next episode / [E]xit ?").upper()
                if confirm == "T":
                    continue
                elif confirm == "S":
                    break
                else:
                    raise SystemExit
            except:
                print "Download failed, attempting again infinitely, Use control C to exit"
                print "Sleeping for %d seconds to avoid spamming requests" %(TIME_INTERVAL)
                sleep(TIME_INTERVAL)


