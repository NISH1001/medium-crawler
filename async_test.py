#!/usr/bin/env python3

import grequests
import posts
from medium_crawler import LinkFetcher


class Test:
    def __init__(self):
        # link_fetcher = LinkFetcher('headless', username='nishparadox')
        # self.urls = link_fetcher.get_links()
        self.urls = [
            "https://psiloveyou.xyz/tonight-300de7515249",
            "https://medium.com/@nishparadox/the-sound-of-life-ffb582f060de"
        ]
        print(self.urls)

    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def get(self, url):
        print(url)
        return grequests.get(url)

    def async(self):
        results = grequests.map((self.get(u) for u in self.urls), exception_handler=self.exception, size=5)
        print(results)



def main():
    test = Test()
    test.async()

if __name__ == "__main__":
    main()

