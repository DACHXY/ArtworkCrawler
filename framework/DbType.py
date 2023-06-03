from typing import List, NoReturn, Any
from tools.helper import get_variable_name
from models.db_model import DBModel


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


class ForeignKey:
    def __init__(self, DBModel):
        self.db_model = DBModel

    def get_foreign_key_reference(self):
        return self.db_model


class DBType:
    class DBTypeBase:
        def __init__(
            self,
            init_type: str,
            primary_key: bool = False,
            foreign_key: ForeignKey | None = None,
        ):
            self.type: str = init_type
            self.primary_key: bool = primary_key
            self.foreign_key: ForeignKey | None = foreign_key

        def get_data_type(self) -> str:
            return self.type

        def is_primary_key(self) -> bool:
            return self.primary_key

        def is_foreign_key(self) -> bool:
            if self.foreign_key is not None:
                return True
            return False

        def get_foreign_key_reference(self) -> DBModel:
            return self.foreign_key.get_foreign_key_reference()

    class String(DBTypeBase):
        def __init__(
            self,
            n=False,
            var=False,
            len=255,
            other_options: List = None,
            primary_key=False,
            foreign_key: ForeignKey | None = None,
        ) -> str:
            super().__init__("", primary_key, foreign_key)
            if n:
                self.type += "N"
            if var:
                self.type += "VAR"
            self.type += "CHAR"
            self.type += f"({len})"
            if other_options != None:
                if type(other_options) == type(list):
                    self.type += f" {' '.join(other_options)}"
                if type(other_options) == type(str):
                    self.type += f" {other_options}"

    class Int(DBTypeBase):
        def __init__(
            self,
            primary_key=False,
            foreign_key: ForeignKey | None = None,
        ):
            super().__init__("INT", primary_key, foreign_key)

    class DateTime(DBTypeBase):
        def __init__(
            self,
            primary_key=False,
            foreign_key: ForeignKey | None = None,
        ):
            super().__init__("DATETIME", primary_key, foreign_key)
