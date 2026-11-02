from scapy.all import sniff, IP, TCP, UDP
import sqlite3
from datetime import datetime

DATABASE = "data/netguard.db"


def save_packet(packet):

    if IP not in packet:
        return

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst
    packet_size = len(packet)

    if TCP in packet:
        protocol = "TCP"
        source_port = packet[TCP].sport
        destination_port = packet[TCP].dport

    elif UDP in packet:
        protocol = "UDP"
        source_port = packet[UDP].sport
        destination_port = packet[UDP].dport

    else:
        protocol = "Other"
        source_port = 0
        destination_port = 0

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO traffic
        (timestamp, source_ip, destination_ip, protocol,
         source_port, destination_port, packet_size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            source_ip,
            destination_ip,
            protocol,
            source_port,
            destination_port,
            packet_size
        )
    )

    connection.commit()
    connection.close()

    print(
        timestamp,
        "|",
        source_ip,
        "->",
        destination_ip,
        "|",
        protocol,
        "|",
        source_port,
        "->",
        destination_port,
        "|",
        packet_size,
        "bytes"
    )


print("========================================")
print("       NETGUARD AI TRAFFIC LOGGER")
print("========================================")
print("Saving live traffic to database...")
print("Press CTRL+C to stop.")
print()

sniff(prn=save_packet, store=False)
