from typing import List, NoReturn, Any
from tools.helper import get_variable_name

class DBListType(list):
    def __init__(self, list, type) -> None:
        super().__init__()
        self.list: List[type] = list
    
    def where(self, lambda_expression) -> list:
        return list(filter(lambda_expression, self.list))
    
    def is_null_or_empty(self) -> bool:
        if self.list == None:
            return True
        if len(self.list) == 0:
            return True
        return False

    def first_or_default(self, lambda_expression) -> Any:
        new_list = self.where(lambda_expression)
        if len(new_list) == 0:
            return None
        return new_list[0]
    
    def containes(self, item) -> bool:
        if item in self.list:
            return True
        return False

    def add(self, item):
        self.list.append(item)
        
    def foreach(self, function) -> NoReturn:
        for item in self.list:
            function(item)
            
class DBStringType(str):
    def __init__(self, string):
        super().__init__()
        self.string = string

class DBType:
    class DBTypeBase:
        def __init__(self, init_type):
            self.type = init_type

        def get_data_type(self):
            return self.type
    
    class String(DBTypeBase):
        def __init__(self, n=False, var=False, len=255, other_options: List =None) -> str:
            super().__init__("")
            if n: self.type += "N"
            if var: self.type += "VAR"
            self.type += "CHAR"
            self.type += f"({len})"
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
