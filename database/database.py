import sqlite3

DATABASE = "data/netguard.db"

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    source_ip TEXT,
    destination_ip TEXT,
    protocol TEXT,
    source_port INTEGER,
    destination_port INTEGER,
    packet_size INTEGER
)
""")

connection.commit()
connection.close()

print("NetGuard AI database created successfully.")
