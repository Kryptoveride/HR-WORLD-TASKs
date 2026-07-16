import time
import re


RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"


mock_log_stream = [
    "2026-07-16 10:00:01 INFO User 'Jason' requested database access.",
    "2026-07-16 10:00:04 INFO User 'Sarah' logged in successfully.",
    "2026-07-16 10:00:07 WARNING Multiple failed login attempts for admin.",
    "2026-07-16 10:00:10 ERROR Database connection failed.",
    "2026-07-16 10:00:13 INFO HTTP GET /index.html returned status 200.",
    "2026-07-16 10:00:16 CRITICAL Unauthorized privilege escalation detected.",
    "2026-07-16 10:00:20 WARNING Firewall blocked suspicious connections.",
    "2026-07-16 10:00:25 CRITICAL Malware detected in invoice.exe."
]


def is_alert(severity, message):
    keywords = [
        "failed",
        "unauthorized",
        "malware",
        "injection",
        "blocked",
        "attack",
        "denied",
        "suspicious",
        "ransomware",
        "exfiltration",
        "compromise",
        "exploit"
    ]

    if severity == "ERROR" or severity == "CRITICAL":
        return True

    message = message.lower()

    for word in keywords:
        if word in message:
            return True

    return False


def parse_mac_log(line):
    parts = line.split(maxsplit=7)

    if len(parts) < 8:
        return None

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", parts[0]):
        return None

    mac_type = parts[3]

    severity_map = {
        "Default": "INFO",
        "Info": "INFO",
        "Debug": "INFO",
        "Error": "ERROR",
        "Fault": "CRITICAL",
        "Activity": "INFO"
    }

    if mac_type not in severity_map:
        return None

    timestamp = f"{parts[0]} {parts[1]}"
    severity = severity_map[mac_type]
    message = parts[7]

    return timestamp, severity, message


def scan_logs(logs, delay):
    pattern = (
        r"^(\d{4}-\d{2}-\d{2} "
        r"\d{2}:\d{2}:\d{2})\s+"
        r"(INFO|WARNING|ERROR|CRITICAL)\s+"
        r"(.*)$"
    )

    total_events = 0
    total_alerts = 0
    critical_alerts = 0
    invalid_logs = 0

    print(f"\n{CYAN}SECURITY LOG MONITOR{RESET}")
    print("-" * 95)
    print(f"{'TIME':<20}{'STATUS':<18}{'LEVEL':<12}MESSAGE")
    print("-" * 95)

    for line in logs:
        if delay > 0:
            time.sleep(delay)

        line = line.strip()

        if not line:
            continue

        match = re.match(pattern, line)

        if match:
            timestamp, severity, message = match.groups()
        else:
            mac_result = parse_mac_log(line)

            if mac_result is None:
                invalid_logs += 1
                print(
                    f"{RED}"
                    f"{'Unknown':<20}"
                    f"{'INVALID LOG':<18}"
                    f"{'UNKNOWN':<12}"
                    f"{line}"
                    f"{RESET}"
                )
                continue

            timestamp, severity, message = mac_result

        total_events += 1

        if is_alert(severity, message):
            total_alerts += 1
            status = "SECURITY ALERT"
            color = RED

            if severity == "CRITICAL":
                critical_alerts += 1
                color = MAGENTA
        else:
            status = "NORMAL"

            if severity == "WARNING":
                color = YELLOW
            else:
                color = GREEN

        print(
            f"{color}"
            f"{timestamp:<20}"
            f"{status:<18}"
            f"{severity:<12}"
            f"{message}"
            f"{RESET}"
        )

    print("-" * 95)
    print(f"Events analyzed : {total_events}")
    print(f"Normal events   : {total_events - total_alerts}")
    print(f"Security alerts : {total_alerts}")
    print(f"Critical alerts : {critical_alerts}")
    print(f"Invalid logs    : {invalid_logs}")


def main():
    print(f"\n{CYAN}SCANNING MOCK LOG STREAM{RESET}")
    scan_logs(mock_log_stream, 1.0)

    file_path = input(
        "\nEnter a log file to scan or press Enter to stop: "
    ).strip()

    if not file_path:
        print(f"{CYAN}Program stopped.{RESET}")
        return

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:
            print(f"\n{CYAN}SCANNING SAVED LOG FILE{RESET}")
            scan_logs(file, 0)

    except FileNotFoundError:
        print(f"{RED}File not found.{RESET}")

    except PermissionError:
        print(f"{RED}Permission denied.{RESET}")

    except OSError as error:
        print(f"{RED}Could not read file: {error}{RESET}")


if __name__ == "__main__":
    main()
