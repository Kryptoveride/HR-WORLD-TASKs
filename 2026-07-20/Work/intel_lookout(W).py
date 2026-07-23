import os
import socket

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("VIRUS_TOTAL_API")

target_ips = [
    "8.8.8.8",          # Google
    "1.1.1.1",          # Cloudflare
    "9.9.9.9",          # Quad9

    "1.222.84.29",       # IOC
    "167.88.173.252",    # IOC
    "23.227.202.253",    # IOC
    "255.255.243.345"
]

# Terminal colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

headers = {
    "accept": "application/json",
    "x-apikey": api_key,
}


def get_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return "Not available"


if not api_key:
    print(f"{RED}[x] VIRUS_TOTAL_API was not found in the .env file.{RESET}")
    raise SystemExit


for target_ip in target_ips:

    url = (
        f"https://www.virustotal.com/api/v3/"
        f"ip_addresses/{target_ip}"
    )

    print("\n" + "=" * 55)
    print(f"Querying VirusTotal for: {target_ip}")
    print("=" * 55)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code == 200:

            data = response.json()
            attributes = data["data"]["attributes"]
            stats = attributes["last_analysis_stats"]

            hostname = get_hostname(target_ip)

            country = attributes.get("country", "Unknown")
            network = attributes.get("network", "Unknown")
            owner = attributes.get("as_owner", "Unknown")
            asn = attributes.get("asn", "Unknown")
            reputation = attributes.get("reputation", 0)

            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            undetected = stats.get("undetected", 0)

            print(f"IP Address : {target_ip}")
            print(f"Hostname   : {hostname}")
            print(f"Country    : {country}")
            print(f"Network    : {network}")
            print(f"Owner      : {owner}")
            print(f"ASN        : {asn}")
            print(f"Reputation : {reputation}")

            print("\nVirusTotal Results")
            print(f"Malicious  : {malicious}")
            print(f"Suspicious : {suspicious}")
            print(f"Harmless   : {harmless}")
            print(f"Undetected : {undetected}")

            if malicious > 0 or suspicious > 0:
                print(f"\nStatus     : {RED}HARMFUL{RESET}")
            else:
                print(f"\nStatus     : {GREEN}SAFE{RESET}")

        elif response.status_code == 401:
            print(f"{RED}[x] Invalid VirusTotal API key.{RESET}")

        elif response.status_code == 404:
            print(f"{RED}[x] No VirusTotal information found.{RESET}")

        elif response.status_code == 429:
            print(f"{RED}[x] VirusTotal API limit reached.{RESET}")

        else:
            print(
                f"{RED}[x] API query failed: "
                f"{response.status_code} - {response.text}{RESET}"
            )

    except requests.exceptions.Timeout:
        print(f"{RED}[x] Request timed out.{RESET}")

    except requests.exceptions.ConnectionError:
        print(f"{RED}[x] Could not connect to VirusTotal.{RESET}")

    except requests.exceptions.RequestException as error:
        print(f"{RED}[x] Request error: {error}{RESET}")

    except Exception as error:
        print(f"{RED}[x] An error occurred: {error}{RESET}")