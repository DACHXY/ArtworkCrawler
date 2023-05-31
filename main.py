import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import Element
from typing import Union
import re

# Config
TEMP_HTML_FILE_PATH = 'TEMP.html'
BASEURL : str = "https://www.artsy.net"
URL : str = BASEURL + "/fair/1-54-new-york-2023/artworks"

class ArtworkSearcher:
    def __init__(self, base_url, page_url):
        self.artworks_url = set()
        self.session = requests.Session()
        self.base_url = base_url
        self.page_url = page_url
        
    def search_urls(self):
        request = self.session.get(self.page_url)
        soup = BeautifulSoup(request.content, "html.parser")

# Main Function
def main():
    request : requests.Response = requests.get(URL)
    soup : BeautifulSoup = BeautifulSoup(request.content, 'html.parser')

    href_elements = soup.find_all('a')

    artwork_urls = set()

    # Get all href element 
    for element in href_elements:
        href = element.get('href')
        refind = re.search(r"/artwork/([a-z-A-Z0-9]+)", href)
        if refind:
            artwork_url = refind.group(0)
            artwork_urls.add(artwork_url)

    print(artwork_urls)

if __name__ == "__main__":
    main()