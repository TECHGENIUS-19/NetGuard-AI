import sqlite3

connection = sqlite3.connect("data/netguard.db")

cursor = connection.cursor()

cursor.execute("""
INSERT INTO traffic
(timestamp, source_ip, destination_ip, protocol, source_port, destination_port, packet_size)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "2026-09-14 21:30:00",
    "10.30.83.242",
    "3.5.149.144",
    "TCP",
    63681,
    443,
    1474
))

connection.commit()

cursor.execute("SELECT * FROM traffic")

rows = cursor.fetchall()

print("========================================")
print("       NETGUARD AI DATABASE TEST")
print("========================================")

for row in rows:
    print(row)

connection.close()
