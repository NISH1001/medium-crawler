#!/usr/bin/env python3


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import requests
import time


class LinkFetcher:
    """
        This fetches the links to all blog posts for a user
    """
    def __init__(self, driver_type='headless', username='nishparadox'):
        if not username:
            raise ValueError("Invalid username")
        self.username = username
        self.url = "https://medium.com/@{}/latest".format(username)
        if driver_type == 'headless':
            options = Options()
            options.set_headless(headless=True)
            self.driver = webdriver.Firefox(firefox_options=options)
        elif driver_type == 'chrome':
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Firefox()

    def _scroll_to_oblivion(self):
        """
            Simulate infinite scroll as per the medium's site
        """
        pause = 3
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        print(last_height)
        i = 0
        self.driver.get_screenshot_as_file("data/screen"+str(i)+".jpg")
        while True:
            print("Scrolling...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print("New Height :: {}".format(new_height))
            if new_height == last_height:
                break
            last_height = new_height
            i += 1
            self.driver.get_screenshot_as_file("data/screen"+str(i)+".jpg")
        return last_height

    def _parse(self, html):
        """
            Parse to get the actual links to the posts
        """
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

    def get_links(self):
        self.driver.get(self.url)
        h = self._scroll_to_oblivion()
        links = self._parse(self.driver.page_source)
        return links



def main():
    link_fetcher = LinkFetcher('headless', username='nishparadox')
    links = link_fetcher.get_links()
    print(links)

if __name__ == "__main__":
    main()

