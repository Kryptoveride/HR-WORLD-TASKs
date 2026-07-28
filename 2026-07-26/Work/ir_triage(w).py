from datetime import datetime

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def cal_incident_priority(impacted_asset, threat_type):
    if impacted_asset in [
        'production_database',
        'domain_controller',
        'payment_server',
        'customer_database'
    ]:
        impact_score = 3
    elif impacted_asset in [
        'web_server',
        'email_server',
        'file_server',
        'backup_server'
    ]:
        impact_score = 2
    elif impacted_asset in [
        'employee_laptop',
        'employee_desktop',
        'test_server',
        'printer'
    ]:
        impact_score = 1
    else:
        impact_score = 2

    if threat_type in [
        'ransomware',
        'data_exfiltration',
        'database_breach',
        'malware_outbreak'
    ]:
        threat_score = 3
    elif threat_type in [
        'phishing',
        'unauthorised_login',
        'brute_force_attack',
        'ddos_attack',
        'sql_injection'
    ]:
        threat_score = 2
    else:
        threat_score = 1

    total_severity = impact_score * threat_score

    if total_severity >= 6:
        return 'CRITICAL', 'Immediate investigation and containment required', impact_score, threat_score, total_severity
    elif total_severity >= 3:
        return 'ELEVATED', 'SOC analyst investigation required', impact_score, threat_score, total_severity
    else:
        return 'STANDARD', 'Monitor and review event', impact_score, threat_score, total_severity


def display_incident(event_id, impacted_asset, threat_type):
    severity, action, impact, threat, total = cal_incident_priority(
        impacted_asset,
        threat_type
    )

    if severity == 'CRITICAL':
        color = RED
        status = 'OPEN - HIGH PRIORITY'
    elif severity == 'ELEVATED':
        color = YELLOW
        status = 'OPEN - INVESTIGATION'
    else:
        color = GREEN
        status = 'OPEN - MONITORING'

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{WHITE}{'=' * 72}{RESET}")
    print(f"{BOLD}SECURITY INCIDENT EVENT{RESET}")
    print(f"{WHITE}{'=' * 72}{RESET}")
    print(f"Event ID        : {event_id}")
    print(f"Timestamp       : {timestamp}")
    print(f"Affected Asset  : {impacted_asset}")
    print(f"Detected Threat : {threat_type}")
    print(f"Impact Score    : {impact}/3")
    print(f"Threat Score    : {threat}/3")
    print(f"Severity Score  : {total}/9")
    print(f"Severity        : {color}{BOLD}{severity}{RESET}")
    print(f"Incident Status : {color}{status}{RESET}")
    print(f"Response Action : {action}")
    print(f"{WHITE}{'=' * 72}{RESET}\n")


if __name__ == '__main__':
    print(f"\n{CYAN}{BOLD}SOC INCIDENT PRIORITY ENGINE{RESET}")
    print(f"System Status: {GREEN}ACTIVE{RESET}")
    print(f"Processing security events...\n")

    incidents = [
        ('INC-2026-001', 'production_database', 'data_exfiltration'),
        ('INC-2026-002', 'employee_laptop', 'phishing'),
        ('INC-2026-003', 'domain_controller', 'ransomware'),
        ('INC-2026-004', 'web_server', 'ddos_attack'),
        ('INC-2026-005', 'email_server', 'unauthorised_login'),
        ('INC-2026-006', 'customer_database', 'sql_injection'),
        ('INC-2026-007', 'file_server', 'malware_outbreak'),
        ('INC-2026-008', 'employee_desktop', 'brute_force_attack')
    ]

    for event_id, system, attack in incidents:
        display_incident(event_id, system, attack)