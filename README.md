# medium-crawler
A crawler for scraping shit from medium blogs

## Dependencies
**python3** is required along with **pip3** (mine is **pip** by default).

First clone this repo:
```bash
git clone https://github.com/NISH1001/medium-crawler
```

Install using `requirements.txt`:
```bash
pip install -r requirements.txt
```


### Webdriver
Since the crawler uses selenium driver (more specifically, a headless driver), be sure to have firefox or chrome installed
in your system. You can always change it in the code if you feel like.  
The web drivers should be in the system path like:
`/usr/bin/`  or `/usr/local/bin/`  

Firefox requires [geckodriver](https://github.com/mozilla/geckodriver). Download the executable to geckodriver and put it in 
the system path.  
Similar process might apply for Chrome or Chromium.  

If nothing works out, you can put the path in the constructor [here](https://github.com/NISH1001/medium-crawler/blob/master/link_fetcher.py#L24)  
(Kind of manual override :D)
Like:
```python
self.driver = webdriver.Chrome(path_to_web_driver)
```

## Usage
The crawler requires username, dump type and the directory where data is to be dumped.  

**help me**
```bash
python mcrawler.py -h
```

```bash
usage: mcrawler [-h] -u USER -t TYPE -dd DUMP_DIR

Crawl shit from medium

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  The username for medium
  -t TYPE, --type TYPE  The format for dumping -> text, json
  -dd DUMP_DIR, --dump-dir DUMP_DIR
                        The directory where the data is to be dumped
```

**example**
```bash
python mcrawler.py -u nishparadox -t text -dd data/
```
