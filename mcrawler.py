#!/usr/bin/env python3


import argparse

from link_fetcher import LinkFetcher
from postutils import save_posts, save_post_as_text, save_post_as_json, create_dir

import requests
import unicodedata
from bs4 import BeautifulSoup



class MediumCrawler:
    """
        Crawls every shit for a user from medium.com
    """

    def __init__(self, username='nishparadox'):
        self.fetcher = LinkFetcher(driver_type='headless', username=username)
        self.nlinks = 0

    def crawl_lazily(self):
        """
            Do the actual thing you want the crawler to do :P
            It uses python generator
        """
        self.posts = []
        links = self.fetcher.get_links()
        self.nlinks = len(links)
        print("Total Number of links :: {}".format(self.nlinks))
        for link in links:
            print("Getting :: {}".format(link))
            post = self.get_post(link)
            self.posts.append(post)
            yield post

    def get_post(self, link):
        """
            GET a single post that the link points to and nicely parse it.
            The returned dictionary is in the format:
                {
                    "title"     :   "...",
                    "timestamp" :   "...",
                    "content"   :   "...",
                    "tags" : [....]
                }
        """
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        divs = soup.find_all('div', {'class' : 'section-inner sectionLayout--insetColumn'})
        title = soup.find('h1', {'class' : 'graf graf--h3 graf--leading graf--title'}).get_text(strip=True)
        title = unicodedata.normalize("NFKD", title)
        content =' '.join( [ div.get_text(strip=True) for div in divs ])
        content = unicodedata.normalize("NFKD", content)
        time = soup.find('time')['datetime']
        tag_divs = soup.find('ul', {'class' : 'tags tags--postTags tags--borderless'})
        tags = [ div.get_text(strip=True) for div in tag_divs ]
        return {
            'title' : title,
            'timestamp' : time,
            'content' : content,
            'tags' : tags
        }

def parse():
    parser = argparse.ArgumentParser(
        "mcrawler",
        description="Crawl shit from medium"
    )
    parser.add_argument(
        '-u',
        '--user',
        # dest='user',
        help='The username for medium',
        required=True
    )
    parser.add_argument(
        '-t',
        '--type',
        # dest='type',
        help='The format for dumping -> text, json',
        required=True
    )
    parser.add_argument(
        '-dd',
        '--dump-dir',
        # dest='dump_dir',
        help='The directory where the data is to be dumped',
        required=True
    )
    return parser.parse_args()

def run_crawler(username, dump_type, dump_dir):
    import os
    print("Crawling for user :: {}".format(username))
    crawler = MediumCrawler(username=username)
    dfunc = save_post_as_text if dump_type == 'text' else save_post_as_json
    create_dir(dump_dir, username)
    for post in crawler.crawl_lazily():
        dfunc(username, post, dump_dir)
    print("Dumped {} Posts to {}".format(crawler.nlinks, os.path.join(dump_dir, username)))

def run(args):
    run_crawler(args.user, args.type, args.dump_dir)

def main():
    args = parse()
    run(args)

if __name__ == "__main__":
    main()

