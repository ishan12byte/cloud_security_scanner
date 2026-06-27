from scanner.main_scanner import run_scan

from services.summary import generate_summary
from services.scoring import calculate_security_score
from services.exporter import export_json, export_csv


findings = run_scan()

summary = generate_summary(findings)

score = calculate_security_score(findings)

export_json(findings)

export_csv(findings)

print(summary)

print(score)