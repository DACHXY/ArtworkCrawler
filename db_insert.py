from db_connect import connection_to_db
import json

def create_database(cursor):
    try:
        sql = open("db_scripts/ArtworkDB.sql", "r").read()
        cursor.execute(sql)
        print("資料表創建成功!")
        return True
    except Exception as e:
        print("資料表創建失敗:", e)
        return False
        
def insert_artwork(cursor, artwork_data):
    sql = """
    INSERT INTO artwork (slug, artwork_name, artist_slug, price, size_in, size_cm, description, additional_information, material, medium, image)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # 執行插入資料的 SQL 指令
    cursor.execute(sql, artwork_data)

def insert_artist(cursor, artist_data):
    try:
        # 執行插入資料的 SQL 指令
        sql = "INSERT INTO artist (slug, name, biography, avatar) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, artist_data)
        
        print("插入資料成功")
    except Exception as e:
        print("資料庫錯誤:", e)


def main():
    cursor = connection_to_db()

    if not create_database(cursor):
        exit()

    artist_json = json.load(open("data/Artists.json", "r"))
    artwork_json = json.load(open("data/Artworks.json", "r"))

    print("ARTIST: ", len(artist_json))
    print("ARTWORK: ", len(artwork_json))

    artist_slug_list = [artist["slug"] for artist in artist_json]
    artist_added_slug = []
    artwork_added_slug = []

    for artist in artist_json:
        slug = artist["slug"]
        if slug in artist_added_slug:
            continue
        artist_added_slug.append(slug)
        artist_data = (slug, artist["name"], artist["biographyBlurb"]["text"], artist["avatar"]["cropped"]["src"])
        insert_artist(cursor=cursor, artist_data=artist_data)

    for artwork in artwork_json:
        slug = artwork["artistName"] + "-"+ "-".join(artwork["artworkName"].split(" "))

        if slug in artwork_added_slug:
            print("S ERROR")
            continue
        if artwork["artistName"] not in artist_slug_list:
            print("N ERROR")
            continue
        if artwork.get("Prices") == None:
            continue
        if artwork.get("images") == None:
            continue
        if len(artwork.get("images")) == 0:
            continue

        artwork_added_slug.append(slug)
        
        price = artwork["Prices"].get("minor")
        if price is None:
            price = int(artwork["Prices"].get("maxPrice").get("minor")) / 10

        artwork_data = (slug, 
                        artwork["artworkName"], 
                        artwork["artistName"], 
                        price, 
                        artwork["size"]["in"], 
                        artwork["size"]["cm"],
                        artwork["description"],
                        artwork["additionalInformation"],
                        "\'"+artwork["material"]+"\'",
                        "\'"+artwork["medium"]+"\'",
                        artwork["images"][0]
                        )
        insert_artwork(cursor=cursor, artwork_data=artwork_data)

    cursor.commit()
    cursor.close()
    
    
if __name__ == "__main__":
    main()