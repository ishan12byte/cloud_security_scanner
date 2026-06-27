from scanner.main_scanner import run_scan
from services.summary import generate_summary

findings = run_scan()

summary = generate_summary(findings)

print(summary)