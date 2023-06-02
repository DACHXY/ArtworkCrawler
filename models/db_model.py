import datetime
from typing import List
from framework.DbType import DBType

class DBModel:
    pass

class User(DBModel):
    id: int = DBType.Int()
    username: str = DBType.String(n=True, var=True, len=255)
    email :str = DBType.String(n=True, var=True, len=255)
    hashed_password: str = DBType.String()
    create_at: datetime = DBType.DateTime()
    
class Artist(DBModel):
    id = DBType.Int()
    slug = DBType.String()
    name = DBType.String()
    biography = DBType.String()
    avatar = DBType.String()
