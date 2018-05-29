"""
Downloads Wallpaper of the day from bing.com
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

url = 'https://www.bing.com/'
download_dir = 'C:/Users/Public/Pictures/Wallpaper'

preferences = {"download.default_directory": download_dir,
               "directory_upgrade": True,
               "safebrowsing.enabled": True}

options = Options()
options.add_experimental_option("prefs", preferences)

driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(5)  # Wait until page is loaded.

photo_info = driver.find_element_by_id('sh_rdiv')
hover = ActionChains(driver).move_to_element(photo_info)
hover.perform()

desc = driver.find_element_by_id('musCardImageTitle')
image_name = desc.get_property('innerHTML')

download_link = driver.find_element_by_id('DownloadHPImage')
download_link.click()

time.sleep(3)  # Wait until download completes.
driver.quit()
