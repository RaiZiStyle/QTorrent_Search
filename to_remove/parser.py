#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup


page = requests.get("https://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')
soup.find_all("li", class_="list-entry")
print(soup.prettify())
