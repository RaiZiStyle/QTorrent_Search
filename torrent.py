#!/usr/bin/env python3
"""
The API for the torrent
"""
from ast import parse
from json import load, dumps
# from bs4 import BeautifulSoup

import requests

from Logger import LogDecorator


class TorrentApi():
    def __init__(self, provider: str = "pirate-proxy.json") -> None:
        with open(f"providers/{provider}") as f:
            self.pirate_proxy = load(f)
            print(self.pirate_proxy)
        self.url = self.pirate_proxy["base_url"] + \
            self.pirate_proxy["search_url"]
        self.bf_item = self.pirate_proxy["itemSelector"]["item"]
        self.bf_id = self.pirate_proxy["itemSelector"]["id"]
        self.bf_class = self.pirate_proxy["itemSelector"]["class"]

        # page , status_code = self.makeRequest()
        # # print(f"[DEBUG] - page.json : {page.json()}")
        # if status_code != 200:
        #     print(f"Error Status code : {status_code} ")
    def updateUrl(self, to_query, tag):
        self.url = self.pirate_proxy["base_url"] + \
            self.pirate_proxy["search_url"]
        temp = self.url.replace("{TO_QUERY}", to_query)
        self.url = temp.replace("{TAG}", tag)

    @LogDecorator()
    def makeRequest(self, to_query: str = "test", tag: str = "all") -> tuple:
        self.updateUrl(to_query, tag)
        print(f"Making request for {self.url}")
        page = requests.get(self.url)
        print(f"Status code : {page.status_code}, Encoding : {page.encoding}")
        return page.json(), page.status_code


if __name__ == '__main__':
    MyTorrentApi = TorrentApi()
# page, status_code = MyTorrentApi.makeRequest()
# soup = BeautifulSoup(page.content, 'html.parser')
