#!/usr/bin/env python3

from bs4 import BeautifulSoup

import requests
import time
import unicodedata

def get_post(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', {'class' : 'section-inner'})
    title = divs[0].get_text(strip=True)
    title = unicodedata.normalize("NFKD", title)
    content =' '.join( [ div.get_text(strip=True) for div in divs[1:] ])
    content = unicodedata.normalize("NFKD", content)
    time = soup.find('time')['datetime']

    return {
        'title' : title,
        'timestamp' : time,
        'content' : content
    }


def main():
    link = "https://medium.com/@nishparadox/the-sound-of-life-ffb582f060de"
    post = get_post(link)
    print(post)

if __name__ == "__main__":
    main()

