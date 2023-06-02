from models.db_model import DBModel
from tools.helper import get_sub_class_names, get_sub_classes


def get_properties_and_type_string(properties : dict) -> str:
    string: str = ""
    for key, value in properties:
        string += f"{key} {value},\n"
        
    string.strip(",\n")
    string += "\n"
    
    return string

def generate_insert_script(table_name, properties_string) -> str:
    INSERT_SCRIPT = (
        f"CREATE TABLE {table_name} (\n"
        f"{properties_string}"
        "\n)"
    )   
    return INSERT_SCRIPT

db_classes = get_sub_classes(DBModel)

for db_class in db_classes:
    # 實例化
    db_model = db_class()
    
    properties = {}
    table_name = db_class.__name__
    cls_dict = vars(db_class).items()
    
    for property, dbtype in cls_dict:
        if property.startswith("__"):
            continue
        bruh = getattr(db_model, property)
        print(property, bruh.get_type())
    
    # properties_string = get_properties_and_type_string(properties)
    # generate_insert_script()