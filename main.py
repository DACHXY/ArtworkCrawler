from typing import Any
from requests import Session, Response
from bs4 import BeautifulSoup, ResultSet
import re
import json


# Config
TEMP_HTML_FILE_PATH = "TEMP.html"
BASEURL: str = "https://www.artsy.net"
URL: str = BASEURL + "/collection/new-this-week"
SEARCH_DETAIL_QL = open("graphql\\detail.graphql").read()
ARTIST_INFO_QL = open("graphql\\artistInfo.graphql").read()


class ArtworkSearcher:
    def __init__(self, base_url, page_url, regex_str):
        self.artworks_url: set = set()
        self.session: Session = Session()
        self.base_url: str = base_url
        self.page_url: str = page_url
        self.regex_str: str = regex_str

    def find_by_rule(self):
        return

    def get_website_content(self) -> bytes:
        request: Response = self.session.get(self.page_url)

        if request.status_code > 400:
            raise Exception("Fetch Website Error, status code:", request.status_code)

        return request.content

    def get_parsed_html(self, content) -> BeautifulSoup:
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def get_all_artwork_urls(self) -> set[Any]:
        content: bytes = self.get_website_content()
        soup: BeautifulSoup = self.get_parsed_html(content)
        href_elements: ResultSet[Any] = soup.find_all("a")
        # Get all href element
        for element in href_elements:
            href: str = element.get("href")
            refind: re.Match[str] | None = re.search(self.regex_str, href)

            # regex not found
            if not refind:
                continue

            artwork_url: str = refind.group(0)
            self.artworks_url.add(artwork_url)

        return self.artworks_url

    def run_page_crawler(self, artwork_url):
        request = self.session.get(artwork_url)
        request.content

    def deploy_page_crawler(self):
        return


# Main Function
def main():
    artworkSearcher = ArtworkSearcher(
        base_url=BASEURL, page_url=URL, regex_str=r"/artwork/([a-z-A-Z0-9]+)"
    )
    artworkSearcher.get_all_artwork_urls()


def get_page_detail():
    session = Session()
    request = session.get("https://www.artsy.net/artwork/trenity-thomas-amicable")
    soup = BeautifulSoup(request.content, "html.parser")

    # 圖片
    element = soup.find(id="transitionFrom--ViewInRoom")
    srcset = element.get("srcset")
    pattern = r"(https://\S+)\s[0-9]x"
    matches = re.findall(pattern, srcset)
    print("作品:\t", matches)

    # 作者
    elements = soup.find_all(class_="RouterLink__RouterAwareLink-sc-1nwbtp5-0")
    for element in elements:
        if "/artist/ekaterina-ermilkina" != element.get("href"):
            continue
        print("作者:\t", element.text)

    # 價格
    element = soup.find(attrs={"data-test": "SaleMessage"})
    print("價格:\t", element.text)

    # 作品名
    element = soup.find(class_="Box-sc-15se88d-0 Text-sc-18gcpao-0 caIGcn bhlKfb")
    print("作品名稱:\t", element.text)

    # 材質
    element = soup.find(class_="Box-sc-15se88d-0 caIGcn")
    child_elements = element.find_all(
        class_="Box-sc-15se88d-0 Text-sc-18gcpao-0 cgchZM", recursive=False
    )
    print("材質:\t", child_elements[0].text)

    # 尺寸
    print("尺寸:\t", child_elements[1].text)

    # 介紹
    description = get_artwork_description()
    print("介紹:\t", description)


def get_artwork_artist_info(title):
    session = Session()
    req = session.post(
        "https://metaphysics-production.artsy.net/v2",
        json={
            "id": "ArtistInfoQuery",
            "query": ARTIST_INFO_QL,
            "variables": {"slug": title},
        },
    )


def get_artwork_description(title):
    session = Session()
    req = session.post(
        "https://metaphysics-production.artsy.net/v2",
        json={
            "id": "ArtworkDetailsQuery",
            "query": SEARCH_DETAIL_QL,
            "variables": {"slug": title},
        },
    )

    jsonList = json.loads(req.content)
    with open("TEST.json", "w", encoding="utf-8") as openfile:
        json.dump(jsonList, openfile, ensure_ascii=False, indent=4)

    return jsonList["data"]["artwork"]["additionalInformation"]


if __name__ == "__main__":
    get_page_detail()

    # main()
