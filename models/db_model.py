import datetime
from typing import List
from tools.helper import get_variable_name

class DBType:
    class DBTypeBase:
        def __init__(self, init_type):
            self.type = init_type

        def get_type(self):
            return self.type
    
    class String(DBTypeBase):
        def __init__(self, n=False, var=False, len=255, other_options: List =None) -> str:
            super().__init__("")
            if n: self.type += "N"
            if var: self.type += "VAR"
            self.type += "CHAR"
            self.type += f"({len}) "
            if other_options != None: 
                if type(other_options) == type(list):
                    self.type += f" {' '.join(other_options)}"
                if type(other_options) == type(str):
                    self.type += f" {other_options}"
    
    class Int(DBTypeBase):
        def __init__(self):
            super().__init__("INT")

    class DateTime(DBTypeBase):
        def __init__(self):    
            super().__init__("DATETIME")
            
    class PrimaryKey:
        def __init__(self, *keys):
            self.pks = []
            for key in keys:
                self.pks.append(get_variable_name(key)) 

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