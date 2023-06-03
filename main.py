from typing import Any, Union
from requests import Session, Response
from bs4 import BeautifulSoup, ResultSet
import re
import json

# Config
BASEURL: str = "https://www.artsy.net"
URL: str = BASEURL + "/collect"
API_URL: str = "https://metaphysics-production.artsy.net/v2"
STORE_FILE_NAME = "data/Artworks.json"
STORE_ARTIST_NAME = "data/Artists.json"

# graph QL
SEARCH_DETAIL_QL = open("graphql/detail.graphql").read()
ARTIST_INFO_QL = open("graphql/artistInfo.graphql").read()
PRICING_QL: str = open("graphql/price.graphql").read()


# 初始化 JSON 檔案
def __init__(filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("[\n")


# 修正 JSON 的結尾
def __end__(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    last_line = lines[-1]

    if last_line.endswith(",\n"):
        lines[-1] = last_line[:-2] + "\n]"
    else:
        lines[-1] = "\n]"

    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)


def wirte_to_file(data, filename) -> None:
    with open(filename, "a+", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.write(",\n")  # 添加换行符，以便每个数据条目占一行


class ArtworkSearcher:
    def __init__(self, base_url, page_url, api_url, regex_str):
        self.artwork_url: set = set()
        self.session: Session = Session()
        self.base_url: str = base_url
        self.page_url: str = page_url
        self.regex_str: str = regex_str
        self.api_url: str = api_url
        self.artwork_count = 0
        self.content = None
        self.all_a_link = []

    def get_website_content(self, url) -> bytes:
        request: Response = self.session.get(url)

        if request.status_code > 400:
            raise Exception("Fetch Website Error, status code:", request.status_code)
        return request.content

    def get_all_href_in_page(self, content):
        soup = BeautifulSoup(content, "html.parser")
        href_elements: ResultSet[Any] = soup.find_all("a")
        links = []
        for element in href_elements:
            links.append(element.get("href"))
        return links

    def get_all_img_in_page(self, content):
        soup = BeautifulSoup(content, "html.parser")
        href_elements: ResultSet[Any] = soup.find_all("img")
        links = []
        for element in href_elements:
            links.append(element.get("src"))
        return links

    def get_all_page_name(self) -> set[Any]:
        content: bytes = self.get_website_content(self.page_url)
        links = self.get_all_href_in_page(content)

        # Get all href element
        for link in links:
            refind: Union(re.Match[str], None) = re.search(self.regex_str, link)

            # regex not found
            if not refind:
                continue

            artwork_url: str = refind.group(1)
            self.artwork_url.add(artwork_url)

        # set artwork count
        self.artwork_count = len(self.artwork_url)

        return self.artwork_url

    # get picture
    def get_artwork_pictures(self, links):
        picture_regex = r"https:\/\/d7hftxdivxxvm\.cloudfront\.net\?height=\d+&quality=\d+&resize_to=fit&src=https%3A%2F%2Fd32dm0rphc51dk\.cloudfront\.net%2F[a-zA-Z0-9-_%]+%2Fnormalized\.jpg&width=\d+"
        regex_links = set()

        for link in links:
            refind = re.search(picture_regex, link)
            if not refind:
                continue
            regex_links.add(link)

        return list(regex_links)

    # get artist
    def get_artwork_artist_info(self, slug):
        res: json = self.get_api_response("ArtistInfoQuery", slug, ARTIST_INFO_QL)
        artist_info = res["data"]["artist"]

        # 刪除不必要的資訊
        del artist_info["internalID"]
        del artist_info["initials"]
        del artist_info["image"]
        del artist_info["exhibitionHighlights"]
        del artist_info["highlights"]
        del artist_info["auctionResultsConnection"]
        del artist_info["id"]

        return artist_info

    # get detail
    def get_artwork_detail_api(self, slug):
        artwork_detail = self.get_api_response(
            "ArtworkDetailsQuery", slug, SEARCH_DETAIL_QL
        )
        return artwork_detail

    # get price
    def get_artwork_prices_api(self, slug):
        response = self.get_api_response("PricingContextQuery", slug, PRICING_QL)

        return response

    def get_api_response(self, id, slug, query) -> json:
        req = self.session.post(
            API_URL,
            json={
                "id": id,
                "query": query,
                "variables": {"slug": slug},
            },
        )

        jsonList = json.loads(req.content)
        return jsonList


# Main Function
def main():
    artworkSearcher = ArtworkSearcher(
        base_url=BASEURL,
        page_url=URL,
        api_url=API_URL,
        regex_str=r"/artwork/([a-z-A-Z0-9]+)",
    )
    page_names = artworkSearcher.get_all_page_name()
    artists_href = set()

    for page_name in page_names:
        # 獲取頁面 Content
        print("獲取頁面 Content", end="")
        page_content = artworkSearcher.get_website_content(
            artworkSearcher.base_url + "/artwork/" + page_name
        )

        # 獲取所有的圖片鏈結
        print("\r獲取所有的圖片鏈結", end="")
        image_urls = artworkSearcher.get_artwork_pictures(
            artworkSearcher.get_all_img_in_page(page_content)
        )

        # 獲取 價格
        print("\r獲取 價格", end="")
        artwork_prices_reponse: Any = artworkSearcher.get_artwork_prices_api(page_name)
        artwork_prices = artwork_prices_reponse["data"]["artwork"]["listPrice"]

        # 獲取 作者名稱 與 作者資訊
        print("\r獲取 作者名稱 與 作者資訊", end="")
        artist_name = artwork_prices_reponse["data"]["artwork"]["artists"][0]["slug"]
        artist_info = artworkSearcher.get_artwork_artist_info(artist_name)
        artist_slug = artist_info["slug"]

        # 獲取 作品名稱
        print("\r獲取 作品名稱", end="")
        artwork_name = page_name.replace(artist_slug, "")
        artwork_name = re.sub(r"-\d+$", "", artwork_name)
        artwork_name = artwork_name.replace("-", " ").strip(" ")

        # 獲取 尺寸
        print("\r獲取 尺寸", end="")
        artwork_detail_reponse = artworkSearcher.get_artwork_detail_api(page_name)
        artwork_size = artwork_detail_reponse["data"]["artwork"]["dimensions"]

        # 獲取 作品介紹
        print("\r獲取 作品介紹", end="")
        artwork_description = artwork_detail_reponse["data"]["artwork"]["description"]
        artwork_additional_information = artwork_detail_reponse["data"]["artwork"][
            "additionalInformation"
        ]

        # 獲取 分類
        print("\r獲取 分類", end="")
        artwork_category = artwork_detail_reponse["data"]["artwork"]["category"]

        # 獲取 作品材質
        print("\r獲取 作品材質", end="")
        artwork_material = artwork_detail_reponse["data"]["artwork"]["mediumType"][
            "longDescription"
        ]

        # 獲取 作品的媒介
        print("\r獲取 作品的媒介", end="")
        artwork_medium = artwork_detail_reponse["data"]["artwork"]["medium"]

        artwork = {
            "artworkName": artwork_name,
            "artistName": artist_name,
            "Prices": artwork_prices,
            "size": artwork_size,
            "description": artwork_description,
            "additionalInformation": artwork_additional_information,
            "category": artwork_category,
            "material": artwork_material,
            "medium": artwork_medium,
            "images": image_urls,
        }

        print("\r寫入檔案", end="")
        wirte_to_file(artwork, STORE_FILE_NAME)

        if artist_info["href"] not in artists_href:
            artists_href.add(artist_info["href"])
            wirte_to_file(artist_info, STORE_ARTIST_NAME)

        print("\r" + artwork_name + " ==> 完成")


if __name__ == "__main__":
    __init__(STORE_FILE_NAME)
    __init__(STORE_ARTIST_NAME)
    main()
    __end__(STORE_FILE_NAME)
    __end__(STORE_ARTIST_NAME)
