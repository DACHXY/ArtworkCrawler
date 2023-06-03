from db_connect import connection_to_db

class DBItem:
    def __init__(self, db_class) -> None:
        pass

class DBTypeList:
    def __init__(self, db_class):
        print(db_class)

# Table 類別
class SQLTable:
    def __init__(self):
        pass    
    
        
# Context 類別
class SQLContext:
    def __init__(self):
        self.cursor = connection_to_db()
        self.table_names = []
        
        # 獲取 table 的名稱
        query = "SELECT name FROM sys.tables;"
        self.cursor.execute(query)
        table_results = self.cursor.fetchall()
        
        self.table_names = [result[0] for result in table_results]

        # 設定 table
        for table_name in self.table_names:
            setattr(self, table_name, None)

    @property
    def dynamic_property(self):
        return self._dynamic_property
    
    @dynamic_property.setter
    def dynamic_property(self, value):
        self._dynamic_property = DBTypeList(SQLTable)

    def close(self):
        self.cursor.close()
        
        
if __name__ == "__main__":
    context = SQLContext()
    print(context.table_names)
    context.test()