from db_connect import connection_to_db
import json

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


cursor = connection_to_db()

artist_json = json.load(open("data/Artists.json"))
artwork_json = json.load(open("data/Artworks.json"))

print("ARTIST: ", len(artist_json))
print("ARTWORK: ", len(artwork_json))

for artist in artist_json:
    artist_data = (artist["slug"], artist["name"], artist["biographyBlurb"]["text"], artist["avatar"]["cropped"]["src"])
    # insert_artist(cursor=cursor, artist_data=artist_data)



for artwork in artwork_json:
    slug = artwork["artistName"] + "-"+ "-".join(artwork["artworkName"].split(" "))
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
    # insert_artwork(cursor=cursor, artwork_data=artwork_data)

# cursor.commit()
cursor.close()