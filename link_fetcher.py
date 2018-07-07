#!/usr/bin/env python3


from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import re
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
        self.driver_type = driver_type
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
            # self.driver.get_screenshot_as_file("data/screen"+str(i)+".jpg")
        return last_height

    def _parse(self, html):
        """
            Parse to get the actual links to the posts
        """
        soup = BeautifulSoup(html, 'html.parser')
        class_name = 'streamItem streamItem--postPreview js-streamItem'
        divs = soup.find_all('div', {'class' : class_name})
        links = []
        regex = re.compile('Read More', re.IGNORECASE)
        for div in divs:
            anchors = div.find_all('a', href=True, text=regex)
            if anchors:
                links.append(anchors[0]['href'])
        return links

    def _parse2(self, html):
        """
            The latest function to fetch actual links of this post.
            Since medium has shifted to react based rendering,
            there is no actual class name for post.
            So, here we fetch all the links that match to the pattern:
                /p/someid/
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=re.compile(r'.*/p/.*'))
        href_list = set()
        base_url = "https://medium.com{}"
        for link in links:
            href = link['href']
            href_list.add(base_url.format(href))
        return href_list


    def get_links(self):
        print("Using driver type :: {}".format(self.driver_type))
        self.driver.get(self.url)
        h = self._scroll_to_oblivion()
        return self._parse2(self.driver.page_source)


def main():
    link_fetcher = LinkFetcher('headless', username='nishparadox')
    links = link_fetcher.get_links()
    print(links)

if __name__ == "__main__":
    main()

