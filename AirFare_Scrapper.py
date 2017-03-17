import requests
from bs4 import BeautifulSoup
#from urlparse import urljoin
import urllib3
import flightscraper
URL = 'http://philadelphia.craigslist.org/search/sss?sort=date&query=firefly%20tickets'
BASE = 'http://philadelphia.craigslist.org/cpg/'

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html5lib")
#print(soup)
for listing in soup.find_all('p',{'class':'row'}):
    if listing.find('span',{'class':'price'}) != None:
        price = listing.text[2:6]
        price = int(price)
        if price <=250 and price > 100:
            print(listing.text)
            link_end = listing.a['href']
            url = urljoin(BASE, link_end)
            print(url)
            print("\n")