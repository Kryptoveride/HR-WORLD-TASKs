import argparse
import socket
import sys
import time


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


COMMON_PORTS = {
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


def banner():
    print(f"""{CYAN}{BOLD}
   ______      __              ____       ____                     
  / ____/_  __/ /_  ___  _____/ __ \\___  / __/__  ____  _________ 
 / /   / / / / __ \\/ _ \\/ ___/ / / / _ \\/ /_/ _ \\/ __ \\/ ___/ _ \\
/ /___/ /_/ / /_/ /  __/ /  / /_/ /  __/ __/  __/ / / (__  )  __/
\\____/\\__, /_.___/\\___/_/  /_____/\\___/_/  \\___/_/ /_/____/\\___/
     /____/

              ☠  CYBER DEFENCE CHECK  ☠
{RESET}""")


def resolve_host(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"{RED}[ERROR] Unable to resolve host: {hostname}{RESET}")
        return None


def check_port(ip, port, timeout=1.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((ip, port)) == 0
    except OSError:
        return False


def print_header(title):
    print(f"\n{CYAN}{'=' * 65}")
    print(f"{title:^65}")
    print(f"{'=' * 65}{RESET}")


def ping_scan(hostname=None):
    print_header("HTTP CONNECTION CHECK")

    hostname = hostname or input("Enter hostname or IP address: ").strip()
    ip = resolve_host(hostname)

    if not ip:
        return

    print(f"Target: {hostname} ({ip})")
    print(f"Testing TCP port 80...\n")

    successful = 0

    for attempt in range(1, 6):
        if check_port(ip, 80, 2):
            successful += 1
            print(
                f"{GREEN}[{attempt}/5] SUCCESS "
                f"HTTP port 80 is accepting connections.{RESET}"
            )
        else:
            print(
                f"{RED}[{attempt}/5] FAILED  "
                f"HTTP port 80 is not accepting connections.{RESET}"
            )

        time.sleep(0.2)

    print(f"\nResult: {successful}/5 successful connections")


def port_scan(hostname=None, port=None):
    print_header("SINGLE PORT SCANNER")

    hostname = hostname or input("Enter hostname or IP address: ").strip()

    if port is None:
        try:
            port = int(input("Enter port number: "))
        except ValueError:
            print(f"{RED}[ERROR] Port must be a number.{RESET}")
            return

    if not 1 <= port <= 65535:
        print(f"{RED}[ERROR] Port must be between 1 and 65535.{RESET}")
        return

    ip = resolve_host(hostname)

    if not ip:
        return

    print(f"Target: {hostname} ({ip})")
    print(f"Port:   {port}\n")

    successful = 0

    for attempt in range(1, 6):
        if check_port(ip, port, 2):
            successful += 1
            print(
                f"{GREEN}[{attempt}/5] OPEN    "
                f"Port {port} accepted the connection.{RESET}"
            )
        else:
            print(
                f"{RED}[{attempt}/5] CLOSED  "
                f"Port {port} rejected or timed out.{RESET}"
            )

        time.sleep(0.2)

    print(f"\nResult: {successful}/5 successful connections")


def top_port_scan(hostname=None):
    print_header("TOP 10 PORT SCANNER")

    hostname = hostname or input("Enter hostname or IP address: ").strip()
    ip = resolve_host(hostname)

    if not ip:
        return

    print(f"Target: {hostname} ({ip})")
    print(f"{'-' * 65}")
    print(f"{'PORT':<10}{'SERVICE':<20}{'STATUS':<15}")
    print(f"{'-' * 65}")

    open_ports = 0

    for port, service in COMMON_PORTS.items():
        if check_port(ip, port):
            open_ports += 1
            status = f"{GREEN}OPEN{RESET}"
        else:
            status = f"{RED}CLOSED{RESET}"

        print(f"{port:<10}{service:<20}{status}")

    print(f"{'-' * 65}")
    print(f"Scan completed. Open ports found: {open_ports}")


def menu():
    while True:
        banner()

        print(f"""
{YELLOW}[1]{RESET} HTTP Connection Check
{YELLOW}[2]{RESET} Single Port Scan
{YELLOW}[3]{RESET} Top 10 Port Scan
{YELLOW}[4]{RESET} Exit
""")

        choice = input("Select an option: ").strip()

        if choice == "1":
            ping_scan()
        elif choice == "2":
            port_scan()
        elif choice == "3":
            top_port_scan()
        elif choice == "4":
            print(f"{CYAN}Cyber Defence Check terminated.{RESET}")
            break
        else:
            print(f"{RED}[ERROR] Invalid menu option.{RESET}")

        input("\nPress Enter to return to the menu...")
        print("\033c", end="")


def main():
    parser = argparse.ArgumentParser(
        description="Cyber Defence TCP connection and port scanner"
    )

    subparsers = parser.add_subparsers(dest="command")

    http_parser = subparsers.add_parser(
        "http",
        help="Check whether a host accepts HTTP connections"
    )
    http_parser.add_argument("host", help="Hostname or IP address")

    port_parser = subparsers.add_parser(
        "port",
        help="Scan a specific TCP port"
    )
    port_parser.add_argument("host", help="Hostname or IP address")
    port_parser.add_argument("port", type=int, help="Port number")

    top_parser = subparsers.add_parser(
        "top",
        help="Scan 10 common TCP ports"
    )
    top_parser.add_argument("host", help="Hostname or IP address")

    args = parser.parse_args()

    if args.command == "http":
        banner()
        ping_scan(args.host)
    elif args.command == "port":
        banner()
        port_scan(args.host, args.port)
    elif args.command == "top":
        banner()
        top_port_scan(args.host)
    else:
        menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan cancelled by user.{RESET}")
        sys.exit(0)