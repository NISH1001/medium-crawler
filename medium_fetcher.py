#!/usr/bin/env python3

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import requests
import time


def get_post_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    # class_name = 'postArticle-content'
    class_name = 'streamItem streamItem--postPreview js-streamItem'
    divs = soup.find_all('div', {'class' : class_name})
    links = []
    for div in divs:
        anchors = div.find_all('a', href=True)
        anchor = anchors[2]
        links.append(anchor['href'])
    return links

def scroll_to_oblivion(driver):
    pause = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    i = 0
    driver.get_screenshot_as_file("screen"+str(i)+".jpg")
    while True:
        print("Scrolling...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("New Height :: {}".format(new_height))
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        driver.get_screenshot_as_file("screen"+str(i)+".jpg")
    return last_height

def fetch_using_selenium(username):
    url = "https://medium.com/@{}/latest".format(username)
    driver = webdriver.Firefox()
    driver.get(url)
    h = scroll_to_oblivion(driver)
    links = get_post_links(driver.page_source)
    return links


def fetch_with_headless(username):
    url = "https://medium.com/@{}/latest".format(username)
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options)
    driver.get(url)
    h = scroll_to_oblivion(driver)
    links = get_post_links(driver.page_source)
    return links

def get_post(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', {'class' : 'section-inner'})
    for div in divs:
        print(div.get_text())


def main():
    username = "nishparadox"
    # fetch_blogs(username)
    # links = fetch_with_headless(username)
    # links = fetch_using_selenium(username)
    # print(len(links))
    # print(links)
    link = "https://medium.com/@nishparadox/the-sound-of-life-ffb582f060de"
    get_post(link)

if __name__ == "__main__":
    main()

