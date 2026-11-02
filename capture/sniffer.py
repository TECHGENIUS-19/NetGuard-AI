from scapy.all import sniff, IP, TCP, UDP

def process_packet(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst

        if TCP in packet:
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport

        elif UDP in packet:
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

        else:
            protocol = "Other"
            src_port = "-"
            dst_port = "-"

        print("----------------------------------------")
        print("NETGUARD AI - LIVE TRAFFIC")
        print("Source IP      :", src)
        print("Destination IP :", dst)
        print("Protocol       :", protocol)
        print("Source Port    :", src_port)
        print("Destination Port:", dst_port)
        print("Packet Size    :", len(packet))
        print("----------------------------------------")


print("========================================")
print("        NETGUARD AI NETWORK MONITOR")
print("========================================")
print("Capturing network traffic...")
print("Press CTRL+C to stop.")
print()

sniff(prn=process_packet, store=False)
