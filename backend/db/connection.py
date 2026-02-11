import os
from dotenv import load_dotenv

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")


def get_connection():
    """
    Returns a database connection.
    In TEST_MODE, returns None and avoids importing pyodbc.
    """

    # 🚫 Do not connect to DB during tests / CI
    if os.getenv("TEST_MODE") == "true":
        return None

    # ✅ Import only when actually needed
    import pyodbc

    conn = pyodbc.connect(
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        "Trusted_Connection=yes;"
    )
    return conn
