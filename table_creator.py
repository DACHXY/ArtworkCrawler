from typing import List
from models.db_model import DBModel
from tools.helper import get_sub_classes


class DBModelAnalyzer:
    """_summary_"""

    def __init__(self, db_class):
        self.db_class = db_class
        self.db_class_instance = db_class()
        self.db_class_property_dict = {
            k: getattr(self.db_class_instance, v)
            for k, v in vars(db_class).items()
            if not k.startswith("__")
        }
        self.table_name = db_class.__name__

    def get_table_name(self) -> str:
        """Get the table name of DB model

        Returns:
            str: Table's name
        """
        return self.table_name

    def get_primary_key(self) -> List[str]:
        """Get the name of property which is primary key

        Returns:
            List[str]: _description_
        """
        primary_keys = []
        for prop, data in self.db_class_property_dict:
            if data.is_primary_key():
                primary_keys.append(prop)
        return primary_keys

    def get_foreign_key(self) -> dict[str, DBModel]:
        foreign_keys: dict[str, DBModel] = {}
        for prop, data in self.db_class_property_dict:
            if data.is_foreign_key():
                foreign_keys[prop] = data.get_foreign_key_reference()
        return foreign_keys


class MultiDBModelAnalyzer:
    def __init__(self):
        self.db_classes = get_sub_classes(DBModel)

    def get_class_properties_to_dict(self):
        pass


def get_properties_and_type_string(properties: dict, primary_keys: List) -> str:
    """_summary_

    Args:
        properties (dict): _description_
        primary_keys (List): _description_

    Returns:
        str: _description_
    """
    string: str = ""
    for key in properties:
        string += f"{key} {properties[key]}, "

    for key in primary_keys:
        string += f"PRIMARY KEY ({key})"

    string = string.rstrip(", ")
    return string


def get_create_table_script(table_name, properties_string) -> str:
    INSERT_SCRIPT = f"CREATE TABLE {table_name} (\n" f"{properties_string}" "\n)"
    return INSERT_SCRIPT


def get_class_properties_to_dict(_class) -> dict[str, str]:
    # 實例化
    db_model = _class()
    cls_dict = vars(_class).items()
    properties = {}
    primary_keys = []
    for property, dbtype in cls_dict:
        if property.startswith("__"):
            continue

        attr = getattr(db_model, property)
        properties[property] = attr.get_data_type()
        if attr.is_primary_key():
            primary_keys.append(property)

    properties[""] = f"PRIMARY KEY ({' '.join(primary_keys)})"

    return properties


def get_sql_create_table_script():
    db_classes = get_sub_classes(DBModel)
    scripts = []
    for db_class in db_classes:
        table_name = db_class.__name__
        properties: dict[str, str] = get_class_properties_to_dict(db_class)
        properties_string = get_properties_and_type_string(properties)
        create_table_script = get_create_table_script(table_name, properties_string)
        scripts.append(create_table_script)

    return "\n\n".join(scripts)


if __name__ == "__main__":
    sql_script = get_sql_create_table_script()
    print(sql_script)
