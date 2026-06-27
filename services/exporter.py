import json
import csv


def export_json(findings, filename="reports/findings.json"):

    with open(filename, "w") as file:

        json.dump(
            findings,
            file,
            indent=4
        )
        
def export_csv(findings, filename="reports/findings.csv"):

    if not findings:
        return

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=findings[0].keys()
        )

        writer.writeheader()
        writer.writerows(findings)