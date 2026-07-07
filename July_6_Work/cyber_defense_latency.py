import socket
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init

init(autoreset=True)

def banner():
    print(r"""
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
            print(f"{Fore.GREEN}[+] Port {port} is OPEN with a connection delay of {latency:.2f} ms. {service} service can be reached.")
        else:
            print(f"{Fore.RED}[-] Port {port} is CLOSED or FILTERED with no connection delay recorded. {service} service cannot be reached.")

        s.close()

    except socket.gaierror:
        print(f"{Fore.RED}[x] Hostname {hostname} could not be resolved.")

    except Exception as e:
        print(f"{Fore.RED}[x] An error occurred: {e}")


def scan_with_python():
    for label, hostname in infrastructure.items():
        print(f"\nInitializing Python Security Profile: {label} ({hostname})")

        host_start = time.time()

        for port, service in ports.items():
            check_host_python(hostname, port, service)

        host_time = time.time() - host_start
        print(f"Total scan time for {label}: {host_time:.2f} seconds")
        print("-" * 60)


def scan_with_nmap():
    port_list = ",".join(str(port) for port in ports.keys())

    for label, hostname in infrastructure.items():
        print(f"\nInitializing Nmap Security Profile: {label} ({hostname})")

        host_start = time.time()

        try:
            command = ["nmap", "-Pn", "-p", port_list, hostname]
            result = subprocess.run(command, capture_output=True, text=True)

            print(result.stdout)

            if result.stderr:
                print(result.stderr)

        except FileNotFoundError:
            print(f"{Fore.RED}[x] Nmap is not installed or not found in PATH.")

        except Exception as e:
            print(f"{Fore.RED}[x] An error occurred: {e}")

        host_time = time.time() - host_start
        print(f"Total scan time for {label}: {host_time:.2f} seconds")
        print("-" * 60)


def scan_with_multithreading():
    for label, hostname in infrastructure.items():
        print(f"\nInitializing Multithreaded Security Profile: {label} ({hostname})")

        host_start = time.time()

        with ThreadPoolExecutor(max_workers=10) as executor:
            for port, service in ports.items():
                executor.submit(check_host_python, hostname, port, service)

        host_time = time.time() - host_start
        print(f"Total scan time for {label}: {host_time:.2f} seconds")
        print("-" * 60)


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
        scan_with_python()

    elif choice == "2":
        scan_with_nmap()

    elif choice == "3":
        scan_with_multithreading()

    elif choice == "4":
        print("\nCyber Defence Check Completed.")
        break

    else:
        print("\nInvalid option. Please try again.\n")