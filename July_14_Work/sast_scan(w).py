import re

mock_code_files = {
    "database.py": [
        "db_conn = 'http://internal-database.local/connect'",
        "secret_token = 'qwertyuiasdfghjkzxcvbn'",
        "user_data = eval(input('Enter ID: '))"
    ],

    "login.py": [
        "password = 'admin123'",
        "api_key = '123456789abcdef'"
    ],

    "system.py": [
        "import os",
        "command = input('Command: ')",
        "os.system(command)",
        "debug = True"
    ],

    "hidden_risks.py": [
        "import subprocess",
        "connection = 'h' + 'ttp://unsafe-server.local'",
        "login_password = input('Enter password: ')",
        "run_code = getattr(__builtins__, 'eval')",
        "result = run_code(input('Enter calculation: '))",
        "subprocess.run(input('Enter command: '), shell=True)",
        "development_mode = bool(1)"

        # This file passes because the scanner only looks for exact patterns.
        # The HTTP address is split into two strings, so "http://" is not present.
        # login_password does not match the exact "password =" pattern.
        # eval() is accessed indirectly using getattr().
        # subprocess with shell=True is dangerous but no rule checks for it.
        # development_mode is enabled, but it does not use "debug = True".
    ]
}

signature_rules = {
    "Unencrypted Connection": r"http://",
    "Hardcoded Password": r"password\s*=",
    "Hardcoded Secret/API Key": r"(secret_token|api_key)\s*=",
    "Dangerous eval()": r"\beval\s*\(",
    "OS Command Execution": r"os\.system\s*\(",
    "Debug Mode Enabled": r"debug\s*=\s*True"
}


def scan_code(file_name, code_lines):
    print(f"\nScanning: {file_name}")
    print("-" * 55)

    findings = 0

    for line_num, line in enumerate(code_lines, start=1):
        for rule_name, rule_regex in signature_rules.items():
            if re.search(rule_regex, line, re.IGNORECASE):
                findings += 1
                print(f"[!] {rule_name}")
                print(f"    Line: {line_num}")
                print(f"    Code: {line.strip()}")

    if findings == 0:
        print("No vulnerabilities found.")

    return findings


print("=" * 55)
print("        SIMPLE SIGNATURE-BASED SAST SCANNER")
print("=" * 55)

total_findings = 0

for file_name, code_lines in mock_code_files.items():
    total_findings += scan_code(file_name, code_lines)

file_path = input("\nEnter a Python file to scan or press Enter to skip: ").strip()

if file_path:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            total_findings += scan_code(file_path, file.readlines())
    except FileNotFoundError:
        print("File not found.")
    except OSError as error:
        print(f"Could not read file: {error}")

print("\n" + "=" * 55)
print(f"Scan complete. Total findings: {total_findings}")
print("=" * 55)