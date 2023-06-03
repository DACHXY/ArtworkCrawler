import datetime
from typing import List
from framework.DbType import DBType


class DBModel:
    pass


class User(DBModel):
    id: DBType.Int = DBType.Int(primary_key=True)
    username: DBType.String = DBType.String(n=True, var=True, len=255)
    email: DBType.String = DBType.String(n=True, var=True, len=255)
    hashed_password: DBType.String = DBType.String()
    create_at: DBType.DateTime = DBType.DateTime()
    artist_id: DBType.Int = DBType.Int()


class Artist(DBModel):
    id = DBType.Int(primary_key=True)
    slug = DBType.String()
    name = DBType.String()
    biography = DBType.String()
    avatar = DBType.String()
