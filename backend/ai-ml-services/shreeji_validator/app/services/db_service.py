import sqlite3
from sqlite3 import Connection
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "certificate_db.sqlite"

def init_db():
    """Initialize database with certificate table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            student_name TEXT,
            degree TEXT,
            status TEXT,
            anomaly_score REAL,
            blockchain_verified BOOLEAN
        )
    """)
    conn.commit()
    conn.close()

def save_certificate(data: dict):
    """Save certificate verification result"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO certificates (filename, student_name, degree, status, anomaly_score, blockchain_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("filename"),
        data.get("student_name", ""),
        data.get("degree", ""),
        data.get("status"),
        data.get("anomaly_score"),
        data.get("blockchain_verified")
    ))
    conn.commit()
    conn.close()

def fetch_certificates():
    """Fetch all certificates"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize DB when module is imported
init_db()
