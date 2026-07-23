import socket
from colorama import Fore, Style, init
init(autoreset=True)

PORTS = [22, 80, 443]

def banner():
    print(r"""
       _____         _                _____        __
      / ____|       | |              |  __ \      / _|
     | |     _    _ | |__   ___ _ __ | |  | | ___| |_ ___ _ __  ___  ___
     | |    | '  | ||| '_ \ / _ \ '__|| |  | |/ _ \  _/ _ \ '_ \/ __|/ _ \
     | |____| |  | || |_) |  __/ |   | |__| |  __/ ||  __/ | | \__ \  __/
      \_____|_|  | ||_.__/ \___|_|   |_____/ \___|_| \___|_| |_|___/\___|
            \ \  / /
             \ \  /
              \/ /
              /_/    ☠  CYBER DEFENCE CHECK  ☠
    ===================================================================
            Default Ports : 22 (SSH) | 80 (HTTP) | 443 (HTTPS)
                      Socket Timeout: 2 Seconds
    ===================================================================
    """)

def check_host(host, port):
    try:
        ip = socket.gethostbyname(host)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        result = s.connect_ex((ip, port))

        if result == 0:
            print(f'{Fore.GREEN} [+] Host: {host} ({ip}) | Port {port} is OPEN and accepting connections.')
        else:
            print(f'{Fore.RED} [-] Host: {host} ({ip}) | Port {port} is CLOSED and not accepting connections.')

        s.close()

    except socket.gaierror:
        print(f"{Fore.RED} [x] Unable to resolve {host}")
    except Exception as e:
        print(f"{Fore.RED} [x] Error: {e}")


def scan_default_targets():
    targets = [
        "google.com",
        "scanme.nmap.org",
        "thiswebsitedoesnotexist123.com"
    ]

    print("\nRunning Network Scan...\n")
    count = 1
    for target in targets:
        print(f"Target {count}/{len(targets)} : {target}")
        for port in PORTS:
            check_host(target, port)
        print("-" * 60)
        count += 1


def scan_single_host():
    host = input("\nEnter Hostname or IP Address: ")
    print()
    for port in PORTS:
        check_host(host, port)


def scan_ip_range():
    base = input("\nEnter Base IP (Example: 192.168.1.): ")
    start = int(input("Enter Start Host: "))
    end = int(input("Enter End Host: "))

    print()

    for i in range(start, end + 1):
        ip = f"{base}{i}"

        print(f"Scanning {ip}")

        for port in PORTS:
            check_host(ip, port)

        print("-" * 60)

banner()

while True:

    print("""
==================== MENU ====================

1. Scan Default Targets
2. Scan IP Range
3. Scan Single Host
4. Exit

==============================================
""")

    choice = input("Select an option: ")

    if choice == "1":
        scan_default_targets()

    elif choice == "2":
        scan_ip_range()

    elif choice == "3":
        scan_single_host()

    elif choice == "4":
        print("\nCyber Defense Check Completed.")
        break

    else:
        print("\nInvalid option. Please try again.\n")