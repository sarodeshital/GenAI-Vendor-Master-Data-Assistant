import sqlite3
import pandas as pd

def create_database(df: pd.DataFrame, db_path: str = ":memory:"):
    conn = sqlite3.connect(db_path)
    df.to_sql("vendor_master", conn, if_exists="replace", index=False)
    return conn

def high_risk_vendors(conn):
    query = """
    SELECT vendor_id, vendor_name, country, status,
           quality_score, missing_critical_fields
    FROM vendor_master
    WHERE quality_score < 80
    ORDER BY quality_score ASC;
    """
    return pd.read_sql_query(query, conn)
