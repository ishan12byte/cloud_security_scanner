from scanner.iam_scanner import scan_iam

results = scan_iam()

print(f"\n Findings: {len(results)}\n")

for finding in results:
    print(finding)