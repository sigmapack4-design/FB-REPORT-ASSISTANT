
cat > fb_report.py <<'PY'
import os
import sys
import json
import time
import random
import shutil
import subprocess
from datetime import datetime
from urllib.parse import urlparse

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = CYAN = MAGENTA = YELLOW = WHITE = BLUE = ""
    class Style:
        RESET_ALL = BRIGHT = ""

G = Fore.GREEN
C = Fore.CYAN
M = Fore.MAGENTA
R = Fore.RED
Y = Fore.YELLOW
W = Fore.WHITE
B = Fore.BLUE

FILE = "reports.json"

CATEGORIES = [
    "Fake account",
    "Impersonation",
    "Harassment",
    "Scam / Fraud",
    "Spam",
    "Copyright",
    "Other"
]

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def center(text):
    width = shutil.get_terminal_size((80, 24)).columns
    print(text.center(width))

def loading(message="INITIALIZING SYSTEM"):
    print()
    print(C + message)
    for i in range(31):
        percent = int(i / 30 * 100)
        bar = "█" * i + "░" * (30-i)
        print(
            "\r" + G + "[" + bar + "] " +
            Y + str(percent) + "%",
            end="", flush=True
        )
        time.sleep(0.025)
    print("\n" + G + "[+] SYSTEM READY")
    time.sleep(0.3)

def banner():
    clear()
    print(C + r"""
   ███████╗██╗ ██████╗ ███╗   ███╗ █████╗
   ██╔════╝██║██╔════╝ ████╗ ████║██╔══██╗
   ███████╗██║██║  ███╗██╔████╔██║███████║
   ╚════██║██║██║   ██║██║╚██╔╝██║██╔══██║
   ███████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║
   ╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝
    """)
    print(M + "=" * 55)
    center(Y + Style.BRIGHT + "Fucking Your Mom")
    print(M + "=" * 55)
    center(G + "ADVANCED TERMINAL EDITION v2.0")
    center(C + "FACEBOOK REPORT ASSISTANT")
    print(M + "=" * 55)
    print()

def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print(R + "[!] Could not read database.")
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def pause():
    input(Y + "\n[ENTER] Return to menu...")

def valid_url(url):
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        return (
            parsed.scheme == "https"
            and host in (
                "facebook.com",
                "www.facebook.com",
                "m.facebook.com"
            )
        )
    except ValueError:
        return False

def add_case(data):
    print(C + "\n[+] NEW REPORT CASE")
    url = input(W + "Facebook URL: ").strip()

    if not valid_url(url):
        print(R + "[!] Invalid Facebook URL.")
        return

    if any(x["url"] == url for x in data):
        print(R + "[!] Duplicate URL detected.")
        return

    print(C + "\nSELECT CATEGORY")
    for i, category in enumerate(CATEGORIES, 1):
        print(G + f" [{i}] " + W + category)

    try:
        choice = int(input(Y + "\nSelect: "))
        category = CATEGORIES[choice - 1]
    except (ValueError, IndexError):
        print(R + "[!] Invalid selection.")
        return

    notes = input(W + "Evidence notes: ").strip()

    data.append({
        "id": random.randint(10000, 99999),
        "url": url,
        "category": category,
        "notes": notes,
        "status": "PENDING",
        "created": datetime.now().isoformat()
    })

    save_data(data)
    print(G + "\n[+] CASE SAVED SUCCESSFULLY")

def view_cases(data):
    print(C + "\n========== CASE DATABASE ==========")

    if not data:
        print(Y + "No cases available.")
        return

    for i, case in enumerate(data, 1):
        print(G + f"\n[{i}] ID: {case['id']}")
        print(W + "URL: " + case["url"])
        print(C + "Category: " + case["category"])
        print(Y + "Status: " + case["status"])
        print(W + "Notes: " + case["notes"])

def search_cases(data):
    query = input(C + "\nSearch URL/category/ID: ").lower()
    results = [
        x for x in data
        if query in x["url"].lower()
        or query in x["category"].lower()
        or query in str(x["id"])
    ]
    view_cases(results)

