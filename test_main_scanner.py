from scanner.main_scanner import run_scan

results = run_scan()

print(f"\nTotal Findings: {len(results)}\n")

for finding in results:
    print(finding)