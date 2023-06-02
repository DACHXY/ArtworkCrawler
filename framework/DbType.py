from typing import List, NoReturn, Any

class DbListType(list):
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
            
class DbStringType(str):
    def __init__(self, string):
        super().__init__()
        self.string = string
