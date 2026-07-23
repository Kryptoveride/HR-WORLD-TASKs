import socket
import time
import subprocess
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

LOG_FILE = "scan_report.txt"

def log(message=""):
    print(message)

    clean_message = re.sub(r'\x1b\[[0-9;]*m', '', str(message))

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {clean_message}\n")


def banner():
    log(r"""
       _____         _                _____        __
      / ____|       | |              |  __ \      / _|
     | |     _   _  | |__   ___ _ __ | |  | | ___| |_ ___ _ __  ___  ___
     | |    | | | | | '_ \ / _ \ '__|| |  | |/ _ \  _/ _ \ '_ \/ __|/ _ \
     | |____| |_| | | |_) |  __/ |   | |__| |  __/ ||  __/ | | \__ \  __/
      \_____|\__, | |_.__/ \___|_|   |_____/ \___|_| \___|_| |_|___/\___|
              __/ |
             |___/

                           ☠  CYBER DEFENCE CHECK  ☠
    ======================================================================
                     Python Socket | Nmap | Multithreading
                          Socket Timeout: 2 Seconds
    ======================================================================
""")


infrastructure = {
    "Nmap Playground": "scanme.nmap.org",
    "Public Gateway": "google.com",
    "Dead System Simulator": "qwerty.local"
}

ports = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS"
}

timeout = 2


def check_host_python(hostname, port, service):
    try:
        ip = socket.gethostbyname(hostname)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        start_time = time.time()
        status = s.connect_ex((ip, port))
        latency = (time.time() - start_time) * 1000

        if status == 0:
            log(f"{Fore.GREEN}[+] Port {port} is OPEN with a connection delay of {latency:.2f} ms. {service} service can be reached.")
        else:
            log(f"{Fore.RED}[-] Port {port} is CLOSED or FILTERED with no connection delay recorded. {service} service cannot be reached.")

        s.close()

    except socket.gaierror:
        log(f"{Fore.RED}[x] Hostname {hostname} could not be resolved.")

    except Exception as e:
        log(f"{Fore.RED}[x] An error occurred: {e}")


def scan_with_python():
    for label, hostname in infrastructure.items():
        log(f"\nInitializing Python Security Profile: {label} ({hostname})")

        host_start = time.time()

        for port, service in ports.items():
            check_host_python(hostname, port, service)

        host_time = time.time() - host_start
        log(f"Total scan time for {label}: {host_time:.2f} seconds")
        log("-" * 60)


def scan_with_nmap():
    port_list = ",".join(str(port) for port in ports.keys())

    for label, hostname in infrastructure.items():
        log(f"\nInitializing Nmap Security Profile: {label} ({hostname})")

        host_start = time.time()

        try:
            command = ["nmap", "-Pn", "-p", port_list, hostname]
            result = subprocess.run(command, capture_output=True, text=True)

            log(result.stdout)

            if result.stderr:
                log(result.stderr)

        except FileNotFoundError:
            log(f"{Fore.RED}[x] Nmap is not installed or not found in PATH.")

        except Exception as e:
            log(f"{Fore.RED}[x] An error occurred: {e}")

        host_time = time.time() - host_start
        log(f"Total scan time for {label}: {host_time:.2f} seconds")
        log("-" * 60)


def scan_with_multithreading():
    for label, hostname in infrastructure.items():
        log(f"\nInitializing Multithreaded Security Profile: {label} ({hostname})")

        host_start = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            for port, service in ports.items():
                executor.submit(check_host_python, hostname, port, service)

        host_time = time.time() - host_start
        log(f"Total scan time for {label}: {host_time:.2f} seconds")
        log("-" * 60)


log("=" * 70)
log("Cyber Defence Check Started")
log("=" * 70)

banner()

while True:
    print("""
==================== MENU ====================

1. Port Scan Using Python
2. Port Scan Using Nmap
3. Port Scan Using Multithreading
4. Exit

==============================================
""")

    choice = input("Select an option: ")

    if choice == "1":
        log("Selected Option 1: Port Scan Using Python")
        scan_with_python()

    elif choice == "2":
        log("Selected Option 2: Port Scan Using Nmap")
        scan_with_nmap()

    elif choice == "3":
        log("Selected Option 3: Port Scan Using Multithreading")
        scan_with_multithreading()

    elif choice == "4":
        log("\nCyber Defence Check Completed.")
        break

    else:
        log("\nInvalid option. Please try again.\n")