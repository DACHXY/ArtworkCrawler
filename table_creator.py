from models.db_model import DBModel
from tools.helper import get_sub_classes

def get_properties_and_type_string(properties : dict) -> str:
    string: str = ""
    for key in properties:
        string += f"{key} {properties[key]}, "
        
    string = string.rstrip(", ")
    return string

def get_create_table_script(table_name, properties_string) -> str:
    INSERT_SCRIPT = (
        f"CREATE TABLE {table_name} (\n"
        f"{properties_string}"
        "\n)"
    )   
    return INSERT_SCRIPT

def get_class_properties_to_dict(_class) -> dict[str, str]:
    # 實例化
    db_model = _class()
    cls_dict = vars(_class).items()
    properties = {}
    for property, dbtype in cls_dict:
        if property.startswith("__"):
            continue
        attr = getattr(db_model, property)
        properties[property] = attr.get_data_type()
                
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
    
    return '\n\n'.join(scripts)
    
if __name__ == "__main__":
    sql_script = get_sql_create_table_script()
    print(sql_script)