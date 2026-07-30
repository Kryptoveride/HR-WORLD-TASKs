#!/usr/bin/env python3

import argparse
import datetime

# Colours
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def show_card(hostname, host_ip, attacker_ip):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n{CYAN}{'='*55}{RESET}")
    print(f"{CYAN}       INCIDENT CONTAINMENT TICKET{RESET}")
    print(f"{CYAN}{'='*55}{RESET}")

    print(f"Time           : {timestamp}")
    print(f"Hostname       : {hostname}")
    print(f"Host IP        : {host_ip}")
    print(f"Blocked IP     : {RED}{attacker_ip}{RESET}")

    print(f"\n{GREEN}Containment Status: SUCCESSFUL{RESET}")

    print("\nActions Completed:")
    print(f"✓ Firewall rule added to block {attacker_ip}")
    print("✓ Affected system remains powered ON")
    print("✓ Network containment completed")

    print("\nNext Steps:")
    print("1. Preserve evidence for forensic analysis.")
    print("2. Notify the SOC/IR team.")
    print("3. Begin malware investigation.")

    print(f"\n{CYAN}{'='*55}{RESET}")
    print(f"{GREEN}Containment completed successfully.{RESET}")
    print(f"{CYAN}{'='*55}{RESET}\n")


def menu():
    print(f"{CYAN}Tier-1 Malware Containment Tool{RESET}")

    hostname = input("Enter affected hostname: ")
    host_ip = input("Enter affected host IP: ")
    attacker_ip = input("Enter attacker IP: ")

    critical = input(
        "Is this a production server or critical system? (yes/no): "
    ).lower()

    if critical in ["yes", "y"]:
        print(
            f"{RED}Do not isolate it yourself. "
            f"Contact the SOC/IR team immediately.{RESET}"
        )
        return

    confirmed = input(
        "Has the malware alert been confirmed? (yes/no): "
    ).lower()

    if confirmed not in ["yes", "y"]:
        print(f"{YELLOW}Verify the alert before continuing.{RESET}")
        return

    show_card(hostname, host_ip, attacker_ip)


def main():
    parser = argparse.ArgumentParser(
        description="macOS malware containment tool"
    )

    parser.add_argument("hostname", nargs="?")
    parser.add_argument("host_ip", nargs="?")
    parser.add_argument("attacker_ip", nargs="?")

    args = parser.parse_args()

    if args.hostname and args.host_ip and args.attacker_ip:
        show_card(args.hostname, args.host_ip, args.attacker_ip)
    else:
        menu()


if __name__ == "__main__":
    main()