def open_workflow(data):
    view_cases(data)
    if not data:
        return

    try:
        n = int(input(Y + "\nSelect case number: ")) - 1
        case = data[n]

        print(C + "\nOpening official Facebook workflow...")

        urls = [
            case["url"],
            "https://www.facebook.com/help/"
        ]

        for url in urls:
            if shutil.which("termux-open-url"):
                subprocess.run(
                    ["termux-open-url", url],
                    check=False
                )
            else:
                import webbrowser
                webbrowser.open(url)

        print(G + "[+] Browser request sent.")
        print(Y + "Complete and verify any report yourself.")

    except (ValueError, IndexError):
        print(R + "[!] Invalid selection.")

def update_case(data):
    view_cases(data)
    if not data:
        return

    try:
        n = int(input(Y + "\nCase number: ")) - 1
        case = data[n]

        print("\n1. PENDING")
        print("2. SUBMITTED")
        print("3. CLOSED")

        choice = int(input("Status: "))
        statuses = {
            1: "PENDING",
            2: "SUBMITTED",
            3: "CLOSED"
        }

        case["status"] = statuses[choice]
        save_data(data)
        print(G + "[+] STATUS UPDATED")

    except (ValueError, IndexError, KeyError):
        print(R + "[!] Invalid selection.")

def delete_case(data):
    view_cases(data)
    if not data:
        return

    try:
        n = int(input(Y + "\nCase number to delete: ")) - 1
        if input(R + "Confirm deletion (y/n): ").lower() == "y":
            data.pop(n)
            save_data(data)
            print(G + "[+] DELETED")
    except (ValueError, IndexError):
        print(R + "[!] Invalid selection.")

def backup(data):
    name = "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    with open(name, "w") as f:
        json.dump(data, f, indent=4)
    print(G + "[+] BACKUP CREATED: " + name)

def stats(data):
    print(C + "\n========== SYSTEM STATISTICS ==========")
    print(G + "TOTAL CASES: " + str(len(data)))
    print(Y + "PENDING: " + str(sum(x["status"] == "PENDING" for x in data)))
    print(G + "SUBMITTED: " + str(sum(x["status"] == "SUBMITTED" for x in data)))
    print(R + "CLOSED: " + str(sum(x["status"] == "CLOSED" for x in data)))

def menu():
    while True:
        banner()
        data = load_data()

        print(G + " [01] " + W + "Add Report Case")
        print(G + " [02] " + W + "View Database")
        print(G + " [03] " + W + "Open Reporting Workflow")
        print(G + " [04] " + W + "Update Case Status")
        print(G + " [05] " + W + "Search Cases")
        print(G + " [06] " + W + "Delete Case")
        print(G + " [07] " + W + "Create JSON Backup")
        print(G + " [08] " + W + "System Statistics")
        print(R + " [00] " + W + "Exit")

        print(M + "\n" + "=" * 55)
        choice = input(C + "\nSIGMA@HACKER >> " + W).strip()

        if choice == "1":
            add_case(data)
            pause()
        elif choice == "2":
            view_cases(data)
            pause()
        elif choice == "3":
            open_workflow(data)
            pause()
        elif choice == "4":
            update_case(data)
            pause()
        elif choice == "5":
            search_cases(data)
            pause()
        elif choice == "6":
            delete_case(data)
            pause()
        elif choice == "7":
            backup(data)
            pause()
        elif choice == "8":
            stats(data)
            pause()
        elif choice == "0":
            print(G + "\n[+] SIGMA SYSTEM SHUTDOWN")
            break
        else:
            print(R + "[!] INVALID COMMAND")
            time.sleep(0.7)

if __name__ == "__main__":
    try:
        banner()
        loading()
        menu()
    except KeyboardInterrupt:
        print(R + "\n[!] SYSTEM INTERRUPTED")
        sys.exit(0)
PY

python fb_report.py
