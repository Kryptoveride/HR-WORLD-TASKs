import sys
import subprocess
import os


# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'


UNSAFE_PATHS_MAC = [
    '/tmp/',
    '/private/tmp/',
    '/var/tmp/',
    '/private/var/tmp/',
    '/Users/Shared/',
    '/Users/Guest/',
    '/Library/Caches/'
]

UNSAFE_PATH_WIN = [
    '\\Windows\\Temp\\',
    '\\AppData\\Local\\Temp\\',
    '\\AppData\\Roaming\\',
    '\\Users\\Public\\',
    '\\ProgramData\\',
    '\\Temp\\'
]


def get_running_process_mac():
    cmd = [
        'ps',
        '-eo',
        'user,pid,ppid,command'
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    processes = []
    lines = result.stdout.strip().split('\n')[1:]

    for line in lines:
        parts = line.split(maxsplit=3)

        if len(parts) == 4:
            processes.append({
                'user': parts[0],
                'pid': parts[1],
                'ppid': parts[2],
                'path': parts[3]
            })

    return processes


def get_running_process_windows():
    cmd = [
        'tasklist',
        '/FO',
        'CSV',
        '/NH'
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    processes = []

    for line in result.stdout.strip().split('\n'):
        line = line.replace('"', '')
        parts = line.split(',')

        if len(parts) >= 2:
            processes.append({
                'user': 'Unknown',
                'pid': parts[1],
                'ppid': 'Unknown',
                'path': parts[0]
            })

    return processes


def kill_process(pid, is_windows):
    try:
        if is_windows:
            subprocess.run(
                ['taskkill', '/PID', str(pid), '/F'],
                check=True
            )
        else:
            os.kill(int(pid), 15)

        print(f'{GREEN}Process {pid} terminated successfully.{RESET}')

    except PermissionError:
        print(f'{RED}Permission denied. Run with administrator privileges.{RESET}')

    except ProcessLookupError:
        print(f'{RED}Process {pid} no longer exists.{RESET}')

    except subprocess.CalledProcessError:
        print(f'{RED}Unable to terminate process {pid}.{RESET}')

    except ValueError:
        print(f'{RED}Invalid PID.{RESET}')


def audit_system():
    is_windows = sys.platform.startswith('win')

    target_unsafe = UNSAFE_PATH_WIN if is_windows else UNSAFE_PATHS_MAC

    if is_windows:
        active_process = get_running_process_windows()
    else:
        active_process = get_running_process_mac()

    print(f'{CYAN}Total Processes Audited: {len(active_process)}{RESET}')

    alerts = 0
    suspicious_pids = []

    for proc in active_process:
        for unsafe_dir in target_unsafe:
            if unsafe_dir.lower() in proc['path'].lower():
                alerts += 1
                suspicious_pids.append(proc['pid'])

                print(f'\n{YELLOW}Suspicious Process Found{RESET}')
                print(f"User: {proc['user']}")
                print(f"PID: {proc['pid']}")
                print(f"PPID: {proc['ppid']}")
                print(f"Process: {proc['path']}")
                print(f"Matched Path: {unsafe_dir}")

                break

    if alerts == 0:
        print(f'\n{GREEN}System Clean{RESET}')
    else:
        print(
            f'\n{RED}Identified {alerts} suspicious '
            f'process(es).{RESET}'
        )

        print(f'\nSuspicious PIDs: {", ".join(suspicious_pids)}')

        choice = input(
            '\nWould you like to kill a process using its PID? (y/n): '
        ).lower()

        if choice == 'y':
            pid = input('Enter the PID to terminate: ').strip()

            if pid in suspicious_pids:
                confirm = input(
                    f'Are you sure you want to terminate PID {pid}? (y/n): '
                ).lower()

                if confirm == 'y':
                    kill_process(pid, is_windows)
                else:
                    print('Process termination cancelled.')
            else:
                print(f'{RED}PID is not in the suspicious process list.{RESET}')


if __name__ == '__main__':
    audit_system()



# option kill the malware pid
# edr platforms
# current industry EDRs
# research
# add more unsafe paths