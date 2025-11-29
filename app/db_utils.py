import sqlite3
import pandas as pd
from dataclasses import dataclass, asdict
DB_FILE = "dim_incidents.db"

@dataclass
class IncidentRecord:
    subject:str 
    body:str
    intent:str
    customer_name:str
    product:str
    requested_action:str
    email:str


# ==========================================
# 2. DATA FUNCTIONS
# ==========================================
def load_data():
    """Reads the current state of the database."""
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM incidents ORDER BY id DESC", conn)
    return df

def to_insert_sql(record: IncidentRecord):
    data = asdict(record)

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))

    sql = f"INSERT INTO incidents ({columns}) VALUES ({placeholders})"
    values = tuple(data.values())

    return sql, values


def insert_record(incident_input:IncidentRecord):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        sql,values = to_insert_sql(incident_input)
        conn.execute(sql,values)
        conn.commit()
    return True

