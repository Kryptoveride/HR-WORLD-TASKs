from scapy.all import sniff, conf
from scapy.layers.inet import IP, TCP
import socket


# ANSI terminal colors
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
RED = "\033[91m"

packet_count = 0

COMMON_PORTS = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL"
}


def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"


def process_packet(packet):
    global packet_count

    if not packet.haslayer(IP) or not packet.haslayer(TCP):
        return

    packet_count += 1

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_port = packet[TCP].sport
    dst_port = packet[TCP].dport

    service = COMMON_PORTS.get(dst_port, "Unknown")
    dst_host = resolve_hostname(dst_ip)

    print(
        f"{BOLD}{packet_count:<5}{RESET}"
        f"{CYAN}{src_ip:<18}{RESET}"
        f"{GREEN}{src_port:<10}{RESET}"
        f"{MAGENTA}{'------->':<10}{RESET}"
        f"{YELLOW}{dst_ip:<18}{RESET}"
        f"{BLUE}{dst_port:<10}{RESET}"
        f"{GREEN}{service:<12}{RESET}"
        f"{RED}{dst_host}{RESET}"
    )


print(f"{BOLD}{GREEN}Starting IPv4 Live Packet Inspection{RESET}")
print(f"{CYAN}Interface:{RESET} {conf.iface}")
print(f"{YELLOW}Open a website to generate TCP traffic.{RESET}")
print(f"{YELLOW}Press Ctrl+C to stop.{RESET}\n")

print(
    f"{BOLD}"
    f"{'#':<5}"
    f"{'Source IP':<18}"
    f"{'Src Port':<10}"
    f"{'':<10}"
    f"{'Destination IP':<18}"
    f"{'Dst Port':<10}"
    f"{'Service':<12}"
    f"{'Destination Host'}"
    f"{RESET}"
)

print("-" * 120)

try:
    sniff(
        iface=conf.iface,
        filter="ip and tcp",
        prn=process_packet,
        store=False
    )

except KeyboardInterrupt:
    print(f"\n{RED}Packet inspection stopped.{RESET}")

except PermissionError:
    print(f"\n{RED}Permission denied. Run the script using sudo.{RESET}")

except Exception as error:
    print(f"\n{RED}Error: {error}{RESET}")