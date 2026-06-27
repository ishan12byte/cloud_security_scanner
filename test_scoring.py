from scanner.main_scanner import run_scan
from services.scoring import calculate_security_score

findings = run_scan()

print(calculate_security_score(findings))