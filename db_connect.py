import pyodbc

# config
SERVER = "sql-server-2"
DBNAME = "ArtworkDB"
USERNAME = "sa"
PASSWORD = "Danny10132024..."
DRIVER = "ODBC Driver 18 for SQL Server"

conn_str = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DBNAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
)

def connection_to_db() -> pyodbc.Cursor :
    conn = pyodbc.connect(conn_str)
    return conn.cursor()

if __name__ == "__main__":
    try:
        db = connection_to_db()
        print("Connected to DataBase")
    except Exception as e:
        print(f"Error occured: {e}")
        