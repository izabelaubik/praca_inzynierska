#https://www.youtube.com/watch?v=SIm2W9TtzR0
#
#
#do zrobienia:
#ładowanie komentarzy z see more i see replies
#usuwanie nie angielskich wierszy działa, ale nie jestem przekonana co do tego czy działa jak
#pojedyncze słowa są w innym języku a nie cały wiersz
#wybór ilości komentarzy jakie chcemy załadować? z jakiej puli statystyki?
#jeżeli tak to trzeba usuwać nie angielskie słowa przed skończeniem scrapowania, żeby scrapowało
#do określonej ilości już bez tych non english komentarzy

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import pandas as pd
import time
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from langdetect import detect
import csv

def detect_language(text):
    try:
        return detect(text)
    except:
        return ""

file_path = Path(r"C:\Users\izabe\Desktop\youtube_scraper\file_comments.csv")
data = []

path = 'chromedriver.exe'
url = 'https://www.youtube.com/watch?v=Bag1gUxuU0g'
chrome_driver = ChromeService(path)
driver = webdriver.Chrome(service=chrome_driver)
driver.get(url)

driver.maximize_window()
wait = WebDriverWait(driver,5)

try:
    print("scrolling")
    driver.execute_script("window.scrollTo(0, 200);")
    time.sleep(10)

    for i in range(0,2):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)
    for comment in wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]'))):
        data.append(comment.text)

    print("deleting non english rows")
    data = list(filter(lambda x: detect_language(x) == 'en', data))
    df = pd.DataFrame(data)
    # headerList=['comment']
    # df.to_csv('file_comments.csv', header=headerList, encoding='utf-8', index=False)
    df.to_csv('file_comments.csv', encoding='utf-8', index=False)

except Exception as e:
    print(e)
driver.close()

#wczytywanie z pliku csv
# df = pd.DataFrame(pd.read_csv("file_comments.csv", sep="\t", encoding="utf-8", quoting=csv.QUOTE_NONE))
# print(df)