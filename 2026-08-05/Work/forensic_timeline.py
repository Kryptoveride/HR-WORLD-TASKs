from colorama import Fore, Style, init

init(autoreset=True)


forensic_artifacts = [
    {
        "timestamp": "2026-08-05 11:52:00",
        "source": "Authentication Logs",
        "event": "Several failed SSH login attempts were detected for the root account",
        "severity": "HIGH",
        "mitigation": "Block the source IP address and disable direct root login"
    },
    {
        "timestamp": "2026-08-05 11:55:30",
        "source": "Authentication Logs",
        "event": "A successful SSH login occurred from an unknown external IP address",
        "severity": "CRITICAL",
        "mitigation": "Terminate the SSH session and reset the affected account password"
    },
    {
        "timestamp": "2026-08-05 11:57:10",
        "source": "Shell History",
        "event": "A suspicious script was downloaded using the curl command",
        "severity": "HIGH",
        "mitigation": "Isolate the system and block the malicious download address"
    },
    {
        "timestamp": "2026-08-05 11:58:25",
        "source": "File System Monitoring",
        "event": "A suspicious file named ransomware.sh was created inside the /tmp directory",
        "severity": "HIGH",
        "mitigation": "Preserve the file as evidence and remove its execution permission"
    },
    {
        "timestamp": "2026-08-05 12:00:00",
        "source": "Process Monitoring",
        "event": "Malicious script execution ran through the zsh shell with PID 4232",
        "severity": "CRITICAL",
        "mitigation": "Kill the process using the kill -9 4232 command"
    },
    {
        "timestamp": "2026-08-05 12:00:15",
        "source": "Process Monitoring",
        "event": "The malicious process created a child encryption process with PID 4251",
        "severity": "CRITICAL",
        "mitigation": "Terminate PID 4251 and isolate the affected system"
    },
    {
        "timestamp": "2026-08-05 12:00:45",
        "source": "File System Monitoring",
        "event": "Multiple user documents were renamed with the .locked extension",
        "severity": "CRITICAL",
        "mitigation": "Stop the encryption process and disconnect shared storage"
    },
    {
        "timestamp": "2026-08-05 12:01:20",
        "source": "Network Monitoring",
        "event": "The system connected to an unknown external IP address on port 443",
        "severity": "HIGH",
        "mitigation": "Block the external IP address and disconnect the system from the network"
    },
    {
        "timestamp": "2026-08-05 12:02:10",
        "source": "Cron Job Monitoring",
        "event": "A new cron job was created to execute ransomware.sh every five minutes",
        "severity": "HIGH",
        "mitigation": "Remove the unauthorized cron job after preserving it as evidence"
    },
    {
        "timestamp": "2026-08-05 12:03:05",
        "source": "User Account Monitoring",
        "event": "An unauthorized user account named system_backup was created",
        "severity": "CRITICAL",
        "mitigation": "Disable the unauthorized account and review its activity"
    },
    {
        "timestamp": "2026-08-05 12:04:30",
        "source": "Security Logs",
        "event": "The attacker attempted to stop the system logging service",
        "severity": "HIGH",
        "mitigation": "Restart the logging service and preserve all available logs"
    },
    {
        "timestamp": "2026-08-05 12:05:40",
        "source": "File System Monitoring",
        "event": "A ransom note named RECOVER_FILES.txt was created in the Documents directory",
        "severity": "CRITICAL",
        "mitigation": "Preserve the ransom note and investigate its contents"
    },
    {
        "timestamp": "2026-08-05 12:06:20",
        "source": "Backup Monitoring",
        "event": "The attacker attempted to delete local backup files",
        "severity": "CRITICAL",
        "mitigation": "Protect offline backups and prevent access to backup storage"
    }
]


def reconstruct_timeline(artifacts):
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "TIMELINE RECONSTRUCTION")
    print(Fore.CYAN + "=" * 60)
    print("\n")

    artifacts.sort(key=lambda item: item["timestamp"])

    for step, artifact in enumerate(artifacts, start=1):

        if artifact["severity"] == "CRITICAL":
            severity_color = Fore.RED

        elif artifact["severity"] == "HIGH":
            severity_color = Fore.YELLOW

        elif artifact["severity"] == "MEDIUM":
            severity_color = Fore.MAGENTA

        else:
            severity_color = Fore.GREEN

        print(Fore.CYAN + f"Forensic Artifact {step}")
        print(Fore.WHITE + f"TIMESTAMP : {artifact['timestamp']}")
        print(
            severity_color
            + f"A {artifact['severity']} event has occurred"
        )
        print(
            Fore.WHITE
            + f"{artifact['event']} was discovered using "
              f"{artifact['source']}"
        )
        print(
            Fore.GREEN
            + f"Possible mitigation: {artifact['mitigation']}"
        )
        print(Fore.CYAN + "-" * 60)
        print()


reconstruct_timeline(forensic_artifacts)