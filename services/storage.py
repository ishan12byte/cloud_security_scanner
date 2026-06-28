import json
from datetime import datetime


def save_scan(findings,account_info=None, filename="reports/findings.json"):
    data = {
        "scan_time": datetime.now().isoformat(),
        "account": account_info,
        "findings": findings
    }

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_scan(filename="reports/findings.json"):

    try:

        with open(filename, "r") as file:

            data = json.load(file)

            # Old format
            if isinstance(data, list):
                return {
                    "scan_time": None,
                    "findings": data
                }

            return data

    except FileNotFoundError:

        return {
            "scan_time": None,
            "findings": []
        }